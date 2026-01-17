/**
 * Landing Page Component.
 *
 * This is the home page of the Todo App that provides:
 * - Welcome message and app description
 * - Navigation links to Sign Up and Sign In pages
 * - Responsive Tailwind CSS styling
 */

import Link from "next/link";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
      <div className="max-w-3xl w-full text-center">
        {/* Hero Section */}
        <div className="mb-8">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-4">
            Welcome to Todo App
          </h1>
          <p className="text-xl md:text-2xl text-gray-700 mb-2">
            Your simple and powerful task management solution
          </p>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Stay organized, boost productivity, and never miss a deadline.
            Manage your tasks effortlessly with our intuitive interface.
          </p>
        </div>

        {/* Features Section */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-3">✓</div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Easy Task Creation
            </h3>
            <p className="text-gray-600 text-sm">
              Create and organize your tasks with just a few clicks
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-3">🔒</div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Secure & Private
            </h3>
            <p className="text-gray-600 text-sm">
              Your tasks are protected with JWT-based authentication
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-3xl mb-3">📱</div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Responsive Design
            </h3>
            <p className="text-gray-600 text-sm">
              Access your tasks from any device, anywhere
            </p>
          </div>
        </div>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link
            href="/signup"
            className="w-full sm:w-auto px-8 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg shadow-md transition-colors duration-200"
          >
            Get Started - Sign Up
          </Link>
          <Link
            href="/signin"
            className="w-full sm:w-auto px-8 py-3 bg-white hover:bg-gray-50 text-indigo-600 font-semibold rounded-lg shadow-md border-2 border-indigo-600 transition-colors duration-200"
          >
            Sign In
          </Link>
        </div>

        {/* Footer Text */}
        <p className="mt-8 text-gray-600 text-sm">
          Join thousands of users who trust Todo App to manage their daily tasks
        </p>
      </div>
    </div>
  );
}
