import { Header } from "@/components/awe/header"
import { Leaf, Zap, Cloud, Recycle, Server, Cpu, Database, BarChart3, Timer, Gauge } from "lucide-react"
import { Button } from "@/components/awe/ui/button"
import Link from "next/link"

export default function SustainabilityPage() {
  const initiatives = [
    {
      icon: Cloud,
      title: "Google Cloud: 100% Renewable Energy",
      description:
        "We run on Google Cloud, the cleanest global cloud infrastructure. Google has matched 100% of its electricity use with renewable energy since 2017 and is committed to 24/7 carbon-free energy in all data centers by 2030. We deploy in low-CO₂ regions with at least 75% carbon-free energy.",
    },
    {
      icon: Cpu,
      title: "Efficient AI Models",
      description:
        "We use compact, optimized models (7B parameters or less) like Mistral 7B and DistilGPT-2 for text generation, and optimized Stable Diffusion for images. These models deliver 95-97% of large model performance while using a fraction of the energy—avoiding wasteful 100B+ parameter models.",
    },
    {
      icon: Server,
      title: "Hardware Optimization",
      description:
        "Our infrastructure leverages energy-efficient hardware like AWS Graviton3 (60% less energy), Inferentia2 ASICs, and NVIDIA Ampere GPUs with TensorRT optimization. We use quantization (INT8/4-bit) to reduce computation by up to 4× while maintaining quality.",
    },
    {
      icon: Timer,
      title: "Carbon-Aware Scheduling",
      description:
        "We batch AI inference jobs and schedule them during times when the grid has the lowest carbon intensity—often overnight when renewable energy is abundant. This flexible scheduling can significantly cut emissions by aligning compute with clean energy availability.",
    },
    {
      icon: Database,
      title: "Intelligent Caching & Reuse",
      description:
        "We cache generated ad copy templates and visual assets to eliminate redundant computation. By reusing and compositing existing content, we dramatically reduce the number of expensive model runs—serving cached content uses trivial energy compared to GPU inference.",
    },
    {
      icon: BarChart3,
      title: "Transparent Carbon Tracking",
      description:
        "We measure our impact using Google Cloud's Carbon Footprint dashboard and tools like Cloud Carbon Footprint. Each image generation produces ~1.5-2g CO₂, and we provide clients with detailed metrics showing exactly how much carbon their campaigns consume and save.",
    },
  ]

  const technicalDetails = [
    {
      title: "Cloud vs On-Premise",
      metric: "84% reduction",
      description:
        "Migrating to public cloud infrastructure cuts associated emissions by up to 84% compared to traditional on-premise setups.",
    },
    {
      title: "Model Efficiency",
      metric: "1B-7B params",
      description:
        "We use compact models like LLaMA-2 7B, Mistral 7B, and T5-Base (220M) that are more than sufficient for ad copy while consuming far less energy than giant models.",
    },
    {
      title: "Image Generation",
      metric: "~2g CO₂/image",
      description:
        "Each AI-generated image produces approximately 1.5-2g CO₂. We optimize with quantization, smaller backbones, and domain-specific models to minimize this footprint.",
    },
    {
      title: "Batch Processing",
      metric: "10× efficiency",
      description:
        "Running 10 inferences in parallel on a GPU uses only slightly more power than one, amortizing energy costs and enabling carbon-aware scheduling during green energy windows.",
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
              AI-Powered Marketing Built on{" "}
              <span className="text-green-600 dark:text-green-500">Sustainable Infrastructure</span>
            </h1>
            <p className="text-pretty text-xl leading-relaxed text-muted-foreground">
              At AWE, sustainability isn't an afterthought—it's engineered into every layer of our platform. From Google
              Cloud's 100% renewable energy to optimized AI models and carbon-aware scheduling, we've built a system
              that delivers powerful results while minimizing environmental impact.
            </p>
          </div>
        </div>
      </section>

      {/* Initiatives Section */}
      <section className="bg-background py-24">
        <div className="container mx-auto px-4">
          <div className="mx-auto mb-16 max-w-2xl text-center">
            <h2 className="mb-4 text-balance text-3xl font-bold tracking-tight md:text-4xl">
              Our Technical Sustainability Approach
            </h2>
            <p className="text-pretty leading-relaxed text-muted-foreground">
              Every technical decision—from cloud provider to model architecture—is optimized for both performance and
              minimal carbon footprint.
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

      {/* Technical Metrics Section */}
      <section className="bg-muted/30 py-24">
        <div className="container mx-auto px-4">
          <div className="mx-auto mb-12 max-w-2xl text-center">
            <h2 className="mb-4 text-3xl font-bold md:text-4xl">Measurable Impact</h2>
            <p className="text-pretty leading-relaxed text-muted-foreground">
              We quantify our carbon footprint at every level—from individual inferences to entire campaigns—using
              industry-standard tools and transparent metrics.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {technicalDetails.map((detail, index) => (
              <div
                key={index}
                className="rounded-2xl border border-green-500/20 bg-gradient-to-br from-green-500/5 to-green-600/5 p-6"
              >
                <div className="mb-2 text-3xl font-bold text-green-600 dark:text-green-500">{detail.metric}</div>
                <h3 className="mb-2 font-semibold">{detail.title}</h3>
                <p className="text-sm leading-relaxed text-muted-foreground">{detail.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Detailed Approach Section */}
      <section className="bg-background py-24">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-4xl">
            <h2 className="mb-12 text-center text-3xl font-bold md:text-4xl">How We Minimize Energy Consumption</h2>

            <div className="space-y-8">
              <div className="rounded-2xl border border-border bg-card p-8">
                <div className="mb-4 flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-green-500/10">
                    <Zap className="h-5 w-5 text-green-600 dark:text-green-500" />
                  </div>
                  <h3 className="text-2xl font-semibold">Right-Sized AI Models</h3>
                </div>
                <p className="mb-4 leading-relaxed text-muted-foreground">
                  Model efficiency outweighs sheer size. We favor smaller, open-source models optimized through
                  distillation and quantization. For text generation, we use models like <strong>DistilGPT-2</strong>{" "}
                  (82M parameters), <strong>Mistral 7B</strong>, and <strong>LLaMA-2 7B</strong>—achieving 95-97% of
                  large model accuracy with a fraction of the energy.
                </p>
                <p className="leading-relaxed text-muted-foreground">
                  For image generation, we use optimized <strong>Stable Diffusion</strong> with quantization
                  (INT8/4-bit) and smaller backbones, cutting energy use by up to 4× while maintaining visual quality.
                  We avoid wasteful 100B+ parameter models that would be overkill for short-form ad content.
                </p>
              </div>

              <div className="rounded-2xl border border-border bg-card p-8">
                <div className="mb-4 flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-green-500/10">
                    <Timer className="h-5 w-5 text-green-600 dark:text-green-500" />
                  </div>
                  <h3 className="text-2xl font-semibold">Carbon-Aware Scheduling</h3>
                </div>
                <p className="mb-4 leading-relaxed text-muted-foreground">
                  Rather than generating ads on-demand, we batch requests and schedule them during times when the
                  electrical grid has the lowest carbon intensity—often overnight when renewable energy is abundant.
                  This flexible scheduling can significantly reduce emissions.
                </p>
                <p className="leading-relaxed text-muted-foreground">
                  We use tools like <strong>ElectricityMaps</strong> to monitor real-time grid carbon intensity and
                  Google Cloud's region-level carbon data to choose the cleanest data centers. By aligning compute with
                  clean energy availability, we minimize our footprint without sacrificing performance.
                </p>
              </div>

              <div className="rounded-2xl border border-border bg-card p-8">
                <div className="mb-4 flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-green-500/10">
                    <Recycle className="h-5 w-5 text-green-600 dark:text-green-500" />
                  </div>
                  <h3 className="text-2xl font-semibold">Intelligent Caching & Reuse</h3>
                </div>
                <p className="mb-4 leading-relaxed text-muted-foreground">
                  We maintain a library of AI-generated templates and visual assets, reusing them with variations rather
                  than generating from scratch every time. For example, a headline template like "50% off sale this
                  weekend!" is generated once and reused with simple modifications.
                </p>
                <p className="leading-relaxed text-muted-foreground">
                  Serving cached content from memory uses trivial energy compared to invoking a GPU model. This approach
                  dramatically reduces total inference count, peak loads, and overall power consumption while
                  maintaining creative variety.
                </p>
              </div>

              <div className="rounded-2xl border border-border bg-card p-8">
                <div className="mb-4 flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-green-500/10">
                    <Gauge className="h-5 w-5 text-green-600 dark:text-green-500" />
                  </div>
                  <h3 className="text-2xl font-semibold">Hardware Optimization</h3>
                </div>
                <p className="leading-relaxed text-muted-foreground">
                  We leverage energy-efficient hardware like <strong>AWS Graviton3</strong> (60% less energy than
                  standard instances), <strong>Inferentia2 ASICs</strong>, and{" "}
                  <strong>NVIDIA Ampere/Hopper GPUs</strong> with TensorRT optimization. We enable batch inference,
                  quantized operations, and power limiting to maximize efficiency—slightly slower but far more
                  power-thrifty operation at the optimal wattage sweet spot.
                </p>
              </div>
            </div>
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
                By combining Google Cloud's renewable infrastructure with optimized AI models and intelligent
                scheduling, we've achieved up to{" "}
                <span className="font-semibold text-green-600 dark:text-green-500">
                  80-90% reduction in CO₂ emissions
                </span>{" "}
                compared to naive approaches. Every technical optimization translates directly into measurable
                environmental benefits.
              </p>
              <div className="grid gap-6 md:grid-cols-3">
                <div className="rounded-xl bg-background/50 p-6">
                  <div className="mb-2 text-4xl font-bold text-green-600 dark:text-green-500">100%</div>
                  <div className="text-sm text-muted-foreground">Renewable Energy (Google Cloud since 2017)</div>
                </div>
                <div className="rounded-xl bg-background/50 p-6">
                  <div className="mb-2 text-4xl font-bold text-green-600 dark:text-green-500">84%</div>
                  <div className="text-sm text-muted-foreground">Emissions Cut vs On-Premise Infrastructure</div>
                </div>
                <div className="rounded-xl bg-background/50 p-6">
                  <div className="mb-2 text-4xl font-bold text-green-600 dark:text-green-500">~2g</div>
                  <div className="text-sm text-muted-foreground">CO₂ per AI-Generated Image (Optimized)</div>
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
            <h2 className="mb-6 text-3xl font-bold md:text-4xl">Transparency & Continuous Improvement</h2>
            <p className="mb-8 text-pretty text-lg leading-relaxed text-muted-foreground">
              We measure our carbon footprint using <strong>Google Cloud's Carbon Footprint dashboard</strong>,{" "}
              <strong>Cloud Carbon Footprint</strong> (open-source tool), and <strong>ElectricityMaps</strong> for
              real-time grid intensity. Every client receives detailed reports showing exactly how much CO₂ their
              campaigns consume—down to grams per image and inference.
            </p>
            <p className="mb-8 text-pretty leading-relaxed text-muted-foreground">
              We're committed to continuous optimization: as Google Cloud moves toward 24/7 carbon-free energy by 2030
              and as AI models become more efficient, our footprint will continue to shrink. We believe in making
              sustainability measurable, transparent, and accessible to businesses of all sizes.
            </p>
            <Button asChild size="lg" className="gap-2">
              <Link href="/register">
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
