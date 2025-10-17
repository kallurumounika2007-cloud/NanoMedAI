import sys, os, time
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
# threading import removed as it was only used for the voice assistant.

# Project imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simulator.simulate_glucose import generate_glucose_trace
from models.controller import autonomous_controller
from models.rl_agent import RLAgent

# Page config + CSS
st.set_page_config(page_title="NanoMed AI Shooter", layout="wide", page_icon="🤖")
st.markdown("""
<style>
h1 { color: #00ffff; font-family: 'Courier New'; text-align:center; font-size:48px; font-weight:bold; }
h3 { color: #ff69b4; font-family: Arial, sans-serif; font-weight:bold; }
.stApp { background-color: #0f111a; color: #ffffff; }
.sidebar .sidebar-content { background-color: #1a1b2a; }
</style>
""", unsafe_allow_html=True)
st.markdown("<h1>🚀 NanoMed AI: Shooting Nanobot 3D Simulation</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Simulation Controls")
hours = st.sidebar.slider("Simulation Duration (hours)", 1, 24, 6)
interval = st.sidebar.slider("Data Interval (minutes)", 1, 10, 5)
simulate_button = st.sidebar.button("Run Simulation")
st.sidebar.subheader("Scenario Triggers")
meal = st.sidebar.checkbox("Meal")
exercise = st.sidebar.checkbox("Exercise")
stress = st.sidebar.checkbox("Stress")
sleep = st.sidebar.checkbox("Sleep")
st.sidebar.subheader("What-If Inputs")
carbs = st.sidebar.number_input("Carbs intake (g)", 0, 200, 50)
exercise_input = st.sidebar.number_input("Exercise intensity (0-10)", 0, 10, 5)
stress_input = st.sidebar.number_input("Stress level (0-10)", 0, 10, 3)
# Voice Assistant section removed entirely to prevent runtime errors.

# RL Agents
agents = {"Nanobot A": RLAgent(), "Nanobot B": RLAgent()}

# Run Simulation
if simulate_button:
    scenarios = {"meal": meal, "exercise": exercise, "stress": stress, "sleep": sleep}
    df = generate_glucose_trace(hours, interval, scenarios)
    
    # Apply What-If effects
    df["Glucose"] += carbs * 0.2 - exercise_input * 0.5 + stress_input * 0.3

    # Rolling prediction
    pred_glucose = df["Glucose"].rolling(5).mean().fillna(df["Glucose"].iloc[0])
    current_glucose = df["Glucose"].iloc[0]

    # Autonomous dose
    auto_dose = autonomous_controller(pred_glucose.tolist(), current_glucose)

    # Multi-agent RL doses
    doses = {}
    for name, agent in agents.items():
        dose = agent.decide_dose(pred_glucose.tolist())
        doses[name] = dose
        agent.train(pred_glucose.tolist(), dose, epochs=1)

    # Layout
    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown("<h3>📈 3D Glucose & Shooting Nanobot Simulation</h3>", unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(
            x=df.index, y=[0]*len(df), z=df["Glucose"],
            mode='lines+markers', line=dict(color='cyan', width=4),
            marker=dict(size=3), name="Glucose Trend"
        ))
        plot_placeholder = st.empty()
        for i in range(len(df)):
            fig.data = fig.data[:1]
            for j, (name, dose) in enumerate(doses.items()):
                fig.add_trace(go.Scatter3d(
                    x=[i], y=[j], z=[df["Glucose"].iloc[i]],
                    mode='markers',
                    marker=dict(size=10, color='magenta'),
                    name=name
                ))
                color = 'cyan'
                if dose > 2: color='red'
                elif dose > 1: color='orange'
                elif dose > 0.5: color='yellow'
                fig.add_trace(go.Scatter3d(
                    x=[i, i], y=[j, j], z=[df["Glucose"].iloc[i], df["Glucose"].iloc[i] + dose],
                    mode='lines+markers',
                    line=dict(color=color, width=6),
                    marker=dict(size=4, color=color),
                    name=f'{name} Dose'
                ))
            plot_placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(0.05)

    with col2:
        st.markdown("<h3>🤖 AI Decisions & Metrics</h3>", unsafe_allow_html=True)
        st.metric("Current Glucose", f"{current_glucose:.2f} mg/dL")
        st.metric("Autonomous Dose", f"{auto_dose:.2f} U")
        for name, dose in doses.items():
            st.metric(f"{name} Dose", f"{dose:.2f} U")
        log = []
        for k,v in scenarios.items():
            if v: log.append(f"{k.capitalize()} scenario applied")
        if carbs>0: log.append(f"Carbs input → {carbs}g")
        if exercise_input>0: log.append(f"Exercise intensity → {exercise_input}")
        if stress_input>0: log.append(f"Stress level → {stress_input}")
        if not log: log.append("Normal simulation")
        for entry in log: st.info(entry)
        st.download_button(
            label="📥 Download Simulation Data",
            data=df.to_csv(index=False),
            file_name="nanobot_simulation.csv",
            mime="text/csv"
        )

st.markdown("<p style='text-align:center;color:gray'>NanoMed AI | Real-Time 3D Nanobot Simulation</p>", unsafe_allow_html=True)
