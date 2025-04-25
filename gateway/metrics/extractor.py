from prometheus_client import Histogram, Gauge, Counter

# Drug extractor metrics
EXTRACTOR_LATENCY = Histogram(
    'extractor_request_duration_seconds',
    'Time spent extracting drug names',
    ['status']
)

DRUGS_EXTRACTED = Gauge(
    'extractor_drugs_total',
    'Number of drug names parsed from text',
    ['status']
)

EXTRACTOR_ERRORS = Counter(
    'extractor_errors_total',
    'Number of failed extractor calls',
    ['error_type']
)

def record_extractor_metrics(duration, drug_count, success=True, error_type=None):
    """Record drug extractor metrics.
    
    Args:
        duration: Time taken for extraction in seconds
        drug_count: Number of drugs extracted
        success: Whether the extraction was successful
        error_type: Type of error if any (e.g., 'timeout', '5xx')
    """
    status = 'success' if success else 'failure'
    EXTRACTOR_LATENCY.labels(status=status).observe(duration)
    DRUGS_EXTRACTED.labels(status=status).set(drug_count)
    
    if not success and error_type:
        EXTRACTOR_ERRORS.labels(error_type=error_type).inc() 