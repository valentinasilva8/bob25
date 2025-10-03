import { Leaf, Zap, Cloud, Recycle, TrendingDown, Heart } from "lucide-react"

export function SustainabilitySection() {
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
    <section id="sustainability" className="bg-background py-24">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-3xl text-center">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-green-500/10 px-4 py-2 text-sm font-medium text-green-700 dark:text-green-400">
            <Leaf className="h-4 w-4" />
            Our Commitment to the Planet
          </div>
          <h2 className="mb-6 text-balance text-4xl font-bold tracking-tight md:text-5xl">
            Marketing That's Good for Your Business{" "}
            <span className="text-green-600 dark:text-green-500">and the Planet</span>
          </h2>
          <p className="text-pretty text-lg leading-relaxed text-muted-foreground">
            At AWE, we believe that powerful marketing shouldn't come at the expense of our environment. Every decision
            we make—from our AI models to our infrastructure—is designed to minimize environmental impact while
            maximizing results for your business.
          </p>
        </div>

        <div className="mt-16 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
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

        <div className="mt-16 rounded-2xl border border-green-500/20 bg-gradient-to-br from-green-500/5 to-green-600/5 p-8 md:p-12">
          <div className="mx-auto max-w-3xl text-center">
            <h3 className="mb-4 text-2xl font-bold md:text-3xl">Our Environmental Impact</h3>
            <p className="mb-8 text-pretty leading-relaxed text-muted-foreground">
              Since our founding, we've helped small businesses reduce their marketing carbon footprint by an average of
              <span className="font-semibold text-green-600 dark:text-green-500"> 85%</span> compared to traditional
              advertising methods. Together with our clients, we've offset over{" "}
              <span className="font-semibold text-green-600 dark:text-green-500">500 tons of CO₂</span> and planted{" "}
              <span className="font-semibold text-green-600 dark:text-green-500">10,000 trees</span> through our
              reforestation partnerships.
            </p>
            <div className="grid gap-6 md:grid-cols-3">
              <div className="rounded-xl bg-background/50 p-6">
                <div className="mb-2 text-3xl font-bold text-green-600 dark:text-green-500">85%</div>
                <div className="text-sm text-muted-foreground">Carbon Reduction vs Traditional Marketing</div>
              </div>
              <div className="rounded-xl bg-background/50 p-6">
                <div className="mb-2 text-3xl font-bold text-green-600 dark:text-green-500">100%</div>
                <div className="text-sm text-muted-foreground">Renewable Energy Powered</div>
              </div>
              <div className="rounded-xl bg-background/50 p-6">
                <div className="mb-2 text-3xl font-bold text-green-600 dark:text-green-500">10K+</div>
                <div className="text-sm text-muted-foreground">Trees Planted Through Partnerships</div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-12 text-center">
          <p className="text-pretty text-sm leading-relaxed text-muted-foreground">
            We're committed to continuous improvement and transparency. Our sustainability practices are regularly
            audited by third-party environmental organizations, and we publish annual impact reports detailing our
            progress toward carbon neutrality and beyond.
          </p>
        </div>
      </div>
    </section>
  )
}
