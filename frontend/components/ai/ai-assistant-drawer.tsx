'use client';

import { useState, useRef, useEffect } from 'react';
import { Sheet, SheetContent, SheetHeader, SheetTitle } from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Sparkles, Send, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAIChat } from '@/hooks/use-ai';
import { toast } from 'sonner';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  suggestions?: string[];
}

interface AIAssistantDrawerProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  eventId?: string;
}

const QUICK_ACTIONS = [
  { label: 'Generate Plan', prompt: 'Generate a comprehensive plan for my event', icon: '📋' },
  { label: 'Generate Tasks', prompt: 'What tasks should I create first for this event?', icon: '✅' },
  { label: 'Budget Advice', prompt: 'How should I split my budget across categories?', icon: '💰' },
  { label: 'Vendor Tips', prompt: 'Which type of vendors should I book first?', icon: '🏪' },
];

export function AIAssistantDrawer({ open, onOpenChange, eventId }: AIAssistantDrawerProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '0',
      role: 'assistant',
      content: "👋 Hi! I'm your FestSync AI assistant. Ask me anything about planning your event!",
      suggestions: ['What tasks should I start with?', 'How to split my budget?'],
    },
  ]);
  const [input, setInput] = useState('');
  const bottomRef = useRef<HTMLDivElement>(null);
  const chat = useAIChat();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text: string) => {
    if (!text.trim() || chat.isPending) return;
    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    try {
      const history = messages.slice(-6).map(m => ({ role: m.role, content: m.content }));
      const res = await chat.mutateAsync({ message: text, eventId, history });
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: res.result.message,
        suggestions: res.result.suggestions,
      }]);
    } catch {
      toast.error('AI failed to respond. Please try again.');
    }
  };

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent side="right" className="w-full sm:max-w-md flex flex-col p-0">
        <SheetHeader className="p-4 border-b shrink-0">
          <SheetTitle className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-indigo-600">
              <Sparkles className="h-4 w-4 text-white" />
            </div>
            FestSync AI
          </SheetTitle>
        </SheetHeader>

        <ScrollArea className="flex-1 px-4 py-3">
          <div className="space-y-4">
            <AnimatePresence initial={false}>
              {messages.map(msg => (
                <motion.div key={msg.id}
                  initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed
                    ${msg.role === 'user'
                      ? 'bg-indigo-600 text-white rounded-br-sm'
                      : 'bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 rounded-bl-sm'}`}>
                    {msg.content}
                    {msg.suggestions && msg.suggestions.length > 0 && (
                      <div className="mt-3 space-y-1.5">
                        {msg.suggestions.map((s, i) => (
                          <button key={i} onClick={() => sendMessage(s)}
                            className="block w-full text-left text-xs text-indigo-600 dark:text-indigo-400
                              bg-indigo-50 dark:bg-indigo-900/30 rounded-lg px-3 py-1.5
                              hover:bg-indigo-100 dark:hover:bg-indigo-900/50 transition-colors">
                            {s}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>

            {chat.isPending && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
                <div className="bg-slate-100 dark:bg-slate-800 rounded-2xl rounded-bl-sm px-4 py-3">
                  <div className="flex gap-1.5 items-center h-4">
                    {[0, 1, 2].map(i => (
                      <motion.div key={i}
                        animate={{ y: [0, -4, 0] }}
                        transition={{ duration: 0.6, repeat: Infinity, delay: i * 0.15 }}
                        className="w-1.5 h-1.5 bg-slate-400 rounded-full" />
                    ))}
                  </div>
                </div>
              </motion.div>
            )}
            <div ref={bottomRef} />
          </div>
        </ScrollArea>

        <div className="px-4 py-3 border-t bg-slate-50 dark:bg-slate-900/50 shrink-0">
          <div className="grid grid-cols-2 gap-2 mb-3">
            {QUICK_ACTIONS.map(action => (
              <button key={action.label} onClick={() => sendMessage(action.prompt)}
                disabled={chat.isPending}
                className="text-left text-xs p-2.5 rounded-xl border bg-white dark:bg-slate-800
                  hover:border-indigo-300 dark:hover:border-indigo-700 transition-colors disabled:opacity-50">
                <span className="block text-base mb-0.5">{action.icon}</span>
                {action.label}
              </button>
            ))}
          </div>
          <div className="flex gap-2">
            <Input placeholder="Ask anything about your event…" value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && !e.shiftKey && sendMessage(input)}
              disabled={chat.isPending} className="flex-1 text-sm" />
            <Button size="icon" onClick={() => sendMessage(input)}
              disabled={!input.trim() || chat.isPending}>
              {chat.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
            </Button>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
