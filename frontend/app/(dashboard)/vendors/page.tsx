'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Star, MapPin, DollarSign, Search, BadgeCheck } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useVendorSearch } from '@/hooks/use-vendors';
import { formatCurrency } from '@/lib/utils';
import type { APIVendorCard } from '@/lib/api-types';

const CATEGORIES = [
  'CATERING','VENUE','PHOTOGRAPHY','VIDEOGRAPHY','DECORATION',
  'MUSIC','DJ','FLORIST','BAKERY','TRANSPORT','MAKEUP','LIGHTING','EVENT_PLANNER',
];
const ALL_CATEGORIES = 'ALL_CATEGORIES';
const ANY_RATING = 'ANY_RATING';

function VendorCardSkeleton() {
  return (
    <Card className="p-5 space-y-3">
      <Skeleton className="h-5 w-3/4" />
      <Skeleton className="h-4 w-1/2" />
      <div className="flex gap-2"><Skeleton className="h-4 w-20" /><Skeleton className="h-4 w-20" /></div>
    </Card>
  );
}

function VendorCard({ vendor }: {
  vendor: APIVendorCard;
}) {
  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
      <Card className="p-5 space-y-3 hover:shadow-lg transition-shadow">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-1.5 mb-1">
              <p className="font-semibold truncate">{vendor.business_name}</p>
              {vendor.verified && <BadgeCheck className="h-4 w-4 text-indigo-500 shrink-0" />}
            </div>
            <Badge variant="outline" className="text-xs">{vendor.category.replace('_', ' ')}</Badge>
          </div>
          <div className="flex items-center gap-1 text-sm text-amber-500 shrink-0">
            <Star className="h-3.5 w-3.5 fill-current" />{vendor.rating.toFixed(1)}
            <span className="text-slate-400 text-xs">({vendor.review_count})</span>
          </div>
        </div>

        {vendor.match_score > 0 && (
          <div className="flex items-center gap-2">
            <div className="h-1.5 flex-1 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
              <div className="h-full bg-indigo-500 rounded-full"
                style={{ width: `${vendor.match_score}%` }} />
            </div>
            <span className="text-xs text-indigo-600 font-medium shrink-0">{vendor.match_score}% match</span>
          </div>
        )}
        {vendor.match_reason && (
          <p className="text-xs text-slate-400">{vendor.match_reason}</p>
        )}

        <div className="space-y-1 text-sm text-slate-500">
          {vendor.city && <div className="flex items-center gap-1.5"><MapPin className="h-3.5 w-3.5" />{vendor.city}</div>}
          {vendor.starting_price != null && (
            <div className="flex items-center gap-1.5">
              <DollarSign className="h-3.5 w-3.5" />from {formatCurrency(vendor.starting_price, vendor.currency)}
            </div>
          )}
        </div>

        <div className="border-t border-slate-100 pt-3 text-xs text-slate-500 dark:border-neutral-900">
          Save vendors from an event workspace.
        </div>
      </Card>
    </motion.div>
  );
}

export default function VendorsPage() {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState<string>('');
  const [minRating, setMinRating] = useState<string>('');
  const [verifiedOnly, setVerifiedOnly] = useState(false);

  const { data, isLoading, isFetching } = useVendorSearch({
    category: category || undefined,
    min_rating: minRating ? Number(minRating) : undefined,
    verified_only: verifiedOnly || undefined,
    limit: 24,
  });

  const filteredItems = search
    ? (data?.items ?? []).filter(v =>
        v.business_name.toLowerCase().includes(search.toLowerCase()) ||
        (v.city ?? '').toLowerCase().includes(search.toLowerCase()))
    : (data?.items ?? []);

  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold">Vendor Marketplace</h1>
          <p className="text-slate-500 mt-1">
            {data ? `${data.total} vendors available` : 'Find the perfect vendors for your event'}
          </p>
        </div>
      </motion.div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <div className="relative flex-1 min-w-48">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
          <Input placeholder="Search vendors…" className="pl-9"
            value={search} onChange={(e) => setSearch(e.target.value)} />
        </div>
        <Select
          value={category || ALL_CATEGORIES}
          onValueChange={(value) => setCategory(value === ALL_CATEGORIES ? '' : value)}
        >
          <SelectTrigger className="w-44"><SelectValue placeholder="All categories" /></SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL_CATEGORIES}>All categories</SelectItem>
            {CATEGORIES.map(c => <SelectItem key={c} value={c}>{c.replace('_', ' ')}</SelectItem>)}
          </SelectContent>
        </Select>
        <Select
          value={minRating || ANY_RATING}
          onValueChange={(value) => setMinRating(value === ANY_RATING ? '' : value)}
        >
          <SelectTrigger className="w-36"><SelectValue placeholder="Any rating" /></SelectTrigger>
          <SelectContent>
            <SelectItem value={ANY_RATING}>Any rating</SelectItem>
            {['4', '4.5', '3'].map(r => <SelectItem key={r} value={r}>{r}+ stars</SelectItem>)}
          </SelectContent>
        </Select>
        <Button variant={verifiedOnly ? 'default' : 'outline'}
          className="gap-2" onClick={() => setVerifiedOnly(!verifiedOnly)}>
          <BadgeCheck className="h-4 w-4" /> Verified only
        </Button>
      </div>

      {isLoading || (isFetching && !data) ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {Array.from({ length: 12 }).map((_, i) => <VendorCardSkeleton key={i} />)}
        </div>
      ) : filteredItems.length === 0 ? (
        <Card className="p-12 text-center">
          <p className="text-4xl mb-3">🔍</p>
          <p className="font-semibold">No vendors found</p>
          <p className="text-slate-500 text-sm mt-1">Try adjusting your filters</p>
        </Card>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {filteredItems.map(vendor => (
            <VendorCard key={vendor.id} vendor={vendor} />
          ))}
        </div>
      )}
    </div>
  );
}
