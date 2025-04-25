from prometheus_client import Counter, Histogram, start_http_server
from prometheus_client.exposition import generate_latest
from flask import request, Response
import time

# HTTP metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

def instrument_app(app):
    """Instrument the Flask app with Prometheus metrics."""
    
    @app.before_request
    def before_request():
        request.start_time = time.time()

    @app.after_request
    def after_request(response):
        # Record request count
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code
        ).inc()

        # Record request latency
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.path
        ).observe(time.time() - request.start_time)

        return response

    @app.route('/metrics')
    def metrics():
        """Expose Prometheus metrics."""
        return Response(generate_latest(), mimetype='text/plain')

def start_metrics_server(port=8000):
    """Start the Prometheus metrics server."""
    start_http_server(port) 