"use client"

import { useEffect, useRef } from "react"
import { gsap } from "gsap"

interface SplitTextProps {
  text: string
  className?: string
  delay?: number
  duration?: number
  ease?: string
  splitType?: "chars" | "words" | "lines"
  from?: {
    opacity?: number
    y?: number
    x?: number
    scale?: number
  }
  to?: {
    opacity?: number
    y?: number
    x?: number
    scale?: number
  }
  threshold?: number
  rootMargin?: string
  textAlign?: "left" | "center" | "right"
  onLetterAnimationComplete?: () => void
}

export default function SplitText({
  text,
  className = "",
  delay = 0,
  duration = 0.6,
  ease = "power3.out",
  splitType = "chars",
  from = { opacity: 0, y: 40 },
  to = { opacity: 1, y: 0 },
  threshold = 0.1,
  rootMargin = "-100px",
  textAlign = "center",
  onLetterAnimationComplete,
}: SplitTextProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const hasAnimated = useRef(false)

  useEffect(() => {
    if (!containerRef.current || hasAnimated.current) return

    const container = containerRef.current
    const elements = Array.from(container.children) as HTMLElement[]

    // Set initial state
    gsap.set(elements, from)

    // Create intersection observer
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !hasAnimated.current) {
            hasAnimated.current = true

            // Animate elements
            gsap.to(elements, {
              ...to,
              duration,
              ease,
              stagger: delay / 1000,
              onComplete: () => {
                if (onLetterAnimationComplete) {
                  onLetterAnimationComplete()
                }
              },
            })

            observer.disconnect()
          }
        })
      },
      {
        threshold,
        rootMargin,
      },
    )

    observer.observe(container)

    return () => {
      observer.disconnect()
    }
  }, [delay, duration, ease, from, to, threshold, rootMargin, onLetterAnimationComplete])

  const splitText = () => {
    if (splitType === "chars") {
      return text.split("").map((char, index) => (
        <span key={index} className="inline-block" style={{ whiteSpace: char === " " ? "pre" : "normal" }}>
          {char}
        </span>
      ))
    } else if (splitType === "words") {
      return text.split(" ").map((word, index) => (
        <span key={index} className="inline-block mr-1">
          {word}
        </span>
      ))
    }
    return text
  }

  return (
    <div ref={containerRef} className={className} style={{ textAlign }}>
      {splitText()}
    </div>
  )
}
