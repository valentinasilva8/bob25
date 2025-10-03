import { Header } from "@/components/awe/header"
import { Card, CardContent } from "@/components/awe/ui/card"
import { Star } from "lucide-react"

export default function TestimonialsPage() {
  const testimonials = [
    {
      name: "Sarah Chen",
      role: "Owner",
      business: "Lotus Wellness Studio",
      image: "/professional-woman-smiling.png",
      quote:
        "AWE transformed how we reach our community. Within three months, our class bookings increased by 65%. The AI understands our voice and creates ads that truly resonate with our audience.",
      rating: 5,
    },
    {
      name: "Marcus Thompson",
      role: "Founder",
      business: "Urban Yoga Collective",
      image: "/professional-man-smiling.png",
      quote:
        "As a small business owner, I was spending hours trying to create effective ads. AWE does in minutes what used to take me days, and the results are honestly better than what I could do myself.",
      rating: 5,
    },
    {
      name: "Elena Rodriguez",
      role: "Co-Owner",
      business: "Mindful Movement Center",
      image: "/professional-woman-portrait.png",
      quote:
        "The targeting capabilities are incredible. We're reaching exactly the right people at the right time. Our cost per acquisition dropped by 40% while our membership sign-ups doubled.",
      rating: 5,
    },
    {
      name: "David Park",
      role: "Director",
      business: "Serenity Spa & Wellness",
      image: "/professional-man-portrait.png",
      quote:
        "I was skeptical about AI-generated ads, but AWE proved me wrong. The creativity and consistency are outstanding. It's like having a full marketing team for a fraction of the cost.",
      rating: 5,
    },
    {
      name: "Jennifer Walsh",
      role: "Owner",
      business: "Balance Pilates Studio",
      image: "/professional-woman-headshot.png",
      quote:
        "AWE helped us compete with the big chains in our area. Our ads look professional, our messaging is clear, and we're finally getting the visibility we deserve. Game changer for small wellness businesses.",
      rating: 5,
    },
    {
      name: "Ahmed Hassan",
      role: "Founder",
      business: "Vitality Fitness & Wellness",
      image: "/professional-man-headshot.png",
      quote:
        "The ROI speaks for itself. We invested in AWE's Growth plan and saw a 3x return in the first quarter. The continuous optimization means our ads keep getting better without any extra work from us.",
      rating: 5,
    },
  ]

  const stats = [
    { value: "500+", label: "Wellness Businesses" },
    { value: "95%", label: "Client Satisfaction" },
    { value: "2.5x", label: "Average ROI Increase" },
    { value: "10M+", label: "People Reached" },
  ]

  return (
    <main className="min-h-screen bg-background">
      <Header />

      {/* Hero Section */}
      <section className="border-b border-border bg-gradient-to-b from-primary/5 to-background py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="mb-6 text-balance text-4xl font-bold tracking-tight md:text-5xl lg:text-6xl">
            Trusted by Wellness Businesses
            <span className="block text-primary">Across the Country</span>
          </h1>
          <p className="mx-auto mb-8 max-w-2xl text-pretty text-lg text-muted-foreground md:text-xl">
            See how AWE is helping small wellness businesses compete with larger chains through AI-powered advertising
            that delivers real results.
          </p>
        </div>
      </section>

      {/* Stats Section */}
      <section className="border-b border-border bg-background py-16">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="mb-2 text-4xl font-bold text-primary md:text-5xl">{stat.value}</div>
                <div className="text-sm text-muted-foreground md:text-base">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Grid */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="mb-12 text-center">
            <h2 className="mb-4 text-3xl font-bold md:text-4xl">What Our Clients Say</h2>
            <p className="mx-auto max-w-2xl text-pretty text-muted-foreground">
              Real stories from real wellness business owners who have transformed their marketing with AWE.
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="flex flex-col">
                <CardContent className="flex flex-1 flex-col p-6">
                  {/* Rating */}
                  <div className="mb-4 flex gap-1">
                    {Array.from({ length: testimonial.rating }).map((_, i) => (
                      <Star key={i} className="h-5 w-5 fill-primary text-primary" />
                    ))}
                  </div>

                  {/* Quote */}
                  <blockquote className="mb-6 flex-1 text-pretty leading-relaxed">"{testimonial.quote}"</blockquote>

                  {/* Author */}
                  <div className="flex items-center gap-4">
                    <img
                      src={testimonial.image || "/placeholder.svg"}
                      alt={testimonial.name}
                      className="h-12 w-12 rounded-full object-cover"
                    />
                    <div>
                      <div className="font-semibold">{testimonial.name}</div>
                      <div className="text-sm text-muted-foreground">
                        {testimonial.role}, {testimonial.business}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="border-t border-border bg-primary/5 py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="mb-4 text-3xl font-bold md:text-4xl">Ready to Join Them?</h2>
          <p className="mx-auto mb-8 max-w-2xl text-pretty text-lg text-muted-foreground">
            Start creating AI-powered ads that help your wellness business thrive. No credit card required to get
            started.
          </p>
          <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
            <a
              href="/auth/sign-up"
              className="inline-flex h-11 items-center justify-center rounded-md bg-primary px-8 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90"
            >
              Start Free Trial
            </a>
            <a
              href="/pricing"
              className="inline-flex h-11 items-center justify-center rounded-md border border-input bg-background px-8 text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground"
            >
              View Pricing
            </a>
          </div>
        </div>
      </section>
    </main>
  )
}
