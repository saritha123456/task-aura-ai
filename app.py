import streamlit as st
import json
import os

st.set_page_config(page_title="TaskAura AI", page_icon="🎓", layout="centered")

# Custom CSS for infographic-style steps and modern card styling
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
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border-left: 6px solid #6366f1;
        border-top: 1px solid #e5e7eb;
        border-right: 1px solid #e5e7eb;
        border-bottom: 1px solid #e5e7eb;
    }
    .infographic-step {
        display: flex;
        align-items: center;
        background: #f8fafc;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 4px solid #a855f7;
        font-weight: 500;
        color: #334155;
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
st.write("Transform any exam, presentation, or project into an interactive, infographic-style milestone roadmap.")
st.divider()

# Sidebar Dashboard
st.sidebar.title("📊 Student Dashboard")
st.sidebar.metric("Total XP", f"{data['xp']} XP")

level = 1 + data['xp'] // 100
st.sidebar.metric("Student Level", f"Level {level}")

if data['xp'] >= 100:
    st.sidebar.success("🏆 Badge: Productivity Master")
else:
    st.sidebar.info("🎯 Complete milestones to earn XP & unlock badges!")

if st.sidebar.button("🚨 Reset Progress"):
    save_data({"tasks": [], "xp": 0})
    st.rerun()

# Main Input Section
st.subheader("✨ Add New Assignment, Exam, or Project")
task_desc = st.text_input("What is your goal?", placeholder="e.g., complete social project on say no to drugs")

col1, col2 = st.columns(2)
with col1:
    days_left = st.number_input("Days left until deadline:", min_value=0.1, value=2.0, step=0.5)
with col2:
    importance = st.slider("Importance Level (1-10):", min_value=1, max_value=10, value=8)

if st.button("🚀 Run AI Decomposition Engine"):
    if not task_desc.strip():
        st.warning("Please enter a goal description first.")
    else:
        # Smart Context-Aware Decomposition
        lower_desc = task_desc.lower()
        if any(word in lower_desc for word in ["ppt", "presentation", "slides", "slide deck", "powerpoint"]):
            subtasks = [
                "Outline slide deck structure & key headings",
                "Collect essential info, facts, & talking points",
                "Verify data accuracy & filter key highlights",
                "Customize slide layouts & content blocks",
                "Beautify with icons, color themes, & visuals"
            ]
        elif any(word in lower_desc for word in ["project", "poster", "model", "chart", "craft", "exhibition"]):
            subtasks = [
                "Research core theme & outline project objectives",
                "Gather required resources, materials, or reference data",
                "Draft/build the core project content or prototype",
                "Finalize presentation, label sections, & guidelines review"
            ]
        elif any(word in lower_desc for word in ["exam", "test", "quiz", "midterm", "finals"]):
            subtasks = [
                "Review core textbook chapters & high-weightage topics",
                "Create structured flashcards & short summary notes",
                "Solve practice questions, sample papers, or past quizzes",
                "Final active recall session & timed mock review"
            ]
        else:
            subtasks = [
                "Define core goals & break down requirements",
                "Draft initial outline or structural framework",
                "Execute main development/writing phase",
                "Final proofread, polish, & submission preparation"
            ]
        
        priority_score = round((importance * 4.0) / max(days_left, 0.1), 2)
        
        new_task = {
            "title": task_desc,
            "days": days_left,
            "score": priority_score,
            "subtasks": subtasks,
            "completed": [False] * len(subtasks)
        }
        
        data["tasks"].append(new_task)
        save_data(data)
        
        st.success(f"Goal analyzed and scheduled with priority score {priority_score}!")
        st.rerun()

st.divider()

# Display Schedule as an Infographic Checklist Roadmap
st.subheader("📋 Professional Milestone Roadmap")
if not data["tasks"]:
    st.info("No tasks added yet. Enter a task above to generate your roadmap!")
else:
    for i, t in enumerate(data["tasks"]):
        st.markdown(f"""
        <div class="task-card">
            <h3 style="margin-top: 0; color: #1f2937;">📌 {t['title'].title()}</h3>
            <p style="color: #4b5563; margin-bottom: 15px;"><b>Deadline:</b> {t['days']} days left &nbsp;|&nbsp; <b>Priority Score:</b> <code>{t['score']}</code></p>
        """, unsafe_allow_html=True)
        
        st.markdown("**Interactive Infographic Milestones:**")
        
        if "completed" not in t:
            t["completed"] = [False] * len(t["subtasks"])
            
        xp_earned_this_refresh = 0
        new_completion_status = []
        
        for j, sub in enumerate(t["subtasks"]):
            # Clean layout for checkbox + roadmap step text
            c1, c2 = st.columns([0.08, 0.92])
            with c1:
                is_checked = st.checkbox("", value=t["completed"][j], key=f"clean_task_{i}_check_{j}")
                new_completion_status.append(is_checked)
                if is_checked and not t["completed"][j]:
                    xp_earned_this_refresh += 10
            with c2:
                step_num = j + 1
                if is_checked:
                    st.markdown(f"<div style='background: #f1f5f9; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #10b981; color: #9ca3af; text-decoration: line-through;'><b>Phase {step_num}:</b> {sub}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='background: #f8fafc; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #6366f1; color: #334155;'><b>Phase {step_num}:</b> {sub}</div>", unsafe_allow_html=True)

        if new_completion_status != t["completed"]:
            t["completed"] = new_completion_status
            data["xp"] += xp_earned_this_refresh
            save_data(data)
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)