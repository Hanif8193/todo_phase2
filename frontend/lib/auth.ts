/**
 * Authentication client for JWT-based authentication.
 *
 * This module provides:
 * - JWT token management
 * - Client-side token storage
 * - Authentication API calls
 */

// Get API URL from environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Type definitions for authentication state.
 */
export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface SignUpData {
  email: string;
  password: string;
}

export interface SignInData {
  email: string;
  password: string;
}

/**
 * Authentication API client functions.
 *
 * These functions interact with the backend authentication endpoints
 * and manage JWT tokens in local storage.
 */
export const authClient = {
  /**
   * Sign up a new user.
   *
   * @param data - User email and password
   * @returns Promise with user data and JWT token
   */
  async signUp(data: SignUpData): Promise<{ user: User; token: string }> {
    const response = await fetch(`${API_URL}/auth/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Signup failed");
    }

    const result = await response.json();

    // Store token in local storage AND set cookie for middleware
    if (result.token) {
      localStorage.setItem("auth_token", result.token);
      // Set cookie for middleware (expires in 7 days)
      document.cookie = `auth_token=${result.token}; path=/; max-age=${7 * 24 * 60 * 60}; SameSite=Lax`;
    }

    return result;
  },

  /**
   * Sign in an existing user.
   *
   * @param data - User email and password
   * @returns Promise with user data and JWT token
   */
  async signIn(data: SignInData): Promise<{ user: User; token: string }> {
    const response = await fetch(`${API_URL}/auth/signin`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Signin failed");
    }

    const result = await response.json();

    // Store token in local storage AND set cookie for middleware
    if (result.token) {
      localStorage.setItem("auth_token", result.token);
      // Set cookie for middleware (expires in 7 days)
      document.cookie = `auth_token=${result.token}; path=/; max-age=${7 * 24 * 60 * 60}; SameSite=Lax`;
    }

    return result;
  },

  /**
   * Sign out the current user.
   *
   * Removes the JWT token from local storage.
   */
  async signOut(): Promise<void> {
    const token = localStorage.getItem("auth_token");

    if (token) {
      try {
        await fetch(`${API_URL}/auth/signout`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
      } catch (error) {
        console.error("Signout request failed:", error);
      }
    }

    // Remove token from storage and delete cookie
    localStorage.removeItem("auth_token");
    // Delete cookie
    document.cookie = "auth_token=; path=/; max-age=0";
  },

  /**
   * Get the current JWT token from local storage.
   *
   * @returns JWT token string or null if not authenticated
   */
  getToken(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("auth_token");
  },

  /**
   * Check if user is authenticated.
   *
   * @returns True if JWT token exists in local storage
   */
  isAuthenticated(): boolean {
    return this.getToken() !== null;
  },

  /**
   * Decode JWT token to get user information.
   *
   * @returns User data from token payload or null if invalid
   */
  getUserFromToken(): User | null {
    const token = this.getToken();
    if (!token) return null;

    try {
      // Decode JWT payload (base64)
      const payload = JSON.parse(atob(token.split(".")[1]));

      return {
        id: parseInt(payload.sub),
        email: payload.email,
        created_at: new Date(payload.iat * 1000).toISOString(),
      };
    } catch (error) {
      console.error("Failed to decode token:", error);
      return null;
    }
  },
};
