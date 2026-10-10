import streamlit as st
import json
import os

st.set_page_config(page_title="TaskAura AI", page_icon="🎓", layout="centered")

# Custom CSS for a professional step-by-step UI
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
    .step-box {
        background-color: #f8fafc;
        padding: 10px 14px;
        border-radius: 8px;
        border-left: 4px solid #a855f7;
        margin-bottom: 8px;
        font-size: 14px;
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
st.write("Transform any exam, physical project, or PowerPoint presentation into an automated step-by-step milestone pipeline.")
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

# Main Input Section
st.subheader("✨ Add New Task, Exam, or PPT Presentation")
task_desc = st.text_input("What do you need to accomplish?", placeholder="e.g., create ppt on artificial intelligence")

col1, col2 = st.columns(2)
with col1:
    days_left = st.number_input("Days left until deadline:", min_value=0.1, value=2.0, step=0.5)
with col2:
    importance = st.slider("Importance Level (1-10):", min_value=1, max_value=10, value=8)

if st.button("🚀 Run AI Decomposition Engine"):
    if not task_desc.strip():
        st.warning("Please enter a task description first.")
    else:
        # Smart Context-Aware Decomposition for PPT, Exams, and Projects
        lower_desc = task_desc.lower()
        if any(word in lower_desc for word in ["ppt", "presentation", "slides", "slide deck", "powerpoint"]):
            subtasks = [
                "Step 1: Outline the slide deck structure and key headings",
                "Step 2: Collect essential info, facts, and talking points",
                "Step 3: Verify data accuracy and filter key highlights",
                "Step 4: Customize slide layouts and content blocks",
                "Step 5: Beautify with icons, color themes, and visuals"
            ]
        elif any(word in lower_desc for word in ["project", "poster", "model", "chart", "craft", "exhibition"]):
            subtasks = [
                "Step 1: Research core theme and outline project objectives",
                "Step 2: Gather required resources, materials, or reference data",
                "Step 3: Draft/build the core project content or prototype",
                "Step 4: Finalize presentation, label sections, and review guidelines"
            ]
        elif any(word in lower_desc for word in ["exam", "test", "quiz", "midterm", "finals"]):
            subtasks = [
                "Step 1: Review core textbook chapters and high-weightage topics",
                "Step 2: Create structured flashcards and short summary notes",
                "Step 3: Solve practice questions, sample papers, or past quizzes",
                "Step 4: Final active recall session and timed mock review"
            ]
        else:
            subtasks = [
                "Step 1: Define core goals and break down requirements",
                "Step 2: Draft initial outline or structural framework",
                "Step 3: Execute main development/writing phase",
                "Step 4: Final proofread, polish, and submission preparation"
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
        
        st.success(f"Successfully decomposed! Priority Score: {priority_score}")
        st.rerun()

st.divider()

# Display Schedule as a Visual Step-by-Step Pipeline
st.subheader("📋 Intelligent Step-by-Step Roadmap")
if not data["tasks"]:
    st.info("No tasks added yet. Enter a task above to generate your milestone pipeline!")
else:
    for i, t in enumerate(data["tasks"]):
        st.markdown(f"""
        <div class="task-card">
            <h3 style="margin-top: 0; color: #1f2937;">📌 {t['title'].title()}</h3>
            <p style="color: #4b5563; margin-bottom: 15px;"><b>Deadline:</b> {t['days']} days left &nbsp;|&nbsp; <b>Priority Score:</b> <code>{t['score']}</code></p>
        """, unsafe_allow_html=True)
        
        st.markdown("**Milestone Progression:**")
        for sub in t["subtasks"]:
            st.markdown(f'<div class="step-box">⏳ {sub}</div>', unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)