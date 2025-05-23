bind = "0.0.0.0:8000"
workers = 3  # Recommended formula is 2 * number of CPU cores + 1
timeout = 120
wsgi_app = "apis.wsgi:application"
