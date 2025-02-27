# Database Schema

## 1. Authentication & Users (auth_user Table)

| Column       | Type         | Constraints                        | Description                     |
|--------------|--------------|------------------------------------|---------------------------------|
| id           | SERIAL       | PRIMARY KEY                        | Auto-incrementing user ID       |
| password     | VARCHAR(128) | NOT NULL                           | Hashed password                 |
| last_login   | TIMESTAMP    | NULLABLE                           | Last authentication timestamp   |
| is_superuser | BOOLEAN      | NOT NULL                           | Admin status                    |
| username     | VARCHAR(150) | UNIQUE, NOT NULL                   | Login username                  |
| email        | VARCHAR(254) | NOT NULL                           | User email                      |
| date_joined  | TIMESTAMP    | NOT NULL                           | Account creation date           |

## 2. Favorite Movies (users_favoritemovie Table)

| Column     | Type      | Constraints                              | Description                     |
|------------|-----------|------------------------------------------|---------------------------------|
| id         | SERIAL    | PRIMARY KEY                              | Auto-incrementing ID            |
| user_id    | INTEGER   | FOREIGN KEY (auth_user.id), NOT NULL     | Reference to user               |
| movie_id   | INTEGER   | NOT NULL                                 | TMDb movie ID                   |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW()                  | Favorite creation timestamp     |

## Indexes

- Composite unique index on (user_id, movie_id)
- Index on created_at for sorting

## Key Relationships

- **User → Favorite Movies (1:M)**: One user can have many favorite movie entries
- **Favorite Movie → TMDb (1:1)**: Each movie_id references a movie in TMDb's database

## Schema Notes

- **No Movie Storage**: Movie metadata (title, poster, etc.) isn't stored locally - fetched from TMDb API on demand

## Redis Cache Structure

```python
{
    "movie_rec:trending_movies": [list of movie dicts],
    "movie_rec:recommendations_550": [list of recommendations],
    "movie_550_details": {
        "title": "Fight Club",
        "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
        "overview": "..."
    }
}


## Optimization Features

- **Composite Index**: Enforces unique favorites per user
- **Timestamp Index**: Enables efficient "recent favorites" queries
- **Redis TTL**: 1 hour for trending/recommendations, 24 hours for movie details

## Sample Data

### auth_user Table

| id | username  | email            | date_joined           |
|----|-----------|------------------|-----------------------|
| 1  | moviebuff | user@example.com | 2023-07-25 14:30:00   |

### users_favoritemovie Table

| id | user_id | movie_id | created_at           |
|----|---------|----------|----------------------|
| 1  | 1       | 550      | 2023-07-25 14:35:00  |
| 2  | 1       | 680      | 2023-07-25 14:40:00  |


This schema provides:

- Scalability: Handles high user/movie volumes
- Performance: Optimized indexes + Redis caching
- Flexibility: Easy integration with TMDb updates

