# 🚀 NanoMedAI: Futuristic Diabetes Nanobot Simulation

**NanoMedAI** is a real-time AI-powered simulator for glucose control using autonomous nanobots.  
It combines advanced AI controllers, Reinforcement Learning, and 3D visualization to mimic futuristic medical nanotechnology.

---

## 🌟 Features
- **Real-Time Glucose Simulation:** Simulates blood glucose levels with multiple triggers like meals, exercise, stress, and sleep.  
- **Autonomous AI Controller:** AI predicts glucose changes and administers micro-doses automatically.  
- **Reinforcement Learning Agent:** Learns and optimizes dosing strategies.  
- **3D Nanobot Visualization:** Animated nanobots “shoot” micro-doses along the glucose curve.  
- **Scenario Logging:** Tracks events and interventions in real-time.  
- **Export & Share:** Simulation results can be exported (CSV) for analysis.  
- **Voice Assistance:** Real-time voice updates on glucose and doses.

---

## 📂 Project Structure
NanoMedAI/
├── simulator/ # Glucose simulation scripts
├── models/ # AI controller and RL agent
├── ui/ # Streamlit web interface
├── assets/ # Animations and small images
├── data/ # Optional datasets
├── requirements.txt # Python dependencies
└── README.md # Project documentation  


---

## 💻 Installation & Run
1. Clone the repo:  
   ```bash
   git clone https://github.com/kallurumounika2007-cloud/NanoMedAI.git


python -m venv myenv
myenv\Scripts\activate   # Windows
source myenv/bin/activate  # Mac/Linux

pip install -r requirements.txt

streamlit run ui/app.py

