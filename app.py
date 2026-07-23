import streamlit as st

st.set_page_config(page_title="Baseball Career Simulator", layout="wide")

st.title("⚾ Procedural Baseball Career Simulator")
st.markdown("Simulate (inaccurate) baseball player careers.")

# --- Define or Import Simulation Function ---
def run_batch_simulation(num_careers, power_nerf):
    """Placeholder simulation function. Replace this with your actual logic or import."""
    mock_results = []
    for i in range(num_careers):
        mock_results.append({
            "name": f"Player {i + 1}",
            "archetype": "Slugger" if i % 2 == 0 else "Contact Hitter",
            "HR": 200 + (i * 3),
            "hof_status": "Inducted" if i % 5 == 0 else "Eligible"
        })
    return mock_results

# --- Initialize Session State ---
if "simulation_results" not in st.session_state:
    st.session_state.simulation_results = None

# --- Sidebar Controls ---
st.sidebar.header("Simulation Settings")
num_careers = st.sidebar.slider("Careers to Simulate", min_value=10, max_value=500, value=100, step=10)
power_nerf = st.sidebar.slider("Post-30 Power Aging Multiplier", min_value=0.05, max_value=0.25, value=0.14, step=0.01)

# --- Main App Action ---
if st.button("Run Batch Simulation", type="primary"):
    with st.spinner("Simulating alternate timelines..."):
        # Call the simulation function and save it to session state
        st.session_state.simulation_results = run_batch_simulation(num_careers, power_nerf)

# --- Display Results if they exist in state ---
if st.session_state.simulation_results is not None:
    st.success("Simulation complete!")
    
    # Example metric
    max_hr = max([player['HR'] for player in st.session_state.simulation_results])
    st.metric(label="Max Home Runs Recorded", value=max_hr)
    
    # Render player dossiers / audit logs
    for player in st.session_state.simulation_results:
        with st.expander(f"{player['name']} - {player['archetype']}"):
            st.markdown(f"**Career HRs:** {player['HR']} | **HoF Status:** {player['hof_status']}")import streamlit as st

# Import your simulation functions from simulation.py
from simulation import run_batch_simulation

st.set_page_config(page_title="Baseball Career Simulator", layout="wide")

st.title("⚾ Procedural Baseball Career Simulator")
st.markdown("Simulate (inaccurate) baseball player careers.")

# --- Initialize Session State ---
if "simulation_results" not in st.session_state:
    st.session_state.simulation_results = None

# --- Sidebar Controls ---
st.sidebar.header("Simulation Settings")
num_careers = st.sidebar.slider("Careers to Simulate", min_value=10, max_value=500, value=100, step=10)
power_nerf = st.sidebar.slider("Post-30 Power Aging Multiplier", min_value=0.05, max_value=0.25, value=0.14, step=0.01)

# --- Main App Action ---
if st.button("Run Batch Simulation", type="primary"):
    with st.spinner("Simulating alternate timelines..."):
        # Call your simulation function and save it to session state
        st.session_state.simulation_results = run_batch_simulation(num_careers, power_nerf)

# --- Display Results if they exist in state ---
if st.session_state.simulation_results is not None:
    st.success("Simulation complete!")
    
    # Example metric (adjust keys to match your dictionary structure)
    max_hr = max([player['HR'] for player in st.session_state.simulation_results])
    st.metric(label="Max Home Runs Recorded", value=max_hr)
    
    # Render your player dossiers / audit logs
    for player in st.session_state.simulation_results:
        with st.expander(f"{player['name']} - {player['archetype']}"):
            st.markdown(f"**Career HRs:** {player['HR']} | **HoF Status:** {player['hof_status']}")
