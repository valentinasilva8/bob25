export function ProblemSection() {
  return (
    <section className="bg-muted py-20">
      <div className="container mx-auto px-4">
        <h2 className="mb-16 text-balance text-center text-3xl font-bold md:text-4xl">
          We know how hard it is to compete with the big guys
        </h2>

        <div className="grid gap-8 md:grid-cols-3">
          <div className="flex flex-col gap-4">
            <h3 className="text-2xl font-bold text-primary md:text-3xl">Ads cost too much</h3>
            <p className="text-pretty leading-relaxed text-muted-foreground">
              Every dollar counts when you're running a small business. You shouldn't have to choose between paying for
              ads and paying your team. We help you get more from every marketing dollar.
            </p>
          </div>

          <div className="flex flex-col gap-4">
            <h3 className="text-2xl font-bold text-primary md:text-3xl">Nobody wants to see the same ad twice</h3>
            <p className="text-pretty leading-relaxed text-muted-foreground">
              Your customers are real people, not numbers. They want to feel understood, not bombarded. We create ads
              that speak to them personally—like a conversation with a friend, not a sales pitch.
            </p>
          </div>

          <div className="flex flex-col gap-4">
            <h3 className="text-2xl font-bold text-primary md:text-3xl">Your business is one-of-a-kind</h3>
            <p className="text-pretty leading-relaxed text-muted-foreground">
              You didn't start your business to be like everyone else. Your values, your story, your relationships with
              customers—that's what makes you special. Let's show the world what makes you different.
            </p>
          </div>
        </div>

        <div className="mt-16 rounded-lg border border-green-500/30 bg-green-500/5 p-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div className="flex flex-col gap-2">
              <h3 className="text-xl font-bold">Good for your business, good for the planet</h3>
              <p className="text-pretty leading-relaxed text-muted-foreground">
                We believe in doing right by our communities and our environment. Our smart technology runs on clean
                energy when it's available, helping you save money while protecting the world we're leaving for our
                kids.
              </p>
            </div>
            <div className="flex items-center gap-2 text-green-600">
              <svg className="h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
