'use client';

import { use, useState } from 'react';
import { Plus, Loader2, Sparkles, TrendingUp, TrendingDown, AlertTriangle } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Skeleton } from '@/components/ui/skeleton';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { useBudgetItems, useBudgetSummary, useCreateBudgetItem, useUpdateBudgetItem, useDeleteBudgetItem } from '@/hooks/use-budget';
import { useBudgetAdvice } from '@/hooks/use-ai';
import { formatCurrency } from '@/lib/utils';
import type { APIBudgetItem } from '@/lib/api-types';
import { toast } from 'sonner';

const HEALTH_CONFIG = {
  GOOD: { color: 'text-green-600', bg: 'bg-green-50 dark:bg-green-900/20', icon: TrendingUp, label: 'On track' },
  WARNING: { color: 'text-amber-600', bg: 'bg-amber-50 dark:bg-amber-900/20', icon: AlertTriangle, label: 'Warning' },
  OVER_BUDGET: { color: 'text-red-600', bg: 'bg-red-50 dark:bg-red-900/20', icon: TrendingDown, label: 'Over budget' },
};

function BudgetItemRow({ item, currency, onUpdate, onDelete }: {
  item: APIBudgetItem; currency: string;
  onUpdate: (id: string, actual: number) => void;
  onDelete: (id: string) => void;
}) {
  const pct = item.planned_amount > 0
    ? Math.min(Math.round((item.actual_amount / item.planned_amount) * 100), 100)
    : 0;
  const over = item.actual_amount > item.planned_amount;

  return (
    <div className="flex items-center gap-4 py-3 border-b last:border-0">
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <p className="font-medium truncate">{item.category}</p>
          {over && <Badge className="text-xs bg-red-100 text-red-700">Over</Badge>}
        </div>
        <Progress value={pct} className={`h-1.5 ${over ? '[&>div]:bg-red-500' : ''}`} />
      </div>
      <div className="text-right text-sm shrink-0">
        <p className="font-medium">{formatCurrency(item.actual_amount, currency)}</p>
        <p className="text-slate-400">/ {formatCurrency(item.planned_amount, currency)}</p>
      </div>
      <div className="flex gap-1 shrink-0">
        <Button size="sm" variant="ghost" className="h-7 px-2 text-xs"
          onClick={() => {
            const val = prompt('Update actual amount:', String(item.actual_amount));
            if (val !== null) onUpdate(item.id, Number(val));
          }}>
          Edit
        </Button>
        <Button size="sm" variant="ghost" className="h-7 px-2 text-xs text-red-500 hover:text-red-600"
          onClick={() => onDelete(item.id)}>
          Del
        </Button>
      </div>
    </div>
  );
}

export default function BudgetPage({ params }: { params: Promise<{ id: string }> }) {
  const { id: eventId } = use(params);
  const { data: summary, isLoading: loadingSummary } = useBudgetSummary(eventId);
  const { data: items, isLoading: loadingItems } = useBudgetItems(eventId);
  const createItem = useCreateBudgetItem(eventId);
  const updateItem = useUpdateBudgetItem(eventId);
  const deleteItem = useDeleteBudgetItem(eventId);
  const budgetAdvice = useBudgetAdvice(eventId);

  const [showAdd, setShowAdd] = useState(false);
  const [showAdvice, setShowAdvice] = useState(false);
  const [form, setForm] = useState({ category: '', planned_amount: '', actual_amount: '', notes: '' });

  const currency = summary?.currency ?? 'INR';
  const health = summary ? HEALTH_CONFIG[summary.budget_health_status] : null;
  const HealthIcon = health?.icon;

  const handleGetAdvice = async () => {
    const res = await budgetAdvice.mutateAsync();
    if (res) setShowAdvice(true);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <h1 className="text-3xl font-bold">Budget</h1>
        <div className="flex gap-2">
          <Button variant="outline" className="gap-2" disabled={budgetAdvice.isPending} onClick={handleGetAdvice}>
            {budgetAdvice.isPending
              ? <><Loader2 className="h-4 w-4 animate-spin" /> Analysing…</>
              : <><Sparkles className="h-4 w-4" /> AI Advice</>}
          </Button>
          <Button className="gap-2" onClick={() => setShowAdd(true)}>
            <Plus className="h-4 w-4" /> Add Item
          </Button>
        </div>
      </div>

      {/* Summary strip */}
      {loadingSummary ? (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-24 rounded-xl" />)}
        </div>
      ) : summary && (
        <>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { label: 'Total budget', value: formatCurrency(summary.total_budget, currency) },
              { label: 'Planned', value: formatCurrency(summary.total_planned, currency) },
              { label: 'Actual spend', value: formatCurrency(summary.total_actual, currency) },
              { label: 'Remaining', value: formatCurrency(summary.remaining_budget, currency) },
            ].map(({ label, value }) => (
              <Card key={label} className="p-4">
                <p className="text-xs text-slate-500 mb-1">{label}</p>
                <p className="text-xl font-bold">{value}</p>
              </Card>
            ))}
          </div>

          {health && (
            <Card className={`p-4 flex items-center gap-3 ${health.bg}`}>
              {HealthIcon && <HealthIcon className={`h-5 w-5 ${health.color}`} />}
              <div className="flex-1">
                <p className={`font-semibold ${health.color}`}>{health.label}</p>
                <Progress value={Math.min(summary.budget_percentage_used, 100)} className="h-1.5 mt-1.5" />
              </div>
              <p className={`text-lg font-bold ${health.color}`}>{summary.budget_percentage_used}%</p>
            </Card>
          )}

          {summary.over_budget_categories.length > 0 && (
            <Card className="p-4 border-red-200 dark:border-red-800">
              <p className="font-semibold text-red-600 mb-2">Over-budget categories</p>
              <div className="space-y-1">
                {summary.over_budget_categories.map((cat) => (
                  <div key={cat.category} className="flex justify-between text-sm">
                    <span>{cat.category}</span>
                    <span className="text-red-500 font-medium">+{formatCurrency(cat.overage, currency)}</span>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </>
      )}

      {/* Items list */}
      <Card className="p-5">
        <p className="font-semibold mb-3">Budget breakdown</p>
        {loadingItems ? (
          <div className="space-y-3">
            {Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-12" />)}
          </div>
        ) : items?.items.length === 0 ? (
          <p className="text-center text-slate-400 py-8">No budget items yet</p>
        ) : (
          items?.items.map((item) => (
            <BudgetItemRow key={item.id} item={item} currency={currency}
              onUpdate={(id, actual) => updateItem.mutate({ itemId: id, payload: { actual_amount: actual } })}
              onDelete={(id) => deleteItem.mutate(id)}
            />
          ))
        )}
      </Card>

      {/* Add dialog */}
      <Dialog open={showAdd} onOpenChange={setShowAdd}>
        <DialogContent>
          <DialogHeader><DialogTitle>Add Budget Item</DialogTitle></DialogHeader>
          <div className="space-y-4 py-2">
            <div className="space-y-1.5">
              <Label>Category</Label>
              <Input placeholder="e.g. Catering" value={form.category}
                onChange={(e) => setForm(p => ({ ...p, category: e.target.value }))} />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <Label>Planned amount</Label>
                <Input type="number" placeholder="0" value={form.planned_amount}
                  onChange={(e) => setForm(p => ({ ...p, planned_amount: e.target.value }))} />
              </div>
              <div className="space-y-1.5">
                <Label>Actual (optional)</Label>
                <Input type="number" placeholder="0" value={form.actual_amount}
                  onChange={(e) => setForm(p => ({ ...p, actual_amount: e.target.value }))} />
              </div>
            </div>
            <div className="space-y-1.5">
              <Label>Notes</Label>
              <Textarea placeholder="Optional notes" value={form.notes}
                onChange={(e) => setForm(p => ({ ...p, notes: e.target.value }))} />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowAdd(false)}>Cancel</Button>
            <Button
              disabled={!form.category || !form.planned_amount || createItem.isPending}
              onClick={async () => {
                await createItem.mutateAsync({
                  category: form.category,
                  planned_amount: Number(form.planned_amount),
                  actual_amount: form.actual_amount ? Number(form.actual_amount) : 0,
                  notes: form.notes || undefined,
                });
                setForm({ category: '', planned_amount: '', actual_amount: '', notes: '' });
                setShowAdd(false);
              }}
            >
              {createItem.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Add'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* AI advice dialog */}
      <Dialog open={showAdvice} onOpenChange={setShowAdvice}>
        <DialogContent className="max-w-lg">
          <DialogHeader><DialogTitle>AI Budget Advice</DialogTitle></DialogHeader>
          {budgetAdvice.data && (
            <div className="space-y-4 max-h-[60vh] overflow-y-auto pr-1">
              <div>
                <p className="font-semibold mb-2">Recommended allocation</p>
                <div className="space-y-1.5">
                  {budgetAdvice.data.result.budget_split.map((s) => (
                    <div key={s.category} className="flex justify-between text-sm border-b pb-1.5">
                      <span>{s.category}</span>
                      <span className="font-medium">{formatCurrency(s.recommended_amount, currency)}</span>
                    </div>
                  ))}
                </div>
              </div>
              {budgetAdvice.data.result.warnings.length > 0 && (
                <div>
                  <p className="font-semibold text-amber-600 mb-1.5">Warnings</p>
                  <ul className="space-y-1">
                    {budgetAdvice.data.result.warnings.map((w, i) => (
                      <li key={i} className="text-sm flex gap-2"><span>⚠️</span>{w}</li>
                    ))}
                  </ul>
                </div>
              )}
              {budgetAdvice.data.result.saving_tips.length > 0 && (
                <div>
                  <p className="font-semibold text-green-600 mb-1.5">Saving tips</p>
                  <ul className="space-y-1">
                    {budgetAdvice.data.result.saving_tips.map((t, i) => (
                      <li key={i} className="text-sm flex gap-2"><span>💡</span>{t}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
          <DialogFooter>
            <Button onClick={() => setShowAdvice(false)}>Close</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
