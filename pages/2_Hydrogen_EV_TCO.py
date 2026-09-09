import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Fleet TCO — Battery vs. Hydrogen Bus", layout="wide")

def calculate_tco(
    beb_purchase,
    fceb_purchase,
    beb_maintenance,
    fceb_maintenance,
    beb_efficiency,
    fceb_efficiency,
    electricity_price,
    hydrogen_price,
    lifetime_miles,
):
    # battery
    beb_energy_per_mile = beb_efficiency * electricity_price
    beb_energy_total = beb_energy_per_mile * lifetime_miles
    beb_maintenance_total = beb_maintenance * lifetime_miles
    beb_total = beb_purchase + beb_energy_total + beb_maintenance_total

    # hydrogen
    hydrogen_per_mile = hydrogen_price / fceb_efficiency
    hydrogen_energy_total = hydrogen_per_mile * lifetime_miles
    hydrogen_maintenance_total = fceb_maintenance * lifetime_miles
    fceb_total = fceb_purchase + hydrogen_energy_total + hydrogen_maintenance_total

    return beb_total, fceb_total


st.title("Fleet Total Cost of Ownership")
st.caption(
    "Compare lifetime cost for battery-electric and hydrogen fuel-cell buses "
    "under adjustable purchase, maintenance, and fuel assumptions."
)

with st.sidebar:
    st.header("Battery-electric bus (BEB)")
    beb_purchase = st.slider("Purchase price ($)", 500_000, 1_200_000, 850_000, 10_000)
    beb_maintenance = st.slider("Maintenance ($/mile)", 0.10, 2.00, 0.90, 0.01)
    beb_efficiency = st.slider("Efficiency (kWh/mile)", 1.0, 5.0, 2.5, 0.1)
    electricity_price = st.slider("Electricity price ($/kWh)", 0.05, 0.50, 0.15, 0.01)

    st.header("Hydrogen fuel-cell bus (FCEB)")
    fceb_purchase = st.slider("Purchase price ($) ", 500_000, 1_500_000, 1_000_000, 10_000)
    fceb_maintenance = st.slider("Maintenance ($/mile) ", 0.10, 2.00, 0.70, 0.01)
    fceb_efficiency = st.slider("Efficiency (miles/kg)", 3.0, 15.0, 8.0, 0.1)
    hydrogen_price = st.slider("Hydrogen price ($/kg)", 1.0, 20.0, 8.0, 0.25)

    st.header("Shared")
    lifetime_miles = st.slider("Lifetime miles", 100_000, 1_000_000, 500_000, 10_000)

beb_total, fceb_total = calculate_tco(
    beb_purchase,
    fceb_purchase,
    beb_maintenance,
    fceb_maintenance,
    beb_efficiency,
    fceb_efficiency,
    electricity_price,
    hydrogen_price,
    lifetime_miles,
)
difference = abs(beb_total - fceb_total)
recommendation = "Battery Electric Bus" if beb_total < fceb_total else "Hydrogen Fuel Cell Bus"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Battery TCO", f"${beb_total:,.0f}")
col2.metric("Hydrogen TCO", f"${fceb_total:,.0f}")
col3.metric("Difference", f"${difference:,.0f}")
col4.metric("Recommendation", recommendation)

st.subheader("Sensitivity to hydrogen price")
st.caption(
    "Hydrogen TCO traced across $1–$20/kg, all other inputs held at current slider values. "
    "Battery TCO shown as a flat reference line."
)

prices = np.linspace(1, 20, 100)
hydrogen_costs = []
for price in prices:
    _, hydrogen_total = calculate_tco(
        beb_purchase,
        fceb_purchase,
        beb_maintenance,
        fceb_maintenance,
        beb_efficiency,
        fceb_efficiency,
        electricity_price,
        price,
        lifetime_miles,
    )
    hydrogen_costs.append(hydrogen_total)

chart_df = pd.DataFrame(
    {
        "Hydrogen Bus": hydrogen_costs,
        "Battery Bus": [beb_total] * len(prices),
    },
    index=pd.Index(prices, name="Hydrogen Price ($/kg)"),
)
st.line_chart(chart_df)
