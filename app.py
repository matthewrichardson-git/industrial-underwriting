import streamlit as st
st.title("Industrial RE Underwriter")
st.header("Property Info")

# creates a text box, stores what user types in the variable "address"
address = st.text_input("Property Address", placeholder="123 Industrial Pkwy, Memphis, TN")

# number box, min_value stops negatives, value is the default, step is how much +/- arrows jump
square_feet = st.number_input("Rentable Square Feet (RSF)", min_value=0, value=50000, step=1000)

# same pattern, max_value added so nobody enters a future year
year_built= st.number_input("Year Built", min_value=1900, max_value=2030, value=1995, step=1000)

st.header("Income")

# rent per square foot per year
rent_psf = st.number_input("Base Rent ($/SF/yr)", min_value=0.0, value=6.50, step=0.25)

# slider instead of number box since occupancy is alwways between 0-100%
# format ="%.0f%%" displays 0.95 as "95%" on screen
occupancy = st.slider("Occupancy Rate", min_value=0.0, max_value=1.0, value=0.95, step=0.01, format="%.0f%%")

# anything else the property earns (parking, storage, etc)
other_income= st.number_input ("Other Annual Income ($)", min_value=0.0, value=0.0, step=500.0)

st.header("Expenses")

# management fee as a percentage of income, not flat dollar amount
mgmt_fee_pct = st.number_input ("Mgmt Fee (% of EGI)", min_value=0.0, max_value=20.0, value=3.0, step=0.5)

# these three are all per-square-foot inputs - same pattern
insurance_psf = st.number_input("Insurance ($/SF/yr)", min_value=0.0, value=0.15, step=0.05)
re_taxes_psf = st.number_input("Real Estate Taxes ($/SF/yr)", min_value=0.0, value=0.80, step=0.05)
maintenance_psf = st.number_input("Maintenance & Repairs ($/SF/yr)", min_value=0.0, value=0.25, step=0.05)

st.header("Underwriting Output")

# Excel formulas
gross_potential_income = square_feet * rent_psf
vacancy_loss = gross_potential_income * (1 - occupancy)
egi = gross_potential_income - vacancy_loss + other_income

mgmt_fee = egi * (mgmt_fee_pct / 100)
insurance = square_feet * insurance_psf
re_taxes = square_feet * re_taxes_psf
maintenance = square_feet * maintenance_psf
total_expenses = mgmt_fee + insurance + re_taxes + maintenance

noi = egi - total_expenses


# splits page into 3 side-by-side columns
col1, col2, col3 = st.columns(3)

#st.metric shows a big bold KPI number with a label above it 
#f"${egi:,.0f}" formats the number with commas after the dollar sign
col1.metric("Effective Gross Income", f"${egi:,.0f}")
col2.metric("Total Expenses", f"${total_expenses:,.0f}")
col3.metric("NOI", f"${noi:,.0f}")

# --- Valuation ---
st.header("Valuation")


cap_rate = st.number_input("Market Cap Rate (%)", min_value=0.1, max_value=20.0, value=6.0, step=0.25)

# Value = NOI / (Cap Rate /100)
value = noi / (cap_rate/100)
st.metric("Implied Property Value", f"${value:,.0f}")

# --- Debt & DSCR ---
st.header("Debt & DSCR")

# LTV
# % of the property value the bank will lend you 
ltv=st.number_input("LTV (%)", min_value=0.0, max_value=95.0, value=65.0, step=5.0)

# Annual Interest
interest_rate = st.number_input("Interest Rate(%)", min_value=0.0, max_value=15.0, value=6.5, step=0.25)

# Amortization 
# how many years to pay back the loan
# longer = lower pmts
amort_years = st.number_input("Amortization (years)", min_value=1, max_value=30, value=25, step=1)

# loan amount = prop val * LTV %
loan_amount = value * (ltv / 100)

# monthly interest 
monthly_rate = (interest_rate / 100) / 12

# number of pmts 
n_payments = amort_years * 12

# PMT calc
monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments -1)

# Debt Service ( pmt * 12 )
annual_debt_service = monthly_payment * 12

# DSCR 
dscr = noi / annual_debt_service

# display all three outputs
col1, col2, col3, = st.columns(3)
col1.metric("Loan Amount", f"${loan_amount:,.0f}")
col2.metric("Annual Debt Service", f"${annual_debt_service:,.0f}")
col3.metric("DSCR", f"{dscr:.2f}x")

with st.expander("What is DSCR and what should it be?"):
    st.write("""
    DSCR (Debt Service Coverage Ratio) measures whether a property generates enough income to cover its loan payments.
    
    - **Below 1.0x** — property can't cover the mortgage. Lender will say no.
    - **1.0x - 1.25x** — breaking even or close. Most lenders won't touch this.
    - **1.25x - 1.35x** — minimum acceptable for most commercial lenders.
    - **Above 1.35x** — comfortable. Strong deal from a lender's perspective.
    
    To improve DSCR: lower your LTV, negotiate a lower rate, or find a property with higher NOI.
    """)


levered_cash_flow = noi - annual_debt_service
equity_invested = value - loan_amount
cash_on_cash = levered_cash_flow / equity_invested

    
col1, col2 = st.columns(2)
col1.metric("Levered Cash Flow", f"${levered_cash_flow:,.0f}")
col2.metric("Cash-on-Cash Return", f"{cash_on_cash:.1%}")

with st.expander("What is Cash-on-Cash and what should it be?"):
    st.write("""
    Cash-on-Cash measures how much cash you get back each year relative to what you put in.

    - **Below 5%** — weak. You could do better in the stock market.
    - **5% - 7%** — acceptable but not exciting.
    - **7% - 10%** — solid return for industrial real estate.
    - **Above 10%** — strong. Usually means you got a good basis or great financing.

    Unlike IRR, cash-on-cash ignores appreciation and only looks at current year income vs equity invested.
    """)

import numpy as np
import numpy_financial as npf

# --- IRR ---
st.header("IRR Analysis")

# inputs
hold_years = st.number_input("Hold Period (years)", min_value=1, max_value=20, value=10, step=1)
noi_growth = st.number_input("Annual NOI Growth (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.25)
exit_cap = st.number_input("Exit Cap Rate (%)", min_value=0.0, max_value=20.0, value=7.0, step=0.25)

# build NOI for each year, growing by noi_growth % annually
# this is a list comprehension — a compact way to build a list with a formula
noi_list = [noi * (1 + noi_growth/100)**year for year in range(1, int(hold_years)+1)]

# levered cash flow each year is NOI minus debt service
annual_cash_flows = [n - annual_debt_service for n in noi_list]

# remaining loan balance at end of hold period
payments_made = int(hold_years) * 12
remaining_payments = (amort_years * 12) - payments_made
remaining_balance = monthly_payment * (1 - (1 + monthly_rate)**-remaining_payments) / monthly_rate

# exit NOI is the year after your last hold year
exit_noi = noi * (1 + noi_growth/100)**(hold_years + 1)
sale_price = exit_noi / (exit_cap/100)
sale_proceeds = sale_price - remaining_balance

# add sale proceeds to final year cash flow
annual_cash_flows[-1] += sale_proceeds

# year 0 is your equity going in as a negative number
cash_flows = [-equity_invested] + annual_cash_flows

# numpy calculates IRR from the list of cash flows
irr = npf.irr(cash_flows)

# display
col1, col2, col3 = st.columns(3)
col1.metric("Sale Price", f"${sale_price:,.0f}")
col2.metric("Sale Proceeds", f"${sale_proceeds:,.0f}")
col3.metric("IRR", f"{irr:.1%}")

with st.expander("📚 What is IRR and what should it be?"):
    st.write("""
    IRR is the annualized return on your equity across the entire hold period, including cash flows and the sale.
    
    - **Below 8%** — weak for value-add industrial. Bond-like returns with real estate risk.
    - **8% - 12%** — acceptable for core/core-plus industrial.
    - **12% - 18%** — target range for most value-add deals.
    - **Above 18%** — strong. Opportunistic territory.
    
    IRR is sensitive to your exit cap rate and hold period — always stress test both.
    """)

import pandas as pd
# --- SENSITIVITY TABLE ---
st.header("Sensitivity Analysis")
st.write("IRR across different exit cap rates and NOI growth assumptions")

# these are the values I'm  test across each axis
exit_caps = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0]
growth_rates = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]

# build the table row by row
# for every combination of exit cap and growth rate, calculate IRR
rows = {}
for g in growth_rates:
    row = []
    for ec in exit_caps:
        # recalculate NOI list and cash flows for this combination
        noi_list_s = [noi * (1 + g/100)**year for year in range(1, int(hold_years)+1)]
        annual_cf_s = [n - annual_debt_service for n in noi_list_s]
        exit_noi_s = noi * (1 + g/100)**(hold_years + 1)
        sale_price_s = exit_noi_s / (ec/100)
        sale_proceeds_s = sale_price_s - remaining_balance
        annual_cf_s[-1] += sale_proceeds_s
        cf_s = [-equity_invested] + annual_cf_s
        irr_s = npf.irr(cf_s)
        row.append(f"{irr_s:.1%}")
    rows[f"{g}% growth"] = row

# turn it into a pandas dataframe
df = pd.DataFrame(rows, index=[f"{ec}% exit cap" for ec in exit_caps]).T
st.dataframe(df)

# --- DEAL SUMMARY ---
st.header("Deal Summary")

# check each metric against typical thresholds
# these are just if/else statements -- if condition is true, show green, else show red
dscr_check = "✅ Pass" if dscr >= 1.25 else "❌ Fail"
coc_check = "✅ Pass" if cash_on_cash >= 0.07 else "❌ Fail"
irr_check = "✅ Pass" if irr >= 0.12 else "❌ Fail"

col1, col2, col3 = st.columns(3)
col1.metric("DSCR", f"{dscr:.2f}x", dscr_check)
col2.metric("Cash-on-Cash", f"{cash_on_cash:.1%}", coc_check)
col3.metric("IRR", f"{irr:.1%}", irr_check)

# overall deal verdict
if dscr >= 1.25 and cash_on_cash >= 0.07 and irr >= 0.12:
    st.success("✅ Deal passes all thresholds — worth pursuing")
elif dscr < 1.0:
    st.error("❌ DSCR below 1.0 — property can't cover debt. Pass on this deal.")
else:
    st.warning("⚠️ Deal passes some thresholds but not all — needs work")

import matplotlib.pyplot as plt
# --- CHARTS ---
st.header("Charts")

# NOI Growth Bar Chart
# build a list of years and projected NOI for each year
years = list(range(1, int(hold_years)+1))
noi_by_year = [noi * (1 + noi_growth/100)**year for year in years]

# create the chart
fig, ax = plt.subplots()
ax.bar(years, noi_by_year, color="#0066cc")
ax.set_xlabel("Year")
ax.set_ylabel("NOI ($)")
ax.set_title("Projected NOI Over Hold Period")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

# display it in streamlit
st.pyplot(fig)

# Waterfall Chart — where do returns come from?
# break total return into three buckets
total_cash_flows = sum(annual_cash_flows[:-1])  # all years except last
appreciation = sale_proceeds
initial_equity = equity_invested

# three bars: cash flow, appreciation, total profit
categories = ["Equity In", "Cash Flow", "Sale Proceeds", "Total Return"]
values = [-initial_equity, total_cash_flows, appreciation, total_cash_flows + appreciation - initial_equity]
colors = ["#cc0000", "#0066cc", "#0066cc", "#00aa44"]

fig2, ax2 = plt.subplots()
ax2.bar(categories, values, color=colors)
ax2.axhline(y=0, color="black", linewidth=0.8)
ax2.set_ylabel("($)")
ax2.set_title("Return Waterfall")
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

st.pyplot(fig2)

