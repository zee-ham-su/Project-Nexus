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
  - Redis caching (6-hour TTL for movie data)
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
- Redis
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

    - Create  file.env:

    ```bash
    SECRET_KEY=your-django-secret-key
    DEBUG=True
    DB_NAME=movie_db
    DB_USER=movie_user
    DB_PASSWORD=securepassword123
    DB_HOST=localhost
    DB_PORT=5432
    TMDB_API_KEY=your-tmdb-api-key
    REDIS_URL=redis://localhost:6379/0
    REDIS_PORT=6379
    ```

4. **Database Setup**

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
<http://localhost:8000/api/docs/>

## Key Endpoints

| Endpoint                                | Method | Description                   | Auth Required |
|-----------------------------------------|--------|-------------------------------|---------------|
| /api/auth/register/                     | POST   | User registration             | No            |
| /api/auth/login/                        | POST   | Get JWT access & refresh tokens | No          |
| /api/auth/token/refresh/                | POST   | Refresh access token          | No            |
| /api/auth/favorites/                    | GET    | Get user's favorite movies     | Yes           |
| /api/auth/favorites/                    | POST   | Add movie to favorites         | Yes           |
| /api/movies/trending/                   | GET    | Get trending movies (weekly)   | No            |
| /api/movies/{movie_id}/recommendations/ | GET    | Get recommendations for a movie | No          |

🔍 Testing Endpoints with Swagger

1. **User Registration**

    ```bash
    curl -X POST "http://localhost:8000/api/auth/register/" \
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
    curl -X POST "http://localhost:8000/api/auth/login/" \
      -H "Content-Type: application/json" \
      -d '{
        "username": "moviebuff",
        "password": "SecurePass123!"
      }'
    ```

3. **Access Protected Endpoint (Favorites)**

    ```bash
    curl -X GET "http://localhost:8000/api/auth/favorites/" \
      -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
    ```

4. **Refresh Token**

    ```bash
    curl -X POST "http://localhost:8000/api/auth/token/refresh/" \
      -H "Content-Type: application/json" \
      -d '{"refresh": "your_refresh_token_here"}'
    ```

5. **Add Favorite Movie**

    ```bash
    curl -X POST "http://localhost:8000/api/auth/favorites/" \
      -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"movie_id": 550}'  # Fight Club example
    ```

## 🌐 Environment Variables

| Variable      | Description            | Example                      |
|---------------|------------------------|------------------------------|
| TMDB_API_KEY  | TMDb API key           | abcdef123456                 |
| REDIS_URL     | Redis connection URL   | redis://localhost:6379/0     |
| DB_*          | PostgreSQL credentials | (See .env example)           |

📜 License
[MIT License](LICENSE) - see LICENSE for details

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Note: Replace placeholder values (YOUR_ACCESS_TOKEN, your-tmdb-api-key, etc.) with actual values when testing.
