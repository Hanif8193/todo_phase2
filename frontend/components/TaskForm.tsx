"use client";

/**
 * TaskForm Component.
 *
 * This component provides:
 * - Form for creating or editing tasks
 * - Title validation (required, max 200 chars)
 * - Description validation (optional, max 2000 chars)
 * - Real-time character count feedback
 * - Integration with API for create/update operations
 * - Error handling and user feedback
 */

import { useState, FormEvent, useEffect } from "react";
import { api, type Task, type TaskCreate, type TaskUpdate } from "@/lib/api";

interface TaskFormProps {
  userId: number;
  task?: Task; // If provided, form is in edit mode
  onSuccess: () => void;
  onCancel?: () => void;
}

export default function TaskForm({
  userId,
  task,
  onSuccess,
  onCancel,
}: TaskFormProps) {
  const isEditMode = !!task;

  const [title, setTitle] = useState(task?.title || "");
  const [description, setDescription] = useState(task?.description || "");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string>("");

  // Character limits
  const TITLE_MAX_LENGTH = 200;
  const DESCRIPTION_MAX_LENGTH = 2000;

  // Character counts
  const titleCharsRemaining = TITLE_MAX_LENGTH - title.length;
  const descriptionCharsRemaining = DESCRIPTION_MAX_LENGTH - description.length;

  const validateForm = (): boolean => {
    setError("");

    // Title validation
    if (!title.trim()) {
      setError("Title is required");
      return false;
    }

    if (title.length > TITLE_MAX_LENGTH) {
      setError(`Title must be ${TITLE_MAX_LENGTH} characters or less`);
      return false;
    }

    // Description validation
    if (description.length > DESCRIPTION_MAX_LENGTH) {
      setError(`Description must be ${DESCRIPTION_MAX_LENGTH} characters or less`);
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    setError("");

    try {
      if (isEditMode) {
        // Update existing task
        const updateData: TaskUpdate = {
          title: title.trim(),
          description: description.trim() || undefined,
        };
        await api.updateTask(userId, task.id, updateData);
      } else {
        // Create new task
        const createData: TaskCreate = {
          title: title.trim(),
          description: description.trim() || undefined,
        };
        await api.createTask(userId, createData);
      }

      // Clear form and notify parent
      setTitle("");
      setDescription("");
      onSuccess();
    } catch (err) {
      const errorMessage =
        err instanceof Error
          ? err.message
          : isEditMode
          ? "Failed to update task"
          : "Failed to create task";
      setError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    // Reset form
    setTitle(task?.title || "");
    setDescription(task?.description || "");
    setError("");
    onCancel?.();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Error Alert */}
      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Title Field */}
      <div>
        <label
          htmlFor="title"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Title <span className="text-red-500">*</span>
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={isSubmitting}
          maxLength={TITLE_MAX_LENGTH}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
          placeholder="Enter task title"
          required
        />
        <div className="mt-1 flex justify-between items-center">
          <p className="text-xs text-gray-500">Required field</p>
          <p
            className={`text-xs ${
              titleCharsRemaining < 20
                ? "text-orange-600 font-medium"
                : "text-gray-500"
            }`}
          >
            {titleCharsRemaining} characters remaining
          </p>
        </div>
      </div>

      {/* Description Field */}
      <div>
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={isSubmitting}
          maxLength={DESCRIPTION_MAX_LENGTH}
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-gray-100 disabled:cursor-not-allowed resize-none"
          placeholder="Enter task description (optional)"
        />
        <div className="mt-1 flex justify-between items-center">
          <p className="text-xs text-gray-500">Optional field</p>
          <p
            className={`text-xs ${
              descriptionCharsRemaining < 100
                ? "text-orange-600 font-medium"
                : "text-gray-500"
            }`}
          >
            {descriptionCharsRemaining} characters remaining
          </p>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3 pt-2">
        <button
          type="submit"
          disabled={isSubmitting}
          className="flex-1 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 disabled:cursor-not-allowed text-white font-medium rounded-md shadow-sm transition-colors duration-200"
        >
          {isSubmitting
            ? isEditMode
              ? "Updating..."
              : "Creating..."
            : isEditMode
            ? "Update Task"
            : "Create Task"}
        </button>

        {onCancel && (
          <button
            type="button"
            onClick={handleCancel}
            disabled={isSubmitting}
            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 disabled:bg-gray-50 disabled:cursor-not-allowed text-gray-700 font-medium rounded-md transition-colors duration-200"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
