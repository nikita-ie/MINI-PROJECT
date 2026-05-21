import streamlit as st
import pandas as pd

from modules.expense_splitter import show_expense_splitter
from modules.health_tracker import show_health_tracker
from modules.assignment_tracker import show_assignment_reminder
from utils.file_handler import load_data

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="CampusSync",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# GLOBAL CSS
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
}

/* ── Background ── */
.stApp {
    background:
        radial-gradient(ellipse at 0% 0%,   rgba(30,58,138,0.6)  0%, transparent 50%),
        radial-gradient(ellipse at 100% 0%,  rgba(124,58,237,0.5) 0%, transparent 50%),
        radial-gradient(ellipse at 0% 100%,  rgba(5,150,105,0.4)  0%, transparent 50%),
        radial-gradient(ellipse at 100% 100%,rgba(220,38,38,0.2)  0%, transparent 50%),
        linear-gradient(160deg, #020617 0%, #0f172a 60%, #1a1040 100%);
    min-height: 100vh;
}

/* ── Remove default Streamlit padding ── */
.block-container {
    padding: 1.5rem 3rem 3rem 3rem !important;
    max-width: 1400px;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── NAVBAR ── */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 0 30px 0;
    margin-bottom: 10px;
}
.navbar-brand {
    display: flex;
    align-items: center;
    gap: 14px;
}
.navbar-logo {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4);
}
.navbar-title {
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff, #c7d2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
}
.navbar-subtitle {
    font-size: 13px;
    color: #94a3b8;
    font-weight: 400;
    margin-top: 2px;
}
.navbar-badge {
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.4);
    color: #a5b4fc;
    padding: 6px 16px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 600;
}

/* ── HERO BANNER ── */
.hero-banner {
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.1));
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 24px;
    padding: 40px 50px;
    margin-bottom: 36px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 30px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(139,92,246,0.2), transparent 70%);
    border-radius: 50%;
}
.hero-left { flex: 1; }
.hero-tag {
    display: inline-block;
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.35);
    color: #a5b4fc;
    padding: 4px 14px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 16px;
}
.hero-heading {
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.15;
    margin-bottom: 14px;
    letter-spacing: -1px;
}
.hero-heading span {
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-desc {
    font-size: 16px;
    color: #94a3b8;
    line-height: 1.7;
    max-width: 520px;
}
.hero-right {
    display: flex;
    gap: 16px;
    flex-shrink: 0;
}
.hero-stat {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px;
    padding: 20px 28px;
    text-align: center;
    min-width: 110px;
}
.hero-stat-number {
    font-size: 32px;
    font-weight: 800;
    color: white;
    line-height: 1;
}
.hero-stat-label {
    font-size: 12px;
    color: #64748b;
    margin-top: 6px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── SECTION HEADING ── */
.section-heading {
    font-size: 13px;
    font-weight: 700;
    color: #64748b;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 18px;
    margin-top: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.06);
}

/* ── MODULE CARDS ── */
.module-card {
    border-radius: 22px;
    padding: 28px 24px 24px 24px;
    color: white;
    position: relative;
    overflow: hidden;
    min-height: 220px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.module-card:hover {
    transform: translateY(-6px);
}
.module-card::after {
    content: '';
    position: absolute;
    bottom: -30px; right: -30px;
    width: 120px; height: 120px;
    border-radius: 50%;
    background: rgba(255,255,255,0.07);
}
.card-expense  { background: linear-gradient(145deg, #3b82f6 0%, #1d4ed8 100%); box-shadow: 0 8px 30px rgba(59,130,246,0.35); }
.card-health   { background: linear-gradient(145deg, #10b981 0%, #047857 100%); box-shadow: 0 8px 30px rgba(16,185,129,0.35); }
.card-assign   { background: linear-gradient(145deg, #a855f7 0%, #7c3aed 100%); box-shadow: 0 8px 30px rgba(168,85,247,0.35); }

.card-top { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 20px; }
.card-emoji-wrap {
    width: 56px; height: 56px;
    background: rgba(255,255,255,0.2);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px;
    backdrop-filter: blur(4px);
}
.card-arrow { font-size: 20px; opacity: 0.5; }
.card-name {
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 8px;
    letter-spacing: -0.3px;
}
.card-desc {
    font-size: 13px;
    opacity: 0.8;
    line-height: 1.5;
    margin-bottom: 18px;
}
.card-pill {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    border-radius: 50px;
    padding: 5px 14px;
    font-size: 12px;
    font-weight: 600;
    backdrop-filter: blur(4px);
}

/* ── OPEN BUTTON ── */
div.stButton > button {
    width: 100%;
    height: 48px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.1) !important;
    font-size: 14px;
    font-weight: 600;
    background: rgba(255,255,255,0.06) !important;
    color: #e2e8f0 !important;
    transition: all 0.2s ease;
    letter-spacing: 0.3px;
    margin-top: 8px;
}
div.stButton > button:hover {
    background: rgba(255,255,255,0.14) !important;
    border-color: rgba(255,255,255,0.25) !important;
    color: white !important;
    transform: translateY(-1px);
}

/* ── REMINDERS PANEL ── */
.reminders-panel {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 28px 32px 16px 32px;
    margin-top: 4px;
}
.reminders-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 22px;
    padding-bottom: 18px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.reminders-icon {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, #f59e0b, #ea580c);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
}
.reminders-title {
    font-size: 18px;
    font-weight: 700;
    color: white;
}
.reminders-subtitle {
    font-size: 12px;
    color: #64748b;
    margin-top: 3px;
}
.reminder-empty {
    text-align: center;
    color: #475569;
    font-size: 15px;
    padding: 24px 0;
}
.done-task {
    color: #334155;
    text-decoration: line-through;
    font-size: 14px;
    padding: 10px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── BACK BUTTON (sub-pages) ── */
.page-title-bar {
    font-size: 26px;
    font-weight: 700;
    color: white;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}

/* ── Checkbox tweak ── */
.stCheckbox label {
    color: #cbd5e1 !important;
    font-size: 14px !important;
}
[data-testid="stCheckbox"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 10px 14px !important;
    margin-bottom: 8px !important;
}
[data-testid="stCheckbox"]:hover {
    background: rgba(255,255,255,0.08);
}

hr { border-color: rgba(255,255,255,0.07) !important; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

expenses    = load_data("data/expenses.csv")
health      = load_data("data/health.csv")
assignments = load_data("data/assignments.csv")

# =====================================================
# SESSION STATE
# =====================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"
if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = []

# =====================================================
# QUICK STATS FOR HERO
# =====================================================

total_expenses  = len(expenses)  if not expenses.empty  else 0
total_medicines = len(health)    if not health.empty    else 0
pending_count   = (
    len(assignments[assignments["Status"] == "Pending"])
    if (not assignments.empty and "Status" in assignments.columns)
    else 0
)

# =====================================================
# HOME PAGE
# =====================================================

if st.session_state.page == "Home":

    # ── NAVBAR ──────────────────────────────────────
    st.markdown("""
<div class="navbar">
<div class="navbar-brand">
<div class="navbar-logo">🎓</div>
<div>
<div class="navbar-title">CampusSync</div>
<div class="navbar-subtitle">Smart Student Life Management</div>
</div>
</div>
<div class="navbar-badge">✦ Student Dashboard</div>
</div>
""", unsafe_allow_html=True)

    # ── HERO BANNER ─────────────────────────────────
    st.markdown(f"""
<div class="hero-banner">
<div class="hero-left">
<div class="hero-tag">✦ All-in-One Platform</div>
<div class="hero-heading">Organize Your<br><span>Student Life</span></div>
<div class="hero-desc">Track expenses, medicines, assignments and daily reminders — everything you need, beautifully designed for college students.</div>
</div>
<div class="hero-right">
<div class="hero-stat">
<div class="hero-stat-number">{total_expenses}</div>
<div class="hero-stat-label">Expenses</div>
</div>
<div class="hero-stat">
<div class="hero-stat-number">{pending_count}</div>
<div class="hero-stat-label">Pending</div>
</div>
<div class="hero-stat">
<div class="hero-stat-number">{total_medicines}</div>
<div class="hero-stat-label">Medicines</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── MODULES SECTION ─────────────────────────────
    st.markdown('<div class="section-heading">Modules</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
<div class="module-card card-expense">
<div class="card-top">
<div class="card-emoji-wrap">💰</div>
<div class="card-arrow">↗</div>
</div>
<div class="card-name">Expense Splitter</div>
<div class="card-desc">Split food, mess and outing expenses with your friends seamlessly.</div>
<div class="card-pill">💸 Track &amp; Split</div>
</div>
""", unsafe_allow_html=True)
        if st.button("Open Expense Splitter →", key="btn_expense"):
            st.session_state.page = "Expense"
            st.rerun()

    with col2:
        st.markdown("""
<div class="module-card card-health">
<div class="card-top">
<div class="card-emoji-wrap">💊</div>
<div class="card-arrow">↗</div>
</div>
<div class="card-name">Health Tracker</div>
<div class="card-desc">Log medicines, monitor water intake and maintain your sleep schedule.</div>
<div class="card-pill">🩺 Stay Healthy</div>
</div>
""", unsafe_allow_html=True)
        if st.button("Open Health Tracker →", key="btn_health"):
            st.session_state.page = "Health"
            st.rerun()

    with col3:
        st.markdown("""
<div class="module-card card-assign">
<div class="card-top">
<div class="card-emoji-wrap">📚</div>
<div class="card-arrow">↗</div>
</div>
<div class="card-name">Assignment Reminder</div>
<div class="card-desc">Stay on top of deadlines, submissions and pending coursework.</div>
<div class="card-pill">📋 Never Miss a Deadline</div>
</div>
""", unsafe_allow_html=True)
        if st.button("Open Assignment Tracker →", key="btn_assign"):
            st.session_state.page = "Assignment"
            st.rerun()

    # ── REMINDERS PANEL ─────────────────────────────
    st.markdown('<div class="section-heading" style="margin-top:36px;">Today\'s Reminders</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="reminders-panel">
<div class="reminders-header">
<div class="reminders-icon">🔔</div>
<div>
<div class="reminders-title">Smart Reminders</div>
<div class="reminders-subtitle">Tick off tasks as you complete them throughout the day</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Build reminder list
    reminders = []

    if not health.empty:
        for i in range(len(health)):
            medicine = health.iloc[i].get("Medicine Reminder", "")
            if pd.notna(medicine) and str(medicine).strip() != "":
                reminders.append(f"💊 Take medicine — {medicine}")

    if not assignments.empty and "Status" in assignments.columns:
        pending = assignments[assignments["Status"] == "Pending"]
        for i in range(len(pending)):
            reminders.append(f"📚 Submit — {pending.iloc[i]['Assignment']}")

    if reminders:
        for i, task in enumerate(reminders):
            if task not in st.session_state.completed_tasks:
                checked = st.checkbox(task, key=f"task_{i}")
                if checked:
                    st.session_state.completed_tasks.append(task)
                    st.rerun()
            else:
                st.markdown(
                    f"<p class='done-task'>✔ {task[2:]}</p>",
                    unsafe_allow_html=True
                )
    else:
        st.markdown(
            "<div class='reminder-empty'>🎉 No pending reminders right now. Great job!</div>",
            unsafe_allow_html=True
        )

    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;color:#1e293b;font-size:13px;'>CampusSync · Built for students</p>",
        unsafe_allow_html=True
    )

# =====================================================
# EXPENSE PAGE
# =====================================================

elif st.session_state.page == "Expense":
    st.markdown('<div class="page-title-bar">💰 Expense Splitter</div>', unsafe_allow_html=True)
    if st.button("← Back to Dashboard"):
        st.session_state.page = "Home"
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    show_expense_splitter()

# =====================================================
# HEALTH PAGE
# =====================================================

elif st.session_state.page == "Health":
    st.markdown('<div class="page-title-bar">💊 Health Tracker</div>', unsafe_allow_html=True)
    if st.button("← Back to Dashboard"):
        st.session_state.page = "Home"
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    show_health_tracker()

# =====================================================
# ASSIGNMENT PAGE
# =====================================================

elif st.session_state.page == "Assignment":
    st.markdown('<div class="page-title-bar">📚 Assignment Tracker</div>', unsafe_allow_html=True)
    if st.button("← Back to Dashboard"):
        st.session_state.page = "Home"
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    show_assignment_reminder()