'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { mockVendors } from '@/lib/mock-data';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';
import {
  MapPin,
  DollarSign,
  Star,
  Filter,
  Search,
  Plus,
  Heart,
  Scale,
} from 'lucide-react';
import { formatCurrency, getVendorTypeIcon } from '@/lib/utils';
import Link from 'next/link';

const vendorCategories = [
  'catering',
  'venue',
  'photography',
  'decoration',
  'music',
  'event_planner',
];

export default function VendorsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [priceRange, setPriceRange] = useState<'all' | 'budget' | 'mid' | 'premium'>('all');
  const [minRating, setMinRating] = useState(0);
  const [savedVendors, setSavedVendors] = useState<Set<string>>(new Set());

  const filteredVendors = mockVendors.filter((vendor) => {
    let matches = true;

    if (searchTerm) {
      matches =
        matches &&
        (vendor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          vendor.description?.toLowerCase().includes(searchTerm.toLowerCase()));
    }

    if (selectedCategory) {
      matches = matches && vendor.vendor_type === selectedCategory;
    }

    if (priceRange !== 'all') {
      matches =
        matches &&
        (priceRange === 'budget'
          ? vendor.price_range === 'budget'
          : priceRange === 'mid'
          ? vendor.price_range === 'mid-range'
          : vendor.price_range === 'premium');
    }

    if (minRating > 0) {
      matches = matches && vendor.rating >= minRating;
    }

    return matches;
  });

  const toggleSaveVendor = (vendorId: string) => {
    const newSaved = new Set(savedVendors);
    if (newSaved.has(vendorId)) {
      newSaved.delete(vendorId);
    } else {
      newSaved.add(vendorId);
    }
    setSavedVendors(newSaved);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-4xl font-bold">Vendor Marketplace</h1>
        <p className="text-slate-600 dark:text-slate-400 mt-2">
          Discover and compare vendors for your event
        </p>
      </motion.div>

      {/* Search & Filters */}
      <motion.div
        className="space-y-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
      >
        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" />
          <Input
            placeholder="Search vendors by name, service..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>

        {/* Filter Buttons */}
        <div className="flex flex-wrap gap-2">
          {/* Category Filter */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm" className="gap-2">
                <Filter className="h-4 w-4" />
                Category
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuLabel>Vendor Type</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => setSelectedCategory(null)}>
                All Categories
              </DropdownMenuItem>
              {vendorCategories.map((cat) => (
                <DropdownMenuItem
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  className={selectedCategory === cat ? 'bg-slate-100 dark:bg-slate-800' : ''}
                >
                  {cat}
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Price Range Filter */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm" className="gap-2">
                <DollarSign className="h-4 w-4" />
                Price
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuLabel>Price Range</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => setPriceRange('all')}
                className={priceRange === 'all' ? 'bg-slate-100 dark:bg-slate-800' : ''}
              >
                All Prices
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => setPriceRange('budget')}
                className={priceRange === 'budget' ? 'bg-slate-100 dark:bg-slate-800' : ''}
              >
                Budget Friendly
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => setPriceRange('mid')}
                className={priceRange === 'mid' ? 'bg-slate-100 dark:bg-slate-800' : ''}
              >
                Mid-Range
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => setPriceRange('premium')}
                className={priceRange === 'premium' ? 'bg-slate-100 dark:bg-slate-800' : ''}
              >
                Premium
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Rating Filter */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm" className="gap-2">
                <Star className="h-4 w-4" />
                Rating
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuLabel>Minimum Rating</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => setMinRating(0)}
                className={minRating === 0 ? 'bg-slate-100 dark:bg-slate-800' : ''}
              >
                All Ratings
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => setMinRating(3)}
                className={minRating === 3 ? 'bg-slate-100 dark:bg-slate-800' : ''}
              >
                3+ Stars
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => setMinRating(4)}
                className={minRating === 4 ? 'bg-slate-100 dark:bg-slate-800' : ''}
              >
                4+ Stars
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => setMinRating(4.5)}
                className={minRating === 4.5 ? 'bg-slate-100 dark:bg-slate-800' : ''}
              >
                4.5+ Stars
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Results Count */}
          <div className="flex-1" />
          <p className="text-sm text-slate-600 dark:text-slate-400 py-2">
            Showing {filteredVendors.length} vendors
          </p>
        </div>
      </motion.div>

      {/* Vendor Grid */}
      {filteredVendors.length === 0 ? (
        <motion.div
          className="text-center py-20"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <p className="text-slate-600 dark:text-slate-400 mb-4">
            No vendors match your filters
          </p>
          <Button
            variant="outline"
            onClick={() => {
              setSelectedCategory(null);
              setPriceRange('all');
              setMinRating(0);
              setSearchTerm('');
            }}
          >
            Clear Filters
          </Button>
        </motion.div>
      ) : (
        <motion.div
          className="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
          variants={{ hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.05 } } }}
          initial="hidden"
          animate="visible"
        >
          {filteredVendors.map((vendor, i) => (
            <motion.div
              key={vendor.id}
              variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
            >
              <Card className="overflow-hidden hover:shadow-lg transition-shadow h-full flex flex-col">
                {/* Header with Image */}
                <div className="h-40 bg-gradient-to-br from-slate-200 to-slate-300 dark:from-slate-700 dark:to-slate-800 relative">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-6xl opacity-50">
                      {getVendorTypeIcon(vendor.vendor_type)}
                    </span>
                  </div>
                  <button
                    onClick={() => toggleSaveVendor(vendor.id)}
                    className="absolute top-3 right-3 p-2 rounded-full bg-white dark:bg-slate-900 shadow-md hover:scale-110 transition-transform"
                  >
                    <Heart
                      className={`h-5 w-5 ${
                        savedVendors.has(vendor.id)
                          ? 'fill-red-500 text-red-500'
                          : 'text-slate-400'
                      }`}
                    />
                  </button>
                </div>

                {/* Content */}
                <div className="p-6 flex-1 flex flex-col">
                  <div className="mb-3">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-bold text-lg">{vendor.name}</h3>
                      {vendor.is_verified && (
                        <Badge className="bg-green-600/20 text-green-700 dark:text-green-400 text-xs">
                          ✓ Verified
                        </Badge>
                      )}
                    </div>
                    <Badge variant="outline" className="text-xs capitalize">
                      {vendor.vendor_type}
                    </Badge>
                  </div>

                  {/* Rating */}
                  <div className="flex items-center gap-2 mb-4">
                    <div className="flex">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`h-4 w-4 ${
                            i < Math.floor(vendor.rating)
                              ? 'fill-yellow-400 text-yellow-400'
                              : 'text-slate-300 dark:text-slate-600'
                          }`}
                        />
                      ))}
                    </div>
                    <span className="text-sm font-semibold">{vendor.rating}</span>
                    <span className="text-xs text-slate-500">({vendor.review_count})</span>
                  </div>

                  {/* Info */}
                  <div className="space-y-2 text-sm mb-4 flex-1">
                    {vendor.city && (
                      <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                        <MapPin className="h-4 w-4" />
                        {vendor.city}
                      </div>
                    )}
                    {vendor.min_price && (
                      <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                        <DollarSign className="h-4 w-4" />
                        {formatCurrency(vendor.min_price)} - {formatCurrency(vendor.max_price || 0)}
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2 pt-4 border-t border-slate-200 dark:border-slate-700">
                    <Link href={`/vendors/${vendor.id}`} className="flex-1">
                      <Button variant="outline" size="sm" className="w-full">
                        View Details
                      </Button>
                    </Link>
                    <Button variant="outline" size="sm" className="gap-2">
                      <Scale className="h-4 w-4" />
                      Compare
                    </Button>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </motion.div>
      )}
    </div>
  );
}
