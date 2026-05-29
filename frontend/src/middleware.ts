import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const protectedPrefixes = ["/dashboard", "/issues", "/sprints", "/approvals", "/recommendations", "/reports", "/jira", "/settings"];

export function middleware(request: NextRequest) {
  const hasToken = request.cookies.get("accessToken")?.value;
  const path = request.nextUrl.pathname;
  const isProtected = protectedPrefixes.some((prefix) => path.startsWith(prefix));

  if (isProtected && !hasToken) {
    return NextResponse.next();
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
