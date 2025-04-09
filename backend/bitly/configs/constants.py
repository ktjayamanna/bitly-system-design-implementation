
# Database connection pool settings
DB_POOL_SIZE = 10         # Maximum number of connections in the pool
DB_MAX_OVERFLOW = 5       # Extra connections beyond pool_size
DB_POOL_TIMEOUT = 30      # Timeout for getting a connection from the pool
DB_POOL_RECYCLE = 1800    # Recycle connections after 30 minutes

# Redis keys
COUNTER_KEY = "global_url_counter"

