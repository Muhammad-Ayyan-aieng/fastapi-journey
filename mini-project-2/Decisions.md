# DECISIONS.md - Mini Project 2

## 1. What is an ODM and why do we use Beanie instead of writing raw MongoDB queries?

**ODM (Object Document Mapper)** is a tool that lets me work with MongoDB documents as Python objects instead of writing raw database queries.

When I tried raw Motor queries, I had to manually write dictionary structures and convert ObjectIds. It was easy to make mistakes like forgetting required fields or mis-typing field names. MongoDB would accept invalid data, and my app would crash later when trying to read it.

With Beanie, I can define my data structure as Python classes with validation. When I create an event using `Event(title="...", description="...")`, Beanie validates everything before saving. If I forget a required field like `location`, it throws an error immediately. Also, features like `Link[Event]` in the User model make relationships easy without managing IDs manually. Beanie saves me from writing repetitive boilerplate code and catches errors early.

---

## 2. What is the role of the `Database` class — why wrap Beanie methods inside it instead of calling them directly in routes?

The `Database` class acts as a wrapper that handles all database operations for a specific model.

When I first started, I called Beanie methods directly in my routes. It worked, but when I needed to add logging or error handling, I had to copy the same code across multiple route files. Also, the update logic for filtering out `None` fields had to be repeated everywhere.

By moving everything into the `Database` class, my routes became cleaner. Now if I want to add logging to track database queries, I only change one file. The update method handles the logic of only updating fields that were actually sent in the request. If I ever switch from Beanie to another library, I only rewrite the Database class instead of touching every route. This separation makes the code easier to maintain and test.

---

## 3. What happens if `initialize_database()` is not called on startup? What would break and why?

If `initialize_database()` is not called, the app starts but crashes when any route tries to access the database.

I learned this the hard way during development. I forgot to add the startup event once, and when I tried to get an event, I got a confusing error about `MotorDatabase` not being callable.

What actually happens: `init_beanie()` registers each Document class with its MongoDB collection. Without this registration, Beanie doesn't know which database to connect to or which collection "events" maps to. The MongoDB client connection is created, but the mapping between my Python classes and database collections is empty. So when Beanie tries to perform an operation, it fails because it doesn't know where to look.

---

## 4. What is the difference between the `Event` document and the `EventUpdate` model, and why are they two separate classes?

The `Event` document inherits from Beanie's `Document` and represents a complete database record. It has required fields and timestamps for creation and updates.

The `EventUpdate` model inherits from Pydantic's `BaseModel` and all its fields are optional. It's only used for validating update requests.

When I first built the update endpoint, I tried using the same `Event` class for both creation and updates. This caused problems because for updates, users might only send a title or only a location. I had to manually check which fields were provided and build the update query. It was messy and error-prone.

With separate classes, the update method can do this:
```python
update_data = {k: v for k, v in body.dict().items() if v is not None}