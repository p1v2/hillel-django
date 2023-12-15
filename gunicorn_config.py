from os import cpu_count

# Bind
bind = "0.0.0.0:8000"

# Worker processes
workers = 1
worker_class = "sync"


# Threads per worker
threads = 1

# Logging
loglevel = "debug"

# Limit count of requests per worker
max_requests = 5

# Other interesting configuration
preload_app = True # Load application code before the worker processes are forked.