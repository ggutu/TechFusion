## Building a Two-Tier Web Application with Flask, MySQL, and Redis

### Context:
Imagine you're a software engineer at a growing tech company, "TechFusion." The company has a customer-facing web application that allows users to log in, manage their profiles, and interact with other features. The application needs to store user data securely and efficiently, with fast access times to frequently used information.  
To meet these needs, the company has decided to build a two-tier architecture for the application using Flask for the web framework, MySQL for persistent data storage, and Redis for caching. This setup is intended to optimize user experience by speeding up data retrieval, ensuring that the application can handle growing traffic, and reducing the load on the database.

### Business Requirements:

#### User Authentication:
- Users will log in using their username and email.
- Once logged in, users should see a personalized dashboard with their profile information.

#### Caching for Performance:
- To improve performance, frequently accessed data (like user profile details) will be cached using Redis. This will avoid repeated database queries, reducing latency and database load.

#### Data Persistence:
- MySQL will store user data in a relational database, ensuring persistence across app restarts or crashes.

#### Scalability:
- As the number of users grows, the application should be able to handle multiple concurrent logins without sacrificing performance, thanks to the Redis cache.


## Two-Tier Web Application Architecture

The app is built with a two-tier architecture:

### Tier 1: Web Application Layer (Flask)
- The Flask application handles HTTP requests and responses.
- It serves dynamic HTML pages and interacts with MySQL and Redis to retrieve and cache data.

### Tier 2: Data Layer

#### MySQL Database:
- Stores user information in a persistent relational format (usernames and emails).

#### Redis Cache:
- Stores frequently accessed data (like user profile details) for fast retrieval.

### Real-World Workflow:

#### Login Workflow:
1. When a user logs in, the app first checks if the user’s data is available in Redis.
2. If the data is cached in Redis (e.g., user profile), it’s served instantly from Redis.
3. If the data is not in Redis, the app queries MySQL to fetch the user data, and then stores it in Redis for future use.
4. This cache is set to expire after an hour to ensure that data remains up-to-date.

#### Caching:
- Once the user logs in, their username and email are cached in Redis.
- The next time the user logs in, Redis will serve the data, avoiding the need to query MySQL again, drastically reducing the response time.

#### MySQL:
- **Persistent Storage**: Even though Redis speeds up data retrieval, MySQL remains the source of truth for user data. MySQL ensures that data is durable and accessible in the event of server crashes or restarts.
