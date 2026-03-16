class DjangoAgentRagError(Exception):
    """Base package exception."""


class ConfigurationError(DjangoAgentRagError):
    """Raised for invalid package configuration."""


class OptionalDependencyMissing(DjangoAgentRagError):
    """Raised when an optional backend is configured without its dependency."""

