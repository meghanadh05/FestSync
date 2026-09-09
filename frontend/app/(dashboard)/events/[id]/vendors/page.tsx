'use client';

import { use, useMemo, useState } from 'react';
import { BadgeCheck, Heart, MapPin, Search, Star, Trash2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import { useSaveVendor, useSavedVendors, useUnsaveVendor, useVendorSearch } from '@/hooks/use-vendors';
import { formatCurrency } from '@/lib/utils';

export default function EventVendorsPage({ params }: { params: Promise<{ id: string }> }) {
  const { id: eventId } = use(params);
  const [search, setSearch] = useState('');
  const { data: saved, isLoading: savedLoading } = useSavedVendors(eventId);
  const { data: market, isLoading: marketLoading } = useVendorSearch({ limit: 24 });
  const saveVendor = useSaveVendor(eventId);
  const unsaveVendor = useUnsaveVendor(eventId);

  const savedIds = useMemo(
    () => new Set((saved?.items ?? []).map((item) => String(item.vendor_id))),
    [saved?.items]
  );
  const vendors = (market?.items ?? []).filter((vendor) => {
    const term = search.toLowerCase();
    return !term || vendor.business_name.toLowerCase().includes(term) || vendor.location.toLowerCase().includes(term);
  });

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Vendors</h1>
        <p className="mt-1 text-sm text-slate-500">Save vendors to this event and keep the shortlist current.</p>
      </div>

      <div className="grid gap-5 lg:grid-cols-[360px_1fr]">
        <Card className="rounded-lg border-slate-200 bg-white shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
          <CardHeader>
            <CardTitle className="text-base">Saved Shortlist</CardTitle>
          </CardHeader>
          <CardContent>
            {savedLoading ? (
              <div className="space-y-3">
                {Array.from({ length: 4 }).map((_, index) => <Skeleton key={index} className="h-20 rounded-md" />)}
              </div>
            ) : saved?.items.length === 0 ? (
              <div className="rounded-lg border border-dashed border-slate-300 p-6 text-center dark:border-neutral-800">
                <p className="text-sm font-medium">No vendors saved</p>
                <p className="mt-1 text-sm text-slate-500">Use the marketplace list to build a shortlist.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {saved?.items.map(({ id, vendor, vendor_id }) => (
                  <div key={id} className="rounded-lg border border-slate-200 p-3 dark:border-neutral-800">
                    <div className="flex items-start justify-between gap-2">
                      <div className="min-w-0">
                        <p className="truncate text-sm font-medium">{vendor.business_name}</p>
                        <p className="mt-1 text-xs text-slate-500">{vendor.category.replace(/_/g, ' ')}</p>
                      </div>
                      <Button
                        size="icon"
                        variant="ghost"
                        className="h-8 w-8 text-red-600 hover:text-red-700"
                        onClick={() => unsaveVendor.mutate(String(vendor_id))}
                        disabled={unsaveVendor.isPending}
                        aria-label="Remove vendor"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="rounded-lg border-slate-200 bg-white shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
          <CardHeader className="gap-3 sm:flex-row sm:items-center sm:justify-between">
            <CardTitle className="text-base">Marketplace</CardTitle>
            <div className="relative w-full sm:w-80">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
              <Input
                className="pl-9"
                placeholder="Search vendors"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />
            </div>
          </CardHeader>
          <CardContent>
            {marketLoading ? (
              <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
                {Array.from({ length: 6 }).map((_, index) => <Skeleton key={index} className="h-40 rounded-md" />)}
              </div>
            ) : vendors.length === 0 ? (
              <div className="rounded-lg border border-dashed border-slate-300 p-8 text-center dark:border-neutral-800">
                <p className="text-sm font-medium">No vendors match this search</p>
              </div>
            ) : (
              <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
                {vendors.map((vendor) => {
                  const isSaved = savedIds.has(vendor.id);
                  return (
                    <div key={vendor.id} className="rounded-lg border border-slate-200 p-4 dark:border-neutral-800">
                      <div className="flex items-start justify-between gap-3">
                        <div className="min-w-0">
                          <div className="flex items-center gap-1.5">
                            <p className="truncate text-sm font-medium">{vendor.business_name}</p>
                            {vendor.verified ? <BadgeCheck className="h-4 w-4 shrink-0 text-emerald-600" /> : null}
                          </div>
                          <Badge variant="outline" className="mt-2 text-xs">{vendor.category.replace(/_/g, ' ')}</Badge>
                        </div>
                        <div className="flex items-center gap-1 text-sm text-amber-600">
                          <Star className="h-4 w-4 fill-current" />
                          {vendor.rating.toFixed(1)}
                        </div>
                      </div>
                      <div className="mt-3 space-y-1 text-sm text-slate-500">
                        <p className="flex items-center gap-1.5">
                          <MapPin className="h-4 w-4" />
                          {vendor.city ?? vendor.location}
                        </p>
                        <p>{vendor.starting_price ? `From ${formatCurrency(vendor.starting_price, vendor.currency, 'en-IN')}` : 'Pricing on request'}</p>
                      </div>
                      <Button
                        className="mt-4 w-full gap-2"
                        variant={isSaved ? 'secondary' : 'outline'}
                        onClick={() => saveVendor.mutate({ vendorId: vendor.id })}
                        disabled={isSaved || saveVendor.isPending}
                      >
                        <Heart className="h-4 w-4" />
                        {isSaved ? 'Saved' : 'Save to event'}
                      </Button>
                    </div>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
