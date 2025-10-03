import { Header } from "@/components/header"
import { Leaf, Zap, Cloud, Recycle, TrendingDown, Heart } from "lucide-react"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function SustainabilityPage() {
  const initiatives = [
    {
      icon: Zap,
      title: "Energy-Efficient AI",
      description:
        "We use optimized AI models that require 60% less computational power than traditional alternatives, significantly reducing our carbon footprint while delivering exceptional results.",
    },
    {
      icon: Cloud,
      title: "Green Cloud Infrastructure",
      description:
        "Our infrastructure runs on 100% renewable energy through partnerships with carbon-neutral data centers powered by wind, solar, and hydroelectric sources.",
    },
    {
      icon: TrendingDown,
      title: "Carbon-Negative Operations",
      description:
        "We offset 150% of our carbon emissions through verified reforestation projects and renewable energy investments, making every campaign actively beneficial for the planet.",
    },
    {
      icon: Recycle,
      title: "Optimized Resource Usage",
      description:
        "Our intelligent algorithms minimize data processing and storage waste, using advanced caching and compression to reduce server loads by up to 70%.",
    },
    {
      icon: Leaf,
      title: "Sustainable Development",
      description:
        "We prioritize lightweight code, efficient databases, and serverless architecture to minimize energy consumption across every aspect of our platform.",
    },
    {
      icon: Heart,
      title: "Transparent Impact",
      description:
        "We provide detailed carbon impact reports to all clients, showing exactly how much CO₂ your marketing campaigns save compared to traditional methods.",
    },
  ]

  return (
    <main className="min-h-screen">
      <Header />

      {/* Hero Section */}
      <section className="bg-gradient-to-b from-green-50 to-background py-24 dark:from-green-950/20">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-green-500/10 px-4 py-2 text-sm font-medium text-green-700 dark:text-green-400">
              <Leaf className="h-4 w-4" />
              Our Commitment to the Planet
            </div>
            <h1 className="mb-6 text-balance text-5xl font-bold tracking-tight md:text-6xl">
              Marketing That's Good for Your Business{" "}
              <span className="text-green-600 dark:text-green-500">and the Planet</span>
            </h1>
            <p className="text-pretty text-xl leading-relaxed text-muted-foreground">
              At AWE, we believe that powerful marketing shouldn't come at the expense of our environment. Every
              decision we make—from our AI models to our infrastructure—is designed to minimize environmental impact
              while maximizing results for your business.
            </p>
          </div>
        </div>
      </section>

      {/* Initiatives Section */}
      <section className="bg-background py-24">
        <div className="container mx-auto px-4">
          <div className="mx-auto mb-16 max-w-2xl text-center">
            <h2 className="mb-4 text-balance text-3xl font-bold tracking-tight md:text-4xl">
              Our Sustainability Initiatives
            </h2>
            <p className="text-pretty leading-relaxed text-muted-foreground">
              We've built sustainability into every layer of our platform, from the code we write to the servers that
              power it.
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {initiatives.map((initiative, index) => {
              const Icon = initiative.icon
              return (
                <div
                  key={index}
                  className="group rounded-2xl border border-border bg-card p-6 transition-all hover:border-green-500/50 hover:shadow-lg"
                >
                  <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-green-500/10 text-green-600 transition-colors group-hover:bg-green-500/20 dark:text-green-500">
                    <Icon className="h-6 w-6" />
                  </div>
                  <h3 className="mb-3 text-xl font-semibold">{initiative.title}</h3>
                  <p className="leading-relaxed text-muted-foreground">{initiative.description}</p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Impact Section */}
      <section className="bg-muted/30 py-24">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-4xl rounded-2xl border border-green-500/20 bg-gradient-to-br from-green-500/5 to-green-600/5 p-8 md:p-12">
            <div className="text-center">
              <h2 className="mb-4 text-3xl font-bold md:text-4xl">Our Environmental Impact</h2>
              <p className="mb-8 text-pretty leading-relaxed text-muted-foreground">
                Since our founding, we've helped small businesses reduce their marketing carbon footprint by an average
                of
                <span className="font-semibold text-green-600 dark:text-green-500"> 85%</span> compared to traditional
                advertising methods. Together with our clients, we've offset over{" "}
                <span className="font-semibold text-green-600 dark:text-green-500">500 tons of CO₂</span> and planted{" "}
                <span className="font-semibold text-green-600 dark:text-green-500">10,000 trees</span> through our
                reforestation partnerships.
              </p>
              <div className="grid gap-6 md:grid-cols-3">
                <div className="rounded-xl bg-background/50 p-6">
                  <div className="mb-2 text-4xl font-bold text-green-600 dark:text-green-500">85%</div>
                  <div className="text-sm text-muted-foreground">Carbon Reduction vs Traditional Marketing</div>
                </div>
                <div className="rounded-xl bg-background/50 p-6">
                  <div className="mb-2 text-4xl font-bold text-green-600 dark:text-green-500">100%</div>
                  <div className="text-sm text-muted-foreground">Renewable Energy Powered</div>
                </div>
                <div className="rounded-xl bg-background/50 p-6">
                  <div className="mb-2 text-4xl font-bold text-green-600 dark:text-green-500">10K+</div>
                  <div className="text-sm text-muted-foreground">Trees Planted Through Partnerships</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Transparency Section */}
      <section className="bg-background py-24">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="mb-6 text-3xl font-bold md:text-4xl">Transparency & Accountability</h2>
            <p className="mb-8 text-pretty text-lg leading-relaxed text-muted-foreground">
              We're committed to continuous improvement and transparency. Our sustainability practices are regularly
              audited by third-party environmental organizations, and we publish annual impact reports detailing our
              progress toward carbon neutrality and beyond.
            </p>
            <p className="mb-8 text-pretty leading-relaxed text-muted-foreground">
              Every client receives detailed carbon impact reports showing exactly how much CO₂ their marketing
              campaigns save compared to traditional methods. We believe in making sustainability measurable,
              transparent, and accessible to businesses of all sizes.
            </p>
            <Button asChild size="lg" className="gap-2">
              <Link href="/auth/sign-up">
                <Leaf className="h-5 w-5" />
                Start Your Sustainable Marketing Journey
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </main>
  )
}
