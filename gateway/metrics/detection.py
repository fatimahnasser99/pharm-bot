from prometheus_client import Histogram, Gauge, Counter

# Detection service metrics
DETECTION_LATENCY = Histogram(
    'detection_request_duration_seconds',
    'Time spent in medicine detection service',
    ['status']
)

OBJECTS_DETECTED = Gauge(
    'detection_objects_total',
    'Number of bounding boxes detected per request',
    ['status']
)

DETECTION_ERRORS = Counter(
    'detection_errors_total',
    'Number of failed detection calls',
    ['error_type']
)

def record_detection_metrics(duration, object_count, success=True, error_type=None):
    """Record detection service metrics.
    
    Args:
        duration: Time taken for detection in seconds
        object_count: Number of objects detected
        success: Whether the detection was successful
        error_type: Type of error if any (e.g., 'timeout', '5xx')
    """
    status = 'success' if success else 'failure'
    DETECTION_LATENCY.labels(status=status).observe(duration)
    OBJECTS_DETECTED.labels(status=status).set(object_count)
    
    if not success and error_type:
        DETECTION_ERRORS.labels(error_type=error_type).inc() 