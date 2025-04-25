from prometheus_client import Histogram, Counter

# Drug interaction metrics
INTERACTION_LATENCY = Histogram(
    'interaction_request_duration_seconds',
    'Time spent querying drug-interaction RAG',
    ['status']
)

INTERACTIONS_FOUND = Counter(
    'interaction_pairs_total',
    'Number of interaction pairs found',
    ['status']
)

INTERACTION_ERRORS = Counter(
    'interaction_errors_total',
    'Number of failed interaction calls',
    ['error_type']
)

def record_interaction_metrics(duration, interaction_count, success=True, error_type=None):
    """Record drug interaction metrics.
    
    Args:
        duration: Time taken for interaction check in seconds
        interaction_count: Number of interactions found
        success: Whether the interaction check was successful
        error_type: Type of error if any (e.g., 'timeout', '5xx')
    """
    status = 'success' if success else 'failure'
    INTERACTION_LATENCY.labels(status=status).observe(duration)
    INTERACTIONS_FOUND.labels(status=status).inc(interaction_count)
    
    if not success and error_type:
        INTERACTION_ERRORS.labels(error_type=error_type).inc()