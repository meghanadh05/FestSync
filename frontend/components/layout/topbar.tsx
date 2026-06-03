'use client';

import { useUIStore } from '@/store/ui-store';
import { mockCurrentUser } from '@/lib/mock-data';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Moon, Sun, Search, Bell } from 'lucide-react';
import { motion } from 'framer-motion';

export function Topbar() {
  const theme = useUIStore((state) => state.theme);
  const setTheme = useUIStore((state) => state.setTheme);

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  const userInitials = mockCurrentUser.full_name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase();

  return (
    <header className="fixed top-0 right-0 left-0 h-16 border-b border-slate-200 bg-white dark:border-slate-700 dark:bg-slate-950 z-40">
      <div className="flex items-center justify-between h-full px-6 gap-4">
        {/* Logo area (for symmetry) */}
        <div className="w-80" />

        {/* Search bar (center) */}
        <div className="flex-1 max-w-md">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
            <Input
              type="text"
              placeholder="Search events, vendors..."
              className="pl-10 bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700"
            />
          </div>
        </div>

        {/* Right side actions */}
        <div className="flex items-center gap-4">
          {/* Notifications */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors relative"
          >
            <Bell className="h-5 w-5 text-slate-700 dark:text-slate-300" />
            <span className="absolute top-1 right-1 h-2 w-2 bg-red-500 rounded-full" />
          </motion.button>

          {/* Theme toggle */}
          <motion.button
            whileHover={{ scale: 1.05 }}
            onClick={toggleTheme}
            className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors"
          >
            {theme === 'dark' ? (
              <Sun className="h-5 w-5 text-slate-700 dark:text-slate-300" />
            ) : (
              <Moon className="h-5 w-5 text-slate-700 dark:text-slate-300" />
            )}
          </motion.button>

          {/* User menu */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="relative h-10 w-10 rounded-full p-0">
                <Avatar className="h-10 w-10">
                  <AvatarImage
                    src={mockCurrentUser.avatar_url}
                    alt={mockCurrentUser.full_name}
                  />
                  <AvatarFallback>{userInitials}</AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuLabel className="flex flex-col space-y-1">
                <p className="text-sm font-medium">{mockCurrentUser.full_name}</p>
                <p className="text-xs text-slate-500">{mockCurrentUser.email}</p>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Profile</DropdownMenuItem>
              <DropdownMenuItem>Settings</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem className="text-red-600 dark:text-red-400">
                Logout
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
}
