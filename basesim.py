import random

POSITIONS = [
    {"name": "Catcher", "pos_modifier": 1.1},
    {"name": "First Baseman", "pos_modifier": 0.8},
    {"name": "Second Baseman", "pos_modifier": 1.0},
    {"name": "Shortstop", "pos_modifier": 1.2},
    {"name": "Third Baseman", "pos_modifier": 1.0},
    {"name": "Outfielder", "pos_modifier": 0.9},
    {"name": "Designated Hitter", "pos_modifier": 0.6}
]

PLAYER_ARCHETYPES = [
    {
        "name": "Three-True-Outcomes Slugger",
        "hit_weights": [0.40, 0.15, 0.02, 0.43],  # [Singles, Doubles, Triples, HR]
        "bb_rate": 0.14,
        "so_rate": 0.32,
        "power_mult": 1.5,
        "contact_mult": 0.75
    },
    {
        "name": "Batting Title Savant",
        "hit_weights": [0.75, 0.22, 0.02, 0.01],  # Arraez / Gwynn style contact profile
        "bb_rate": 0.08,
        "so_rate": 0.06,                             # Extremely low strikeouts
        "power_mult": 0.4,
        "contact_mult": 1.20                         # Reined in to keep peaks around .320-.335
    },
    {
        "name": "Elite MVP Dual-Threat",
        "hit_weights": [0.52, 0.26, 0.03, 0.19],  # Great mix of doubles, singles, and solid HR power
        "bb_rate": 0.11,
        "so_rate": 0.16,                             # Controlled strikeouts
        "power_mult": 1.2,
        "contact_mult": 1.10                         # High average (.290-.315) with 30-40 HR power
    },
    {
        "name": "Contact Speedster",
        "hit_weights": [0.72, 0.20, 0.07, 0.01],
        "bb_rate": 0.08,
        "so_rate": 0.15,
        "power_mult": 0.6,
        "contact_mult": 1.10
    },
    {
        "name": "Gap Power Hitter",
        "hit_weights": [0.55, 0.30, 0.05, 0.10],
        "bb_rate": 0.10,
        "so_rate": 0.20,
        "power_mult": 1.0,
        "contact_mult": 1.0
    },
    {
        "name": "Balanced Veteran",
        "hit_weights": [0.60, 0.25, 0.03, 0.12],
        "bb_rate": 0.10,
        "so_rate": 0.18,
        "power_mult": 0.9,
        "contact_mult": 1.0
    }
]

def generate_player():
    name_pools_first = ["Alex", "Carlos", "Luis", "Marcus", "Trey", "Jackson", "Ken", "Shohei", "Vladimir", "Bryce"]
    name_pools_last = ["Arraez", "Gallo", "Soto", "Acuna", "Ohtani", "Judge", "Witt", "Devers", "Seager", "Henderson"]
    
    name = f"{random.choice(name_pools_first)} {random.choice(name_pools_last)}"
    position = random.choice(POSITIONS)
    archetype = random.choice(PLAYER_ARCHETYPES)
    
    tier_roll = random.random()
    if tier_roll < 0.03:
        tier = "Generational Icon"
        talent_multiplier = random.uniform(1.2, 1.4)
    elif tier_roll < 0.15:
        tier = "Star"
        talent_multiplier = random.uniform(1.0, 1.19)
    elif tier_roll < 0.50:
        tier = "Solid Regular"
        talent_multiplier = random.uniform(0.85, 0.99)
    else:
        tier = "Fringe Prospect / Utility Glove"
        talent_multiplier = random.uniform(0.65, 0.84)
        
    return {
        "name": name,
        "position": position,
        "archetype": archetype,
        "tier": tier,
        "talent_multiplier": talent_multiplier,
        "age": 21,
        "consecutive_bad_years": 0
    }

def determine_games_played(profile, last_ops=None):
    base_games = random.choices([162, 155, 145, 130, 110, 80], weights=[0.4, 0.2, 0.15, 0.1, 0.1, 0.05])[0]
    if profile["tier"] == "Generational Icon":
        return min(162, base_games + random.randint(0, 3))
    return base_games

def simulate_season(games, profile):
    ab = int(games * random.uniform(3.5, 4.1))
    archetype = profile["archetype"]
    
    hit_rate = (0.23 + (profile["talent_multiplier"] * 0.03)) * archetype["contact_mult"]
    hits = int(ab * hit_rate * random.uniform(0.92, 1.08))
    hits = min(hits, ab)
    
    walks = int(ab * archetype["bb_rate"] * random.uniform(0.85, 1.15))
    strikeouts = int(ab * archetype["so_rate"] * random.uniform(0.9, 1.1))
    
    hw = archetype["hit_weights"]
    singles = int(hits * hw[0])
    doubles = int(hits * hw[1])
    triples = int(hits * hw[2])
    home_runs = int(hits * hw[3])
    
    total_distributed = singles + doubles + triples + home_runs
    if total_distributed < hits:
        singles += (hits - total_distributed)
    
    runs = int((home_runs * 1.2) + (doubles * 0.5) + (walks * 0.3))
    rbi = int((home_runs * 1.8) + (doubles * 0.7) + (singles * 0.3))
    
    pa = ab + walks
    ba = hits / max(1, ab)
    obp = (hits + walks) / max(1, pa)
    slg = (singles + (2 * doubles) + (3 * triples) + (4 * home_runs)) / max(1, ab)
    ops = obp + slg
    
    return {
        "games": games,
        "at_bats": ab,
        "hits": hits,
        "singles": singles,
        "doubles": doubles,
        "triples": triples,
        "home_runs": home_runs,
        "walks": walks,
        "strikeouts": strikeouts,
        "rbi": rbi,
        "runs": runs,
        "stolen_bases": random.randint(0, 15),
        "caught_stealing": random.randint(0, 5),
        "batting_average": ba,
        "ops": ops
    }

def calculate_season_war(season, profile):
    offensive_runs = (season["home_runs"] * 1.4) + (season["hits"] * 0.4) + (season["walks"] * 0.3)
    position_bonus = profile["position"]["pos_modifier"]
    raw_war = (offensive_runs / 10.0) * position_bonus * (profile["talent_multiplier"] * 0.8)
    return round(max(-0.5, raw_war / 15.0), 1)

def evaluate_hall_of_fame(career_stats, career_war):
    if career_war >= 60.0 or career_stats["home_runs"] >= 500:
        return "First Ballot Hall of Famer"
    elif career_war >= 45.0 or career_stats["home_runs"] >= 350:
        return "Hall of Famer"
    elif career_war >= 30.0:
        return "Hall of Fame Fringe"
    else:
        return "Not Inducted"
