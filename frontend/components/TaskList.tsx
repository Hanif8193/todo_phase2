"use client";

/**
 * TaskList Component.
 *
 * This component provides:
 * - Fetches and displays all tasks for a user
 * - Loading state during data fetch
 * - Empty state when no tasks exist
 * - Error handling for API failures
 * - Renders TaskItem for each task
 */

import { useEffect, useState } from "react";
import { api, type Task } from "@/lib/api";
import TaskItem from "./TaskItem";

interface TaskListProps {
  userId: number;
  onTaskUpdated?: () => void;
  refreshTrigger?: number;
}

export default function TaskList({ userId, onTaskUpdated, refreshTrigger }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>("");

  const fetchTasks = async () => {
    setIsLoading(true);
    setError("");

    try {
      const fetchedTasks = await api.getTasks(userId);
      setTasks(fetchedTasks);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to load tasks";
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [userId, refreshTrigger]);

  const handleTaskDeleted = (taskId: number) => {
    // Remove task from local state
    setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
    onTaskUpdated?.();
  };

  const handleTaskToggled = (taskId: number, isCompleted: boolean) => {
    // Update task in local state
    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === taskId ? { ...task, is_completed: isCompleted } : task
      )
    );
    onTaskUpdated?.();
  };

  const handleTaskEdited = () => {
    // Refresh task list after edit
    fetchTasks();
    onTaskUpdated?.();
  };

  // Loading State
  if (isLoading) {
    return (
      <div className="p-8 text-center">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading tasks...</p>
      </div>
    );
  }

  // Error State
  if (error) {
    return (
      <div className="p-8">
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-red-400"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">
                Error loading tasks
              </h3>
              <p className="mt-1 text-sm text-red-700">{error}</p>
              <button
                onClick={fetchTasks}
                className="mt-3 text-sm font-medium text-red-600 hover:text-red-500"
              >
                Try again
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Empty State
  if (tasks.length === 0) {
    return (
      <div className="p-12 text-center">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
        <h3 className="mt-4 text-lg font-medium text-gray-900">
          No tasks yet
        </h3>
        <p className="mt-2 text-sm text-gray-500">
          Get started by creating your first task.
        </p>
      </div>
    );
  }

  // Task List
  return (
    <div className="divide-y divide-gray-200">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          userId={userId}
          onDeleted={handleTaskDeleted}
          onToggled={handleTaskToggled}
          onEdited={handleTaskEdited}
        />
      ))}
    </div>
  );
}
