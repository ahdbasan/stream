import streamlit as st

st.title("☀️ Resilience Classroom Sizing Calculator")
st.markdown("Adjust the inputs below based on location and usage to size the solar system needed for energy autonomy.")

# --- 1. USER INPUTS (The Variables People Play With) ---
st.header("1. Critical Inputs")

col1, col2 = st.columns(2)

with col1:
    # Architectural Input: What's the school's load?
    daily_peak_load_watts = st.slider(
        "Peak Load (W): Lights, Fans, Charging",
        min_value=100, max_value=1000, value=300, step=50,
        help="Total continuous power required by the systems."
    )
    
    hours_of_operation = st.slider(
        "Hours of Operation (h/day)",
        min_value=2, max_value=12, value=6, step=1,
        help="How many hours a day does the classroom need power?"
    )

with col2:
    # Data Science Input: What did your analysis show?
    peak_sun_hours = st.number_input(
        "Local PSH (Peak Sun Hours)",
        min_value=3.0, max_value=7.0, value=5.5, step=0.1,
        help="The average daily solar irradiance (from your data analysis)."
    )

    battery_autonomy_days = st.number_input(
        "Backup Days Required (Autonomy)",
        min_value=1, max_value=7, value=3, step=1,
        help="How many days must the battery power the load without sun (Critical for crisis zones)."
    )
    
# Fixed Engineering Assumptions (Can be hidden or made inputs later)
system_loss_derate = 0.75
panel_watt_peak = 250
battery_dod = 0.5 # 50% Depth of Discharge

# --- 2. CALCULATIONS ---
daily_consumption_Wh = daily_peak_load_watts * hours_of_operation
array_size_Wp = (daily_consumption_Wh / system_loss_derate) / peak_sun_hours
num_panels_needed = array_size_Wp / panel_watt_peak
required_battery_Wh = daily_consumption_Wh * battery_autonomy_days
battery_capacity_kWh = (required_battery_Wh / 1000) / battery_dod

# --- 3. OUTPUTS (The Results) ---
st.header("2. Data-Validated Specifications")
st.subheader(f"Required Daily Energy: {daily_consumption_Wh/1000:.2f} kWh/day")
st.markdown("---")

col_out1, col_out2, col_out3 = st.columns(3)

with col_out1:
    st.metric("☀️ PV Array Size (Wp)", f"{array_size_Wp:.0f} Wp")
    st.caption("Total rated power needed from panels.")

with col_out2:
    st.metric(" panels Required", f"{int(num_panels_needed + 0.99)} Panels", delta="Based on 250W panels")
    st.caption("This justifies the roof space required.")

with col_out3:
    st.metric("⚡ Battery Capacity", f"{battery_capacity_kWh:.1f} kWh")
    st.caption(f"Provides {battery_autonomy_days} days of autonomy.")
