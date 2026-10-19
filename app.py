import streamlit as st
import json
import os

st.set_page_config(page_title="TaskAura AI", page_icon="🎓", layout="centered")

# Custom CSS for modern UI
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
        border-left: 6px solid #6366f1;
        border-top: 1px solid #e5e7eb;
        border-right: 1px solid #e5e7eb;
        border-bottom: 1px solid #e5e7eb;
    }
    .rescue-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fee2e2 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #f59e0b;
        margin-bottom: 20px;
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
st.markdown("### *Intelligent Student Task Prioritizer & Anti-Procrastination Engine*")
st.divider()

# Sidebar Dashboard
st.sidebar.title("📊 Student Dashboard")
st.sidebar.metric("Total XP", f"{data['xp']} XP")

level = 1 + data['xp'] // 100
st.sidebar.metric("Student Level", f"Level {level}")

if data['xp'] >= 100:
    st.sidebar.success("🏆 Badge: Productivity Master")
else:
    st.sidebar.info("🎯 Complete milestones to unlock badges!")

if st.sidebar.button("🚨 Reset Progress"):
    save_data({"tasks": [], "xp": 0})
    st.rerun()

# Tabs Layout
tab1, tab2, tab3 = st.tabs(["📊 Priority Master List", "🗺️ Step-by-Step Roadmaps", "⚡ Anti-Procrastination Engine"])

with tab1:
    st.subheader("✨ Add Any Assignment, Goal, or Task")
    task_desc = st.text_input("What is your goal?", placeholder="e.g., gym workout, clean room, physics homework...", key="input_task")

    col1, col2 = st.columns(2)
    with col1:
        days_left = st.number_input("Days left until deadline:", min_value=0.1, value=2.0, step=0.5, key="input_days")
    with col2:
        importance = st.slider("Importance Level (1-10):", min_value=1, max_value=10, value=8, key="input_imp")

    if st.button("🚀 Analyze & Prioritize Task"):
        if not task_desc.strip():
            st.warning("Please enter a goal description first.")
        else:
            lower_desc = task_desc.strip().lower()
            existing_titles = [t["title"].strip().lower() for t in data["tasks"]]
            
            if lower_desc in existing_titles:
                st.warning("⚠️ This task is already in your priority list!")
            else:
                # Intelligent Task Categorization
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
                elif any(word in lower_desc for word in ["exam", "test", "quiz", "midterm", "finals", "study", "homework"]):
                    subtasks = [
                        "Review core textbook chapters & high-weightage topics",
                        "Create structured flashcards & short summary notes",
                        "Solve practice questions, sample papers, or past quizzes",
                        "Final active recall session & timed mock review"
                    ]
                elif any(word in lower_desc for word in ["gym", "workout", "fitness", "exercise", "run", "training"]):
                    subtasks = [
                        "Pack gear, water bottle, and prepare workout playlist",
                        "Dynamic warm-up and mobility stretches",
                        "Execute main workout routine with proper form",
                        "Cool down, static stretching, and post-workout hydration"
                    ]
                else:
                    subtasks = [
                        "Define core objective and gather necessary resources",
                        "Break down the first major milestone or section",
                        "Execute primary work session with zero distractions",
                        "Final review, polish, and completion check"
                    ]
                
                priority_score = round((importance * 4.0) / max(days_left, 0.1), 2)
                
                new_task = {
                    "title": task_desc.strip(),
                    "days": days_left,
                    "score": priority_score,
                    "subtasks": subtasks,
                    "completed": [False] * len(subtasks)
                }
                
                data["tasks"].append(new_task)
                save_data(data)
                st.success("Task added successfully! Check the Priority List below.")
                st.rerun()

    st.divider()
    st.subheader("🔥 Ranked Priority Schedule")
    if not data["tasks"]:
        st.info("No tasks added yet. Add a task above to see your ranked priority queue.")
    else:
        sorted_tasks = sorted(data["tasks"], key=lambda x: x["score"], reverse=True)
        for idx, t in enumerate(sorted_tasks):
            st.markdown(f"""
            <div class="task-card">
                <h3 style="margin-top: 0; color: #1f2937;">#{idx+1}: {t['title'].title()}</h3>
                <p style="color: #4b5563; margin-bottom: 0;"><b>Priority Score:</b> <code>{t['score']}</code> &nbsp;|&nbsp; <b>Deadline:</b> {t['days']} days left</p>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.subheader("🗺️ Interactive Milestone Roadmaps")
    if not data["tasks"]:
        st.info("No tasks found. Add a task in the first tab to view its step-by-step roadmap!")
    else:
        for i, t in enumerate(data["tasks"]):
            st.markdown(f"""
            <div class="task-card">
                <h3 style="margin-top: 0; color: #1f2937;">📌 {t['title'].title()}</h3>
                <p style="color: #4b5563; margin-bottom: 15px;"><b>Priority Score:</b> <code>{t['score']}</code></p>
            """, unsafe_allow_html=True)
            
            if "completed" not in t or len(t["completed"]) != len(t["subtasks"]):
                t["completed"] = [False] * len(t["subtasks"])
                
            xp_earned = 0
            new_status = []
            
            for j, sub in enumerate(t["subtasks"]):
                step_num = j + 1
                is_checked = st.checkbox(f"Phase {step_num}: {sub}", value=t["completed"][j], key=f"tab2_task_{i}_check_{j}")
                new_status.append(is_checked)
                if is_checked and not t["completed"][j]:
                    xp_earned += 15

            if new_status != t["completed"]:
                t["completed"] = new_status
                data["xp"] += xp_earned
                save_data(data)
                st.rerun()
                
            st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.subheader("⚡ Feeling sluggish? No worries, let's break it one step at a time.")
    st.markdown("When you feel paralyzed or overwhelmed by a task, don't try to finish it all at once. Let's isolate the very first micro-action.")
    
    if not data["tasks"]:
        st.info("Add a task in Tab 1 first so we can break it down for you!")
    else:
        task_titles = [t["title"] for t in data["tasks"]]
        selected_task_title = st.selectbox("Select the task you are avoiding:", task_titles, key="rescue_select")
        
        task_idx = next((i for i, t in enumerate(data["tasks"]) if t["title"] == selected_task_title), None)
        
        if task_idx is not None:
            target_task = data["tasks"][task_idx]
            
            if "completed" not in target_task or len(target_task["completed"]) != len(target_task["subtasks"]):
                target_task["completed"] = [False] * len(target_task["subtasks"])
                
            all_done = all(target_task["completed"])
            
            if all_done:
                st.success("🎉 Incredible job! All phases for this task are already completed. You crushed it!")
            else:
                first_uncompleted_idx = target_task["completed"].index(False)
                micro_step = target_task["subtasks"][first_uncompleted_idx]
                
                st.markdown(f"""
                <div class="rescue-box">
                    <h3 style="margin-top: 0; color: #b45309;">🔬 Your 5-Minute Micro-Action Plan</h3>
                    <p style="font-size: 16px; color: #78350f;">Instead of thinking about the entire assignment, your *only* goal right now is:</p>
                    <p style="font-size: 18px; font-weight: bold; color: #92400e;">👉 Phase {first_uncompleted_idx + 1}: {micro_step}</p>
                    <hr style="border-color: #f6d860;">
                    <p style="margin-bottom: 0; font-size: 14px; color: #78350f;"><b>Rule of Thumb:</b> Set a timer for 5 minutes. Take that first small step to break the paralysis!</p>
                </div>
                """, unsafe_allow_html=True)
                
                confirmed = st.checkbox("✅ I confirm I have focused on and completed this 5-minute micro-step", key=f"confirm_{task_idx}_{first_uncompleted_idx}")
                
                lock_key = f"lock_{task_idx}_{first_uncompleted_idx}"
                if lock_key not in st.session_state:
                    st.session_state[lock_key] = False

                if st.button("✨ Claim XP & Advance", disabled=not confirmed or st.session_state[lock_key]):
                    st.session_state[lock_key] = True
                    if not target_task["completed"][first_uncompleted_idx]:
                        target_task["completed"][first_uncompleted_idx] = True
                        data["xp"] += 15
                        save_data(data)
                        st.balloons()
                        st.success(f"🎉 +15 XP Claimed! Advanced to the next phase.")
                        st.rerun()