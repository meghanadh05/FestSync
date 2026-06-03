'use client';

import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import Link from 'next/link';
import {
  ArrowRight,
  Sparkles,
  CheckCircle2,
  Users,
  BarChart3,
  Zap,
  TrendingUp,
  Target,
  Clock,
  Shield,
} from 'lucide-react';

const features = [
  {
    icon: Sparkles,
    title: 'AI Event Planning',
    description: 'Generate comprehensive event plans in minutes. Our AI analyzes your event type, budget, and timeline to create actionable plans.',
    details: [
      'Smart timeline generation',
      'Task list auto-creation',
      'Budget allocation suggestions',
      'Vendor recommendations',
    ],
  },
  {
    icon: CheckCircle2,
    title: 'Smart To-Do Board',
    description: 'Organize all event tasks with an intelligent Kanban board. Track progress and never miss a deadline.',
    details: [
      'Drag-and-drop task management',
      'Priority-based organization',
      'Due date tracking',
      'Team collaboration',
    ],
  },
  {
    icon: Users,
    title: 'Vendor Discovery',
    description: 'Find the perfect vendors for your event. Search by category, location, budget, and ratings.',
    details: [
      'Smart vendor matching',
      'Verified vendor badges',
      'Real customer reviews',
      'Vendor portfolio galleries',
    ],
  },
  {
    icon: BarChart3,
    title: 'Budget Tracking',
    description: 'Stay in control of your spending. Real-time expense tracking with analytics and forecasting.',
    details: [
      'Category-wise breakdown',
      'Spending trends',
      'Budget forecasting',
      'Receipt management',
    ],
  },
  {
    icon: Target,
    title: 'Vendor Comparison',
    description: 'Compare multiple vendors side-by-side. Make data-driven decisions with detailed comparisons.',
    details: [
      'Price comparison',
      'Service comparison',
      'Rating analysis',
      'Quick decision making',
    ],
  },
  {
    icon: TrendingUp,
    title: 'Event Analytics',
    description: 'Track event progress with beautiful dashboards. Get insights into planning progress and spending.',
    details: [
      'Real-time metrics',
      'Progress tracking',
      'Completion forecasts',
      'Performance insights',
    ],
  },
];

const testimonials = [
  {
    name: 'Emily Chen',
    role: 'Wedding Planner',
    text: 'FestSync saved me 20+ hours of planning time. The AI suggestions were spot-on and the vendor matching is incredible.',
    image: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop',
    rating: 5,
  },
  {
    name: 'Marcus Rodriguez',
    role: 'Event Organizer',
    text: 'The vendor comparison feature alone paid for itself. We found better vendors and saved 30% on costs.',
    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop',
    rating: 5,
  },
  {
    name: 'Sarah Johnson',
    role: 'Corporate Events Manager',
    text: 'Finally, a tool that understands event planning complexity. The budget tracking is phenomenal.',
    image: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop',
    rating: 5,
  },
];

const stats = [
  { label: 'Events Planned', value: '10,000+' },
  { label: 'Average Savings', value: '28%' },
  { label: 'Time Saved', value: '15+ hrs' },
  { label: 'Happy Planners', value: '4.9/5' },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5 },
  },
};

export default function Home() {
  return (
    <div className="min-h-screen bg-white dark:bg-slate-950">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 dark:bg-slate-950/80 backdrop-blur-sm border-b border-slate-200 dark:border-slate-800 z-40">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="text-2xl font-bold">🎉 FestSync</div>
          <div className="flex gap-4">
            <Link href="/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/signup">
              <Button>Get Started Free</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <motion.section
        className="pt-32 pb-20 px-6 bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-950"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            variants={itemVariants}
            className="inline-block mb-6 px-4 py-2 rounded-full bg-indigo-100 dark:bg-indigo-900"
          >
            <span className="text-sm font-semibold text-indigo-600 dark:text-indigo-400">
              ✨ AI-Powered Event Planning
            </span>
          </motion.div>
          <motion.h1
            variants={itemVariants}
            className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent"
          >
            Plan Perfect Events in Minutes
          </motion.h1>
          <motion.p
            variants={itemVariants}
            className="text-xl text-slate-600 dark:text-slate-400 mb-8 max-w-2xl mx-auto leading-relaxed"
          >
            From weddings to corporate conferences, FestSync uses AI to help you generate plans, discover vendors, track budgets, and execute flawlessly.
          </motion.p>
          <motion.div variants={itemVariants} className="flex gap-4 justify-center">
            <Link href="/signup">
              <Button size="lg" className="gap-2 text-base h-12 px-8">
                Start Planning Free <ArrowRight className="h-5 w-5" />
              </Button>
            </Link>
            <Button variant="outline" size="lg" className="text-base h-12 px-8">
              Watch Demo
            </Button>
          </motion.div>

          {/* Stats */}
          <motion.div
            variants={itemVariants}
            className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8"
          >
            {stats.map((stat, i) => (
              <div key={i} className="text-center">
                <p className="text-3xl font-bold text-indigo-600 dark:text-indigo-400">
                  {stat.value}
                </p>
                <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                  {stat.label}
                </p>
              </div>
            ))}
          </motion.div>
        </div>
      </motion.section>

      {/* Features Grid */}
      <section className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold mb-4">Everything You Need</h2>
            <p className="text-xl text-slate-600 dark:text-slate-400">
              All the tools to plan, organize, and execute perfect events
            </p>
          </motion.div>

          <motion.div
            className="grid md:grid-cols-2 lg:grid-cols-3 gap-8"
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            {features.map((feature, i) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={i}
                  variants={itemVariants}
                  className="p-8 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-indigo-500 dark:hover:border-indigo-500 transition-all duration-300 hover:shadow-lg hover:-translate-y-1"
                >
                  <div className="h-12 w-12 rounded-lg bg-indigo-100 dark:bg-indigo-900 flex items-center justify-center mb-4">
                    <Icon className="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
                  </div>
                  <h3 className="font-bold text-lg mb-2">{feature.title}</h3>
                  <p className="text-slate-600 dark:text-slate-400 mb-4 text-sm leading-relaxed">
                    {feature.description}
                  </p>
                  <ul className="space-y-2">
                    {feature.details.map((detail, j) => (
                      <li
                        key={j}
                        className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400"
                      >
                        <div className="h-1.5 w-1.5 rounded-full bg-indigo-600 dark:bg-indigo-400" />
                        {detail}
                      </li>
                    ))}
                  </ul>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-24 px-6 bg-slate-50 dark:bg-slate-900">
        <div className="max-w-6xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold mb-4">How It Works</h2>
            <p className="text-xl text-slate-600 dark:text-slate-400">
              Start planning your perfect event in 6 simple steps
            </p>
          </motion.div>

          <motion.div
            className="grid md:grid-cols-3 gap-8 mb-12"
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            {[
              {
                step: 1,
                title: 'Create Event',
                description: 'Enter basic event details like type, date, and location',
              },
              {
                step: 2,
                title: 'Generate Plan',
                description: 'AI creates a comprehensive plan with timeline and tasks',
              },
              {
                step: 3,
                title: 'Find Vendors',
                description: 'Discover and compare vendors for your event needs',
              },
              {
                step: 4,
                title: 'Track Budget',
                description: 'Monitor expenses and stay within your budget',
              },
              {
                step: 5,
                title: 'Manage Tasks',
                description: 'Organize tasks with our smart to-do board',
              },
              {
                step: 6,
                title: 'Execute Event',
                description: 'Use the dashboard as your command center on event day',
              },
            ].map((item, i) => (
              <motion.div
                key={i}
                variants={itemVariants}
                className="relative"
              >
                <div className="p-6 rounded-lg bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-center">
                  <div className="h-12 w-12 rounded-full bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center text-white font-bold text-lg mx-auto mb-4">
                    {item.step}
                  </div>
                  <h3 className="font-semibold mb-2">{item.title}</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    {item.description}
                  </p>
                </div>
                {i < 5 && (
                  <div className="hidden md:block absolute top-1/2 right-0 translate-x-1/2 -translate-y-1/2">
                    <ArrowRight className="h-6 w-6 text-slate-400" />
                  </div>
                )}
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold mb-4">Loved by Event Planners</h2>
            <p className="text-xl text-slate-600 dark:text-slate-400">
              Join thousands of professionals using FestSync
            </p>
          </motion.div>

          <motion.div
            className="grid md:grid-cols-3 gap-8"
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            {testimonials.map((testimonial, i) => (
              <motion.div
                key={i}
                variants={itemVariants}
                className="p-8 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-indigo-500 dark:hover:border-indigo-500 transition-all"
              >
                <div className="flex gap-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, j) => (
                    <span key={j} className="text-yellow-400">
                      ⭐
                    </span>
                  ))}
                </div>
                <p className="text-slate-700 dark:text-slate-300 mb-6 leading-relaxed">
                  "{testimonial.text}"
                </p>
                <div className="flex items-center gap-3">
                  <img
                    src={testimonial.image}
                    alt={testimonial.name}
                    className="h-10 w-10 rounded-full object-cover"
                  />
                  <div>
                    <p className="font-semibold text-sm">{testimonial.name}</p>
                    <p className="text-xs text-slate-500">{testimonial.role}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <motion.section
        className="py-24 px-6 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
      >
        <div className="max-w-2xl mx-auto text-center text-white">
          <h2 className="text-4xl font-bold mb-6">
            Start Planning Your Perfect Event
          </h2>
          <p className="text-lg mb-8 text-indigo-100">
            Join 10,000+ event planners who save 15+ hours per event with FestSync.
          </p>
          <Link href="/signup">
            <Button size="lg" variant="secondary" className="gap-2 text-base h-12 px-8">
              Get Started Free <ArrowRight className="h-5 w-5" />
            </Button>
          </Link>
        </div>
      </motion.section>

      {/* Footer */}
      <footer className="bg-slate-900 dark:bg-slate-950 text-white py-12 px-6 border-t border-slate-800">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-bold mb-4">FestSync</h3>
              <p className="text-sm text-slate-400">
                AI-powered event planning for everyone
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4 text-sm">Product</h4>
              <ul className="space-y-2 text-sm text-slate-400">
                <li><a href="#" className="hover:text-white transition">Features</a></li>
                <li><a href="#" className="hover:text-white transition">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition">Security</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4 text-sm">Company</h4>
              <ul className="space-y-2 text-sm text-slate-400">
                <li><a href="#" className="hover:text-white transition">About</a></li>
                <li><a href="#" className="hover:text-white transition">Blog</a></li>
                <li><a href="#" className="hover:text-white transition">Contact</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4 text-sm">Legal</h4>
              <ul className="space-y-2 text-sm text-slate-400">
                <li><a href="#" className="hover:text-white transition">Privacy</a></li>
                <li><a href="#" className="hover:text-white transition">Terms</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-slate-800 pt-8 text-center text-slate-400 text-sm">
            <p>© 2024 FestSync. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
