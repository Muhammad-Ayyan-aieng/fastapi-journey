Using an ODM (Beanie) instead of raw MongoDB queries

An ODM (Object Document Mapper) allows me to interact with MongoDB using Python classes instead of manually writing queries.

When I initially experimented with raw Motor queries, I had to construct dictionaries manually and handle things like ObjectIds myself. This quickly became error-prone. For example, it was easy to forget required fields or mistype keys, and MongoDB would still accept the data. The problem would only appear later when reading the data, causing runtime errors.
    
Switching to Beanie improved this significantly. I could define my schema using Python classes, and validation happens before data is saved. If I try to create an event without a required field like location, it immediately raises an error instead of silently failing.

Beanie also simplifies relationships using things like Link[Event], so I don’t have to manually manage IDs between collections. Overall, it reduced boilerplate and helped catch mistakes early.

Why I introduced a Database class

At the beginning, I directly used Beanie methods inside my route handlers. While this worked, it quickly led to duplicated logic.

For example:

I had to repeat error handling in multiple routes
Update logic (filtering out None values) was copied everywhere
Adding logging would require modifying many files

To fix this, I created a Database class that wraps all database operations for a model.

This made my routes much cleaner and easier to read. It also centralized logic like updating only provided fields. Now, if I want to add logging or change how database operations work, I only need to update one place.

Another advantage is flexibility — if I ever switch away from Beanie, I only need to rewrite the Database class instead of the entire application.

Why initialize_database() is required on startup

If initialize_database() is not called, the application starts but fails as soon as any database operation is triggered.

I ran into this issue during development when I forgot to register the startup event. The error message was confusing at first, but the root cause is that Beanie was never initialized.

init_beanie() is responsible for:

Connecting to MongoDB
Registering all Document models
Mapping Python classes to collections

Without this step, Beanie has no knowledge of which collection corresponds to which model. So when a query runs, it fails because that mapping doesn’t exist.

Why Event and EventUpdate are separate models

The Event model represents a full database document and includes required fields and metadata like timestamps.

The EventUpdate model is different — it is designed specifically for update operations, so all fields are optional.

Initially, I tried using the same model for both creation and updates. This caused issues because updates don’t always include all fields. For example, a user might only update the title.

This forced me to manually check which fields were provided and construct update queries carefully, which became messy.

By introducing a separate EventUpdate model, I can cleanly handle partial updates like this:

update_data = {k: v for k, v in body.dict().items() if v is not None}

This ensures only the provided fields are updated and prevents accidentally overwriting existing values with None.

Why the Docker setup uses mongo instead of localhost

When I first containerised the app, I kept localhost in the database URL, and the connection failed.

What I learned is that each container runs in its own isolated environment. Inside the FastAPI container, localhost refers to the container itself — not the MongoDB container.

Since MongoDB runs in a separate container, the connection fails.

Using mongo works because it matches the service name in docker-compose.yml. Docker automatically creates a shared network where services can communicate using these names as hostnames.

So mongodb://mongo:27017 correctly connects the FastAPI container to the MongoDB container.

What depends_on actually does

At first, I assumed depends_on ensures MongoDB is fully ready before FastAPI starts. In practice, that’s not true.

depends_on only guarantees that the MongoDB container starts before the FastAPI container. It does not wait for MongoDB to finish initializing.

I noticed that sometimes FastAPI would start and immediately fail with a connection error because MongoDB wasn’t ready yet.

To fully solve this, the application would need:

A retry mechanism, or
A script that waits until MongoDB is reachable before starting the API
Why a volume is required for MongoDB

The volume (./mongo-data:/data/db) is what makes the database persistent.

When I tested without it, everything worked until I restarted the containers. After running docker compose down and starting again, all previously created data was gone.

This happens because, by default, MongoDB stores data inside the container’s filesystem. When the container is removed, the data is deleted as well.

By using a volume, the data is stored on the host machine instead. This allows it