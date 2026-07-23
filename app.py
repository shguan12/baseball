import streamlit as st
# Make sure simulation.py is in the same directory and contains run_batch_simulation
from simulation import run_batch_simulation

# --- Page Configuration ---
st.set_page_config(
    page_title="Baseball Career Simulator", 
    page_icon="⚾", 
    layout="wide"
)

# --- Session State Initialization ---
if "simulation_results" not in st.session_state:
    st.session_state.simulation_results = None

# --- UI Header ---
st.title("⚾ Procedural Baseball Career Simulator")
st.markdown("Simulate alternate timelines and inaccurate baseball player careers.")

# --- Sidebar Controls ---
st.sidebar.header("Simulation Settings")
num_careers = st.sidebar.slider("Careers to Simulate", min_value=10, max_value=500, value=100, step=10)
power_nerf = st.sidebar.slider("Post-30 Power Aging Multiplier", min_value=0.05, max_value=0.25, value=0.14, step=0.01)

# --- Action Trigger ---
if st.sidebar.button("Run Batch Simulation", type="primary"):
    # Clear any potential caching issues by forcing a clean execution call
    with st.spinner("Simulating alternate timelines..."):
        # Run the simulation function fresh
        results = run_batch_simulation(num_careers, power_nerf)
        # Store directly into session state
        st.session_state.simulation_results = results

# --- Main Results Display Area ---
if st.session_state.simulation_results:
    st.success("Simulation complete!")
    
    results = st.session_state.simulation_results
    
    # Top-level summary metric
    if len(results) > 0 and 'HR' in results[0]:
        max_hr = max(player['HR'] for player in results)
        st.metric(label="Max Home Runs Recorded Across Batch", value=max_hr)
    
    st.markdown("---")
    st.subheader("Player Dossiers (Chronological Order)")

    # Render players precisely in the order they were simulated (no sorting)
    for player in results:
        # Fallback keys safely handled using .get() to prevent KeyErrors
        name = player.get('name', 'Unknown Player')
        archetype = player.get('archetype', 'Unknown Archetype')
        hr = player.get('HR', 0)
        hof = player.get('hof_status', 'Pending')
        
        expander_label = f"{name} — {archetype} | HR: {hr} | HoF: {hof}"
        
        with st.expander(expander_label):
            # If your original script generated a full text dossier string:
            if 'dossier_text' in player:
                st.code(player['dossier_text'], language="text")
            
            # Otherwise, render individual stats cleanly in columns
            else:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Career Home Runs", hr)
                    st.metric("Hits", player.get('H', 0))
                with col2:
                    st.metric("Batting Average", player.get('BA', '.000'))
                    st.metric("WAR", player.get('WAR', 0.0))
                with col3:
                    st.metric("Hall of Fame Status", hof)
                    st.metric("Peak Years", player.get('peak_years', 'N/A'))
                
                # Full career text log if available
                if 'yearly_log' in player:
                    st.text(player['yearly_log'])
else:
    st.info("Adjust your settings in the sidebar and click **Run Batch Simulation** to begin.")
