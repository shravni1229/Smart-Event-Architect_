"""
Smart Event Architect - Rule-Based Recommendation Engine
Provides intelligent, explainable recommendations for event services,
budget allocation, themes, and feasibility analysis for college mini-projects.
"""

def classify_budget_tier(budget):
    """Classifies user budget into standardized tiers."""
    budget = float(budget)
    if budget < 50000:
        return 'Economy'
    elif budget < 200000:
        return 'Standard'
    elif budget < 500000:
        return 'Premium'
    else:
        return 'Luxury'

def assess_feasibility(event_type, budget, guest_count):
    """
    Evaluates whether the allocated budget is feasible for the given guest count
    and returns a status, badge class, and human-friendly explanation.
    """
    guest_count = max(1, int(guest_count))
    budget = float(budget)
    per_guest = budget / guest_count

    # Baseline cost thresholds per guest across event types
    event_lower = event_type.lower()
    if 'wedding' in event_lower or 'engagement' in event_lower:
        min_per_guest = 600
        optimal_per_guest = 1500
    elif 'corporate' in event_lower:
        min_per_guest = 500
        optimal_per_guest = 1200
    elif 'fest' in event_lower:
        min_per_guest = 200
        optimal_per_guest = 600
    else: # Birthday, Anniversary, Farewell
        min_per_guest = 350
        optimal_per_guest = 800

    if per_guest < min_per_guest:
        return {
            'status': 'Tight Budget',
            'badge': 'warning',
            'per_guest': round(per_guest, 2),
            'message': f"₹{int(per_guest)} per guest is slightly tight for a {event_type}. We recommend focusing on core catering and essential decor to avoid overspending."
        }
    elif per_guest >= optimal_per_guest:
        return {
            'status': 'Optimal & Spacious',
            'badge': 'success',
            'per_guest': round(per_guest, 2),
            'message': f"₹{int(per_guest)} per guest gives excellent flexibility! You can easily include premium photography, live entertainment, and customized theme decor."
        }
    else:
        return {
            'status': 'Well-Balanced',
            'badge': 'info',
            'per_guest': round(per_guest, 2),
            'message': f"₹{int(per_guest)} per guest is well-balanced. You can comfortably book professional standard catering, photography, and audio setup."
        }

def get_theme_recommendation(event_type, budget_tier):
    """Returns curated color schemes and decor themes based on event type & tier."""
    event_lower = event_type.lower()
    
    if 'wedding' in event_lower:
        if budget_tier in ['Premium', 'Luxury']:
            return "Royal Orchid Purple & Blush Pink with Grand Crystal Chandeliers and Fresh Floral Mandap"
        else:
            return "Romantic Pastel Rose & Lavender Drapes with Fairy Light Canopy"
    elif 'birthday' in event_lower:
        if budget_tier in ['Premium', 'Luxury']:
            return "Neon Cyber-Magenta & Electric Violet Balloon Arch with LED Silhouette Backdrop"
        else:
            return "Soft Pastel Pink, Lavender & Cloud White Balloon Cloud Theme"
    elif 'corporate' in event_lower:
        return "Executive Deep Indigo & Radiant Magenta Lighting with Minimalist Clean White Stage"
    elif 'fest' in event_lower:
        return "Electric Violet & High-Voltage Pink Glow with Strobe Effects and Trussing"
    elif 'engagement' in event_lower:
        return "Blush Rose, Plum & Warm Golden Fairytale Ring Stage with Floral Accents"
    elif 'anniversary' in event_lower:
        return "Champagne White & Velvet Mauve Candlelit Dining with Vintage Floral Centerpieces"
    elif 'farewell' in event_lower:
        return "Twilight Purple & Starry Pink Memory Wall with Polaroid Photo Booth"
    else:
        return "Harmonious Purple, Pink & Crisp White Ambient Theme"

def get_pro_tips(event_type, budget_tier):
    """Provides practical tips to optimize expenses."""
    tips = [
        "Booking core services 4 to 6 weeks in advance guarantees vendor rate locks.",
        "Opting for a buffet layout instead of individual table service can save 12-18% on food waste and staff costs.",
        "Combining photography and videography into a single vendor package offers substantial combo discounts."
    ]
    if budget_tier == 'Economy':
        tips.append("Consider non-peak days (weekdays or Sunday afternoons) to unlock up to 20% discount on venue booking.")
    elif budget_tier in ['Premium', 'Luxury']:
        tips.append("Pre-plan a detailed 30-minute buffer in the event timeline to prevent overtime vendor penalties.")
    return tips

def recommend_services(event_type, budget, guest_count):
    """
    Core Recommendation Engine:
    Takes event type, total budget, and guest count.
    Generates intelligent rule-based services with itemized cost estimation.
    """
    budget = float(budget)
    guest_count = max(1, int(guest_count))
    tier = classify_budget_tier(budget)
    feasibility = assess_feasibility(event_type, budget, guest_count)
    theme = get_theme_recommendation(event_type, tier)
    tips = get_pro_tips(event_type, tier)
    
    event_lower = event_type.lower()
    services = []

    # Helper to calculate and round service estimate
    def calc_cost(percentage, min_val=2000):
        val = budget * percentage
        return max(min_val, round(val / 500) * 500)

    # 1. CATERING & BEVERAGE SERVICE (Core across all events)
    if 'wedding' in event_lower or 'engagement' in event_lower:
        catering_pct = 0.45 if tier in ['Economy', 'Standard'] else 0.42
        c_cost = calc_cost(catering_pct, min_val=15000)
        c_spec = "Multi-Cuisine Royal Buffet (Welcome Mocktails, Starters, 3 Main Courses, Desserts)" if tier in ['Premium', 'Luxury'] else "Standard Festive Multi-course Buffet with Welcome Drinks"
        services.append({
            'name': 'Catering & Dining Hospitality',
            'category': 'Catering',
            'priority': 'Essential',
            'tier_fit': 'All Tiers',
            'estimated_cost': c_cost,
            'description': f"{c_spec} tailored for {guest_count} honored guests."
        })
    elif 'corporate' in event_lower:
        c_cost = calc_cost(0.35, min_val=8000)
        services.append({
            'name': 'Executive Conference Catering',
            'category': 'Catering',
            'priority': 'Essential',
            'tier_fit': 'All Tiers',
            'estimated_cost': c_cost,
            'description': f"Continuous Coffee/Tea Station, Executive High Tea, and Balanced Buffet Lunch for {guest_count} delegates."
        })
    elif 'fest' in event_lower:
        c_cost = calc_cost(0.25, min_val=10000)
        services.append({
            'name': 'Food Court & Refreshment Stalls',
            'category': 'Catering',
            'priority': 'Essential',
            'tier_fit': 'All Tiers',
            'estimated_cost': c_cost,
            'description': "Hygienic multi-stall fast bites, energy beverages, and packed refreshments for fest attendees."
        })
    else: # Birthday, Anniversary, Farewell
        c_cost = calc_cost(0.40, min_val=6000)
        services.append({
            'name': 'Gourmet Party Buffet & Specialty Cake',
            'category': 'Catering',
            'priority': 'Essential',
            'tier_fit': 'All Tiers',
            'estimated_cost': c_cost,
            'description': f"Designer custom theme cake, finger foods, mocktails, and celebration buffet dinner for {guest_count} guests."
        })

    # 2. DECORATION & THEME SETUP
    if tier in ['Premium', 'Luxury']:
        d_cost = calc_cost(0.20, min_val=20000)
        d_desc = f"Luxury bespoke {theme} with grand entrance arch, designer stage, photo booth, and dynamic uplighting."
    elif tier == 'Standard':
        d_cost = calc_cost(0.18, min_val=10000)
        d_desc = f"Cohesive thematic styling with fresh flower/balloon accents, thematic stage backdrop, and table centerpieces."
    else:
        d_cost = calc_cost(0.15, min_val=4000)
        d_desc = "Smart minimalist stage backdrop with welcome standee, balloon/fabric drapery, and ambient accents."
    
    services.append({
        'name': 'Theme Decor & Stage Styling',
        'category': 'Decoration',
        'priority': 'Essential',
        'tier_fit': 'All Tiers',
        'estimated_cost': d_cost,
        'description': d_desc
    })

    # 3. PHOTOGRAPHY & CINEMATOGRAPHY
    if tier in ['Premium', 'Luxury']:
        p_cost = calc_cost(0.14, min_val=18000)
        p_desc = "Dual-candid photographers, 4K cinematic video teaser, drone aerial venue coverage, and premium hardcover photo book."
    elif tier == 'Standard':
        p_cost = calc_cost(0.12, min_val=8000)
        p_desc = "1 Professional candid photographer + 1 Full HD videographer covering all major highlights and raw edited footage."
    else:
        p_cost = calc_cost(0.10, min_val=3500)
        p_desc = "Single traditional photographer capturing key stage moments with color-graded digital gallery link."
    
    services.append({
        'name': 'Photography & Video Memories',
        'category': 'Media',
        'priority': 'Essential' if tier != 'Economy' else 'Recommended',
        'tier_fit': 'All Tiers',
        'estimated_cost': p_cost,
        'description': p_desc
    })

    # 4. AUDIO, DJ & LIGHTING
    if 'fest' in event_lower:
        s_cost = calc_cost(0.28, min_val=15000)
        s_desc = "Concert-grade JBL/RCF line-array sound system, heavy bass, moving head sharpies, fog machines, and professional club DJ."
    elif tier in ['Premium', 'Luxury']:
        s_cost = calc_cost(0.10, min_val=10000)
        s_desc = "High-definition sound setup, cordless handheld mics, DJ console with illuminated dance floor and intelligent beam lighting."
    elif tier == 'Standard':
        s_cost = calc_cost(0.08, min_val=5000)
        s_desc = "Professional DJ sound setup, dual wireless mics, dance floor party lights, and personalized playlist coordination."
    else:
        s_cost = calc_cost(0.07, min_val=2500)
        s_desc = "Compact high-clarity PA sound system, background music player, and microphone for speeches and announcements."
    
    services.append({
        'name': 'Sound, DJ & Intelligent Lighting',
        'category': 'Audio/Visual',
        'priority': 'Essential' if 'fest' in event_lower else 'Recommended',
        'tier_fit': 'All Tiers',
        'estimated_cost': s_cost,
        'description': s_desc
    })

    # 5. MASTER OF CEREMONIES (ANCHOR / EMCEE) & ENTERTAINMENT
    if tier in ['Standard', 'Premium', 'Luxury']:
        e_cost = calc_cost(0.05, min_val=4000)
        if 'birthday' in event_lower:
            e_desc = "Lively games host & kids entertainer with engaging party activities and prize distribution."
        elif 'wedding' in event_lower or 'engagement' in event_lower:
            e_desc = "Bilingual charismatic anchor to guide rituals, engage family members, and manage the evening flow seamlessly."
        elif 'corporate' in event_lower:
            e_desc = "Professional corporate moderator for keynote introductions, panel transitions, and award distribution."
        else:
            e_desc = "Dynamic party host to keep guest energy high and announce event milestones."

        services.append({
            'name': 'Anchor / Emcee & Guest Engagement',
            'category': 'Entertainment',
            'priority': 'Recommended',
            'tier_fit': 'Standard, Premium, Luxury',
            'estimated_cost': e_cost,
            'description': e_desc
        })

    # 6. DEDICATED EVENT COORDINATOR / FLOOR MANAGER
    if tier in ['Standard', 'Premium', 'Luxury']:
        m_cost = calc_cost(0.05, min_val=3500)
        services.append({
            'name': 'On-Site Event Coordinator',
            'category': 'Coordination',
            'priority': 'Recommended' if tier == 'Standard' else 'Essential',
            'tier_fit': 'Standard, Premium, Luxury',
            'estimated_cost': m_cost,
            'description': "Dedicated on-ground coordinator ensuring vendors arrive on time, schedule runs smoothly, and client stays stress-free."
        })

    # 7. LUXURY ADD-ONS (Only for Premium and Luxury tiers)
    if tier in ['Premium', 'Luxury']:
        l_cost = calc_cost(0.04, min_val=5000)
        services.append({
            'name': 'Customized Invitations & Return Favors',
            'category': 'Hospitality',
            'priority': 'Optional Add-on',
            'tier_fit': 'Premium & Luxury',
            'estimated_cost': l_cost,
            'description': "Digital animated invitation video, QR code guest RSVP check-in, and personalized luxury gift hampers."
        })

    # Calculate total estimated cost
    total_estimated = sum(s['estimated_cost'] for s in services)
    budget_difference = budget - total_estimated

    return {
        'event_type': event_type,
        'guest_count': guest_count,
        'budget': budget,
        'budget_tier': tier,
        'per_guest_budget': feasibility['per_guest'],
        'feasibility': feasibility,
        'theme_recommendation': theme,
        'pro_tips': tips,
        'recommended_services': services,
        'total_estimated_cost': total_estimated,
        'budget_difference': budget_difference,
        'is_within_budget': total_estimated <= budget
    }
