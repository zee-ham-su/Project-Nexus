# Deployment Guide for Movie Recommender

This guide explains how to deploy the Movie Recommender application using Docker on Render and Railway platforms.

## Why Dockerize?

Dockerizing your application provides several benefits:

1. **Consistency**: Ensures the application runs the same way in development and production
2. **Isolation**: Packages all dependencies in one container
3. **Easy Deployment**: Simplifies the deployment process on various cloud platforms
4. **Scalability**: Makes scaling your application easier
5. **Infrastructure as Code**: Your deployment configuration is versioned along with your code

We've already set up the following Docker-related files:
- `Dockerfile`: Defines how to build the application container
- `docker-compose.yml`: For local development with PostgreSQL and Redis

## Setting up for Deployment

Before deploying, ensure you have:

1. A GitHub repository with your code
2. Docker-related files in your repository
3. An account on either Render or Railway

## Deploying on Render

Render provides an easy way to deploy Docker containers with their Web Service option.

### Steps:

1. **Create a New Web Service**:
   - Log in to your Render account
   - Click "New" and select "Web Service"
   - Connect your GitHub repository

2. **Configure the Service**:
   - Select "Docker" as the Environment
   - Set the name for your service
   - Choose a region close to your users
   - Select the branch to deploy (usually `main`)

3. **Set Environment Variables**:
   Under the "Environment" section, add the following:
   ```
   SECRET_KEY=<your-secure-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=<your-render-domain>.onrender.com
   DB_NAME=<db-name>
   DB_USER=<db-user>
   DB_PASSWORD=<db-password>
   DB_HOST=<db-host>
   DB_PORT=5432
   ```

4. **Set up Database**:
   - Create a PostgreSQL service on Render
   - Link it to your web service
   - Update the environment variables with the database connection information

5. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically build and deploy your Docker container

### Auto-deploy on Push

Render automatically redeploys your application when you push changes to your connected GitHub repository.

## Deploying on Railway

Railway offers a developer-friendly platform for deploying containerized applications.

### Steps:

1. **Create a New Project**:
   - Log in to Railway
   - Click "New Project" and select "Deploy from GitHub repo"
   - Connect your GitHub repository

2. **Configure the Service**:
   - Railway will automatically detect your Dockerfile
   - Click on the service and navigate to "Settings"
   - Set the start command to match your Dockerfile CMD

3. **Set Environment Variables**:
   In the "Variables" tab, add:
   ```
   SECRET_KEY=<your-secure-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=<your-railway-domain>.railway.app
   DB_NAME=<db-name>
   DB_USER=<db-user>
   DB_PASSWORD=<db-password>
   DB_HOST=<db-host>
   DB_PORT=5432
   ```

4. **Add a Database**:
   - Click "New" and select "Database" to add a PostgreSQL database
   - Railway will automatically link it to your service
   - Update your environment variables with the connection details

5. **Deploy**:
   - Railway will automatically build and deploy your application

### Domain Configuration

Both Render and Railway provide temporary domains. To use a custom domain:
1. Purchase a domain from a provider like Namecheap or GoDaddy
2. Add the domain in your platform's settings
3. Configure DNS settings as instructed by the platform
4. Update the `ALLOWED_HOSTS` environment variable to include your custom domain

## Local Development with Docker

To run the application locally using Docker:

```bash
# Create a .env file with your local environment variables
cp .env.example .env

# Build and start the services
docker-compose up --build
```

This will start the Django application, PostgreSQL database, and Redis server.

## Troubleshooting

### Common Issues:

1. **Database Connection Errors**:
   - Verify your database environment variables
   - Ensure your database service is running

2. **Static Files Not Loading**:
   - Make sure `collectstatic` runs during the Docker build
   - Verify WhiteNoise configuration in settings.py

3. **Application Errors**:
   - Check the logs in your platform dashboard
   - Temporarily set `DEBUG=True` to see detailed error messages

## Conclusion

Dockerizing your application makes deployment more consistent and manageable across different platforms. Both Render and Railway provide excellent options for hosting containerized applications, with Railway being slightly more developer-focused and Render offering more built-in features for larger applications.

Choose the platform that best fits your needs and budget!