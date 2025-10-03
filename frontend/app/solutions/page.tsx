"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Header } from "@/components/header"
import {
  Sparkles,
  Target,
  TrendingUp,
  Clock,
  DollarSign,
  Users,
  BarChart3,
  Zap,
  Heart,
  CheckCircle2,
  ArrowRight,
} from "lucide-react"
import { useEffect, useRef } from "react"
import { gsap } from "gsap"
import SplitText from "@/components/split-text"

export default function SolutionsPage() {
  const statsRef = useRef<HTMLDivElement>(null)
  const hasAnimated = useRef(false)

  useEffect(() => {
    if (!statsRef.current || hasAnimated.current) return

    const statCards = statsRef.current.querySelectorAll(".stat-card")

    gsap.set(statCards, { opacity: 0, y: 50, scale: 0.9 })

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !hasAnimated.current) {
            hasAnimated.current = true

            gsap.to(statCards, {
              opacity: 1,
              y: 0,
              scale: 1,
              duration: 0.8,
              ease: "power3.out",
              stagger: 0.15,
            })

            observer.disconnect()
          }
        })
      },
      {
        threshold: 0.1,
        rootMargin: "-50px",
      },
    )

    observer.observe(statsRef.current)

    return () => {
      observer.disconnect()
    }
  }, [])

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <Header />

      {/* Hero Section */}
      <section className="relative overflow-hidden border-b border-border bg-gradient-to-b from-primary/5 to-background py-20 md:py-32">
        <div className="container relative z-10 mx-auto px-4">
          <div className="mx-auto max-w-4xl text-center">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-2 text-sm font-medium text-primary">
              <Sparkles className="h-4 w-4" />
              AI-Powered Advertising Solutions
            </div>
            <h1 className="mb-6 text-balance text-4xl font-bold tracking-tight md:text-6xl">
              Advertising That Works for <span className="text-primary">Your Business</span>
            </h1>
            <p className="mb-8 text-pretty text-lg text-muted-foreground md:text-xl">
              AWE transforms how small businesses advertise. Our AI-powered platform creates professional,
              high-performing ads that connect with your community and drive real results—without the enterprise budget.
            </p>
            <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Button asChild size="lg" className="w-full sm:w-auto">
                <Link href="/auth/sign-up">
                  Start Creating Ads
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg" className="w-full sm:w-auto bg-transparent">
                <Link href="#how-it-works">See How It Works</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* What We Do */}
      <section className="border-b border-border py-20">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="mb-4 text-balance text-3xl font-bold md:text-4xl">What AWE Does for You</h2>
            <p className="mb-12 text-pretty text-lg text-muted-foreground">
              We use advanced AI to understand your business story and create ads that resonate with your target
              audience—automatically optimized for maximum impact.
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            <Card className="border-2 transition-all hover:border-primary/50 hover:shadow-lg">
              <CardContent className="p-6">
                <div className="mb-4 inline-flex rounded-lg bg-primary/10 p-3">
                  <Sparkles className="h-6 w-6 text-primary" />
                </div>
                <h3 className="mb-2 text-xl font-bold">AI-Generated Creative</h3>
                <p className="text-muted-foreground">
                  Our AI analyzes your business story, products, and audience to generate compelling ad copy and visuals
                  that capture attention and drive action.
                </p>
              </CardContent>
            </Card>

            <Card className="border-2 transition-all hover:border-primary/50 hover:shadow-lg">
              <CardContent className="p-6">
                <div className="mb-4 inline-flex rounded-lg bg-primary/10 p-3">
                  <Target className="h-6 w-6 text-primary" />
                </div>
                <h3 className="mb-2 text-xl font-bold">Smart Targeting</h3>
                <p className="text-muted-foreground">
                  Reach the right people at the right time. Our platform identifies and targets your ideal customers
                  based on demographics, interests, and behaviors.
                </p>
              </CardContent>
            </Card>

            <Card className="border-2 transition-all hover:border-primary/50 hover:shadow-lg">
              <CardContent className="p-6">
                <div className="mb-4 inline-flex rounded-lg bg-primary/10 p-3">
                  <TrendingUp className="h-6 w-6 text-primary" />
                </div>
                <h3 className="mb-2 text-xl font-bold">Continuous Optimization</h3>
                <p className="text-muted-foreground">
                  Your ads get smarter over time. Our AI continuously tests and optimizes campaigns to improve
                  performance and maximize your return on investment.
                </p>
              </CardContent>
            </Card>

            <Card className="border-2 transition-all hover:border-primary/50 hover:shadow-lg">
              <CardContent className="p-6">
                <div className="mb-4 inline-flex rounded-lg bg-primary/10 p-3">
                  <BarChart3 className="h-6 w-6 text-primary" />
                </div>
                <h3 className="mb-2 text-xl font-bold">Real-Time Analytics</h3>
                <p className="text-muted-foreground">
                  Track every impression, click, and conversion. Get actionable insights that help you understand what's
                  working and where to invest more.
                </p>
              </CardContent>
            </Card>

            <Card className="border-2 transition-all hover:border-primary/50 hover:shadow-lg">
              <CardContent className="p-6">
                <div className="mb-4 inline-flex rounded-lg bg-primary/10 p-3">
                  <Users className="h-6 w-6 text-primary" />
                </div>
                <h3 className="mb-2 text-xl font-bold">Multi-Platform Reach</h3>
                <p className="text-muted-foreground">
                  One campaign, multiple platforms. Automatically distribute your ads across social media, search
                  engines, and display networks for maximum visibility.
                </p>
              </CardContent>
            </Card>

            <Card className="border-2 transition-all hover:border-primary/50 hover:shadow-lg">
              <CardContent className="p-6">
                <div className="mb-4 inline-flex rounded-lg bg-primary/10 p-3">
                  <Heart className="h-6 w-6 text-primary" />
                </div>
                <h3 className="mb-2 text-xl font-bold">Community Connection</h3>
                <p className="text-muted-foreground">
                  Build authentic relationships with your local community. Our ads emphasize your story, values, and the
                  people behind your business.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="border-b border-border bg-muted/30 py-20">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="mb-4 text-balance text-3xl font-bold md:text-4xl">How AWE Works</h2>
            <p className="mb-12 text-pretty text-lg text-muted-foreground">
              From onboarding to optimization, we make advertising simple and effective.
            </p>
          </div>

          <div className="mx-auto max-w-4xl space-y-8">
            <div className="flex gap-6">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-primary text-lg font-bold text-primary-foreground">
                1
              </div>
              <div>
                <h3 className="mb-2 text-xl font-bold">Tell Us Your Story</h3>
                <p className="text-muted-foreground">
                  Share your business mission, products, target audience, and growth goals. Our AI learns what makes
                  your business unique and what matters most to your customers.
                </p>
              </div>
            </div>

            <div className="flex gap-6">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-primary text-lg font-bold text-primary-foreground">
                2
              </div>
              <div>
                <h3 className="mb-2 text-xl font-bold">AI Creates Your Campaigns</h3>
                <p className="text-muted-foreground">
                  Within minutes, our AI generates multiple ad variations with compelling copy, eye-catching visuals,
                  and strategic targeting—all tailored to your business and audience.
                </p>
              </div>
            </div>

            <div className="flex gap-6">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-primary text-lg font-bold text-primary-foreground">
                3
              </div>
              <div>
                <h3 className="mb-2 text-xl font-bold">Launch & Monitor</h3>
                <p className="text-muted-foreground">
                  Review and approve your campaigns, then launch with one click. Track performance in real-time through
                  your personalized dashboard with clear, actionable metrics.
                </p>
              </div>
            </div>

            <div className="flex gap-6">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-primary text-lg font-bold text-primary-foreground">
                4
              </div>
              <div>
                <h3 className="mb-2 text-xl font-bold">Continuous Improvement</h3>
                <p className="text-muted-foreground">
                  Our AI continuously analyzes performance data, automatically adjusting targeting, bidding, and
                  creative elements to maximize your results and ROI over time.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="border-b border-border py-20">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="mb-4 text-balance text-3xl font-bold md:text-4xl">The AWE Advantage for Small Businesses</h2>
            <p className="mb-12 text-pretty text-lg text-muted-foreground">
              Finally, advertising technology that levels the playing field.
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-2">
            <div className="flex gap-4">
              <div className="shrink-0">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                  <Clock className="h-5 w-5 text-primary" />
                </div>
              </div>
              <div>
                <h3 className="mb-2 text-lg font-bold">Save Time</h3>
                <p className="text-muted-foreground">
                  No more spending hours creating ads or managing campaigns. What used to take days now takes minutes,
                  freeing you to focus on running your business.
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="shrink-0">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                  <DollarSign className="h-5 w-5 text-primary" />
                </div>
              </div>
              <div>
                <h3 className="mb-2 text-lg font-bold">Reduce Costs</h3>
                <p className="text-muted-foreground">
                  Eliminate expensive agency fees and wasted ad spend. Our AI optimizes every dollar to deliver maximum
                  impact at a fraction of traditional advertising costs.
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="shrink-0">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                  <Zap className="h-5 w-5 text-primary" />
                </div>
              </div>
              <div>
                <h3 className="mb-2 text-lg font-bold">Compete with Confidence</h3>
                <p className="text-muted-foreground">
                  Access the same advanced advertising technology that big corporations use. Level the playing field and
                  compete effectively in your market.
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="shrink-0">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                  <TrendingUp className="h-5 w-5 text-primary" />
                </div>
              </div>
              <div>
                <h3 className="mb-2 text-lg font-bold">Drive Real Growth</h3>
                <p className="text-muted-foreground">
                  Increase brand awareness, attract new customers, and boost sales. Our clients see measurable results
                  within weeks of launching their first campaign.
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="shrink-0">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                  <CheckCircle2 className="h-5 w-5 text-primary" />
                </div>
              </div>
              <div>
                <h3 className="mb-2 text-lg font-bold">No Expertise Required</h3>
                <p className="text-muted-foreground">
                  You don't need to be a marketing expert. Our platform handles the complexity while you maintain full
                  control over your brand message and budget.
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="shrink-0">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                  <Heart className="h-5 w-5 text-primary" />
                </div>
              </div>
              <div>
                <h3 className="mb-2 text-lg font-bold">Stay Authentic</h3>
                <p className="text-muted-foreground">
                  Your ads reflect your unique story and values. We help you connect authentically with your community,
                  not just sell products.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Impact Stats */}
      <section className="border-b border-border bg-primary/5 py-20">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="mb-4 text-balance text-3xl font-bold md:text-4xl">Real Results for Real Businesses</h2>
            <p className="mb-12 text-pretty text-lg text-muted-foreground">
              See the impact AWE has on businesses just like yours.
            </p>
          </div>

          <div ref={statsRef} className="grid gap-8 md:grid-cols-4">
            <div className="stat-card text-center">
              <SplitText
                text="3.2x"
                className="mb-2 text-4xl font-bold text-primary md:text-5xl"
                delay={50}
                duration={0.6}
                ease="power3.out"
                splitType="chars"
                from={{ opacity: 0, y: 30 }}
                to={{ opacity: 1, y: 0 }}
                threshold={0.1}
                rootMargin="-50px"
                textAlign="center"
              />
              <div className="text-sm font-medium text-muted-foreground">Average ROI Increase</div>
            </div>
            <div className="stat-card text-center">
              <SplitText
                text="67%"
                className="mb-2 text-4xl font-bold text-primary md:text-5xl"
                delay={50}
                duration={0.6}
                ease="power3.out"
                splitType="chars"
                from={{ opacity: 0, y: 30 }}
                to={{ opacity: 1, y: 0 }}
                threshold={0.1}
                rootMargin="-50px"
                textAlign="center"
              />
              <div className="text-sm font-medium text-muted-foreground">Reduction in Ad Costs</div>
            </div>
            <div className="stat-card text-center">
              <SplitText
                text="89%"
                className="mb-2 text-4xl font-bold text-primary md:text-5xl"
                delay={50}
                duration={0.6}
                ease="power3.out"
                splitType="chars"
                from={{ opacity: 0, y: 30 }}
                to={{ opacity: 1, y: 0 }}
                threshold={0.1}
                rootMargin="-50px"
                textAlign="center"
              />
              <div className="text-sm font-medium text-muted-foreground">Customer Satisfaction</div>
            </div>
            <div className="stat-card text-center">
              <SplitText
                text="24hrs"
                className="mb-2 text-4xl font-bold text-primary md:text-5xl"
                delay={50}
                duration={0.6}
                ease="power3.out"
                splitType="chars"
                from={{ opacity: 0, y: 30 }}
                to={{ opacity: 1, y: 0 }}
                threshold={0.1}
                rootMargin="-50px"
                textAlign="center"
              />
              <div className="text-sm font-medium text-muted-foreground">Average Time to First Results</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="mb-4 text-balance text-3xl font-bold md:text-4xl">Ready to Transform Your Advertising?</h2>
            <p className="mb-8 text-pretty text-lg text-muted-foreground">
              Join thousands of small businesses using AWE to grow their reach, connect with customers, and achieve
              their goals.
            </p>
            <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Button asChild size="lg" className="w-full sm:w-auto">
                <Link href="/auth/sign-up">
                  Get Started Free
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg" className="w-full sm:w-auto bg-transparent">
                <Link href="/#contact">Contact Sales</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
