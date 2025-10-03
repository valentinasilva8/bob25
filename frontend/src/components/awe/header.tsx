import Link from "next/link"
import { Button } from "@/components/awe/ui/button"
import { createClient } from "@/components/awe/lib/supabase/server"

export async function Header() {
  const supabase = await createClient()
  let user = null

  if (supabase) {
    const {
      data: { user: authUser },
    } = await supabase.auth.getUser()
    user = authUser
  }

  return (
    <header className="relative z-20 border-b border-border bg-background">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-2">
          <div className="flex items-center gap-2">
            <svg
              width="32"
              height="32"
              viewBox="0 0 32 32"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              className="text-primary"
            >
              <path d="M16 4L4 10L16 16L28 10L16 4Z" fill="currentColor" opacity="0.8" />
              <path
                d="M4 16L16 22L28 16"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M4 22L16 28L28 22"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <span className="text-xl font-bold">AWE</span>
          </div>
        </Link>

        <nav className="hidden items-center gap-8 md:flex">
          <Link href="/" className="text-sm font-medium text-primary transition-colors hover:text-primary/80">
            HOME
          </Link>
          <Link href="/solutions" className="text-sm font-medium text-foreground transition-colors hover:text-primary">
            SOLUTIONS
          </Link>
          <Link
            href="/sustainability"
            className="text-sm font-medium text-foreground transition-colors hover:text-primary"
          >
            SUSTAINABILITY
          </Link>
          <Link href="/pricing" className="text-sm font-medium text-foreground transition-colors hover:text-primary">
            PRICING
          </Link>
          <Link
            href="/testimonials"
            className="text-sm font-medium text-foreground transition-colors hover:text-primary"
          >
            TESTIMONIALS
          </Link>
          <Link href="/contact" className="text-sm font-medium text-foreground transition-colors hover:text-primary">
            CONTACT
          </Link>
        </nav>

        {user ? (
          <div className="flex items-center gap-4">
            <Button asChild variant="outline">
              <Link href="/dashboard">Dashboard</Link>
            </Button>
          </div>
        ) : (
          <div className="flex items-center gap-4">
            <Button asChild variant="ghost" className="hidden md:inline-flex">
              <Link href="/auth/login">Login</Link>
            </Button>
            <Button asChild>
              <Link href="/register">Get Started</Link>
            </Button>
          </div>
        )}
      </div>
    </header>
  )
}
