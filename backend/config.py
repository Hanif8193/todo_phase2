"""
Configuration management for backend application.

This module handles:
- Environment variable loading
- Application settings
- Secret validation
"""

import os
from dotenv import load_dotenv
from typing import List

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application configuration settings."""

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Authentication
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_DAYS: int = 7

    # Server
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))

    # CORS
    CORS_ORIGINS: List[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    ]

    def validate(self) -> None:
        """
        Validate required configuration values.

        Raises:
            ValueError: If any required configuration is missing or invalid
        """
        if not self.DATABASE_URL:
            raise ValueError(
                "DATABASE_URL is required. Please set it in backend/.env file."
            )

        if not self.BETTER_AUTH_SECRET:
            raise ValueError(
                "BETTER_AUTH_SECRET is required. Please set it in backend/.env file."
            )

        if len(self.BETTER_AUTH_SECRET) < 32:
            raise ValueError(
                "BETTER_AUTH_SECRET must be at least 32 characters long. "
                "Generate a secure secret with: openssl rand -base64 32"
            )

        print("Configuration validated successfully")


# Global settings instance
settings = Settings()
