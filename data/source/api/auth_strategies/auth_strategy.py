from abc import ABC, abstractmethod

class AuthStrategy(ABC):
    """Abstract base class for authentication strategies."""

    @abstractmethod
    def authenticate(self) -> str:
        """Authenticate and return the token.

        Returns:
            str: The authentication token.
        """
        pass

    @abstractmethod
    def is_authenticated(self) -> bool:
        """Check if the current authentication is still valid.

        Returns:
            bool: True if authenticated, False otherwise.
        """
        pass
