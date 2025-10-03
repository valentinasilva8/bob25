"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Star, ChevronLeft, ChevronRight } from "lucide-react"
import { useState, useEffect } from "react"

export function TestimonialsSection() {
  const testimonials = [
    {
      name: "Maria Rodriguez",
      business: "Maria's Bakery",
      location: "Austin, TX",
      image: "/latina-woman-baker-smiling-warmly-in-apron.jpg",
      quote:
        "Before AWE, I was spending money on ads that just weren't working. Now my ads feel like me—warm, personal, and authentic. My regulars tell me they love seeing my story online, and I'm getting new customers every week who say they felt connected before they even walked in.",
      rating: 5,
    },
    {
      name: "James Chen",
      business: "Chen Family Hardware",
      location: "Portland, OR",
      image: "/asian-man-hardware-store-owner-with-family.jpg",
      quote:
        "My dad started this store 30 years ago, and I was worried we couldn't compete with the big box stores. AWE helped us tell our family's story in a way that really resonates with our community. Sales are up 40% and people keep telling us how much they appreciate supporting a local family business.",
      rating: 5,
    },
    {
      name: "Sarah & Tom Williams",
      business: "Green Thumb Garden Center",
      location: "Nashville, TN",
      image: "/couple-garden-center-owners-with-plants-smiling.jpg",
      quote:
        "We're not tech people—we're plant people! AWE made everything so simple. They took the time to understand our passion for sustainable gardening and turned it into ads that actually bring in customers who share our values. It feels good to market in a way that's honest and helps the environment too.",
      rating: 5,
    },
  ]

  const [currentTestimonialIndex, setCurrentTestimonialIndex] = useState(0)
  const [autoPlayKey, setAutoPlayKey] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTestimonialIndex((prevIndex) => (prevIndex + 1) % testimonials.length)
    }, 6000)

    return () => clearInterval(interval)
  }, [testimonials.length, autoPlayKey])

  const goToPrevious = () => {
    setCurrentTestimonialIndex((prevIndex) => (prevIndex - 1 + testimonials.length) % testimonials.length)
    setAutoPlayKey((prev) => prev + 1)
  }

  const goToNext = () => {
    setCurrentTestimonialIndex((prevIndex) => (prevIndex + 1) % testimonials.length)
    setAutoPlayKey((prev) => prev + 1)
  }

  const goToTestimonial = (index: number) => {
    setCurrentTestimonialIndex(index)
    setAutoPlayKey((prev) => prev + 1)
  }

  return (
    <section className="container mx-auto px-4 py-20">
      <div className="mb-16 text-center">
        <h2 className="mb-4 text-balance text-3xl font-bold md:text-4xl">Real stories from real business owners</h2>
        <p className="mx-auto max-w-2xl text-pretty text-lg text-muted-foreground">
          These aren't just clients—they're families and neighbors building something meaningful in their communities
        </p>
      </div>

      <div className="mx-auto max-w-3xl">
        <div className="relative min-h-[400px]">
          <button
            onClick={goToPrevious}
            className="absolute left-0 top-1/2 z-10 -translate-x-12 -translate-y-1/2 rounded-full bg-primary p-3 text-primary-foreground shadow-lg transition-all hover:scale-110 hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
            aria-label="Previous testimonial"
          >
            <ChevronLeft className="h-6 w-6" />
          </button>

          {testimonials.map((testimonial, index) => (
            <Card
              key={index}
              className={`absolute inset-0 border-2 transition-opacity duration-1000 ${
                index === currentTestimonialIndex ? "opacity-100" : "opacity-0"
              }`}
            >
              <CardContent className="flex flex-col gap-4 p-8">
                <div className="flex gap-1">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 fill-accent text-accent" />
                  ))}
                </div>

                <p className="text-pretty text-lg leading-relaxed">"{testimonial.quote}"</p>

                <div className="mt-auto flex items-center gap-4">
                  <img
                    src={testimonial.image || "/placeholder.svg"}
                    alt={testimonial.name}
                    className="h-16 w-16 rounded-full object-cover"
                  />
                  <div>
                    <p className="font-semibold text-lg">{testimonial.name}</p>
                    <p className="text-sm text-muted-foreground">{testimonial.business}</p>
                    <p className="text-sm text-muted-foreground">{testimonial.location}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}

          <button
            onClick={goToNext}
            className="absolute right-0 top-1/2 z-10 -translate-y-1/2 translate-x-12 rounded-full bg-primary p-3 text-primary-foreground shadow-lg transition-all hover:scale-110 hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
            aria-label="Next testimonial"
          >
            <ChevronRight className="h-6 w-6" />
          </button>
        </div>

        <div className="mt-6 flex justify-center gap-2">
          {testimonials.map((_, index) => (
            <button
              key={index}
              onClick={() => goToTestimonial(index)}
              className={`h-2 w-2 rounded-full transition-all ${
                index === currentTestimonialIndex ? "w-8 bg-primary" : "bg-muted-foreground/30"
              }`}
              aria-label={`Go to testimonial ${index + 1}`}
            />
          ))}
        </div>
      </div>

      <div className="mt-16 grid gap-8 md:grid-cols-2">
        <div className="overflow-hidden rounded-2xl">
          <img
            src="/small-business-owner-family-in-their-shop--diverse.jpg"
            alt="Small business families"
            className="h-full w-full object-cover"
          />
        </div>
        <div className="flex flex-col justify-center gap-6 rounded-2xl bg-primary/5 p-8">
          <h3 className="text-2xl font-bold">Built by a family, for families</h3>
          <p className="text-pretty leading-relaxed text-muted-foreground">
            We started AWE because we saw too many hardworking business owners struggling to compete online. Our founder
            grew up helping in her parents' restaurant and knows firsthand how tough it is to wear all the hats—chef,
            accountant, marketer, and everything in between.
          </p>
          <p className="text-pretty leading-relaxed text-muted-foreground">
            That's why we built something different. No confusing dashboards, no tech speak, no long contracts. Just
            honest marketing that helps you connect with your community and grow your business—so you can focus on what
            you do best.
          </p>
        </div>
      </div>
    </section>
  )
}
