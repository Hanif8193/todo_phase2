/**
 * Root layout for the Next.js application.
 *
 * This layout wraps all pages and provides:
 * - Global styles
 * - Authentication context
 * - HTML structure
 * - Logout functionality
 */

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/components/AuthProvider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: {
    default: "Todo App - Phase II",
    template: "%s | Todo App",
  },
  description: "Multi-user todo application with secure authentication",
  keywords: ["todo", "task management", "productivity", "web app"],
  authors: [{ name: "Todo App Team" }],
  viewport: "width=device-width, initial-scale=1",
  themeColor: "#4F46E5",
  icons: {
    icon: [
      { url: "/favicon.ico" },
      { url: "/favicon-16x16.png", sizes: "16x16", type: "image/png" },
      { url: "/favicon-32x32.png", sizes: "32x32", type: "image/png" },
    ],
    apple: [
      { url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" },
    ],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
