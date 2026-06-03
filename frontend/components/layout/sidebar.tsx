'use client';

import { useUIStore } from '@/store/ui-store';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard,
  Calendar,
  Users,
  BarChart3,
  Settings,
  ChevronRight,
} from 'lucide-react';
import Link from 'next/link';
import { motion } from 'framer-motion';

const navItems = [
  { label: 'Dashboard', icon: LayoutDashboard, href: '/dashboard' },
  { label: 'Events', icon: Calendar, href: '/events' },
  { label: 'Vendors', icon: Users, href: '/vendors' },
  { label: 'Budget', icon: BarChart3, href: '/budget' },
  { label: 'Settings', icon: Settings, href: '/settings' },
];

export function Sidebar() {
  const sidebarOpen = useUIStore((state) => state.sidebarOpen);
  const toggleSidebar = useUIStore((state) => state.toggleSidebar);

  return (
    <motion.aside
      initial={{ width: sidebarOpen ? 280 : 80 }}
      animate={{ width: sidebarOpen ? 280 : 80 }}
      transition={{ duration: 0.3 }}
      className="fixed left-0 top-16 h-[calc(100vh-4rem)] border-r border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-950 z-30"
    >
      <div className="flex flex-col h-full">
        {/* Sidebar Header */}
        <div className="p-4 flex items-center justify-between">
          {sidebarOpen && <h2 className="font-bold text-lg">FestSync</h2>}
          <button
            onClick={toggleSidebar}
            className="p-1 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-md transition-colors"
          >
            <ChevronRight
              className={cn(
                'h-5 w-5 transition-transform',
                !sidebarOpen && 'rotate-180'
              )}
            />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-2 py-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <Link key={item.href} href={item.href}>
                <motion.div
                  whileHover={{ x: 4 }}
                  className={cn(
                    'flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors hover:bg-slate-100 dark:hover:bg-slate-800',
                    'text-slate-700 dark:text-slate-300'
                  )}
                >
                  <Icon className="h-5 w-5 flex-shrink-0" />
                  {sidebarOpen && <span>{item.label}</span>}
                </motion.div>
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-slate-200 dark:border-slate-700">
          {sidebarOpen && (
            <p className="text-xs text-slate-500 dark:text-slate-400">
              © 2024 FestSync
            </p>
          )}
        </div>
      </div>
    </motion.aside>
  );
}
