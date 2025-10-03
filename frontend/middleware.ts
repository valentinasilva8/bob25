import type { NextRequest } from "next/server"
import { NextResponse } from "next/server"

// Mock middleware - no authentication needed for demo
export async function middleware(request: NextRequest) {
  // For demo purposes, allow all requests
  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - images - .svg, .png, .jpg, .jpeg, .gif, .webp
     * - /register routes (uses external API, not Supabase)
     * Feel free to modify this pattern to include more paths.
     */
    "/((?!_next/static|_next/image|favicon.ico|register|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
}
