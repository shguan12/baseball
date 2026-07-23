# Let's check how the metrics and summary stats are calculated in app.py
# In app.py, results list has:
# "batting_average", "ops", etc. Let's make sure we also store career obp and slg in the dictionary so we can compute the maximums easily.

code_app_updated = '''import streamlit as st
import random
from basesim import (
    generate_player, 
    simulate_season, 
    determine_games_played, 
    calculate_season_war, 
    evaluate_hall_of_fame,
    PLAYER_ARCHETYPES,
    POSITIONS
)

st.set_page_config(
    page_title="Baseball Career Simulator",
    page_icon="⚾",
    layout="wide"
)

st.title("⚾ Procedural Baseball Career Simulator")
st.markdown("Simulate alternate timelines and inaccurate baseball player careers using your `basesim.py` engine.")

# --- Session State Initialization ---
if "simulation_results" not in st.session_state:
    st.session_state.simulation_results = None

# --- Sidebar Controls ---
st.sidebar.header("Simulation Settings")
num_players = st.sidebar.slider("Careers to Simulate", min_value=10, max_value=500, value=100, step=10)

# Custom function to capture results cleanly for Streamlit without forcing print statements
def run_streamlit_batch(num_players):
    results = []
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
        c_bb = career_stats["walks"]
        c_pa = c_ab + c_bb
        c_hits = career_stats["hits"]
        c_singles = career_stats["singles"]
        c_doubles = career_stats["doubles"]
        c_triples = career_stats["triples"]
        c_hr = career_stats["home_runs"]

        career_avg = c_hits / c_ab
        career_obp = (c_hits + c_bb) / max(1, c_pa)
        career_slg = (c_singles + (2 * c_doubles) + (3 * c_triples) + (4 * c_hr)) / c_ab
        career_ops = career_obp + career_slg

        results.append({
            "name": name,
            "position": profile["position"]["name"],
            "tier": profile["tier"],
            "archetype": profile["archetype"]["name"],
            "games": career_stats["games"],
            "at_bats": c_ab,
            "hits": c_hits,
            "home_runs": c_hr,
            "batting_average": round(career_avg, 3),
            "obp": round(career_obp, 3),
            "slg": round(career_slg, 3),
            "ops": round(career_ops, 3),
            "war": round(career_war, 1),
            "hof_verdict": evaluate_hall_of_fame(career_stats, career_war)
        })
    return results

# --- Main Action Trigger ---
if st.sidebar.button("Run Batch Simulation", type="primary"):
    with st.spinner(f"Simulating {num_players} baseball careers..."):
        st.session_state.simulation_results = run_streamlit_batch(num_players)

# --- Display Results ---
if st.session_state.simulation_results is not None:
    results = st.session_state.simulation_results
    st.success(f"Successfully simulated {len(results)} player careers!")

    # Summary Metrics
    max_hr = max(p["home_runs"] for p in results)
    max_war = max(p["war"] for p in results)
    max_avg = max(p["batting_average"] for p in results)
    max_obp = max(p["obp"] for p in results)
    max_slg = max(p["slg"] for p in results)
    avg_league_war = sum(p["war"] for p in results) / len(results)

    # First row of metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Max Home Runs in Batch", max_hr)
    with col2:
        st.metric("Max Career WAR", max_war)
    with col3:
        st.metric("Average Career WAR", round(avg_league_war, 1))

    # Second row of metrics for slash line
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Highest Batting Average", f"{max_avg:.3f}")
    with col5:
        st.metric("Highest OBP", f"{max_obp:.3f}")
    with col6:
        st.metric("Highest SLG", f"{max_slg:.3f}")

    st.markdown("---")
    st.subheader("Simulated Player Dossiers (Chronological Order)")
    st.caption("Presented in the exact order generated by the simulation engine.")

    # Render each player in the chronological order they were simulated
    for player in results:
        title = f"{player['name']} — {player['position']} ({player['tier']})"
        with st.expander(title):
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Career HRs", player["home_runs"])
                st.metric("Career Hits", player["hits"])
            with c2:
                st.metric("Career WAR", player["war"])
                st.metric("Batting Average", f"{player['batting_average']:.3f}")
            with c3:
                st.metric("Career OPS", f"{player['ops']:.3f}")
                st.metric("Total Games", player["games"])
            with c4:
                st.metric("Archetype", player["archetype"])
                st.metric("Hall of Fame Status", player["hof_verdict"])
else:
    st.info("Configure your batch size in the sidebar and click **Run Batch Simulation** to start.")
'''

with open("app.py", "w") as f:
    f.write(code_app_updated)

print("app.py updated with BA, OBP, and SLG metrics successfully!")
