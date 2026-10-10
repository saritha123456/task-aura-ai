import streamlit as st
import json
import os

st.set_page_config(page_title="TaskAura AI", page_icon="🎓", layout="centered")

# Custom CSS for a beautiful, modern look
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.6rem 1rem;
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3);
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
    div.stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
    }
    .task-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
        border-left: 5px solid #6366f1;
        border-top: 1px solid #e5e7eb;
        border-right: 1px solid #e5e7eb;
        border-bottom: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "task_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"tasks": [], "xp": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# App Header
st.title("🎓 TaskAura AI")
st.markdown("### *Intelligent Student Task Decomposition & Prioritizer*")
st.write("Transform overwhelming assignments and exam preparation into structured, bite-sized steps instantly.")
st.divider()

# Sidebar Dashboard
st.sidebar.title("📊 Student Dashboard")
st.sidebar.metric("Total XP", f"{data['xp']} XP")

level = 1 + data['xp'] // 100
st.sidebar.metric("Student Level", f"Level {level}")

if data['xp'] >= 50:
    st.sidebar.success("🏆 Badge: Productivity Master")
else:
    st.sidebar.info("🎯 Complete tasks to unlock badges!")

if st.sidebar.button("🚨 Reset Progress"):
    save_data({"tasks": [], "xp": 0})
    st.rerun()

# Main Input Form Container
st.subheader("✨ Add New Assignment or Exam")
task_desc = st.text_input("What do you need to study or complete?", placeholder="e.g., Prepare for Physics chapter 3 exam")

col1, col2 = st.columns(2)
with col1:
    days_left = st.number_input("Days left until deadline:", min_value=0.1, value=2.0, step=0.5)
with col2:
    importance = st.slider("Importance Level (1-10):", min_value=1, max_value=10, value=8)

if st.button("🚀 Analyze & Decompose Task"):
    if not task_desc.strip():
        st.warning("Please enter a task description first.")
    else:
        # Intelligent automated step-by-step breakdown
        subtasks = [
            f"Review core concepts and summaries for {task_desc}",
            "Create short revision flashcards or mind maps",
            "Solve practice problems or previous year questions",
            "Final active recall session and timed review"
        ]
        
        # Priority calculation formula
        priority_score = round((importance * 4.0) / max(days_left, 0.1), 2)
        
        new_task = {
            "title": task_desc,
            "days": days_left,
            "score": priority_score,
            "subtasks": subtasks
        }
        
        data["tasks"].append(new_task)
        data["xp"] += 50
        save_data(data)
        
        st.success(f"Successfully scheduled! Priority Score: {priority_score}")
        st.rerun()

st.divider()

# Display Schedule
st.subheader("📋 Your Priority Schedule & Subtasks")
if not data["tasks"]:
    st.info("No tasks added yet. Enter a task above to generate your smart schedule!")
else:
    for i, t in enumerate(data["tasks"]):
        st.markdown(f"""
        <div class="task-card">
            <h3 style="margin-top: 0; color: #1f2937;">📌 {t['title']}</h3>
            <p style="color: #4b5563; margin-bottom: 0;"><b>Deadline:</b> {t['days']} days left &nbsp;|&nbsp; <b>Priority Score:</b> <code>{t['score']}</code></p>
        </div>
        """, unsafe_allow_html=True)
        
        for sub in t["subtasks"]:
            st.checkbox(sub, key=f"sub_{i}_{sub}")
        st.write("")