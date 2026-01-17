"use client";

/**
 * Authentication Provider Component.
 *
 * This component provides:
 * - Authentication state management
 * - User context for all child components
 * - Logout functionality
 */

import { createContext, useContext, useEffect, useState } from "react";
import { authClient, type User } from "@/lib/auth";
import { useRouter, usePathname } from "next/navigation";

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    // Check for stored token and decode user info
    const token = authClient.getToken();
    if (token) {
      const userData = authClient.getUserFromToken();
      setUser(userData);
    }
    setIsLoading(false);
  }, []);

  const handleSignOut = async () => {
    await authClient.signOut();
    setUser(null);
    router.push("/signin");
  };

  const value = {
    user,
    isAuthenticated: user !== null,
    isLoading,
    signOut: handleSignOut,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Hook to access authentication context.
 *
 * Must be used within AuthProvider.
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
