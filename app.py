import streamlit as st
import json
import os
import streamlit_antd_components as sac

st.set_page_config(page_title="TaskAura AI", page_icon="🎓", layout="centered")

# Custom CSS for the beautiful card interface
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
st.write("Transform overwhelmling exams or creative projects into a professional, automated, step-by-step milestone pipeline.")
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
            # Specific steps for PPT (requested in previous turn)
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
            # Fallback for generic tasks like writing (requested in previous turn)
            subtasks = [
                "Define core goals & break down requirements",
                "Draft initial outline or structural framework",
                "Execute main development/writing phase",
                "Final proofread, polish, & submission preparation"
            ]
        
        # Priority calculation formula
        priority_score = round((importance * 4.0) / max(days_left, 0.1), 2)
        
        new_task = {
            "title": task_desc,
            "days": days_left,
            "score": priority_score,
            "subtasks": subtasks,
            "completed": [False] * len(subtasks)
        }
        
        data["tasks"].append(new_task)
        # data["xp"] += 20  # Removed to focus XP only on step completion as per checklist requirement
        save_data(data)
        
        st.success(f"Goal analyzed and scheduled with priority score {priority_score}!")
        st.rerun()

st.divider()

# Display Schedule as a Visual Infographic-style Roadmap
st.subheader("📋 Professional Milestone Roadmap")
if not data["tasks"]:
    st.info("No tasks added yet. Enter a task above to generate your interactive roadmap!")
else:
    for i, t in enumerate(data["tasks"]):
        # Card container for task header
        st.markdown(f"""
        <div class="task-card">
            <h3 style="margin-top: 0; color: #1f2937;">📌 {t['title'].title()}</h3>
            <p style="color: #4b5563; margin-bottom: 5px;"><b>Deadline:</b> {t['days']} days left &nbsp;|&nbsp; <b>Priority Score:</b> <code>{t['score']}</code></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Check off milestones to progress:**")
        
        # Compatibility fix for older JSON data structures
        if "completed" not in t:
            t["completed"] = [False] * len(t["subtasks"])
            
        # Create beautiful timeline milestones using sac.steps
        # This replaces the generic checkbox checklist with a beautiful interactive timeline[cite: 3]
        sac_steps = []
        current_step_index = 0
        
        # Calculate progress and update completion status dynamically
        xp_earned_this_refresh = 0
        new_completion_status = []
        
        for j, sub in enumerate(t["subtasks"]):
            # Use columns to put a standard checkbox next to the description.
            # We must use standard checkboxes to allow XP calculation on click, sac.steps is static.
            c1, c2 = st.columns([0.1, 0.9])
            
            with c1:
                # Add extra padding/alignment fix to get checkbox in line with text
                st.markdown('<div style="margin-top: -3px;">', unsafe_allow_html=True)
                is_checked = st.checkbox("", value=t["completed"][j], key=f"sac_task_{i}_check_{j}")
                st.markdown('</div>', unsafe_allow_html=True)
                new_completion_status.append(is_checked)
                
                if is_checked and not t["completed"][j]:
                    xp_earned_this_refresh += 10 # 10 XP per step

            with c2:
                # Color code current vs completed vs pending steps for visual roadmap effect[cite: 1, 3]
                desc_style = "color: #4b5563;" # Pending
                if is_checked:
                    desc_style = "color: #9ca3af; text-decoration: line-through;" # Completed
                    current_step_index = max(current_step_index, j + 1)
                
                st.markdown(f'<p style="{desc_style} margin: 0 0 8px 0;">⏳ {sub}</p>', unsafe_allow_html=True)

        # Update XP and save if status changed (XP gamification requirement from turn 3)
        if new_completion_status != t["completed"]:
            t["completed"] = new_completion_status
            data["xp"] += xp_earned_this_refresh
            save_data(data)
            # Re-calculating badges based on new XP (Badge requirement from turn 1)
            # Not needed because sidebar handles it on refresh.
            st.rerun()

        # Render the overall vertical progress timeline graphic after the checklist[cite: 3]
        total_steps = len(t["subtasks"])
        items = []
        for index in range(total_steps):
            title_text = f"Step {index+1}"
            status = 'wait'
            icon = sac.AntIcon(name='clock-circle-o', size=18)
            
            if index < current_step_index:
                status = 'finish'
                icon = sac.AntIcon(name='check-circle-o', size=18)
            elif index == current_step_index:
                status = 'process'
                icon = sac.AntIcon(name='rocket', size=18)
                
            items.append(sac.StepsItem(title=title_text, status=status, icon=icon))
            
        sac.steps(
            items=items,
            current=current_step_index,
            direction='vertical',
            size='small',
            placement='right'
        )
            
        st.write("---")