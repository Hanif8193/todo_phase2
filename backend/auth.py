"""
JWT authentication middleware and utilities.

This module handles:
- JWT token verification
- User authentication dependency for FastAPI routes
- Token creation and validation
- User ID extraction from JWT claims
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme for FastAPI
security = HTTPBearer()


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.

    Args:
        password: Plaintext password to hash

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.

    Args:
        plain_password: Plaintext password to verify
        hashed_password: Hashed password to compare against

    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, email: str) -> str:
    """
    Create a JWT access token for a user.

    Args:
        user_id: User's database ID
        email: User's email address

    Returns:
        str: Encoded JWT token

    Token payload includes:
        - sub: User ID (subject)
        - email: User's email
        - exp: Expiration timestamp
        - iat: Issued at timestamp
    """
    expires_delta = timedelta(days=settings.JWT_EXPIRATION_DAYS)
    expire = datetime.utcnow() + expires_delta

    payload = {
        "sub": str(user_id),  # Subject: user ID
        "email": email,
        "exp": expire,  # Expiration time
        "iat": datetime.utcnow(),  # Issued at time
    }

    token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string to verify

    Returns:
        dict: Decoded token payload with user_id and email

    Raises:
        HTTPException: If token is invalid or expired (401 Unauthorized)
    """
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "user_id": int(user_id),
            "email": email
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    FastAPI dependency to extract and verify the current authenticated user.

    This dependency should be used in all protected routes to ensure
    the user is authenticated.

    Usage:
        @app.get("/protected")
        async def protected_route(user: dict = Depends(get_current_user)):
            user_id = user["user_id"]
            email = user["email"]
            # ... use user_id to access user-scoped data

    Args:
        credentials: HTTP Bearer token credentials from request header

    Returns:
        dict: User information with 'user_id' and 'email' keys

    Raises:
        HTTPException: If token is invalid or expired (401 Unauthorized)
    """
    token = credentials.credentials
    return verify_token(token)


def validate_user_access(current_user_id: int, resource_user_id: int) -> None:
    """
    Validate that the current user has access to a resource.

    This function ensures that users can only access their own resources.
    Should be called in routes where user_id appears in the URL path.

    Args:
        current_user_id: User ID from JWT token
        resource_user_id: User ID from URL path parameter

    Raises:
        HTTPException: If user IDs don't match (403 Forbidden)
    """
    if current_user_id != resource_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other user's resources",
        )
