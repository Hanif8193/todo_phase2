"""
Authentication routes for user registration, signin, and signout.

This module implements:
- POST /auth/signup: User registration with email and password
- POST /auth/signin: User authentication and JWT token generation
- POST /auth/signout: User signout (stateless JWT acknowledgment)

All routes follow REST conventions with proper error handling and status codes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_session
from models import User, UserCreate, UserLogin, UserResponse
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter()


@router.post(
    "/signup",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password. Returns JWT token and user data.",
)
async def signup(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    """
    Register a new user account.

    Args:
        user_data: UserCreate schema with email and password
        session: Database session (injected dependency)

    Returns:
        dict: {
            "token": str (JWT access token),
            "user": UserResponse (user data without password)
        }

    Raises:
        HTTPException 400: If email already exists
        HTTPException 422: If validation fails (email/password format)

    Validation Rules:
        - Email: 3-255 characters
        - Password: 8-100 characters (plaintext, will be hashed)

    Security:
        - Password is hashed using bcrypt before storage
        - JWT token expires after configured JWT_EXPIRATION_DAYS
    """
    # Check if email already exists
    result = await session.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash the password
    password_hash = hash_password(user_data.password)

    # Create new user
    new_user = User(
        email=user_data.email,
        password_hash=password_hash,
    )

    session.add(new_user)
    await session.flush()  # Flush to get the user ID
    await session.refresh(new_user)  # Refresh to get all fields including created_at

    # Generate JWT token
    token = create_access_token(user_id=new_user.id, email=new_user.email)

    # Return token and user data
    return {
        "token": token,
        "user": UserResponse(
            id=new_user.id,
            email=new_user.email,
            created_at=new_user.created_at,
        ),
    }


@router.post(
    "/signin",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Sign in a user",
    description="Authenticate user with email and password. Returns JWT token and user data.",
)
async def signin(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_session),
):
    """
    Authenticate a user and generate access token.

    Args:
        credentials: UserLogin schema with email and password
        session: Database session (injected dependency)

    Returns:
        dict: {
            "token": str (JWT access token),
            "user": UserResponse (user data without password)
        }

    Raises:
        HTTPException 401: If email not found or password incorrect

    Security:
        - Password verification using bcrypt
        - Constant-time password comparison to prevent timing attacks
        - Generic error message to prevent email enumeration
    """
    # Query user by email
    result = await session.execute(
        select(User).where(User.email == credentials.email)
    )
    user = result.scalar_one_or_none()

    # Verify user exists and password is correct
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token
    token = create_access_token(user_id=user.id, email=user.email)

    # Return token and user data
    return {
        "token": token,
        "user": UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
        ),
    }


@router.post(
    "/signout",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Sign out a user",
    description="Sign out the authenticated user. Since JWT is stateless, this is an acknowledgment endpoint.",
)
async def signout(
    current_user: dict = Depends(get_current_user),
):
    """
    Sign out the authenticated user.

    Args:
        current_user: Current authenticated user (injected from JWT token)

    Returns:
        dict: Success message

    Note:
        JWT tokens are stateless and cannot be invalidated server-side.
        Clients should discard the token upon receiving this response.
        For additional security, implement token blacklisting or use refresh tokens.

    Security:
        - Requires valid JWT token (enforced by get_current_user dependency)
        - Client must remove token from storage after this call
    """
    return {
        "message": "Signed out successfully",
    }
