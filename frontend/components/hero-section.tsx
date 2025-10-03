"use client"

import { Button } from "@/components/ui/button"
import { Leaf } from "lucide-react"
import { useState, useEffect } from "react"
import Link from "next/link"
import { motion } from "framer-motion"

export function HeroSection() {
  const rotatingPhrases = [
    "waste-free ad delivery",
    "local impact stories",
    "human-feeling ads",
    "small-business breakthroughs",
    "greener advertising",
  ]

  const backgroundImages = [
    "/yoga-studio-with-people-practicing-in-natural-ligh.jpg",
    "/fitness-center-with-diverse-people-working-out.jpg",
    "/wellness-spa-with-calming-atmosphere.jpg",
    "/pilates-studio-with-small-group-class.jpg",
    "/meditation-space-with-peaceful-environment.jpg",
  ]

  const [currentPhraseIndex, setCurrentPhraseIndex] = useState(0)
  const [fadeState, setFadeState] = useState("fade-in")
  const [currentImageIndex, setCurrentImageIndex] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setFadeState("fade-out")
      setTimeout(() => {
        setCurrentPhraseIndex((prevIndex) => (prevIndex + 1) % rotatingPhrases.length)
        setFadeState("fade-in")
      }, 500)
    }, 3000)

    return () => clearInterval(interval)
  }, [rotatingPhrases.length])

  useEffect(() => {
    const imageInterval = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % backgroundImages.length)
    }, 5000)

    return () => clearInterval(imageInterval)
  }, [backgroundImages.length])

  return (
    <section className="relative min-h-[600px] md:min-h-[700px]">
      <div className="absolute inset-0 overflow-hidden">
        {backgroundImages.map((image, index) => (
          <div
            key={index}
            className={`absolute inset-0 transition-opacity duration-1000 ${
              index === currentImageIndex ? "opacity-100" : "opacity-0"
            }`}
          >
            <img
              src={image || "/placeholder.svg"}
              alt={`Wellness business ${index + 1}`}
              className="h-full w-full object-cover"
            />
          </div>
        ))}
        <div className="absolute inset-0 bg-gradient-to-r from-black/60 via-black/40 to-black/30" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="relative z-10 container mx-auto px-4 py-20 md:py-32"
      >
        <div className="max-w-3xl">
          <div className="flex flex-col gap-6">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="flex flex-col gap-4"
            >
              <div className="text-sm font-semibold uppercase tracking-wider text-emerald-400 drop-shadow-[0_0_8px_rgba(52,211,153,0.5)]">
                AWE — not A-I. It's A-WE.
              </div>
              <h1 className="text-balance text-4xl font-bold leading-tight tracking-tight text-white md:text-5xl lg:text-6xl drop-shadow-[0_2px_10px_rgba(0,0,0,0.8)]">
                Let's create tomorrow's{" "}
                <span
                  className={`inline-block text-blue-400 drop-shadow-[0_0_12px_rgba(96,165,250,0.6)] transition-opacity duration-500 ${
                    fadeState === "fade-in" ? "opacity-100" : "opacity-0"
                  }`}
                >
                  {rotatingPhrases[currentPhraseIndex]}
                </span>
              </h1>
            </motion.div>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="text-pretty text-lg leading-relaxed text-gray-100 md:text-xl drop-shadow-[0_2px_8px_rgba(0,0,0,0.8)]"
            >
              More customers. Stronger community. Smaller footprint.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
              className="flex flex-col gap-3 sm:flex-row"
            >
              <Button
                size="lg"
                className="gap-2 bg-emerald-600 hover:bg-emerald-700 text-white animate-pulse hover:animate-none drop-shadow-[0_4px_12px_rgba(52,211,153,0.4)]"
                asChild
              >
                <Link href="/register">
                  <Leaf className="h-4 w-4" />
                  See How We Help
                </Link>
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="border-white text-white hover:bg-white/10 bg-white/5 backdrop-blur-sm"
                asChild
              >
                <Link href="/contact">Let's Talk</Link>
              </Button>
            </motion.div>
          </div>
        </div>
      </motion.div>
    </section>
  )
}
