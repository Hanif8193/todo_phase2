"use client";

/**
 * TaskItem Component.
 *
 * This component provides:
 * - Display individual task with title, description, and status
 * - Checkbox to toggle task completion
 * - Edit and Delete action buttons
 * - Visual styling for completed tasks (strikethrough, gray color)
 * - Inline edit mode for updating task details
 */

import { useState } from "react";
import { api, type Task } from "@/lib/api";
import TaskForm from "./TaskForm";

interface TaskItemProps {
  task: Task;
  userId: number;
  onDeleted: (taskId: number) => void;
  onToggled: (taskId: number, isCompleted: boolean) => void;
  onEdited: () => void;
}

export default function TaskItem({
  task,
  userId,
  onDeleted,
  onToggled,
  onEdited,
}: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isToggling, setIsToggling] = useState(false);
  const [error, setError] = useState<string>("");

  const handleToggleCompletion = async () => {
    setIsToggling(true);
    setError("");

    try {
      await api.toggleTaskCompletion(userId, task.id, !task.is_completed);
      onToggled(task.id, !task.is_completed);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to update task";
      setError(errorMessage);
    } finally {
      setIsToggling(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this task?")) {
      return;
    }

    setIsDeleting(true);
    setError("");

    try {
      await api.deleteTask(userId, task.id);
      onDeleted(task.id);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to delete task";
      setError(errorMessage);
      setIsDeleting(false);
    }
  };

  const handleEditSuccess = () => {
    setIsEditing(false);
    onEdited();
  };

  const handleEditCancel = () => {
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <div className="p-6 bg-gray-50">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Edit Task</h3>
          <button
            onClick={handleEditCancel}
            className="text-gray-500 hover:text-gray-700"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
        <TaskForm
          userId={userId}
          task={task}
          onSuccess={handleEditSuccess}
          onCancel={handleEditCancel}
        />
      </div>
    );
  }

  return (
    <div className="p-6 hover:bg-gray-50 transition-colors duration-150">
      {/* Error Message */}
      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <div className="flex items-start gap-4">
        {/* Completion Checkbox */}
        <div className="flex-shrink-0 pt-1">
          <input
            type="checkbox"
            checked={task.is_completed}
            onChange={handleToggleCompletion}
            disabled={isToggling || isDeleting}
            className="w-5 h-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500 disabled:cursor-not-allowed disabled:opacity-50 cursor-pointer"
            aria-label={`Mark task "${task.title}" as ${task.is_completed ? "incomplete" : "complete"}`}
          />
        </div>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`text-lg font-medium ${
              task.is_completed
                ? "text-gray-500 line-through"
                : "text-gray-900"
            }`}
          >
            {task.title}
          </h3>

          {task.description && (
            <p
              className={`mt-1 text-sm ${
                task.is_completed ? "text-gray-400" : "text-gray-600"
              }`}
            >
              {task.description}
            </p>
          )}

          <div className="mt-2 flex items-center gap-4 text-xs text-gray-500">
            <span>
              Created: {new Date(task.created_at).toLocaleDateString()}
            </span>
            {task.updated_at !== task.created_at && (
              <span>
                Updated: {new Date(task.updated_at).toLocaleDateString()}
              </span>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex-shrink-0 flex items-center gap-2">
          <button
            onClick={() => setIsEditing(true)}
            disabled={isDeleting}
            className="p-2 text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-md transition-colors duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label={`Edit task "${task.title}"`}
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
          </button>

          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors duration-150 disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label={`Delete task "${task.title}"`}
          >
            {isDeleting ? (
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-red-600"></div>
            ) : (
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
