import Link from "next/link"
import Image from "next/image"
import { Button } from "@/components/ui/button"

export function Header() {
  // For demo purposes, no user authentication
  const user = null

  return (
    <header className="relative z-20 border-b border-border bg-background">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link href="/" className="flex items-center">
          <Image 
            src="/awe-logo.jpg" 
            alt="AWE Logo" 
            width={80} 
            height={80} 
            className="rounded" 
            style={{ 
              mixBlendMode: 'multiply'
            }} 
          />
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
