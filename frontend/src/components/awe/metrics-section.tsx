"use client"

import { TrendingUp, Users, DollarSign, Star } from "lucide-react"
import { useEffect, useRef } from "react"
import { gsap } from "gsap"
import SplitText from "./split-text"

export function MetricsSection() {
  const cardsRef = useRef<HTMLDivElement>(null)
  const hasAnimated = useRef(false)

  const metrics = [
    {
      icon: TrendingUp,
      value: "127%",
      label: "Average Revenue Growth",
      description: "in the first year",
    },
    {
      icon: Users,
      value: "2,400+",
      label: "Small Businesses Helped",
      description: "across the country",
    },
    {
      icon: DollarSign,
      value: "$8.2M",
      label: "Additional Revenue Generated",
      description: "for our clients",
    },
    {
      icon: Star,
      value: "4.9/5",
      label: "Client Satisfaction",
      description: "from 500+ reviews",
    },
  ]

  useEffect(() => {
    if (!cardsRef.current || hasAnimated.current) return

    const cards = cardsRef.current.querySelectorAll(".metric-card")

    gsap.set(cards, { opacity: 0, y: 50, scale: 0.9 })

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !hasAnimated.current) {
            hasAnimated.current = true

            gsap.to(cards, {
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

    observer.observe(cardsRef.current)

    return () => {
      observer.disconnect()
    }
  }, [])

  return (
    <section className="py-16 bg-gradient-to-b from-background to-muted/30">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">Real Results for Real Businesses</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            We're proud to help small businesses like yours compete and win in today's market
          </p>
        </div>

        <div ref={cardsRef} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {metrics.map((metric, index) => {
            const Icon = metric.icon
            return (
              <div
                key={index}
                className="metric-card flex flex-col items-center text-center p-6 rounded-lg bg-card border border-border hover:shadow-lg transition-shadow"
              >
                <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                  <Icon className="w-8 h-8 text-primary" />
                </div>
                <SplitText
                  text={metric.value}
                  className="text-4xl font-bold text-foreground mb-2"
                  delay={50}
                  duration={0.6}
                  ease="power3.out"
                  splitType="chars"
                  from={{ opacity: 0, y: 20 }}
                  to={{ opacity: 1, y: 0 }}
                  threshold={0.1}
                  rootMargin="-50px"
                  textAlign="center"
                />
                <div className="text-lg font-semibold text-foreground mb-1">{metric.label}</div>
                <div className="text-sm text-muted-foreground">{metric.description}</div>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
