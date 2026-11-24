from prometheus_client import Counter, Histogram

#Total HTTP requests
HTTP_REQUESTS =Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "status_code"]
)

#HTTP errors (4xx and 5xx)
HTTP_ERRORS = Counter(
    "http_errors_total",
    "Total number of HTTP errors",
    ["method", "status_code"]
)

#Request processing duration
HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method"]
)

# Successfully created orders
ORDERS_CREATED = Counter(
    "orders_created_total",
    "Total number of successfully created orders"
)