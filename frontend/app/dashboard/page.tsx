"use client";

/**
 * Dashboard Page Component.
 *
 * This is a protected route that provides:
 * - User authentication check and redirect
 * - Task management interface
 * - Task creation form
 * - Task list display
 * - Logout functionality
 */

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import TaskList from "@/components/TaskList";
import TaskForm from "@/components/TaskForm";

export default function DashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading, signOut } = useAuth();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  // Redirect to signin if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/signin");
    }
  }, [isAuthenticated, isLoading, router]);

  const handleSignOut = async () => {
    await signOut();
  };

  const handleTaskCreated = () => {
    setShowCreateForm(false);
    // Trigger task list refresh
    setRefreshTrigger((prev) => prev + 1);
  };

  const handleTaskUpdated = () => {
    // Trigger task list refresh
    setRefreshTrigger((prev) => prev + 1);
  };

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Don't render dashboard if not authenticated
  if (!isAuthenticated || !user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                My Tasks
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                Welcome back, {user.email}
              </p>
            </div>
            <button
              onClick={handleSignOut}
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-md transition-colors duration-200"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Create Task Section */}
        <div className="mb-8">
          {!showCreateForm ? (
            <button
              onClick={() => setShowCreateForm(true)}
              className="w-full sm:w-auto px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg shadow-md transition-colors duration-200"
            >
              + Create New Task
            </button>
          ) : (
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold text-gray-900">
                  Create New Task
                </h2>
                <button
                  onClick={() => setShowCreateForm(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <svg
                    className="w-6 h-6"
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
                userId={user.id}
                onSuccess={handleTaskCreated}
                onCancel={() => setShowCreateForm(false)}
              />
            </div>
          )}
        </div>

        {/* Task List Section */}
        <div className="bg-white rounded-lg shadow-md">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">
              Your Tasks
            </h2>
          </div>
          <TaskList
            userId={user.id}
            onTaskUpdated={handleTaskUpdated}
            refreshTrigger={refreshTrigger}
          />
        </div>
      </main>
    </div>
  );
}
