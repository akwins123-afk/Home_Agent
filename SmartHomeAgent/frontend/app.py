import streamlit as st
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Self Developing Home Agent",
    layout="wide"
)

# -----------------------------
# SESSION STATE INIT
# -----------------------------
defaults = {
    "temperature": 27.0,   # ✅ Average room temperature
    "target": 26.0,
    "energy": 0.0,
    "occupancy": 5,
    "ac_state": False,
    "fan_state": False,
    "decision_ran": False,
    "message": None,
    "memory": []
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("🎛 Control Panel")

    st.session_state.target = st.slider(
        "Target Temperature (°C)", 18.0, 30.0, st.session_state.target
    )

    st.session_state.occupancy = st.selectbox(
        "Occupancy", [0, 1, 2, 3, 4, 5],
        index=st.session_state.occupancy
    )

    if st.button("▶ Run Next Decision Cycle"):
        st.session_state.decision_ran = True
        st.session_state.message = None

        if st.session_state.ac_state:
            st.session_state.temperature -= 0.6
            st.session_state.energy += 1.5
        elif st.session_state.fan_state:
            st.session_state.temperature -= 0.2
            st.session_state.energy += 0.3
        else:
            st.session_state.temperature += 0.2

        st.session_state.temperature = round(st.session_state.temperature, 2)
        st.session_state.energy = round(st.session_state.energy, 2)

# -----------------------------
# HEADER
# -----------------------------
st.title("🏠 Self Developing Home Agent")

col1, col2 = st.columns([2, 1])

with col1:
    st.metric("🌡 Temperature (°C)", st.session_state.temperature)
    st.metric("⚡ Energy Used (kWh)", st.session_state.energy)
    st.metric("👥 Occupancy", st.session_state.occupancy)

# -----------------------------
# DEVICE STATUS (UI ONLY)
# -----------------------------
st.subheader("🔌 Device Status")

ui_col1, ui_col2 = st.columns(2)

with ui_col1:
    ac_ui = st.toggle("❄ Air Conditioner", value=st.session_state.ac_state)

with ui_col2:
    fan_ui = st.toggle("🌀 Fan", value=st.session_state.fan_state)

# Sync UI → internal state
st.session_state.ac_state = ac_ui
st.session_state.fan_state = fan_ui

# -----------------------------
# AI DECISION LOGIC
# -----------------------------
best = None

if st.session_state.decision_ran:
    if st.session_state.temperature > st.session_state.target + 0.5:
        best = "AC"
    elif st.session_state.temperature <= st.session_state.target:
        best = "FAN"

chosen = (
    "AC" if st.session_state.ac_state
    else "FAN" if st.session_state.fan_state
    else "NONE"
)

regret = 0.0
if best and chosen != "NONE" and chosen != best:
    regret = round(st.session_state.energy * 0.7, 2)

if st.session_state.decision_ran:
    st.session_state.memory.append({
        "temperature": st.session_state.temperature,
        "energy": st.session_state.energy,
        "chosen": chosen,
        "best": best if best else "NONE",
        "regret": regret
    })

# -----------------------------
# DECISION EVALUATION
# -----------------------------
with col2:
    st.subheader("🧠 Decision Evaluation")
    st.write(f"**Chosen:** {chosen}")
    st.write(f"**Best:** {best if best else '-'}")
    st.write(f"**Regret:** {regret}")

# -----------------------------
# ENERGY EFFICIENCY DECISION
# -----------------------------
if st.session_state.decision_ran and best and chosen != best:
    st.subheader("⚡ Energy Efficiency Decision")

    if best == "AC":
        msg = "🔥 It's getting warm. Turning ON AC improves comfort efficiently."
    else:
        msg = "😌 Target reached. FAN maintains comfort with lower energy."

    st.info(msg)

    col_yes, col_no = st.columns(2)

    with col_yes:
        if st.button("✅ Apply Change"):
            if best == "AC":
                st.session_state.ac_state = True
                st.session_state.fan_state = False
            else:
                st.session_state.ac_state = False
                st.session_state.fan_state = True

            st.session_state.message = "✅ AI decision applied successfully."
            st.rerun()

    with col_no:
        if st.button("❌ Ignore"):
            st.session_state.message = (
                f"⚠ Regret detected. Ignoring this decision cost extra energy "
                f"(Regret = {regret})."
            )

# -----------------------------
# SMART HOME INBOX
# -----------------------------
st.subheader("📬 Smart Home Inbox")

if st.session_state.decision_ran:
    if st.session_state.message:
        st.success(st.session_state.message)

    if st.session_state.temperature > 30:
        st.warning("🔥 High temperature detected. Cooling recommended.")

    if (
        st.session_state.temperature <= st.session_state.target
        and st.session_state.ac_state
    ):
        st.warning(
            "💸 Overcooling detected. FAN can maintain comfort with less energy."
        )

# -----------------------------
# LEARNING MEMORY
# -----------------------------
st.subheader("📊 Learning Memory")
st.dataframe(st.session_state.memory, use_container_width=True)

# -----------------------------
# 📈 PLOTLY GRAPH (FINAL ADDITION)
# -----------------------------
if len(st.session_state.memory) > 1:
    temps = [m["temperature"] for m in st.session_state.memory]
    energy = [m["energy"] for m in st.session_state.memory]
    steps = list(range(len(temps)))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=steps,
        y=temps,
        mode="lines+markers",
        name="Temperature (°C)",
        line=dict(width=3)
    ))

    fig.add_trace(go.Scatter(
        x=steps,
        y=energy,
        mode="lines+markers",
        name="Energy Used (kWh)",
        yaxis="y2",
        line=dict(width=3)
    ))

    fig.update_layout(
        title="📈 Energy & Temperature Over Time",
        xaxis_title="Decision Cycle",
        yaxis=dict(title="Temperature (°C)"),
        yaxis2=dict(
            title="Energy Used (kWh)",
            overlaying="y",
            side="right"
        ),
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)
