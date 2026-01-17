"""
Task management routes for CRUD operations and completion toggling.

This module implements:
- GET /api/{user_id}/tasks: List all tasks for a user
- POST /api/{user_id}/tasks: Create a new task
- GET /api/{user_id}/tasks/{id}: Get a specific task
- PUT /api/{user_id}/tasks/{id}: Update a task
- DELETE /api/{user_id}/tasks/{id}: Delete a task
- PATCH /api/{user_id}/tasks/{id}/complete: Toggle task completion status

All routes enforce user-scoped data access and require authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime
from db import get_session
from models import Task, TaskCreate, TaskUpdate, TaskResponse, TaskCompletionToggle
from auth import get_current_user, validate_user_access

router = APIRouter()


@router.get(
    "/{user_id}/tasks",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all tasks for a user",
    description="Retrieve all tasks belonging to the authenticated user. Results are ordered by creation date.",
)
async def get_tasks(
    user_id: int = Path(..., description="User ID (must match authenticated user)"),
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Retrieve all tasks for the authenticated user.

    Args:
        user_id: User ID from URL path (must match JWT user)
        current_user: Authenticated user from JWT token
        session: Database session (injected dependency)

    Returns:
        List[TaskResponse]: List of tasks ordered by creation date (oldest first)

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user

    Security:
        - User can only access their own tasks
        - Tasks are filtered by user_id from JWT, NOT from URL
    """
    # Validate user has access to this resource
    validate_user_access(current_user["user_id"], user_id)

    # Query tasks for authenticated user (using JWT user_id, not URL parameter)
    result = await session.execute(
        select(Task)
        .where(Task.user_id == current_user["user_id"])
        .order_by(Task.created_at)
    )
    tasks = result.scalars().all()

    # Convert to response models
    return [
        TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
        for task in tasks
    ]


@router.post(
    "/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the authenticated user.",
)
async def create_task(
    task_data: TaskCreate,
    user_id: int = Path(..., description="User ID (must match authenticated user)"),
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Create a new task for the authenticated user.

    Args:
        task_data: TaskCreate schema with title and optional description
        user_id: User ID from URL path (must match JWT user)
        current_user: Authenticated user from JWT token
        session: Database session (injected dependency)

    Returns:
        TaskResponse: Created task data

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user
        HTTPException 422: If validation fails

    Validation Rules:
        - Title: 1-200 characters (non-empty)
        - Description: Optional, max 2000 characters

    Security:
        - Task is created with user_id from JWT token, NOT from URL
        - User cannot create tasks for other users
    """
    # Validate user has access to this resource
    validate_user_access(current_user["user_id"], user_id)

    # Create new task with user_id from JWT token (NOT from URL)
    new_task = Task(
        user_id=current_user["user_id"],
        title=task_data.title,
        description=task_data.description,
        is_completed=False,
    )

    session.add(new_task)
    await session.flush()  # Flush to get the task ID
    await session.refresh(new_task)  # Refresh to get all fields

    return TaskResponse(
        id=new_task.id,
        user_id=new_task.user_id,
        title=new_task.title,
        description=new_task.description,
        is_completed=new_task.is_completed,
        created_at=new_task.created_at,
        updated_at=new_task.updated_at,
    )


@router.get(
    "/{user_id}/tasks/{id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a specific task",
    description="Retrieve a single task by ID for the authenticated user.",
)
async def get_task(
    user_id: int = Path(..., description="User ID (must match authenticated user)"),
    id: int = Path(..., description="Task ID"),
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Retrieve a specific task by ID.

    Args:
        user_id: User ID from URL path (must match JWT user)
        id: Task ID to retrieve
        current_user: Authenticated user from JWT token
        session: Database session (injected dependency)

    Returns:
        TaskResponse: Task data

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user
        HTTPException 404: If task not found or belongs to another user

    Security:
        - User can only access their own tasks
        - Returns 404 (not 403) to prevent information leakage about task existence
    """
    # Validate user has access to this resource
    validate_user_access(current_user["user_id"], user_id)

    # Query task by ID and user_id (user-scoped)
    result = await session.execute(
        select(Task).where(
            Task.id == id,
            Task.user_id == current_user["user_id"]
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.put(
    "/{user_id}/tasks/{id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a task",
    description="Update title and/or description of an existing task.",
)
async def update_task(
    task_update: TaskUpdate,
    user_id: int = Path(..., description="User ID (must match authenticated user)"),
    id: int = Path(..., description="Task ID"),
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Update an existing task's title and/or description.

    Args:
        task_update: TaskUpdate schema with optional title and description
        user_id: User ID from URL path (must match JWT user)
        id: Task ID to update
        current_user: Authenticated user from JWT token
        session: Database session (injected dependency)

    Returns:
        TaskResponse: Updated task data

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user
        HTTPException 404: If task not found or belongs to another user
        HTTPException 422: If validation fails

    Validation Rules:
        - Title: If provided, 1-200 characters (non-empty)
        - Description: If provided, max 2000 characters

    Note:
        - Only provided fields are updated (partial update)
        - updated_at timestamp is automatically refreshed
    """
    # Validate user has access to this resource
    validate_user_access(current_user["user_id"], user_id)

    # Query task by ID and user_id (user-scoped)
    result = await session.execute(
        select(Task).where(
            Task.id == id,
            Task.user_id == current_user["user_id"]
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Update fields if provided
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description

    # Update the updated_at timestamp
    task.updated_at = datetime.utcnow()

    await session.flush()
    await session.refresh(task)

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.delete(
    "/{user_id}/tasks/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Permanently delete a task by ID.",
)
async def delete_task(
    user_id: int = Path(..., description="User ID (must match authenticated user)"),
    id: int = Path(..., description="Task ID"),
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Delete a task permanently.

    Args:
        user_id: User ID from URL path (must match JWT user)
        id: Task ID to delete
        current_user: Authenticated user from JWT token
        session: Database session (injected dependency)

    Returns:
        None (204 No Content)

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user
        HTTPException 404: If task not found or belongs to another user

    Security:
        - User can only delete their own tasks
        - Deletion is permanent and cannot be undone
    """
    # Validate user has access to this resource
    validate_user_access(current_user["user_id"], user_id)

    # Query task by ID and user_id (user-scoped)
    result = await session.execute(
        select(Task).where(
            Task.id == id,
            Task.user_id == current_user["user_id"]
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Delete the task
    await session.delete(task)
    # No content response (204) - FastAPI handles this automatically
    return None


@router.patch(
    "/{user_id}/tasks/{id}/complete",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Toggle task completion status",
    description="Mark a task as completed or incomplete.",
)
async def toggle_task_completion(
    completion_data: TaskCompletionToggle,
    user_id: int = Path(..., description="User ID (must match authenticated user)"),
    id: int = Path(..., description="Task ID"),
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Update the completion status of a task.

    Args:
        completion_data: TaskCompletionToggle schema with is_completed boolean
        user_id: User ID from URL path (must match JWT user)
        id: Task ID to update
        current_user: Authenticated user from JWT token
        session: Database session (injected dependency)

    Returns:
        TaskResponse: Updated task data

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user
        HTTPException 404: If task not found or belongs to another user
        HTTPException 422: If is_completed is not a boolean

    Validation Rules:
        - is_completed: Must be a boolean (true/false)

    Note:
        - updated_at timestamp is automatically refreshed
    """
    # Validate user has access to this resource
    validate_user_access(current_user["user_id"], user_id)

    # Query task by ID and user_id (user-scoped)
    result = await session.execute(
        select(Task).where(
            Task.id == id,
            Task.user_id == current_user["user_id"]
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Update completion status
    task.is_completed = completion_data.is_completed

    # Update the updated_at timestamp
    task.updated_at = datetime.utcnow()

    await session.flush()
    await session.refresh(task)

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
