# Upstash Redis Configuration and CLI Usage

This guide provides instructions on how to configure and use Redis from Upstash with the Redis CLI.

## Prerequisites

- Upstash account
- Redis CLI installed on your local machine

## Getting Started

### 1. Create an Upstash Redis Database

1. Log in to your Upstash account.
2. Navigate to the "Databases" section.
3. Click on "Create Database" and follow the prompts to set up your Redis database.
4. Note down the connection details provided by Upstash (e.g., REST URL, Redis URL, and credentials).

### 2. Configure Environment Variables

Update your `.env` file with the following variables:

```env
UPSTASH_REDIS_REST_URL
UPSTASH_REDIS_REST_TOKEN
```

### Using Redis CLI with Upstash

To connect to your Upstash Redis instance using the Redis CLI, follow these steps:

1. **Install Redis CLI:**
   If you don't have the Redis CLI installed, you can install it using your package manager. For example, on Ubuntu:
   ```bash
   sudo apt-get install redis-tools
   ```

2. **Connect to Upstash Redis:**
   Use the following command to connect to your Upstash Redis instance. Replace `<password>`, `<host>`, and `<port>` with your Upstash Redis credentials:
   ```bash
   redis-cli --tls -u redis://default:<password>@<host>:<port>
   ```

   Example:
   ```bash
   redis-cli --tls -u redis://default:Ad8OAAIjcDfdjfmdfjdiMGY3Mzg0NDQwYWU0OWE0NTIxMDE3YTg2OXAxMA@hamza-tiger-57102.upstash.io:6379
   ```

#### Common Redis CLI Commands

- **PING**: Check if the server is running.

    ```bash
    redis-cli -u redis://:<password>@<host>:<port> ping
    ```

- **SET**: Set a key-value pair.

    ```bash
    redis-cli -u redis://:<password>@<host>:<port> set key value
    ```

- **GET**: Retrieve the value of a key.

    ```bash
    redis-cli -u redis://:<password>@<host>:<port> get key
    ```

- **DEL**: Delete a key.

    ```bash
    redis-cli -u redis://:<password>@<host>:<port> del key
    ```

### 4. Additional Resources

- [Upstash Documentation](https://docs.upstash.com/)
- [Redis CLI Documentation](https://redis.io/topics/rediscli)

## Troubleshooting

If you encounter any issues, refer to the Upstash documentation or contact their support for assistance.
