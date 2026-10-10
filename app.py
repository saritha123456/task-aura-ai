import streamlit as st
import json
import os

st.set_page_config(page_title="TaskAura AI", page_icon="🎓", layout="centered")

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
st.caption("Intelligent Student Task Decomposition & Prioritizer")

# Sidebar Progress
st.sidebar.title("📊 Student Stats")
st.sidebar.metric("Total XP", f"{data['xp']} XP")
if data['xp'] >= 50:
    st.sidebar.success("🏆 Badge Unlocked: Productivity Master!")
else:
    st.sidebar.info("Complete tasks to unlock badges.")

if st.sidebar.button("🚨 Reset Progress"):
    save_data({"tasks": [], "xp": 0})
    st.rerun()

# Main Input Section
task_desc = st.text_input("What is your task or upcoming exam?", placeholder="e.g., Prepare for Social Science exam")
days_left = st.number_input("Days left until deadline:", min_value=0.1, value=2.0, step=0.5)

if st.button("✨ Decompose Task & Schedule"):
    if not task_desc.strip():
        st.warning("Please enter a task description.")
    else:
        # Intelligent automated step-by-step breakdown
        subtasks = [
            f"Review core chapters and key concepts for {task_desc}",
            "Make short revision notes and flashcards",
            "Solve practice questions or past papers",
            "Final quick review and active recall"
        ]
        
        # Priority calculation formula
        priority_score = round((8 * 4.0) / max(days_left, 0.1), 2)
        
        new_task = {
            "title": task_desc,
            "days": days_left,
            "score": priority_score,
            "subtasks": subtasks
        }
        
        data["tasks"].append(new_task)
        data["xp"] += 50
        save_data(data)
        
        st.success(f"Task successfully analyzed! Priority Score: {priority_score}")
        st.rerun()

st.divider()

# Display Schedule
st.subheader("📋 Your Priority Schedule & Subtasks")
if not data["tasks"]:
    st.info("No tasks added yet. Enter a task above to get started!")
else:
    for i, t in enumerate(data["tasks"]):
        st.markdown(f"### 📌 {t['title']}")
        st.caption(f"Deadline in {t['days']} days | Priority Score: {t['score']}")
        for sub in t["subtasks"]:
            st.checkbox(sub, key=f"sub_{i}_{sub}")
        st.write("---")