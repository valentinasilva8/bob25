import { Header } from "@/components/header"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Mail, Phone, MapPin, Clock } from "lucide-react"

export default function ContactPage() {
  return (
    <main className="min-h-screen bg-background">
      <Header />

      {/* Hero Section */}
      <section className="border-b border-border bg-gradient-to-b from-primary/5 to-background py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="mb-4 text-balance text-4xl font-bold tracking-tight md:text-5xl lg:text-6xl">Get in Touch</h1>
          <p className="mx-auto max-w-2xl text-pretty text-lg text-muted-foreground md:text-xl">
            Have questions about AWE? We're here to help you transform your wellness business with AI-powered
            advertising.
          </p>
        </div>
      </section>

      {/* Contact Content */}
      <section className="py-16 md:py-24">
        <div className="container mx-auto px-4">
          <div className="grid gap-12 lg:grid-cols-2">
            {/* Contact Form */}
            <div>
              <h2 className="mb-6 text-3xl font-bold">Send Us a Message</h2>
              <Card>
                <CardContent className="p-6">
                  <form className="space-y-6">
                    <div className="grid gap-6 md:grid-cols-2">
                      <div className="space-y-2">
                        <label htmlFor="firstName" className="text-sm font-medium">
                          First Name
                        </label>
                        <Input id="firstName" placeholder="John" required />
                      </div>
                      <div className="space-y-2">
                        <label htmlFor="lastName" className="text-sm font-medium">
                          Last Name
                        </label>
                        <Input id="lastName" placeholder="Doe" required />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <label htmlFor="email" className="text-sm font-medium">
                        Email
                      </label>
                      <Input id="email" type="email" placeholder="john@example.com" required />
                    </div>

                    <div className="space-y-2">
                      <label htmlFor="phone" className="text-sm font-medium">
                        Phone Number
                      </label>
                      <Input id="phone" type="tel" placeholder="(555) 123-4567" />
                    </div>

                    <div className="space-y-2">
                      <label htmlFor="businessName" className="text-sm font-medium">
                        Business Name
                      </label>
                      <Input id="businessName" placeholder="Your Wellness Business" />
                    </div>

                    <div className="space-y-2">
                      <label htmlFor="message" className="text-sm font-medium">
                        Message
                      </label>
                      <Textarea
                        id="message"
                        placeholder="Tell us about your business and how we can help..."
                        rows={6}
                        required
                      />
                    </div>

                    <Button type="submit" size="lg" className="w-full">
                      Send Message
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </div>

            {/* Contact Information */}
            <div className="space-y-8">
              <div>
                <h2 className="mb-6 text-3xl font-bold">Contact Information</h2>
                <p className="mb-8 text-muted-foreground">
                  Reach out to us through any of these channels. We typically respond within 24 hours during business
                  days.
                </p>

                <div className="space-y-6">
                  <Card>
                    <CardContent className="flex items-start gap-4 p-6">
                      <div className="rounded-lg bg-primary/10 p-3">
                        <Mail className="h-6 w-6 text-primary" />
                      </div>
                      <div>
                        <h3 className="mb-1 font-semibold">Email</h3>
                        <p className="text-muted-foreground">hello@aweads.com</p>
                        <p className="text-sm text-muted-foreground">support@aweads.com</p>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardContent className="flex items-start gap-4 p-6">
                      <div className="rounded-lg bg-primary/10 p-3">
                        <Phone className="h-6 w-6 text-primary" />
                      </div>
                      <div>
                        <h3 className="mb-1 font-semibold">Phone</h3>
                        <p className="text-muted-foreground">+1 (555) 123-4567</p>
                        <p className="text-sm text-muted-foreground">Mon-Fri, 9am-6pm EST</p>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardContent className="flex items-start gap-4 p-6">
                      <div className="rounded-lg bg-primary/10 p-3">
                        <MapPin className="h-6 w-6 text-primary" />
                      </div>
                      <div>
                        <h3 className="mb-1 font-semibold">Office</h3>
                        <p className="text-muted-foreground">123 Wellness Way</p>
                        <p className="text-muted-foreground">San Francisco, CA 94102</p>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardContent className="flex items-start gap-4 p-6">
                      <div className="rounded-lg bg-primary/10 p-3">
                        <Clock className="h-6 w-6 text-primary" />
                      </div>
                      <div>
                        <h3 className="mb-1 font-semibold">Business Hours</h3>
                        <p className="text-muted-foreground">Monday - Friday: 9:00 AM - 6:00 PM EST</p>
                        <p className="text-muted-foreground">Saturday - Sunday: Closed</p>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>

              {/* Quick Links */}
              <Card className="bg-primary/5">
                <CardContent className="p-6">
                  <h3 className="mb-4 text-xl font-semibold">Quick Links</h3>
                  <div className="space-y-3">
                    <Button variant="link" className="h-auto p-0 text-primary" asChild>
                      <a href="/pricing">View Pricing Plans</a>
                    </Button>
                    <br />
                    <Button variant="link" className="h-auto p-0 text-primary" asChild>
                      <a href="/solutions">Explore Solutions</a>
                    </Button>
                    <br />
                    <Button variant="link" className="h-auto p-0 text-primary" asChild>
                      <a href="/auth/sign-up">Start Free Trial</a>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="border-t border-border bg-primary/5 py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="mb-4 text-3xl font-bold">Ready to Transform Your Advertising?</h2>
          <p className="mb-8 text-lg text-muted-foreground">
            Join hundreds of wellness businesses already using AWE to grow their reach.
          </p>
          <Button size="lg" asChild>
            <a href="/auth/sign-up">Get Started Today</a>
          </Button>
        </div>
      </section>
    </main>
  )
}
