from prometheus_client import Histogram, Gauge, Counter

# OCR service metrics
OCR_LATENCY = Histogram(
    'ocr_request_duration_seconds',
    'Time spent in OCR service',
    ['status']
)

TEXT_LENGTH = Gauge(
    'ocr_text_length_total',
    'Total characters of OCR\'d text per request',
    ['status']
)

OCR_ERRORS = Counter(
    'ocr_errors_total',
    'Number of failed OCR invocations',
    ['error_type']
)

def record_ocr_metrics(duration, text_length, success=True, error_type=None):
    """Record OCR service metrics.
    
    Args:
        duration: Time taken for OCR in seconds
        text_length: Length of extracted text
        success: Whether the OCR was successful
        error_type: Type of error if any (e.g., 'timeout', '5xx')
    """
    status = 'success' if success else 'failure'
    OCR_LATENCY.labels(status=status).observe(duration)
    TEXT_LENGTH.labels(status=status).set(text_length)
    
    if not success and error_type:
        OCR_ERRORS.labels(error_type=error_type).inc() 