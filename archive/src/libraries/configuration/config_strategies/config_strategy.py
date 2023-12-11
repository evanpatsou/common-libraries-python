from abc import ABC, abstractmethod

class ConfigStrategy(ABC):
    """Abstract base class defining the interface for configuration strategies."""

    @abstractmethod
    def read_config(self) -> dict:
        """Abstract method to read configuration data."""
        pass
