# Movie Recommender Database ERD

This Entity Relationship Diagram (ERD) represents the database schema for the Movie Recommender application as described in the Database_schema.md documentation.

```mermaid
erDiagram
    auth_user {
        integer id PK
        varchar password
        timestamp last_login
        boolean is_superuser
        varchar username
        varchar email
        timestamp date_joined
    }

    users_favoritemovie {
        integer id PK
        integer user_id FK
        integer movie_id
        timestamp created_at
    }

    auth_user ||--o{ users_favoritemovie : "has favorites"
    
    users_favoritemovie }o--|| "TMDb API" : "references"
```

## Notes

- The ERD shows two main entities: `auth_user` and `users_favoritemovie`
- There is a one-to-many relationship between users and favorite movies (one user can have many favorite movies)
- Movie metadata is not stored locally but is fetched from TMDb API using the movie_id
- Redis is used for caching movie details, trending movies, and recommendations, but is not part of the persistent database schema
- A unique composite index exists on (user_id, movie_id) in the users_favoritemovie table
- An index exists on created_at in the users_favoritemovie table for sorting