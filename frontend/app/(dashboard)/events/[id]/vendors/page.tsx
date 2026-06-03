'use client';

import { use } from 'react';
import Link from 'next/link';
import { Star, MapPin, DollarSign, BadgeCheck, Trash2, ExternalLink } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { useSavedVendors, useUnsaveVendor } from '@/hooks/use-vendors';
import { formatCurrency } from '@/lib/utils';

export default function EventVendorsPage({ params }: { params: Promise<{ id: string }> }) {
  const { id: eventId } = use(params);
  const { data, isLoading } = useSavedVendors(eventId);
  const unsave = useUnsaveVendor(eventId);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Saved Vendors</h1>
        <Link href="/vendors">
          <Button variant="outline">Browse marketplace</Button>
        </Link>
      </div>

      {isLoading ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => <Skeleton key={i} className="h-40 rounded-xl" />)}
        </div>
      ) : data?.items.length === 0 ? (
        <Card className="p-12 text-center">
          <p className="text-4xl mb-4">🛍️</p>
          <p className="font-semibold text-lg">No vendors saved yet</p>
          <p className="text-slate-500 text-sm mt-1">Browse vendors and save the ones you like</p>
          <Link href="/vendors" className="mt-4 inline-block">
            <Button className="mt-4">Browse vendors</Button>
          </Link>
        </Card>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {data?.items.map(({ id, vendor, notes, vendor_id }) => (
            <Card key={id} className="p-4 space-y-3">
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-1.5 mb-1">
                    <p className="font-semibold truncate">{vendor.business_name}</p>
                    {vendor.verified && (
                      <BadgeCheck className="h-4 w-4 text-indigo-500 shrink-0" />
                    )}
                  </div>
                  <Badge variant="outline" className="text-xs">{vendor.category}</Badge>
                </div>
                <div className="flex items-center gap-1 text-sm text-amber-500 shrink-0">
                  <Star className="h-3.5 w-3.5 fill-current" />
                  {vendor.rating.toFixed(1)}
                </div>
              </div>

              <div className="space-y-1 text-sm text-slate-500">
                {vendor.city && (
                  <div className="flex items-center gap-1.5">
                    <MapPin className="h-3.5 w-3.5 shrink-0" />{vendor.city}
                  </div>
                )}
                {vendor.starting_price != null && (
                  <div className="flex items-center gap-1.5">
                    <DollarSign className="h-3.5 w-3.5 shrink-0" />
                    from {formatCurrency(vendor.starting_price, vendor.currency)}
                  </div>
                )}
              </div>

              {notes && (
                <p className="text-xs text-slate-400 italic line-clamp-2">{notes}</p>
              )}

              <div className="flex gap-2 pt-1">
                <Link href={`/vendors/${vendor_id}`} className="flex-1">
                  <Button size="sm" variant="outline" className="w-full gap-1.5 text-xs">
                    <ExternalLink className="h-3 w-3" /> View
                  </Button>
                </Link>
                <Button size="sm" variant="ghost"
                  className="text-red-500 hover:text-red-600 hover:bg-red-50 px-2"
                  onClick={() => unsave.mutate(String(vendor_id))}
                  disabled={unsave.isPending}>
                  <Trash2 className="h-3.5 w-3.5" />
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
