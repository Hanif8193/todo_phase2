/**
 * Next.js Middleware for protected routes.
 *
 * This middleware:
 * - Redirects unauthenticated users to signin page
 * - Protects dashboard and other authenticated routes
 * - Runs on every request to protected paths
 */

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // Get the auth token from cookies or local storage (we check for cookie here)
  const token = request.cookies.get("auth_token")?.value;

  // If no token found, redirect to signin
  if (!token) {
    const url = request.nextUrl.clone();
    url.pathname = "/signin";
    url.searchParams.set("redirect", request.nextUrl.pathname);
    return NextResponse.redirect(url);
  }

  // Allow the request to continue
  return NextResponse.next();
}

// Specify which routes this middleware should run on
export const config = {
  matcher: [
    "/dashboard/:path*",
    // Add more protected routes here as needed
  ],
};
