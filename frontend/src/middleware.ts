import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const protectedPrefixes = [
  "/dashboard",
  "/onboarding",
  "/jira",
  "/issues",
  "/approvals",
  "/settings",
  "/reports",
  "/recommendations",
  "/sprints",
  "/projects",
];

const publicPaths = ["/", "/auth/login", "/auth/register", "/auth/forgot-password", "/auth/reset-password"];

export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;
  const token = request.cookies.get("accessToken")?.value;
  const isProtected = protectedPrefixes.some((prefix) => path.startsWith(prefix));
  const isPublic = publicPaths.includes(path);

  if (path === "/" && !token) {
    return NextResponse.redirect(new URL("/auth/login", request.url));
  }

  if (isProtected && !token) {
    return NextResponse.redirect(new URL("/auth/login", request.url));
  }

  if (isPublic && token && (path === "/auth/login" || path === "/auth/register")) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
