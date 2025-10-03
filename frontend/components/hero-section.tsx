"use client"

import { Button } from "@/components/ui/button"
import { Heart } from "lucide-react"
import { useState, useEffect } from "react"

export function HeroSection() {
  const images = [
    {
      src: "/diverse-small-business-owners-and-families-smiling.jpg",
      alt: "Small business owners and families smiling together",
    },
    {
      src: "/small-business-owner-family-in-their-shop--diverse.jpg",
      alt: "Family running their small business",
    },
    {
      src: "/latina-woman-baker-smiling-warmly-in-apron.jpg",
      alt: "Baker proudly showing her craft",
    },
    {
      src: "/asian-man-hardware-store-owner-with-family.jpg",
      alt: "Hardware store owner with family",
    },
    {
      src: "/couple-garden-center-owners-with-plants-smiling.jpg",
      alt: "Couple running their garden center",
    },
  ]

  const [currentImageIndex, setCurrentImageIndex] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length)
    }, 5000)

    return () => clearInterval(interval)
  }, [images.length])

  return (
    <section className="relative min-h-[600px] md:min-h-[700px]">
      {/* Background slideshow */}
      <div className="absolute inset-0 overflow-hidden">
        {images.map((image, index) => (
          <img
            key={index}
            src={image.src || "/placeholder.svg"}
            alt={image.alt}
            className={`absolute inset-0 h-full w-full object-cover transition-opacity duration-1000 ${
              index === currentImageIndex ? "opacity-100" : "opacity-0"
            }`}
          />
        ))}
        {/* Dark overlay for text readability */}
        <div className="absolute inset-0 bg-gradient-to-r from-black/70 via-black/50 to-black/30" />
      </div>

      {/* Content overlay */}
      <div className="relative z-10 container mx-auto px-4 py-20 md:py-32">
        <div className="max-w-2xl">
          <div className="flex flex-col gap-6">
            <div className="flex flex-col gap-4">
              <p className="text-sm font-semibold uppercase tracking-wider text-orange-400">
                Marketing That Feels Like Family
              </p>
              <h1 className="text-balance text-4xl font-bold leading-tight tracking-tight text-white md:text-5xl lg:text-6xl">
                Your story deserves to be heard
              </h1>
            </div>

            <p className="text-pretty text-lg leading-relaxed text-gray-100 md:text-xl">
              You pour your heart into your business. We help you share that passion with the people who'll love what
              you do. No tech jargon, no cookie-cutter ads—just real connections that grow your business and support
              your community.
            </p>

            <div className="flex flex-col gap-3 sm:flex-row">
              <Button size="lg" className="gap-2 bg-primary hover:bg-primary/90">
                <Heart className="h-4 w-4" />
                See How We Help
              </Button>
              <Button size="lg" variant="outline" className="border-white text-white hover:bg-white/10 bg-transparent">
                Let's Talk
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
