-- FestSync Seed Data
-- Migration 003: Populate with sample vendors across all categories
-- Run this AFTER 001_initial_schema.sql and 002_rls_policies.sql
-- NOTE: This uses NULL for user_id as these are platform-created vendors, not vendor-owned

-- ============================================================================
-- CATERING VENDORS
-- ============================================================================

INSERT INTO vendors (
  name, description, vendor_type, location, city, state, country,
  phone_number, email, website_url, social_media,
  price_range, min_price, max_price, rating, review_count,
  response_time_hours, availability_status, certifications, is_verified
) VALUES
(
  'The Culinary Artisans',
  'Premium catering service specializing in multi-course tasting menus and custom cuisine. Award-winning chefs with 15+ years of experience. Offers vegetarian, vegan, and allergen-free options.',
  'catering',
  '456 Gourmet Lane, San Francisco, CA 94102',
  'San Francisco',
  'CA',
  'USA',
  '+1-415-555-0123',
  'info@culinaryartisans.com',
  'https://culinaryartisans.com',
  '{"instagram": "https://instagram.com/culinaryartisans", "facebook": "https://facebook.com/culinaryartisans"}',
  'premium',
  '5000',
  '25000',
  4.9,
  247,
  2,
  'available',
  ARRAY['Fine Dining Certificate', 'Food Safety Certification', 'Michelin-Trained'],
  true
),
(
  'Fresh & Fit Catering Co.',
  'Health-conscious catering with organic, locally-sourced ingredients. Specializes in modern cuisine with cultural fusion options. Perfect for corporate and wellness events.',
  'catering',
  '789 Organic Ave, Los Angeles, CA 90001',
  'Los Angeles',
  'CA',
  'USA',
  '+1-213-555-0456',
  'hello@freshnfitcatering.com',
  'https://freshnfitcatering.com',
  '{"instagram": "https://instagram.com/freshnfitcatering", "facebook": "https://facebook.com/freshnfitcatering"}',
  'mid-range',
  '2000',
  '12000',
  4.7,
  189,
  3,
  'available',
  ARRAY['Organic Certified', 'Sustainable Practices', 'Chef Trained'],
  true
),
(
  'Classic Cuisine Catering',
  'Traditional and contemporary catering for all event sizes. Experienced with weddings, corporate events, and celebrations. Customizable menu options.',
  'catering',
  '321 Event Street, New York, NY 10001',
  'New York',
  'NY',
  'USA',
  '+1-212-555-0789',
  'bookings@classiccuisine.com',
  'https://classiccuisine.com',
  '{"instagram": "https://instagram.com/classiccuisine", "facebook": "https://facebook.com/classiccuisine"}',
  'mid-range',
  '1500',
  '8000',
  4.6,
  156,
  4,
  'available',
  ARRAY['Professional Catering Certification'],
  true
),
(
  'Spice Route Catering',
  'Authentic Indian cuisine with modern fusion options. Specialized in wedding catering with traditional ceremonies. Dietary accommodations available.',
  'catering',
  '567 Spice St, Chicago, IL 60601',
  'Chicago',
  'IL',
  'USA',
  '+1-312-555-0012',
  'contact@spiceroute.com',
  'https://spiceroute.com',
  '{"instagram": "https://instagram.com/spiceroute", "facebook": "https://facebook.com/spiceroute"}',
  'budget',
  '1000',
  '5000',
  4.8,
  203,
  2,
  'available',
  ARRAY['Professional Cooking School', 'Hygiene Certified'],
  true
);

-- ============================================================================
-- VENUE VENDORS
-- ============================================================================

INSERT INTO vendors (
  name, description, vendor_type, location, city, state, country,
  phone_number, email, website_url, social_media,
  price_range, min_price, max_price, rating, review_count,
  response_time_hours, availability_status, certifications, is_verified
) VALUES
(
  'Grand Ballroom Palace',
  'Luxurious 15,000 sq ft ballroom with crystal chandeliers, elegant decor, and capacity for 500+ guests. Includes bridal suite and dedicated catering kitchen. Full event coordination available.',
  'venue',
  '1000 Luxury Lane, San Francisco, CA 94102',
  'San Francisco',
  'CA',
  'USA',
  '+1-415-555-1234',
  'events@grandballroom.com',
  'https://grandballroom.com',
  '{"instagram": "https://instagram.com/grandballroom", "facebook": "https://facebook.com/grandballroom"}',
  'premium',
  '8000',
  '50000',
  4.8,
  342,
  1,
  'available',
  ARRAY['ADA Compliant', 'Fire Safety Certified', 'Licensed Venue'],
  true
),
(
  'The Modern Loft Downtown',
  'Industrial-chic 8,000 sq ft loft with soaring ceilings, natural light, and flexible layout. Perfect for contemporary weddings, corporate events, and celebrations. Capacity 50-300 guests.',
  'venue',
  '2500 Industrial Blvd, Los Angeles, CA 90001',
  'Los Angeles',
  'CA',
  'USA',
  '+1-213-555-5678',
  'reservations@modernloft.com',
  'https://modernloft.com',
  '{"instagram": "https://instagram.com/modernloft", "facebook": "https://facebook.com/modernloft"}',
  'mid-range',
  '3000',
  '15000',
  4.7,
  267,
  2,
  'available',
  ARRAY['Event Liability Insurance', 'Licensed Venue'],
  true
),
(
  'Riverside Garden Estate',
  'Beautiful outdoor venue with riverside views, manicured gardens, and historic manor house. Ideal for garden weddings and outdoor celebrations. Capacity 100-400 guests.',
  'venue',
  '5000 Garden Path, Sonoma, CA 95476',
  'Sonoma',
  'CA',
  'USA',
  '+1-707-555-9101',
  'info@riversidegarden.com',
  'https://riversidegarden.com',
  '{"instagram": "https://instagram.com/riversidegarden", "facebook": "https://facebook.com/riversidegarden"}',
  'premium',
  '5000',
  '30000',
  4.9,
  189,
  3,
  'available',
  ARRAY['Outdoor Event License', 'Insurance Required'],
  true
),
(
  'Urban Event Studio',
  'Versatile 6,000 sq ft venue with multiple breakout rooms. Great for corporate events, seminars, and conferences. Full AV setup and internet included.',
  'venue',
  '123 Business Center, New York, NY 10001',
  'New York',
  'NY',
  'USA',
  '+1-212-555-2345',
  'bookings@urbaneventstudio.com',
  'https://urbaneventstudio.com',
  '{"instagram": "https://instagram.com/urbaneventstudio", "facebook": "https://facebook.com/urbaneventstudio"}',
  'mid-range',
  '2000',
  '10000',
  4.6,
  198,
  2,
  'available',
  ARRAY['ADA Compliant', 'Tech Equipment Certified'],
  true
);

-- ============================================================================
-- PHOTOGRAPHY VENDORS
-- ============================================================================

INSERT INTO vendors (
  name, description, vendor_type, location, city, state, country,
  phone_number, email, website_url, social_media,
  price_range, min_price, max_price, rating, review_count,
  response_time_hours, availability_status, certifications, is_verified
) VALUES
(
  'Memories in Motion Photography',
  'Professional wedding and event photography with artistic vision. Offers both traditional and candid styles. Includes pre-wedding session and 500+ edited images.',
  'photography',
  '789 Photo Lane, San Francisco, CA 94102',
  'San Francisco',
  'CA',
  'USA',
  '+1-415-555-3456',
  'hello@memoriesinmotion.com',
  'https://memoriesinmotion.com',
  '{"instagram": "https://instagram.com/memoriesinmotion", "facebook": "https://facebook.com/memoriesinmotion"}',
  'premium',
  '3000',
  '8000',
  4.9,
  456,
  1,
  'available',
  ARRAY['Professional Photographers Association', 'Certified Editor'],
  true
),
(
  'Capture the Moment Studios',
  'Full-service photography and videography for weddings and events. Quick turnaround on edits (2 weeks). Drone photography available.',
  'photography',
  '456 Studio Ave, Los Angeles, CA 90001',
  'Los Angeles',
  'CA',
  'USA',
  '+1-213-555-6789',
  'bookings@capturethemoment.com',
  'https://capturethemoment.com',
  '{"instagram": "https://instagram.com/capturethemoment", "facebook": "https://facebook.com/capturethemoment"}',
  'mid-range',
  '1500',
  '5000',
  4.7,
  321,
  2,
  'available',
  ARRAY['Professional Photographer', 'Drone Certified'],
  true
),
(
  'Timeless Moments Photography',
  'Intimate and documentary-style wedding photography. Available for elopements and small ceremonies. Includes digital copies and album design.',
  'photography',
  '999 Artisan Lane, Portland, OR 97201',
  'Portland',
  'OR',
  'USA',
  '+1-503-555-7890',
  'info@timelessmoments.com',
  'https://timelessmoments.com',
  '{"instagram": "https://instagram.com/timelessmoments", "facebook": "https://facebook.com/timelessmoments"}',
  'budget',
  '800',
  '3000',
  4.8,
  234,
  3,
  'available',
  ARRAY['Professional Photographer'],
  true
),
(
  'Event Lens Pro',
  'Corporate event and conference photography. Specializes in multi-camera coverage for large events. Rapid delivery of photos for social media.',
  'photography',
  '321 Corporate Blvd, New York, NY 10001',
  'New York',
  'NY',
  'USA',
  '+1-212-555-8901',
  'events@eventlenspro.com',
  'https://eventlenspro.com',
  '{"instagram": "https://instagram.com/eventlenspro", "facebook": "https://facebook.com/eventlenspro"}',
  'mid-range',
  '2000',
  '7000',
  4.6,
  178,
  2,
  'available',
  ARRAY['Professional Photographer', 'Corporate Events Specialist'],
  true
);

-- ============================================================================
-- DECORATION VENDORS
-- ============================================================================

INSERT INTO vendors (
  name, description, vendor_type, location, city, state, country,
  phone_number, email, website_url, social_media,
  price_range, min_price, max_price, rating, review_count,
  response_time_hours, availability_status, certifications, is_verified
) VALUES
(
  'Elegant Expressions Decor',
  'Premium event decoration with floral arrangements, lighting design, and custom installations. Specializes in wedding and gala events. Custom color schemes available.',
  'decoration',
  '555 Floral St, San Francisco, CA 94102',
  'San Francisco',
  'CA',
  'USA',
  '+1-415-555-4567',
  'design@elegantexpressions.com',
  'https://elegantexpressions.com',
  '{"instagram": "https://instagram.com/elegantexpressions", "facebook": "https://facebook.com/elegantexpressions"}',
  'premium',
  '2000',
  '15000',
  4.8,
  289,
  2,
  'available',
  ARRAY['Floral Designer Certified', 'Event Decorator'],
  true
),
(
  'Creative Canvas Events',
  'Contemporary and artistic event styling. Specializes in minimalist to elaborate designs. Expert in theme-based decorations and installations.',
  'decoration',
  '777 Art Ave, Los Angeles, CA 90001',
  'Los Angeles',
  'CA',
  'USA',
  '+1-213-555-0123',
  'hello@creativecanvas.com',
  'https://creativecanvas.com',
  '{"instagram": "https://instagram.com/creativecanvas", "facebook": "https://facebook.com/creativecanvas"}',
  'mid-range',
  '1000',
  '8000',
  4.7,
  201,
  3,
  'available',
  ARRAY['Event Stylist', 'Interior Decorator'],
  true
),
(
  'Balloons & Blossoms Decor',
  'Specialized in balloon arrangements, floral designs, and centerpieces. Budget-friendly with high-quality work. Great for all event types.',
  'decoration',
  '888 Celebration Ln, Chicago, IL 60601',
  'Chicago',
  'IL',
  'USA',
  '+1-312-555-2345',
  'info@balloonsandblossoms.com',
  'https://balloonsandblossoms.com',
  '{"instagram": "https://instagram.com/balloonsandblossoms", "facebook": "https://facebook.com/balloonsandblossoms"}',
  'budget',
  '300',
  '3000',
  4.6,
  156,
  4,
  'available',
  ARRAY['Balloon Technician', 'Florist'],
  true
),
(
  'Luminous Design Studio',
  'Expert in lighting design and special effects. Creates ambient and dramatic lighting for events. Includes LED displays and projection mapping.',
  'decoration',
  '444 Light Lane, New York, NY 10001',
  'New York',
  'NY',
  'USA',
  '+1-212-555-5678',
  'bookings@luminousdesign.com',
  'https://luminousdesign.com',
  '{"instagram": "https://instagram.com/luminousdesign", "facebook": "https://facebook.com/luminousdesign"}',
  'mid-range',
  '1500',
  '10000',
  4.8,
  167,
  2,
  'available',
  ARRAY['Lighting Designer', 'Technician Certified'],
  true
);

-- ============================================================================
-- MUSIC / DJ VENDORS
-- ============================================================================

INSERT INTO vendors (
  name, description, vendor_type, location, city, state, country,
  phone_number, email, website_url, social_media,
  price_range, min_price, max_price, rating, review_count,
  response_time_hours, availability_status, certifications, is_verified
) VALUES
(
  'Rhythm Masters DJ Service',
  'Professional DJ services with custom music curation and MC hosting. State-of-the-art sound system. Experienced with weddings, parties, and corporate events.',
  'music',
  '666 Beat St, San Francisco, CA 94102',
  'San Francisco',
  'CA',
  'USA',
  '+1-415-555-6789',
  'bookings@rhythmmasters.com',
  'https://rhythmmasters.com',
  '{"instagram": "https://instagram.com/rhythmmasters", "facebook": "https://facebook.com/rhythmmasters"}',
  'mid-range',
  '800',
  '3000',
  4.8,
  278,
  2,
  'available',
  ARRAY['Professional DJ', 'Sound Engineer'],
  true
),
(
  'Live Band Entertainment Co.',
  'Live bands for weddings and events. Jazz, pop, rock, and Bollywood options. Full sound and lighting included.',
  'music',
  '777 Melody Lane, Los Angeles, CA 90001',
  'Los Angeles',
  'CA',
  'USA',
  '+1-213-555-7890',
  'info@liveband.com',
  'https://liveband.com',
  '{"instagram": "https://instagram.com/liveband", "facebook": "https://facebook.com/liveband"}',
  'premium',
  '2000',
  '8000',
  4.9,
  145,
  3,
  'available',
  ARRAY['Musicians Guild', 'Professional Band'],
  true
),
(
  'DJ Vibes Entertainment',
  'Energetic DJ services specializing in dance parties and celebrations. Good value for money. Works with all music genres.',
  'music',
  '888 Sound Ave, Chicago, IL 60601',
  'Chicago',
  'IL',
  'USA',
  '+1-312-555-8901',
  'contact@djvibes.com',
  'https://djvibes.com',
  '{"instagram": "https://instagram.com/djvibes", "facebook": "https://facebook.com/djvibes"}',
  'budget',
  '400',
  '1500',
  4.5,
  98,
  4,
  'available',
  ARRAY['Professional DJ'],
  true
),
(
  'Sonic Celebrations DJ & Lighting',
  'Full-service DJ and lighting combination. Perfect for creating immersive experiences. Includes fog machines and laser effects.',
  'music',
  '999 Sound Blvd, New York, NY 10001',
  'New York',
  'NY',
  'USA',
  '+1-212-555-9012',
  'bookings@soniccelebrations.com',
  'https://soniccelebrations.com',
  '{"instagram": "https://instagram.com/soniccelebrations", "facebook": "https://facebook.com/soniccelebrations"}',
  'mid-range',
  '1200',
  '5000',
  4.7,
  189,
  2,
  'available',
  ARRAY['Professional DJ', 'Lighting Technician'],
  true
);

-- ============================================================================
-- EVENT PLANNER VENDORS
-- ============================================================================

INSERT INTO vendors (
  name, description, vendor_type, location, city, state, country,
  phone_number, email, website_url, social_media,
  price_range, min_price, max_price, rating, review_count,
  response_time_hours, availability_status, certifications, is_verified
) VALUES
(
  'Dream Day Event Planning',
  'Full-service event planning and coordination. Specializes in weddings with multi-vendor management. Stress-free planning experience guaranteed.',
  'event_planner',
  '111 Planning Blvd, San Francisco, CA 94102',
  'San Francisco',
  'CA',
  'USA',
  '+1-415-555-0111',
  'hello@dreamday.com',
  'https://dreamday.com',
  '{"instagram": "https://instagram.com/dreamday", "facebook": "https://facebook.com/dreamday"}',
  'premium',
  '2000',
  '10000',
  4.9,
  312,
  1,
  'available',
  ARRAY['Professional Event Planner', 'Wedding Planner Certified'],
  true
),
(
  'Events Perfected',
  'Comprehensive event planning for all occasions. Experienced with corporate events, celebrations, and conferences. Vendor coordination included.',
  'event_planner',
  '222 Management Ln, Los Angeles, CA 90001',
  'Los Angeles',
  'CA',
  'USA',
  '+1-213-555-0222',
  'info@eventsperfected.com',
  'https://eventsperfected.com',
  '{"instagram": "https://instagram.com/eventsperfected", "facebook": "https://facebook.com/eventsperfected"}',
  'mid-range',
  '1000',
  '5000',
  4.7,
  234,
  2,
  'available',
  ARRAY['Professional Event Planner', 'ISES Member'],
  true
),
(
  'Budget-Friendly Event Coordination',
  'Affordable event planning without sacrificing quality. Perfect for smaller events and those with budget constraints. Day-of coordination available.',
  'event_planner',
  '333 Affordable Ave, Chicago, IL 60601',
  'Chicago',
  'IL',
  'USA',
  '+1-312-555-0333',
  'contact@budgetfriendlyevents.com',
  'https://budgetfriendlyevents.com',
  '{"instagram": "https://instagram.com/budgetfriendlyevents", "facebook": "https://facebook.com/budgetfriendlyevents"}',
  'budget',
  '300',
  '2000',
  4.6,
  145,
  3,
  'available',
  ARRAY['Professional Event Coordinator'],
  true
),
(
  'Corporate Excellence Events',
  'Specialized in corporate events, conferences, and business celebrations. Experienced with large-scale events and vendor management.',
  'event_planner',
  '444 Corporate Ave, New York, NY 10001',
  'New York',
  'NY',
  'USA',
  '+1-212-555-0444',
  'bookings@corporateexcellence.com',
  'https://corporateexcellence.com',
  '{"instagram": "https://instagram.com/corporateexcellence", "facebook": "https://facebook.com/corporateexcellence"}',
  'premium',
  '3000',
  '15000',
  4.8,
  201,
  2,
  'available',
  ARRAY['Professional Event Planner', 'MPI Member'],
  true
);

-- ============================================================================
-- ADD VENDOR SERVICES FOR SAMPLE VENDORS
-- ============================================================================

-- Catering Services
INSERT INTO vendor_services (vendor_id, name, description, price, duration, available)
SELECT id, 'Multi-Course Tasting Menu', 'Premium 5-course meal with wine pairing', 150, 'per person', true
FROM vendors WHERE name = 'The Culinary Artisans' LIMIT 1;

INSERT INTO vendor_services (vendor_id, name, description, price, duration, available)
SELECT id, 'Cocktail Reception & Appetizers', 'Passed appetizers and open bar', 75, 'per person', true
FROM vendors WHERE name = 'The Culinary Artisans' LIMIT 1;

INSERT INTO vendor_services (vendor_id, name, description, price, duration, available)
SELECT id, 'Organic Farm-to-Table', 'Seasonal organic menu with local ingredients', 95, 'per person', true
FROM vendors WHERE name = 'Fresh & Fit Catering Co.' LIMIT 1;

-- Venue Services
INSERT INTO vendor_services (vendor_id, name, description, price, duration, available)
SELECT id, 'Full Day Rental (10am-11pm)', 'Includes setup and breakdown', 12000, 'single event', true
FROM vendors WHERE name = 'Grand Ballroom Palace' LIMIT 1;

INSERT INTO vendor_services (vendor_id, name, description, price, duration, available)
SELECT id, 'Half Day Rental (4-hour)', 'Evening reception or ceremony only', 6000, '4 hours', true
FROM vendors WHERE name = 'Grand Ballroom Palace' LIMIT 1;

INSERT INTO vendor_services (vendor_id, name, description, price, duration, available)
SELECT id, 'Full Day Loft Rental', 'Flexible layout, move-in day before', 8000, 'single event', true
FROM vendors WHERE name = 'The Modern Loft Downtown' LIMIT 1;

-- Photography Services
INSERT INTO vendor_services (vendor_id, name, description, price, duration, available)
SELECT id, 'Wedding Package (8 hours)', 'Two photographers, 500+ edited images', 4500, '8 hours', true
FROM vendors WHERE name = 'Memories in Motion Photography' LIMIT 1;

INSERT INTO vendor_services (vendor_id, name, description, price, duration, available)
SELECT id, 'Pre-Wedding Session', 'Engagement photo shoot (2 hours)', 800, '2 hours', true
FROM vendors WHERE name = 'Memories in Motion Photography' LIMIT 1;

-- Decoration Services
INSERT INTO vendor_services (vendor_id, name, description, price, duration, available)
SELECT id, 'Complete Venue Styling', 'Floral, lighting, centerpieces, and setup', 8000, 'single event', true
FROM vendors WHERE name = 'Elegant Expressions Decor' LIMIT 1;

INSERT INTO vendor_services (vendor_id, name, description, price, duration, available)
SELECT id, 'Floral Arrangements Only', 'Custom bridal bouquet and centerpieces', 3000, 'single event', true
FROM vendors WHERE name = 'Elegant Expressions Decor' LIMIT 1;

-- DJ Services
INSERT INTO vendor_services (vendor_id, name, description, price, duration, available)
SELECT id, 'Wedding Reception DJ (5 hours)', 'Music, MC hosting, and equipment', 2000, '5 hours', true
FROM vendors WHERE name = 'Rhythm Masters DJ Service' LIMIT 1;

INSERT INTO vendor_services (vendor_id, name, description, price, duration, available)
SELECT id, 'Party DJ (4 hours)', 'Dance party setup with sound system', 1200, '4 hours', true
FROM vendors WHERE name = 'Rhythm Masters DJ Service' LIMIT 1;

-- Event Planner Services
INSERT INTO vendor_services (vendor_id, name, description, price, duration, available)
SELECT id, 'Full Planning Package', 'Complete planning from concept to execution', 5000, 'full duration', true
FROM vendors WHERE name = 'Dream Day Event Planning' LIMIT 1;

INSERT INTO vendor_services (vendor_id, name, description, price, duration, available)
SELECT id, 'Day-Of Coordination Only', 'Coordination and execution on event day', 1500, 'single event', true
FROM vendors WHERE name = 'Dream Day Event Planning' LIMIT 1;

-- ============================================================================
-- ADD SAMPLE VENDOR IMAGES
-- ============================================================================

INSERT INTO vendor_images (vendor_id, image_url, caption, order_index)
SELECT id, 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800', 'Elegant wedding reception setup', 1
FROM vendors WHERE name = 'The Culinary Artisans' LIMIT 1;

INSERT INTO vendor_images (vendor_id, image_url, caption, order_index)
SELECT id, 'https://images.unsplash.com/photo-1569718212df3a3a0ff1d002413b87fdd?w=800', 'Premium catering presentation', 2
FROM vendors WHERE name = 'The Culinary Artisans' LIMIT 1;

INSERT INTO vendor_images (vendor_id, image_url, caption, order_index)
SELECT id, 'https://images.unsplash.com/photo-1517457373614-b7152f800bb1?w=800', 'Grand ballroom setup', 1
FROM vendors WHERE name = 'Grand Ballroom Palace' LIMIT 1;

INSERT INTO vendor_images (vendor_id, image_url, caption, order_index)
SELECT id, 'https://images.unsplash.com/photo-1519167758481-83f19106d718?w=800', 'Decorated ballroom for wedding', 2
FROM vendors WHERE name = 'Grand Ballroom Palace' LIMIT 1;

INSERT INTO vendor_images (vendor_id, image_url, caption, order_index)
SELECT id, 'https://images.unsplash.com/photo-1502729783557-d7a0a8dda356?w=800', 'Wedding photography moment', 1
FROM vendors WHERE name = 'Memories in Motion Photography' LIMIT 1;

INSERT INTO vendor_images (vendor_id, image_url, caption, order_index)
SELECT id, 'https://images.unsplash.com/photo-1511379938547-c1f69b13d835?w=800', 'Professional event photography', 2
FROM vendors WHERE name = 'Memories in Motion Photography' LIMIT 1;

INSERT INTO vendor_images (vendor_id, image_url, caption, order_index)
SELECT id, 'https://images.unsplash.com/photo-1530953436266-dbb5de53b586?w=800', 'Beautiful floral decoration', 1
FROM vendors WHERE name = 'Elegant Expressions Decor' LIMIT 1;

INSERT INTO vendor_images (vendor_id, image_url, caption, order_index)
SELECT id, 'https://images.unsplash.com/photo-1519741497674-611481863552?w=800', 'Event venue decoration', 2
FROM vendors WHERE name = 'Elegant Expressions Decor' LIMIT 1;

-- ============================================================================
-- SEED DATA COMPLETE
-- ============================================================================
-- 24 vendors across 6 categories with services and images
-- All vendors are verified and available
-- Ready for testing and initial UI development
