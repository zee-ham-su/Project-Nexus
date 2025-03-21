# Movie Recommendation Backend

A high-performance backend for a movie recommendation application featuring user authentication, trending/recommended movies, and Redis caching.

## 🎯 Features

### Core Functionality

- **Movie Recommendations**
  - Get trending movies (updated weekly)
  - Get recommendations based on specific movies
- **User Management**
  - JWT-based authentication
  - User registration/login
  - Favorite movie storage
- **Performance**
  - Redis caching (1-hour TTL for movie data)
  - Optimized database queries

### Technical Features

- RESTful API endpoints
- Comprehensive Swagger documentation
- PostgreSQL database
- Error handling and validation
- Secure password hashing

## 🛠️ Technologies Used

| Category        | Technologies                          |
|-----------------|---------------------------------------|
| Backend         | Django, Django REST Framework         |
| Database        | PostgreSQL                            |
| Caching         | Redis                                 |
| Authentication  | JWT (djangorestframework-simplejwt)   |
| API Docs        | Swagger (drf-yasg)                    |
| Movie Data      | TMDb API integration                  |

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL
- Redis (free at  [Upstash Documentation](https://docs.upstash.com/))
- TMDb API key (free at [themoviedb.org](https://www.themoviedb.org/settings/api))

### Setup

1. **Clone Repository**

    ```bash
    git clone https://github.com/yourusername/movie_recommender.git
    cd movie_recommender
    ```

2. **Install Dependencies**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate  # Windows
    pip install -r requirements.txt
    ```

3. **Configure Environment**

  ## Environment Setup
      Copy the example environment file:
      - Create  file.env:
   ```bash
   - Create  file.env:
   cp .env.example .env
    
  ```
4. **Run Migrations**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Start Service**

    ```bash
    # Start Redis (new terminal)
    redis-server

    # Start Django
    python3 manage.py runserver
    ```

📚 API Documentation
Access interactive documentation at:
<https://flick-nexus-finder-7b5f0047c57a.herokuapp.com/api/docs/>

...

## Key Endpoints

| Endpoint                                | Method | Description                   | Auth Required |
|-----------------------------------------|--------|-------------------------------|---------------|
| /api/v1/auth/register/                  | POST   | User registration             | No            |
| /api/v1/auth/login/                     | POST   | Get JWT access & refresh tokens | No          |
| /api/v1/auth/token/refresh/             | POST   | Refresh access token          | No            |
| /api/v1/auth/favorites/                 | GET    | Get user's favorite movies     | Yes           |
| /api/v1/auth/favorites/                 | POST   | Add movie to favorites         | Yes           |
| /api/v1/auth/favorites/<int:id>/        | DELETE | Remove a movie from favorites  | Yes           |
| /api/v1/movies/trending/                | GET    | Get trending movies (weekly)   | No            |
| /api/v1/movies/{movie_id}/recommendations/ | GET    | Get recommendations for a movie | No          |
| /api/v1/movies/{movie_id}/              | GET    | Get details of a movie by ID   | No           |
| /api/v1/movies/search/                  | GET    | Search for movies              | No           |

...

🔍 Testing Endpoints with Swagger

1. **User Registration**

    ```bash
    curl -X POST "http://localhost:8000/api/v1/auth/register/" \
      -H "Content-Type: application/json" \
      -d '{
        "username": "movieenthusiast",
        "password": "SecurePass123!",
        "password2": "SecurePass123!",
        "email": "user@example.com"
      }'
    ```

2. **User Login**

    ```bash
    curl -X POST "http://localhost:8000/api/v1/auth/login/" \
      -H "Content-Type: application/json" \
      -d '{
        "username": "moviebuff",
        "password": "SecurePass123!"
      }'
    ```

3. **Access Protected Endpoint (Favorites)**

    ```bash
    curl -X GET "http://localhost:8000/api/v1/auth/favorites/" \
      -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
    ```

4. **Refresh Token**

    ```bash
    curl -X POST "http://localhost:8000/api/v1/auth/token/refresh/" \
      -H "Content-Type: application/json" \
      -d '{"refresh": "your_refresh_token_here"}'
    ```

5. **Add Favorite Movie**

    ```bash
    curl -X POST "http://localhost:8000/api/v1/auth/favorites/" \
      -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"movie_id": 550}'  # Fight Club example
    ```

6. **Search for Movies**

    ```bash
    curl -X GET "http://localhost:8000/api/v1/movies/search/?query=Inception&year=2010&genre=Action&page=1&page_size=20" \
      -H "Content-Type: application/json"
    ```

7. **Get Movie Details by ID**

    ```bash
    curl -X GET "http://localhost:8000/api/v1/movies/550/" \
      -H "Content-Type: application/json"
    ```

## 🌐 Environment Variables

| Variable      | Description            | Example                      |
|---------------|------------------------|------------------------------|
| TMDB_API_KEY  | TMDb API key           | abcdef123456                 |
| REDIS_HOST    | Redis host address      | localhost                    |
| REDIS_PORT    | Redis port number       | 6379                        |
| DB_*          | PostgreSQL credentials | (See .env example)           |

## 📚 Additional Documentation

For more detailed documentation, please refer to the `docs` directory:

- [Database Schema](movie_recommender/docs/Database_schema.md)
- [ERD Diagram Analysis](movie_recommender/docs/ERD_Diagram_Analysis.md)
- [Redis Setup](movie_recommender/docs/REDIS_SETUP.md)

📜 License
[MIT License](LICENSE) - see LICENSE for details

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Note: Replace placeholder values (YOUR_ACCESS_TOKEN, your-tmdb-api-key, etc.) with actual values when testing.