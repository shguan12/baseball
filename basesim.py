import random

# --- MODERN NAME POOLS ---
FIRST_NAMES = [
    "Liam", "Noah", "Oliver", "Mateo", "Lucas", "Leo", "Julian", "Ezra",
    "Aiden", "Gabriel", "Caleb", "Christian", "Eli", "Gavin", "Xavier",
    "Landon", "Nolan", "Wyatt", "Connor", "Hunter", "Adrian",
    "Evan", "Theodore", "Miles", "Declan", "Wesley", "Cole", "Bryson",
    "Carlos", "Eduardo", "Alejandro", "Miguel", "Angel", "Diego", "Hayden"
]

LAST_NAMES = [
    "Smith", "Johnson", "Rodriguez", "Martinez", "Hernandez", "Lopez",
    "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore",
    "Jackson", "Martin", "Perez", "Thompson", "Sanchez", "Ramirez",
    "Torres", "Flores", "Rivera", "Gomez", "Cruz", "Reyes", "Morales",
    "Ortiz", "Gutierrez", "Chavez", "Ramos", "Vargas", "Jimenez", "Silva"
]

def generate_random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

# --- 1. POSITIONS & ARCHETYPE REGISTRY ---
POSITIONS = {
    "C": {"name": "Catcher", "adjustment": 12.5},
    "SS": {"name": "Shortstop", "adjustment": 7.5},
    "2B": {"name": "Second Baseman", "adjustment": 2.5},
    "3B": {"name": "Third Baseman", "adjustment": 2.5},
    "CF": {"name": "Center Fielder", "adjustment": 2.5},
    "RF": {"name": "Right Fielder", "adjustment": -7.5},
    "LF": {"name": "Left Fielder", "adjustment": -7.5},
    "1B": {"name": "First Baseman", "adjustment": -12.5},
    "DH": {"name": "Designated Hitter", "adjustment": -17.5}
}

PLAYER_ARCHETYPES = {
    "three_true_outcomes": {
        "name": "The Three-True-Outcomes Slugger",
        "ab_per_game_min": 3.5, "ab_per_game_max": 4.2,
        "hit_weights": [0.40, 0.15, 0.02, 0.43],
        "bb_rate": 0.12, "so_rate": 0.36, "steal_tendency": 0.02, "success_rate": 0.50,
        "defensive_runs_per_season": -5.0
    },
    "contact_speedster": {
        "name": "The Leadoff Slap Hitter",
        "ab_per_game_min": 3.8, "ab_per_game_max": 4.5,
        "hit_weights": [0.78, 0.18, 0.03, 0.01],
        "bb_rate": 0.08, "so_rate": 0.11, "steal_tendency": 0.45, "success_rate": 0.82,
        "defensive_runs_per_season": 8.0
    },
    "pure_contact": {
        "name": "The Pure Contact Hitter",
        "ab_per_game_min": 3.9, "ab_per_game_max": 4.6,
        "hit_weights": [0.65, 0.25, 0.03, 0.07],
        "bb_rate": 0.07, "so_rate": 0.09, "steal_tendency": 0.10, "success_rate": 0.70,
        "defensive_runs_per_season": 2.0
    },
    "defensive_wizard": {
        "name": "The Defensive Wizard (Glove First)",
        "ab_per_game_min": 3.2, "ab_per_game_max": 4.0,
        "hit_weights": [0.85, 0.12, 0.02, 0.01],
        "bb_rate": 0.06, "so_rate": 0.25, "steal_tendency": 0.08, "success_rate": 0.65,
        "defensive_runs_per_season": 18.0
    },
    "spray_hitter": {
        "name": "The Line-Drive Spray Hitter",
        "ab_per_game_min": 3.7, "ab_per_game_max": 4.4,
        "hit_weights": [0.58, 0.30, 0.05, 0.07],
        "bb_rate": 0.10, "so_rate": 0.14, "steal_tendency": 0.12, "success_rate": 0.72,
        "defensive_runs_per_season": 3.0
    }
}

def generate_player(name=None, archetype_key=None, pos_key=None):
    if name is None:
        name = generate_random_name()
    if archetype_key is None or archetype_key not in PLAYER_ARCHETYPES:
        archetype_key = random.choice(list(PLAYER_ARCHETYPES.keys()))
    if pos_key is None or pos_key not in POSITIONS:
        pos_key = random.choice(list(POSITIONS.keys()))

    # Tightened tiers: Generational Icons are now exceptionally rare (top 0.5% instead of 3%)
    tier_roll = random.random()
    if tier_roll < 0.55:
        talent_mult = random.uniform(0.60, 0.78)
        tier_name = "Fringe Prospect / Utility Glove"
    elif tier_roll < 0.90:
        talent_mult = random.uniform(0.79, 0.97)
        tier_name = "Solid Everyday Starter"
    elif tier_roll < 0.995:
        talent_mult = random.uniform(0.98, 1.08)
        tier_name = "Star"
    else:
        talent_mult = random.uniform(1.09, 1.15) # Lowered max ceiling to curb 900+ HR inflation
        tier_name = "Generational Icon"

    return {
        "name": name,
        "age": 21,
        "tier": tier_name,
        "talent_multiplier": talent_mult,
        "archetype_key": archetype_key,
        "archetype": PLAYER_ARCHETYPES[archetype_key].copy(),
        "position_key": pos_key,
        "position": POSITIONS[pos_key],
        "durability": random.randint(65, 95),
        "consecutive_bad_years": 0
    }

# --- 2. SINGLE SEASON SIMULATION ENGINE ---
def simulate_season(games, profile):
    arch = profile["archetype"]
    age = profile["age"]

    if age <= 30:
        power_multiplier = 1.0
    else:
        decline_years = age - 30
        # Steeper exponential-style cliff to force natural regressions and retirements
        power_multiplier = max(0.05, 1.0 - (decline_years * 0.14))

    tier_power_caps = {
        "Fringe Prospect / Utility Glove": 0.45,
        "Solid Everyday Starter": 0.70,
        "Star": 1.0,
        "Generational Icon": 1.35
    }
    tier_cap = tier_power_caps.get(profile["tier"], 1.0)
    effective_power_weight = max(0.015, arch["hit_weights"][3] * power_multiplier * (profile["talent_multiplier"] ** 1.2) * tier_cap)

    ab = int(games * random.uniform(arch["ab_per_game_min"], arch["ab_per_game_max"]))
    bb = int(ab * (arch["bb_rate"] * profile["talent_multiplier"]) * random.uniform(0.9, 1.1))
    so = int(ab * arch["so_rate"] * random.uniform(0.9, 1.1))

    hits_est = int(ab * (0.20 + (profile["talent_multiplier"] * 0.04)) * random.uniform(0.85, 1.15))

    adjusted_weights = arch["hit_weights"].copy()
    adjusted_weights[3] = effective_power_weight

    hit_types = random.choices(
        ["single", "double", "triple", "hr"],
        weights=adjusted_weights,
        k=max(1, hits_est)
    )

    singles = hit_types.count("single")
    doubles = hit_types.count("double")
    triples = hit_types.count("triple")
    hr = hit_types.count("hr")
    hits = singles + doubles + triples + hr

    rbi_hrs = hr * random.choice([1, 1, 1, 2, 2, 3])
    rbi_triples = triples * random.choice([1, 1, 2])
    rbi_singles = sum(1 for _ in range(singles) if random.random() < 0.28 and random.choices([1, 2], weights=[0.85, 0.15])[0] == 1)
    rbi_doubles = sum(1 for _ in range(doubles) if random.random() < 0.60)
    total_rbi = rbi_hrs + rbi_triples + rbi_singles + rbi_doubles
    runs = hr + int(singles * 0.15) + int(doubles * 0.25) + int(triples * 0.5)

    stolen_bases, caught_stealing = 0, 0
    for _ in range(singles + bb):
        if random.random() < arch["steal_tendency"]:
            if random.random() < arch["success_rate"]: stolen_bases += 1
            else: caught_stealing += 1

    pa = ab + bb
    return {
        "games": games, "at_bats": ab, "hits": hits, "singles": singles,
        "doubles": doubles, "triples": triples, "home_runs": hr,
        "walks": bb, "strikeouts": so, "rbi": total_rbi, "runs": runs,
        "stolen_bases": stolen_bases, "caught_stealing": caught_stealing,
        "avg": hits / max(1, ab), "obp": (hits + bb) / max(1, pa),
        "slg": (singles + (2 * doubles) + (3 * triples) + (4 * hr)) / max(1, ab),
        "ops": ((hits + bb) / max(1, pa)) + ((singles + (2 * doubles) + (3 * triples) + (4 * hr)) / max(1, ab))
    }

# --- 3. HEALTH & PLAYING TIME ---
def determine_games_played(profile, last_season_ops):
    max_games = 162
    arch = profile["archetype"]

    if arch.get("defensive_runs_per_season", 0) >= 15 and profile["tier"] != "Fringe Prospect / Utility Glove":
        return random.randint(130, 160)

    if last_season_ops is not None and last_season_ops < 0.620:
        return random.randint(15, 45)

    injury_risk = max(0.0, (profile["age"] - 28) * 0.03)
    missed_base = random.expovariate(0.18) * (1 + injury_risk)
    missed_games = int(missed_base * (100 - profile["durability"]) / 20)

    base_games = int(max_games * min(1.0, profile["talent_multiplier"]))
    return max(10, min(162, base_games - missed_games))

# --- 4. WAR & EVALUATION ---
def calculate_season_war(season, profile):
    arch = profile["archetype"]
    pos = profile["position"]

    w_singles = season["singles"] * 0.08
    w_doubles = season["doubles"] * 0.18
    w_triples = season["triples"] * 0.25
    w_hr = season["home_runs"] * 0.65
    w_bb = season["walks"] * 0.18
    w_runs = season["runs"] * 0.12
    w_rbi = season["rbi"] * 0.08
    w_sb = (season["stolen_bases"] * 0.20) - (season["caught_stealing"] * 0.25)

    offensive_value = w_singles + w_doubles + w_triples + w_hr + w_bb + w_runs + w_rbi + w_sb
    replacement_baseline = 28.0

    batting_war = (offensive_value - replacement_baseline) / 9.5

    playing_fraction = season["games"] / 162.0
    defensive_runs = arch.get("defensive_runs_per_season", 0.0)
    positional_runs = pos["adjustment"]

    raw_fielding_runs = (defensive_runs + positional_runs) * playing_fraction
    if pos["adjustment"] <= -15.0 and offensive_value > 65.0:
        raw_fielding_runs = max(-10.0, raw_fielding_runs * 0.5)

    fielding_and_pos_war = raw_fielding_runs / 9.5
    total_war = batting_war + fielding_and_pos_war

    if pos["adjustment"] >= 2.5 and batting_war > 3.0:
        total_war *= 1.25

    return round(max(-1.5, total_war), 1)

def evaluate_hall_of_fame(stats, war):
    if war >= 75.0 or stats["hits"] >= 3300 or stats["home_runs"] >= 600:
        return "First-Ballot Hall of Famer"
    elif war >= 65.0 or stats["hits"] >= 3000 or stats["home_runs"] >= 500:
        return "Hall of Famer"
    elif war >= 45.0 or stats["hits"] >= 2000 or stats["home_runs"] >= 300:
        return "Hall of Very Good / Borderline Candidate"
    elif war >= 25.0:
        return "Solid Major League Career (Falls Short)"
    else:
        return "Fringe / Short-Lived Career"

# --- 5. BATCH SIMULATION & STATISTICAL AUDIT ---
def simulate_batch_careers(num_players=100):
    results = []
    print(f"Simulating {num_players} careers...\n")

    for _ in range(num_players):
        profile = generate_player()
        name = profile["name"]

        career_stats = {
            "games": 0, "at_bats": 0, "hits": 0, "singles": 0, "doubles": 0,
            "triples": 0, "home_runs": 0, "walks": 0, "strikeouts": 0,
            "rbi": 0, "runs": 0, "stolen_bases": 0, "caught_stealing": 0
        }

        career_war = 0.0
        season_count = 0
        is_active = True
        last_ops = None

        while is_active and season_count < 25:
            games = determine_games_played(profile, last_ops)
            season = simulate_season(games, profile)
            last_ops = season["ops"]
            s_war = calculate_season_war(season, profile)
            career_war += s_war

            for key in career_stats:
                career_stats[key] += season[key]

            season_count += 1

            if season["ops"] < 0.670:
                profile["consecutive_bad_years"] += 1
            else:
                profile["consecutive_bad_years"] = 0

            retire_chance = 0.0
            if profile["tier"] not in ["Star", "Generational Icon"] and profile["age"] >= 32:
                retire_chance = (profile["age"] - 31) * 0.35
            elif profile["age"] >= 36:
                retire_chance = (profile["age"] - 35) * 0.40
            elif profile["tier"] in ["Fringe Prospect / Utility Glove"] and profile["consecutive_bad_years"] >= 2:
                is_active = False

            if is_active and random.random() < retire_chance:
                is_active = False
            elif is_active:
                profile["age"] += 1

        c_ab = max(1, career_stats["at_bats"])
        career_ops = ((career_stats["hits"] + career_stats["walks"]) / max(1, c_ab + career_stats["walks"])) + \
                     ((career_stats["singles"] + (2 * career_stats["doubles"]) + (3 * career_stats["triples"]) + (4 * career_stats["home_runs"])) / c_ab)

        results.append({
            "name": name,
            "position": profile["position"]["name"],
            "tier": profile["tier"],
            "games": career_stats["games"],
            "home_runs": career_stats["home_runs"],
            "hits": career_stats["hits"],
            "war": round(career_war, 1),
            "ops": career_ops,
            "hof_verdict": evaluate_hall_of_fame(career_stats, career_war)
        })

    # --- TEXT-BASED AUDIT REPORT ---
    print("=" * 80)
    print(f" BATCH SIMULATION AUDIT REPORT ({num_players} PLAYERS)")
    print("=" * 80)

    # Sort by WAR descending to find top performers & check anomalies
    sorted_by_war = sorted(results, key=lambda x: x["war"], reverse=True)

    print("\n[TOP 10 PLAYERS BY CAREER WAR]")
    print(f"{'Player Name':<20} | {'Position':<15} | {'Tier':<25} | {'HR':<5} | {'WAR':<5} | {'Verdict'}")
    print("-" * 85)
    for p in sorted_by_war[:10]:
        print(f"{p['name']:<20} | {p['position']:<15} | {p['tier']:<25} | {p['home_runs']:<5} | {p['war']:<5.1f} | {p['hof_verdict']}")

    print("\n[TOP 5 HOME RUN LEADERS]")
    print(f"{'Player Name':<20} | {'Position':<15} | {'HR':<5} | {'WAR':<5} | {'Verdict'}")
    print("-" * 65)
    sorted_by_hr = sorted(results, key=lambda x: x["home_runs"], reverse=True)
    for p in sorted_by_hr[:5]:
        print(f"{p['name']:<20} | {p['position']:<15} | {p['home_runs']:<5} | {p['war']:<5.1f} | {p['hof_verdict']}")

    print("\n[POTENTIAL OUTLIERS / ANOMALY CHECK]")
    print("Flagging players with >400 HRs but <50 WAR, or other logic checks:")
    anomalies = [p for p in results if p["home_runs"] >= 400 and p["war"] < 50.0]
    if anomalies:
        for p in anomalies:
            print(f"⚠️  {p['name']} ({p['position']}) — {p['home_runs']} HRs with only {p['war']} WAR ({p['hof_verdict']})")
    else:
        print("✓ No extreme HR/WAR disconnects detected in this batch run.")
    print("=" * 80)

# Run batch simulation with clean text output
simulate_batch_careers(100)
