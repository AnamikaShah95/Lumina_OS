class LuminaCoreException(Exception):
    """Base exception matrix tracking all structural anomalies inside Lumina OS architecture."""
    def __init__(self, message: str, dashboard_alert_level: str = "ERROR"):
        super().__init__(message)
        self.message = message
        self.alert_level = dashboard_alert_level

class TranscriptExtractionError(LuminaCoreException):
    """Triggered specifically when remote scrapers encounter missing or unparseable metadata streams."""
    def __init__(self, message: str):
        super().__init__(message, dashboard_alert_level="WARNING")

class SchemaValidationException(LuminaCoreException):
    """Triggered when LLM JSON outputs violate structural formatting boundaries mapped in Pydantic templates."""
    def __init__(self, message: str):
        super().__init__(message, dashboard_alert_level="CRITICAL")