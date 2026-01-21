/**
 * Centralized API client with JWT authentication.
 *
 * This module provides:
 * - API request wrapper with automatic JWT token injection
 * - Type-safe API methods for task operations
 * - Error handling and response parsing
 */

import { authClient } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Task type definition matching backend Task model.
 */
export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Task creation request data.
 */
export interface TaskCreate {
  title: string;
  description?: string;
}

/**
 * Task update request data.
 */
export interface TaskUpdate {
  title?: string;
  description?: string;
}

/**
 * API client for making authenticated requests.
 */
class ApiClient {
  /**
   * Make an authenticated API request.
   *
   * @param endpoint - API endpoint path (without base URL)
   * @param options - Fetch options (method, body, etc.)
   * @returns Promise with parsed JSON response
   * @throws Error if request fails or response is not ok
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = authClient.getToken();

    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...(options.headers || {}),
      // Add JWT token to Authorization header if available
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    };

    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    // Handle authentication errors
    if (response.status === 401) {
      // Token expired or invalid - clear local storage and redirect to signin
      authClient.signOut();
      if (typeof window !== "undefined") {
        window.location.href = "/signin?error=Session expired. Please sign in again.";
      }
      throw new Error("Unauthorized");
    }

    // Handle other errors
    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: "Request failed",
      }));
      throw new Error(error.detail || `Request failed with status ${response.status}`);
    }

    // Handle 204 No Content responses
    if (response.status === 204) {
      return null as T;
    }

    return response.json();
  }

  // ============================================================================
  // Task API Methods
  // ============================================================================

  /**
   * Get all tasks for a user.
   *
   * @param userId - User ID to fetch tasks for
   * @returns Promise with array of tasks
   */
  async getTasks(userId: number): Promise<Task[]> {
    return this.request<Task[]>(`/api/${userId}/tasks`, {
      method: "GET",
    });
  }

  /**
   * Get a single task by ID.
   *
   * @param userId - User ID who owns the task
   * @param taskId - Task ID to fetch
   * @returns Promise with task data
   */
  async getTask(userId: number, taskId: number): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: "GET",
    });
  }

  /**
   * Create a new task.
   *
   * @param userId - User ID to create task for
   * @param data - Task creation data (title, description)
   * @returns Promise with created task data
   */
  async createTask(userId: number, data: TaskCreate): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  /**
   * Update an existing task.
   *
   * @param userId - User ID who owns the task
   * @param taskId - Task ID to update
   * @param data - Task update data (title, description)
   * @returns Promise with updated task data
   */
  async updateTask(
    userId: number,
    taskId: number,
    data: TaskUpdate
  ): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  /**
   * Delete a task.
   *
   * @param userId - User ID who owns the task
   * @param taskId - Task ID to delete
   * @returns Promise that resolves when task is deleted
   */
  async deleteTask(userId: number, taskId: number): Promise<void> {
    return this.request<void>(`/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    });
  }

  /**
   * Toggle task completion status.
   *
   * @param userId - User ID who owns the task
   * @param taskId - Task ID to toggle
   * @param isCompleted - New completion status
   * @returns Promise with updated task data
   */
  async toggleTaskCompletion(
    userId: number,
    taskId: number,
    isCompleted: boolean
  ): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: "PATCH",
      body: JSON.stringify({ is_completed: isCompleted }),
    });
  }
}

// Export singleton instance
export const api = new ApiClient();
