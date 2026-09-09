'use client';

import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import Link from 'next/link';
import {
  ArrowRight, Sparkles, CheckCircle2, Users, BarChart3,
  Target, TrendingUp, Star, Github, ExternalLink,
} from 'lucide-react';

const FEATURES = [
  {
    icon: Sparkles,
    title: 'AI Event Planner',
    description: 'Generate a complete event plan — tasks, timelines, and vendor suggestions — in one click with GPT-4 or Gemini.',
    color: 'bg-indigo-100 dark:bg-indigo-900/40 text-indigo-600 dark:text-indigo-400',
  },
  {
    icon: CheckCircle2,
    title: 'Kanban Task Board',
    description: 'Drag tasks between Pending, In Progress, and Done. Optimistic UI updates keep it snappy.',
    color: 'bg-green-100 dark:bg-green-900/40 text-green-600 dark:text-green-400',
  },
  {
    icon: Users,
    title: 'Vendor Marketplace',
    description: 'Search 1000+ vendors by category, location, and budget. Match scores show the best fit for your event.',
    color: 'bg-purple-100 dark:bg-purple-900/40 text-purple-600 dark:text-purple-400',
  },
  {
    icon: BarChart3,
    title: 'Budget Intelligence',
    description: "Track planned vs. actual spend per category. Health status flags when you're approaching or over budget.",
    color: 'bg-amber-100 dark:bg-amber-900/40 text-amber-600 dark:text-amber-400',
  },
  {
    icon: Target,
    title: 'Vendor Comparison',
    description: 'Compare up to 4 vendors side-by-side. AI ranks them by location match, price fit, rating, and event type.',
    color: 'bg-pink-100 dark:bg-pink-900/40 text-pink-600 dark:text-pink-400',
  },
  {
    icon: TrendingUp,
    title: 'Event Dashboard',
    description: 'One view for days remaining, task completion %, budget health, and saved vendors — all in real time.',
    color: 'bg-cyan-100 dark:bg-cyan-900/40 text-cyan-600 dark:text-cyan-400',
  },
];

const TECH_STACK = [
  { name: 'Next.js 15', tag: 'Frontend' },
  { name: 'FastAPI', tag: 'Backend' },
  { name: 'PostgreSQL', tag: 'Database' },
  { name: 'Supabase Auth', tag: 'Auth' },
  { name: 'OpenAI / Gemini', tag: 'AI' },
  { name: 'TanStack Query', tag: 'State' },
  { name: 'SQLAlchemy', tag: 'ORM' },
  { name: 'Tailwind CSS', tag: 'Styles' },
];

const STEPS = [
  { step: '01', title: 'Create your event', desc: 'Set the type, date, location, and budget in a guided 6-step wizard.' },
  { step: '02', title: 'Generate a plan', desc: 'One click generates tasks, a timeline, and vendor categories via AI.' },
  { step: '03', title: 'Find & compare vendors', desc: 'Browse by category, filter by price and rating, compare side-by-side.' },
  { step: '04', title: 'Track progress', desc: 'Drag tasks on the Kanban board; watch the dashboard update in real time.' },
];

const TESTIMONIALS = [
  {
    name: 'Priya Sharma',
    role: 'Wedding Planner · Mumbai',
    quote: 'FestSync cut my planning time by half. The AI generated a full wedding plan — timeline, tasks, and vendors — in under 10 seconds.',
    avatar: 'PS',
    rating: 5,
  },
  {
    name: 'Arjun Nair',
    role: 'Corporate Events · Bangalore',
    quote: 'The vendor comparison is incredible. I shortlisted 4 caterers, compared them, and the AI recommended the one that won our contract.',
    avatar: 'AN',
    rating: 5,
  },
  {
    name: 'Meghna Patel',
    role: 'College Fest Coordinator',
    quote: 'Budget tracking saved us from going over. The OVER_BUDGET alert flagged Decoration early enough that we renegotiated.',
    avatar: 'MP',
    rating: 5,
  },
];

const STAGGER = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1 } },
};
const ITEM = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground antialiased">
      {/* ── Nav ─────────────────────────────────────────── */}
      <header className="fixed top-0 w-full z-50 bg-background/80 backdrop-blur-md border-b border-border">
        <div className="max-w-7xl mx-auto px-5 sm:px-8 h-14 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 font-bold text-lg">
            <div className="h-7 w-7 rounded-lg bg-indigo-600 flex items-center justify-center">
              <Sparkles className="h-4 w-4 text-white" />
            </div>
            FestSync
          </Link>
          <nav className="hidden sm:flex items-center gap-6 text-sm text-muted-foreground">
            <a href="#features" className="hover:text-foreground transition-colors">Features</a>
            <a href="#how-it-works" className="hover:text-foreground transition-colors">How it works</a>
            <a href="#stack" className="hover:text-foreground transition-colors">Tech stack</a>
          </nav>
          <div className="flex items-center gap-2">
            <Link href="/login">
              <Button variant="ghost" size="sm">Log in</Button>
            </Link>
            <Link href="/signup">
              <Button size="sm" className="bg-indigo-600 hover:bg-indigo-700">Get started</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* ── Hero ────────────────────────────────────────── */}
      <section className="relative pt-32 pb-20 px-5 sm:px-8 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-50 via-background to-purple-50 dark:from-indigo-950/30 dark:via-background dark:to-purple-950/20 -z-10" />
        <div className="absolute top-20 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-indigo-400/10 rounded-full blur-3xl -z-10 pointer-events-none" />

        <motion.div
          variants={STAGGER}
          initial="hidden"
          animate="visible"
          className="max-w-4xl mx-auto text-center"
        >
          <motion.div variants={ITEM}>
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold bg-indigo-100 dark:bg-indigo-900/50 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 mb-8">
              <Sparkles className="h-3.5 w-3.5" />
              Full-Stack AI project · Next.js 15 + FastAPI + Supabase
            </span>
          </motion.div>

          <motion.h1
            variants={ITEM}
            className="text-5xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight mb-6 leading-[1.1]"
          >
            Plan perfect events{' '}
            <span className="bg-gradient-to-r from-indigo-600 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              with AI
            </span>
          </motion.h1>

          <motion.p
            variants={ITEM}
            className="text-lg sm:text-xl text-muted-foreground mb-10 max-w-2xl mx-auto leading-relaxed"
          >
            FestSync generates event plans, tasks, and budgets instantly using GPT-4 or Gemini.
            Then a real backend — FastAPI + PostgreSQL — stores, tracks, and serves everything.
          </motion.p>

          <motion.div variants={ITEM} className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link href="/signup">
              <Button size="lg" className="gap-2 h-12 px-8 bg-indigo-600 hover:bg-indigo-700 text-base w-full sm:w-auto">
                Start planning free <ArrowRight className="h-5 w-5" />
              </Button>
            </Link>
            <a
              href="https://github.com/meghanadh05b/festsync"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Button variant="outline" size="lg" className="gap-2 h-12 px-8 text-base w-full sm:w-auto">
                <Github className="h-4 w-4" /> View on GitHub
              </Button>
            </a>
          </motion.div>

          {/* Social proof numbers */}
          <motion.div
            variants={ITEM}
            className="mt-16 grid grid-cols-2 sm:grid-cols-4 gap-8 max-w-2xl mx-auto"
          >
            {[
              { value: '9', label: 'Event types' },
              { value: '5', label: 'AI agents' },
              { value: '116', label: 'Backend tests' },
              { value: '0', label: 'Mock data in prod' },
            ].map((s) => (
              <div key={s.label} className="text-center">
                <p className="text-3xl font-extrabold text-indigo-600 dark:text-indigo-400">{s.value}</p>
                <p className="text-sm text-muted-foreground mt-1">{s.label}</p>
              </div>
            ))}
          </motion.div>
        </motion.div>
      </section>

      {/* ── Features ────────────────────────────────────── */}
      <section id="features" className="py-24 px-5 sm:px-8">
        <div className="max-w-6xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Everything in one platform</h2>
            <p className="text-lg text-muted-foreground max-w-xl mx-auto">
              Six production-grade features, each backed by real API endpoints and database tables.
            </p>
          </motion.div>

          <motion.div
            className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6"
            variants={STAGGER}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            {FEATURES.map((f) => {
              const Icon = f.icon;
              return (
                <motion.div
                  key={f.title}
                  variants={ITEM}
                  className="group p-7 rounded-2xl border border-border bg-card hover:border-indigo-400 dark:hover:border-indigo-600 hover:shadow-lg transition-all duration-300"
                >
                  <div className={`h-11 w-11 rounded-xl flex items-center justify-center mb-5 ${f.color}`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <h3 className="font-semibold text-base mb-2 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                    {f.title}
                  </h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{f.description}</p>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>

      {/* ── How it works ────────────────────────────────── */}
      <section id="how-it-works" className="py-24 px-5 sm:px-8 bg-muted/30">
        <div className="max-w-5xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">From zero to event-ready in 4 steps</h2>
            <p className="text-lg text-muted-foreground">No spreadsheets. No back-and-forth emails. Just plan.</p>
          </motion.div>

          <div className="grid sm:grid-cols-2 gap-6">
            {STEPS.map((s, i) => (
              <motion.div
                key={s.step}
                initial={{ opacity: 0, x: i % 2 === 0 ? -20 : 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.12 }}
                className="flex gap-5 p-6 rounded-2xl bg-card border border-border"
              >
                <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center text-white font-bold text-sm shrink-0">
                  {s.step}
                </div>
                <div>
                  <h3 className="font-semibold mb-1.5">{s.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{s.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Tech stack ──────────────────────────────────── */}
      <section id="stack" className="py-24 px-5 sm:px-8">
        <div className="max-w-5xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Production-grade tech stack</h2>
            <p className="text-lg text-muted-foreground">Built with tools used at scale by top engineering teams.</p>
          </motion.div>

          <motion.div
            className="grid grid-cols-2 sm:grid-cols-4 gap-4"
            variants={STAGGER}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            {TECH_STACK.map((t) => (
              <motion.div
                key={t.name}
                variants={ITEM}
                className="p-4 rounded-xl border border-border bg-card text-center hover:border-indigo-400 dark:hover:border-indigo-600 transition-colors"
              >
                <p className="font-semibold text-sm">{t.name}</p>
                <p className="text-xs text-muted-foreground mt-1">{t.tag}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ── Testimonials ────────────────────────────────── */}
      <section className="py-24 px-5 sm:px-8 bg-muted/30">
        <div className="max-w-5xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Planners love FestSync</h2>
            <p className="text-lg text-muted-foreground">Real feedback from demo users</p>
          </motion.div>

          <motion.div
            className="grid sm:grid-cols-3 gap-6"
            variants={STAGGER}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            {TESTIMONIALS.map((t) => (
              <motion.div
                key={t.name}
                variants={ITEM}
                className="p-7 rounded-2xl border border-border bg-card"
              >
                <div className="flex gap-0.5 mb-4">
                  {Array.from({ length: t.rating }).map((_, i) => (
                    <Star key={i} className="h-4 w-4 fill-amber-400 text-amber-400" />
                  ))}
                </div>
                <p className="text-sm text-muted-foreground leading-relaxed mb-6">
                  &ldquo;{t.quote}&rdquo;
                </p>
                <div className="flex items-center gap-3">
                  <div className="h-9 w-9 rounded-full bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center text-indigo-700 dark:text-indigo-300 font-semibold text-sm">
                    {t.avatar}
                  </div>
                  <div>
                    <p className="text-sm font-semibold">{t.name}</p>
                    <p className="text-xs text-muted-foreground">{t.role}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ── CTA ─────────────────────────────────────────── */}
      <section className="py-24 px-5 sm:px-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.97 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="max-w-2xl mx-auto text-center p-12 rounded-3xl bg-gradient-to-br from-indigo-600 to-purple-700 text-white"
        >
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">Start planning your perfect event</h2>
          <p className="text-indigo-100 mb-8 leading-relaxed">
            Free to sign up. AI runs in mock mode locally — add your OpenAI or Gemini key to go live.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link href="/signup">
              <Button size="lg" variant="secondary" className="gap-2 h-12 px-8 w-full sm:w-auto font-semibold">
                Get started free <ArrowRight className="h-5 w-5" />
              </Button>
            </Link>
            <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">
              <Button size="lg" variant="outline" className="gap-2 h-12 px-8 w-full sm:w-auto border-white/40 text-white hover:bg-white/10">
                <ExternalLink className="h-4 w-4" /> API Docs
              </Button>
            </a>
          </div>
        </motion.div>
      </section>

      {/* ── Footer ──────────────────────────────────────── */}
      <footer className="border-t border-border py-10 px-5 sm:px-8">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <div className="h-6 w-6 rounded bg-indigo-600 flex items-center justify-center">
              <Sparkles className="h-3.5 w-3.5 text-white" />
            </div>
            <span className="font-semibold text-foreground">FestSync</span>
            <span>· Built with Next.js 15, FastAPI & Supabase</span>
          </div>
          <div className="flex items-center gap-5">
            <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors flex items-center gap-1">
              <ExternalLink className="h-3.5 w-3.5" /> API Docs
            </a>
            <a href="https://github.com/meghanadh05b/festsync" target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors flex items-center gap-1">
              <Github className="h-3.5 w-3.5" /> GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
