'use client';

import { useUIStore } from '@/store/ui-store';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard,
  Calendar,
  Users,
  ChevronRight,
  Sparkles,
} from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';

const navItems = [
  { label: 'Dashboard', icon: LayoutDashboard, href: '/dashboard' },
  { label: 'Events', icon: Calendar, href: '/events' },
  { label: 'Vendors', icon: Users, href: '/vendors' },
];

export function Sidebar() {
  const sidebarOpen = useUIStore((state) => state.sidebarOpen);
  const toggleSidebar = useUIStore((state) => state.toggleSidebar);
  const pathname = usePathname();

  return (
    <motion.aside
      initial={{ width: sidebarOpen ? 280 : 80 }}
      animate={{ width: sidebarOpen ? 280 : 80 }}
      transition={{ duration: 0.3 }}
      className="sticky top-0 hidden h-screen shrink-0 border-r border-slate-200 bg-white/95 shadow-sm dark:border-neutral-800 dark:bg-neutral-950/95 md:block"
    >
      <div className="flex flex-col h-full">
        <div className="flex h-14 items-center justify-between border-b border-slate-200 px-4 dark:border-neutral-800">
          <Link href="/dashboard" className="flex items-center gap-2 overflow-hidden">
            <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-slate-950 text-white dark:bg-white dark:text-slate-950">
              <Sparkles className="h-4 w-4" />
            </span>
            {sidebarOpen && <span className="truncate text-sm font-semibold">FestSync</span>}
          </Link>
          <button
            onClick={toggleSidebar}
            className="rounded-md p-1.5 text-slate-500 transition-colors hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-neutral-900 dark:hover:text-slate-100"
            aria-label={sidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
          >
            <ChevronRight
              className={cn(
                'h-5 w-5 transition-transform',
                sidebarOpen && 'rotate-180'
              )}
            />
          </button>
        </div>

        <nav className="flex-1 space-y-1 px-3 py-4">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <Link key={item.href} href={item.href}>
                <motion.div
                  whileHover={{ x: sidebarOpen ? 2 : 0 }}
                  className={cn(
                    'flex h-10 items-center gap-3 rounded-md px-3 text-sm font-medium transition-colors',
                    active
                      ? 'bg-slate-950 text-white dark:bg-white dark:text-slate-950'
                      : 'text-slate-600 hover:bg-slate-100 hover:text-slate-950 dark:text-slate-400 dark:hover:bg-neutral-900 dark:hover:text-slate-50',
                    !sidebarOpen && 'justify-center'
                  )}
                >
                  <Icon className="h-5 w-5 flex-shrink-0" />
                  {sidebarOpen && <span>{item.label}</span>}
                </motion.div>
              </Link>
            );
          })}
        </nav>

        <div className="border-t border-slate-200 p-4 dark:border-neutral-800">
          {sidebarOpen && (
            <p className="text-xs text-slate-500 dark:text-slate-400">Local workspace</p>
          )}
        </div>
      </div>
    </motion.aside>
  );
}
