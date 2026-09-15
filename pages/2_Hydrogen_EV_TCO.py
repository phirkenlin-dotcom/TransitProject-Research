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
During my time on Congresswoman Norma Torres's Youth Advisory Committee, I had the opportunity to meet the Foothill Transit leadership team and tour their Pomona Operations and Maintenance Facility. 
Foothill Transit operates North America’s largest hydrogen fuel cell bus fleet and houses a 25,000-gallon liquid hydrogen fueling station. 
While conversing with their team, I learned that while battery-electric buses (BEBs) offer low daily electricity costs, their limited range and long charge cycles create constraints. 
However, hydrogen fuel cell electric buses (FCEBs) have a fast 8-minute refueling speed, but current hydrogen fuel prices and sourcing make them significantly more expensive to run day-to-day. 
This economic tradeoff led me to build a Total Cost of Ownership (TCO)  model to analyze when each type of bus makes sense to utilize.

### The question this model answers
At what hydrogen price per kilogram ($/kg) does a hydrogen fuel cell bus become cheaper over its full lifetime than a battery-electric bus?


### How the model works
The Total Cost of Ownership (TCO) for each vehicle type is calculated by combining three variables over a 500,000-mile lifetime:

- Capital Cost: The upfront vehicle price ($850,000 for BEBs vs. $1,000,000 for FCEBs).

- Operating Cost: Scheduled maintenance expenses per mile ($0.90/mi for BEBs vs. $0.70/mi for FCEBs).

- Energy Cost: Consumption efficiency multiplied by unit fuel price. BEB energy cost relies on electricity (\$/kWh) and efficiency (kWh/mile), whereas FCEB energy cost factors hydrogen price (\$/kg) converted to a per-mile expense based on fuel efficiency (miles/kg).

The model combines these components into a lifetime total for both types of buses and evaluates them across changing hydrogen prices.


### Adjust Input Values
Users can adjust the parameters (purchase price, maintenance cost per mile, vehicle efficiency, electricity rates, and fuel costs) to simulate real-world scenarios and an understanding of how price changes can affect the prices of buses overall. Under typical market conditions (\$0.15/kWh electricity vs. \$8.00/kg hydrogen):

        """
    )



#st.subheader("Adjust Input Values")
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
    
st.subheader("Break-even Electric vs hydrogen price ")


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

### 
### Break-even Electric vs. Hydrogen Price
The graph plots total lifetime cost (Y-axis) against changing hydrogen prices per kilogram (X-axis). Because electricity rates remain fixed (assuming prices won't change in the future), the battery-electric bus line remains flat, while the hydrogen bus line slopes upward as fuel prices rise. That being said, the reason why these variables can be changed is to understand how break-even costs can change, as input prices can change.

The intersection point where the two lines cross marks the exact financial break-even cost. At current market rates ($8.00/kg), hydrogen carries a higher lifetime expense. However, if hydrogen production scales up and fuel prices drop below the break-even threshold on the X-axis, hydrogen fuel cell buses become the lower-cost solution over a 500,000-mile lifecycle.

### Interpretation
While battery-electric buses seem to win under current costs,  models alone do not capture the full picture. Transit agencies choosing between these technologies must weigh trade-offs: battery-electric fleets require heavy investment in charging infrastructure and route adjustments for charging times, while hydrogen fleets fit existing route schedules but require hydrogen production costs to decline.


### Sources
- Reference 1 — https://www.transit.dot.gov/research-innovation/national-fuel-cell-bus-program-reports
- Reference 2 — Comparative TCO Analysis of Battery Electric and Hydrogen Fuel Cell Buses for Public Transport System in Small to Midsize Cities. https://www.mdpi.com/1996-1073/14/14/4384 ]
- Reference 3 — https://www.hydrogen.energy.gov/docs/hydrogenprogramlibraries/pdfs/progress04/vc3_eudy.pdf?sfvrsn=c327c1b2_1
- Reference 4 —https://californiahydrogen.org/resources/hydrogen-fuel-cell-bus-info-page-the-better-electric-bus/
"""
)
