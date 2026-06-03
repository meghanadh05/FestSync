'use client';

import { useState } from 'react';
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';
import { Sparkles, Send, Zap, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface AIAssistantDrawerProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  eventId?: string;
}

const quickActions = [
  {
    icon: '📋',
    label: 'Generate Event Plan',
    description: 'Create a comprehensive plan for your event',
    action: 'generate_plan',
  },
  {
    icon: '✅',
    label: 'Generate Tasks',
    description: 'Auto-generate tasks based on your event',
    action: 'generate_tasks',
  },
  {
    icon: '💰',
    label: 'Suggest Budget',
    description: 'Get AI-powered budget allocation',
    action: 'suggest_budget',
  },
  {
    icon: '👥',
    label: 'Recommend Vendors',
    description: 'Find vendors that match your event',
    action: 'recommend_vendors',
  },
];

export function AIAssistantDrawer({
  open,
  onOpenChange,
  eventId,
}: AIAssistantDrawerProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'assistant',
      content: '👋 Hi! I\'m your AI event planning assistant. I can help you generate plans, suggest tasks, optimize your budget, and recommend vendors. What would you like help with today?',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleQuickAction = async (action: string) => {
    const actionLabels: Record<string, string> = {
      generate_plan: 'Please generate a comprehensive event plan',
      generate_tasks: 'Please generate tasks for my event',
      suggest_budget: 'Please suggest a budget breakdown',
      recommend_vendors: 'Please recommend vendors for my event',
    };

    const userMessage = actionLabels[action] || 'Help me with my event';
    addMessage(userMessage, 'user');

    // Simulate AI response
    setIsLoading(true);
    setTimeout(() => {
      const responses: Record<string, string> = {
        generate_plan:
          '📅 I\'ve generated a comprehensive event plan with:\n• Pre-event preparation timeline\n• Day-of execution checklist\n• Post-event follow-up tasks\n\nYou can view the full plan in your Event Details page. Would you like me to break it down further?',
        generate_tasks:
          '✅ I\'ve created 15 tasks organized by category:\n• 5 Venue-related tasks\n• 4 Catering tasks\n• 3 Decoration tasks\n• 2 Entertainment tasks\n• 1 Guest management task\n\nAll tasks have been added to your to-do board!',
        suggest_budget:
          '💰 Based on your event details, here\'s a suggested budget breakdown:\n• Venue: 30%\n• Catering: 35%\n• Decoration: 15%\n• Entertainment: 15%\n• Contingency: 5%\n\nWould you like me to adjust this allocation?',
        recommend_vendors:
          '👥 I found 12 vendors that match your event:\n• 3 Premium venues\n• 2 Catering services\n• 3 Photographers\n• 2 Decoration specialists\n• 2 DJ/Entertainment\n\nI\'ve saved the top matches to your event. Check them out in the Vendors section!',
      };

      addMessage(
        responses[action] ||
          'I\'m processing your request. Please check your event dashboard for updates!',
        'assistant'
      );
      setIsLoading(false);
    }, 1500);
  };

  const handleSendMessage = () => {
    if (!input.trim()) return;

    addMessage(input, 'user');
    setInput('');

    // Simulate AI response
    setIsLoading(true);
    setTimeout(() => {
      const responses = [
        'Great question! Let me analyze your event details and provide some recommendations.',
        'I\'ve reviewed your event plan. Would you like me to adjust anything?',
        'Based on your preferences, I think the premium catering option would work best.',
        'Let me check your calendar and suggest some vendor meeting times.',
        'I can help you optimize your timeline. Which area would you like to focus on?',
      ];

      const randomResponse =
        responses[Math.floor(Math.random() * responses.length)];
      addMessage(randomResponse, 'assistant');
      setIsLoading(false);
    }, 1500);
  };

  const addMessage = (content: string, type: 'user' | 'assistant') => {
    const newMessage: Message = {
      id: Date.now().toString(),
      type,
      content,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, newMessage]);
  };

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent side="right" className="w-full sm:w-[500px] flex flex-col p-0">
        <SheetHeader className="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center">
              <Sparkles className="h-5 w-5 text-white" />
            </div>
            <div>
              <SheetTitle>AI Event Assistant</SheetTitle>
              <SheetDescription>
                Get instant help with your event planning
              </SheetDescription>
            </div>
          </div>
        </SheetHeader>

        <ScrollArea className="flex-1 overflow-hidden">
          <div className="p-6 space-y-4 flex flex-col">
            {messages.length === 1 ? (
              // Initial state: show quick actions
              <motion.div
                className="space-y-3"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <p className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                  Quick Actions
                </p>
                {quickActions.map((action, i) => (
                  <motion.button
                    key={action.action}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.1 }}
                    onClick={() => handleQuickAction(action.action)}
                    className="w-full text-left p-4 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-indigo-500 dark:hover:border-indigo-500 hover:bg-slate-50 dark:hover:bg-slate-900 transition-all group"
                  >
                    <div className="flex items-start gap-3">
                      <span className="text-2xl">{action.icon}</span>
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-sm group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition">
                          {action.label}
                        </p>
                        <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
                          {action.description}
                        </p>
                      </div>
                      <Zap className="h-4 w-4 text-slate-400 group-hover:text-indigo-500 transition flex-shrink-0 mt-1" />
                    </div>
                  </motion.button>
                ))}
              </motion.div>
            ) : (
              // Chat messages
              <>
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`flex ${
                      message.type === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`max-w-xs px-4 py-2 rounded-lg ${
                        message.type === 'user'
                          ? 'bg-indigo-600 text-white'
                          : 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-50'
                      }`}
                    >
                      <p className="text-sm whitespace-pre-wrap">
                        {message.content}
                      </p>
                      <p
                        className={`text-xs mt-1 ${
                          message.type === 'user'
                            ? 'text-indigo-100'
                            : 'text-slate-500 dark:text-slate-400'
                        }`}
                      >
                        {message.timestamp.toLocaleTimeString([], {
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </p>
                    </div>
                  </motion.div>
                ))}

                {isLoading && (
                  <div className="flex gap-2">
                    <div className="h-2 w-2 rounded-full bg-slate-400 animate-bounce" />
                    <div className="h-2 w-2 rounded-full bg-slate-400 animate-bounce delay-100" />
                    <div className="h-2 w-2 rounded-full bg-slate-400 animate-bounce delay-200" />
                  </div>
                )}
              </>
            )}
          </div>
        </ScrollArea>

        {/* Input Area */}
        <div className="border-t border-slate-200 dark:border-slate-700 p-6 space-y-3">
          {messages.length > 1 && (
            <div className="flex gap-2 flex-wrap">
              <Badge variant="outline" className="text-xs">
                💡 Tip: Ask about budget, vendors, or timeline
              </Badge>
            </div>
          )}
          <div className="flex gap-2">
            <Input
              placeholder="Ask me anything..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') handleSendMessage();
              }}
              disabled={isLoading}
              className="text-sm"
            />
            <Button
              size="icon"
              onClick={handleSendMessage}
              disabled={isLoading || !input.trim()}
              className="flex-shrink-0"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
