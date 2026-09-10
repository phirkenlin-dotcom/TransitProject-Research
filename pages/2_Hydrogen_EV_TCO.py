import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Fleet TCO Calculator", layout="wide")

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

st.markdown(
      
"""
### Introduction
At current lifetime-mile and maintenance assumptions, hydrogen becomes cost-competitive
with battery-electric once hydrogen prices fall to roughly **$[X.XX]/kg**
*(replace with your model's actual break-even — read it off the chart below where the
two lines cross)*. At today's typical hydrogen prices, **[battery-electric / hydrogen]**
comes out ahead over the bus's lifetime.

**What that means practically:** [e.g., "At current hydrogen prices, battery-electric
wins unless hydrogen production costs drop substantially — which would require X, Y, or Z
to happen (cheaper electrolysis, subsidies, regional production, etc.)."]

### The question this model answers
At what hydrogen price ($/kg) does a hydrogen fuel-cell bus become cheaper, over its
full lifetime, than a battery-electric bus?

### How the model works
Total cost of ownership for each bus type is built from three pieces:
- **Capital cost** — upfront purchase price of the bus
- **Operating cost** — maintenance cost per mile × lifetime miles
- **Energy cost** — for battery buses, efficiency (kWh/mile) × electricity price; for
  hydrogen buses, efficiency (miles/kg) and hydrogen price ($/kg), converted to a
  per-mile cost

All three are summed to get each bus type's lifetime total, then compared directly
against each other and, in the chart below, across a full range of hydrogen prices.


        """
    )



st.subheader("Adjust Input Values")
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    st.markdown("** Battery-electric bus (BEB)**")

    r1, r2 = st.columns(2)

    with r1:
        beb_purchase = st.slider(
            "Purchase ($)",
            500_000, 1_200_000, 850_000, 10_000
        )

    with r2:
        beb_maintenance = st.slider(
            "Maintenance ($/mile)",
            0.10, 2.00, 0.90, 0.01
        )

    r3, r4 = st.columns(2)

    with r3:
        beb_efficiency = st.slider(
            "Efficiency (kWh/mile)",
            1.0, 5.0, 2.5, 0.1
        )

    with r4:
        electricity_price = st.slider(
            "Electricity ($/kWh)",
            0.05, 0.50, 0.15, 0.01
        )

with col2:
    st.markdown("** Hydrogen fuel-cell bus (FCEB)**")

    r1, r2 = st.columns(2)

    with r1:
        fceb_purchase = st.slider(
            "Purchase ($)",
            500_000, 1_500_000, 1_000_000, 10_000
        )

    with r2:
        fceb_maintenance = st.slider(
            "Maintenance ($/mile)",
            0.10, 2.00, 0.70, 0.01
        )

    r3, r4 = st.columns(2)

    with r3:
        fceb_efficiency = st.slider(
            "Efficiency (miles/kg)",
            3.0, 15.0, 8.0, 0.1
        )

    with r4:
        hydrogen_price = st.slider(
            "Hydrogen ($/kg)",
            1.0, 20.0, 8.0, 0.25
        )

with col3:
    st.markdown("** Total Miles **")

    lifetime_miles = st.slider(
        "Lifetime miles",
        100_000, 1_000_000, 500_000, 10_000
    )
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

st.markdown(
"""
### Result
"""
)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write(f"**Battery TCO :  ${beb_total:,.0f}**")

with col2:
    st.write(f"**Hydrogen TCO :  ${fceb_total:,.0f}**")

with col3:
    st.write(f"**Difference :  ${difference:,.0f}**")

with col4:
    st.write(f"**Recommendation :  {recommendation}**")
    
st.subheader("Breakeven Electric vs hydrogen price ")


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

st.markdown(
"""

### Interpretation

### Sources
- [Reference 1 — e.g., FTA or DOE hydrogen bus cost data, with link]
- [Reference 2 — e.g., local transit authority procurement documents]
- [Reference 3 — e.g., DOE Alternative Fuels Data Center]
"""
)
