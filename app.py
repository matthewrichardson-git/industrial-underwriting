import streamlit as st
import numpy as np
import numpy_financial as npf
import pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Industrial RE Underwriter",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --navy:      #0A0E1A;
    --navy2:     #131929;
    --navy3:     #1C2333;
    --gold:      #C9A84C;
    --gold-dim:  #9A7A38;
    --white:     #E8E8E8;
    --white-dim: #9AA0B0;
    --green:     #2ECC71;
    --red:       #E74C3C;
    --amber:     #F39C12;
    --border:    rgba(201,168,76,0.2);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--navy);
    color: var(--white);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

[data-testid="stSidebar"] {
    background-color: var(--navy2);
    border-right: 1px solid var(--border);
}

.sidebar-section {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--gold);
    padding: 1rem 0 0.4rem 0;
    border-top: 1px solid var(--border);
    margin-top: 0.5rem;
}
.sidebar-section:first-child { border-top: none; margin-top: 0; }

.page-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding: 0.5rem 0 1.5rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.page-header-left h1 {
    font-size: 1.4rem;
    font-weight: 600;
    color: var(--white);
    margin: 0 0 0.2rem 0;
    letter-spacing: -0.01em;
}
.page-header-left p {
    font-size: 0.78rem;
    color: var(--white-dim);
    margin: 0;
    font-family: 'DM Mono', monospace;
}
.status-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.3rem 0.75rem;
    border-radius: 2px;
    margin-top: 0.25rem;
}
.badge-pass   { background: rgba(46,204,113,0.15); color: var(--green); border: 1px solid rgba(46,204,113,0.3); }
.badge-fail   { background: rgba(231,76,60,0.15);  color: var(--red);   border: 1px solid rgba(231,76,60,0.3); }
.badge-review { background: rgba(243,156,18,0.15); color: var(--amber); border: 1px solid rgba(243,156,18,0.3); }

.section-header {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--gold);
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
    margin: 1.5rem 0 1rem 0;
}

.metric-card {
    background: var(--navy2);
    border: 1px solid var(--border);
    border-top: 2px solid var(--gold);
    padding: 1rem 1.25rem;
    border-radius: 2px;
}
.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--white-dim);
    margin-bottom: 0.4rem;
}
.metric-value {
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--white);
    line-height: 1;
    margin-bottom: 0.3rem;
    letter-spacing: -0.02em;
}
.metric-sub { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--white-dim); }
.metric-pass { color: var(--green) !important; }
.metric-fail { color: var(--red)   !important; }
.metric-warn { color: var(--amber) !important; }

/* ── Rent roll table ── */
.rr-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.78rem;
}
.rr-table th {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--gold);
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid var(--border);
    text-align: right;
    white-space: nowrap;
}
.rr-table th:first-child { text-align: left; }
.rr-table td {
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    color: var(--white);
    text-align: right;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
}
.rr-table td:first-child {
    text-align: left;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--white);
}
.rr-table tr:hover td { background: rgba(201,168,76,0.04); }
.risk-critical { color: #E74C3C; font-weight: 600; }
.risk-watch    { color: #F39C12; }
.risk-stable   { color: #2ECC71; }
.mtm-positive  { color: #2ECC71; }
.mtm-negative  { color: #E74C3C; }

.noi-row { display: flex; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.82rem; }
.noi-row:last-child { border-bottom: none; font-weight: 600; color: var(--gold); }
.noi-label { color: var(--white-dim); }
.noi-value { font-family: 'DM Mono', monospace; color: var(--white); }
.noi-negative { color: var(--red) !important; }

[data-testid="stExpander"] {
    background: var(--navy2);
    border: 1px solid var(--border) !important;
    border-radius: 2px;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid var(--border);
    gap: 0;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--white-dim);
    background: transparent;
    border: none;
    padding: 0.6rem 1.25rem;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom: 2px solid var(--gold) !important;
    background: transparent !important;
}

.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, var(--gold) 0%, transparent 100%);
    margin: 1.5rem 0;
    opacity: 0.4;
}

/* ── Walt bar ── */
.walt-bar-bg {
    background: var(--navy3);
    border-radius: 2px;
    height: 6px;
    margin-top: 0.4rem;
}
.walt-bar-fill {
    background: var(--gold);
    border-radius: 2px;
    height: 6px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def metric_card(label, value, sub="", sub_class=""):
    sub_html = f'<div class="metric-sub {sub_class}">{sub}</div>' if sub else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

def section(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏭 Deal Inputs")

    st.markdown('<div class="sidebar-section">Property</div>', unsafe_allow_html=True)
    address       = st.text_input("Address", placeholder="123 Industrial Pkwy, Memphis, TN")
    square_feet   = st.number_input("Rentable SF", min_value=0, value=355000, step=1000)
    year_built    = st.number_input("Year Built", min_value=1900, max_value=2030, value=1995, step=1)

    st.markdown('<div class="sidebar-section">Income</div>', unsafe_allow_html=True)
    rent_psf      = st.number_input("Base Rent ($/SF/yr)", min_value=0.0, value=6.50, step=0.25)
    occupancy     = st.slider("Occupancy", min_value=0.0, max_value=1.0, value=0.95, step=0.01, format="%.0f%%")
    other_income  = st.number_input("Other Income ($/yr)", min_value=0.0, value=0.0, step=500.0)

    st.markdown('<div class="sidebar-section">Expenses</div>', unsafe_allow_html=True)
    mgmt_fee_pct    = st.number_input("Mgmt Fee (% EGI)", min_value=0.0, max_value=20.0, value=3.0, step=0.5)
    insurance_psf   = st.number_input("Insurance ($/SF/yr)", min_value=0.0, value=0.15, step=0.05)
    re_taxes_psf    = st.number_input("RE Taxes ($/SF/yr)", min_value=0.0, value=0.80, step=0.05)
    maintenance_psf = st.number_input("Maintenance ($/SF/yr)", min_value=0.0, value=0.25, step=0.05)

    st.markdown('<div class="sidebar-section">Valuation & Debt</div>', unsafe_allow_html=True)
    cap_rate      = st.number_input("Market Cap Rate (%)", min_value=0.1, max_value=20.0, value=6.0, step=0.25)
    ltv           = st.number_input("LTV (%)", min_value=0.0, max_value=95.0, value=65.0, step=5.0)
    interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=15.0, value=6.5, step=0.25)
    amort_years   = st.number_input("Amortization (yrs)", min_value=1, max_value=30, value=25, step=1)

    st.markdown('<div class="sidebar-section">Returns</div>', unsafe_allow_html=True)
    hold_years = st.number_input("Hold Period (yrs)", min_value=1, max_value=20, value=10, step=1)
    noi_growth = st.number_input("NOI Growth (%/yr)", min_value=0.0, max_value=10.0, value=2.0, step=0.25)
    exit_cap   = st.number_input("Exit Cap Rate (%)", min_value=0.0, max_value=20.0, value=7.0, step=0.25)


# ─────────────────────────────────────────────
#  CORE CALCULATIONS (same as Session 2)
# ─────────────────────────────────────────────
gross_potential_income = square_feet * rent_psf
vacancy_loss           = gross_potential_income * (1 - occupancy)
egi                    = gross_potential_income - vacancy_loss + other_income

mgmt_fee       = egi * (mgmt_fee_pct / 100)
insurance      = square_feet * insurance_psf
re_taxes       = square_feet * re_taxes_psf
maintenance    = square_feet * maintenance_psf
total_expenses = mgmt_fee + insurance + re_taxes + maintenance
noi            = egi - total_expenses

value               = noi / (cap_rate / 100)
loan_amount         = value * (ltv / 100)
monthly_rate        = (interest_rate / 100) / 12
n_payments          = amort_years * 12
monthly_payment     = loan_amount * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)
annual_debt_service = monthly_payment * 12
dscr                = noi / annual_debt_service

levered_cash_flow = noi - annual_debt_service
equity_invested   = value - loan_amount
cash_on_cash      = levered_cash_flow / equity_invested

payments_made      = int(hold_years) * 12
remaining_payments = (amort_years * 12) - payments_made
remaining_balance  = monthly_payment * (1 - (1 + monthly_rate)**-remaining_payments) / monthly_rate

noi_list          = [noi * (1 + noi_growth/100)**yr for yr in range(1, int(hold_years)+1)]
annual_cash_flows = [n - annual_debt_service for n in noi_list]
exit_noi          = noi * (1 + noi_growth/100)**(hold_years + 1)
sale_price        = exit_noi / (exit_cap / 100)
sale_proceeds     = sale_price - remaining_balance
annual_cash_flows[-1] += sale_proceeds
cash_flows        = [-equity_invested] + annual_cash_flows
irr               = npf.irr(cash_flows)

dscr_pass = dscr >= 1.25
coc_pass  = cash_on_cash >= 0.07
irr_pass  = irr >= 0.12
all_pass  = dscr_pass and coc_pass and irr_pass
hard_fail = dscr < 1.0

if all_pass:
    badge_class, badge_text = "badge-pass",   "● PASS — Worth Pursuing"
elif hard_fail:
    badge_class, badge_text = "badge-fail",   "● FAIL — Pass on Deal"
else:
    badge_class, badge_text = "badge-review", "● REVIEW — Needs Work"


# ─────────────────────────────────────────────
#  RENT ROLL MODEL
#  Takes a DataFrame from CSV upload and returns:
#  - enriched DataFrame with risk flags & MTM
#  - year-by-year revenue schedule per tenant
#  - summary metrics (WALT, occupancy, risk SF)
# ─────────────────────────────────────────────
def build_rent_roll(df, hold_yrs, today=None):
    """
    Parameters
    ----------
    df        : raw DataFrame from CSV upload
    hold_yrs  : integer hold period (from sidebar)
    today     : date to calculate months-to-expiry from (defaults to real today)

    Returns
    -------
    enriched  : df with added columns for display
    rev_sched : dict {year: total_revenue}
    summary   : dict of portfolio-level metrics
    """
    if today is None:
        today = date.today()

    # ── Parse dates ──────────────────────────
    # pd.to_datetime converts string "2026-06-30" → datetime object
    df["lease_start"] = pd.to_datetime(df["lease_start"]).dt.date
    df["lease_end"]   = pd.to_datetime(df["lease_end"]).dt.date

    # ── Months to expiry ─────────────────────
    # (lease_end - today) gives a timedelta; .days / 30 converts to months
    df["months_to_expiry"] = df["lease_end"].apply(
        lambda d: max(0, (d - today).days / 30)
    )

    # ── Risk flag ────────────────────────────
    # Bucket each tenant into Critical / Watch / Stable
    def risk_flag(months):
        if months <= 12:   return "🔴 Critical"
        elif months <= 24: return "🟡 Watch"
        else:              return "🟢 Stable"

    df["risk"] = df["months_to_expiry"].apply(risk_flag)

    # ── Years remaining on lease ─────────────
    df["years_remaining"] = df["months_to_expiry"] / 12

    # ── Current in-place rent (escalated from lease start to today) ──
    # How many years has this tenant been in place?
    # We escalate their base rent to get today's actual in-place rent
    df["years_in_place"] = df["lease_start"].apply(
        lambda d: max(0, (today - d).days / 365)
    )
    df["current_rent_psf"] = df.apply(
        lambda r: r["rent_psf"] * (1 + r["annual_escalation_pct"]/100) ** r["years_in_place"],
        axis=1
    )

    # ── Mark-to-market ───────────────────────
    # How does in-place rent compare to market?
    # Positive = tenant is paying below market (rent bump on renewal)
    # Negative = tenant paying above market (rollover risk)
    df["mark_to_market_pct"] = (
        (df["market_rent_psf"] - df["current_rent_psf"]) / df["current_rent_psf"]
    )

    # ── In-place annual revenue ──────────────
    df["annual_revenue"] = df["sf"] * df["current_rent_psf"]

    # ── WALT (Weighted Average Lease Term) ───
    # Each tenant's weight = their SF as a fraction of total SF
    # WALT = Σ(weight_i × years_remaining_i)
    # Tells you: on average, how many years of lease term remain across the portfolio
    total_sf = df["sf"].sum()
    df["sf_weight"] = df["sf"] / total_sf
    walt = (df["sf_weight"] * df["years_remaining"]).sum()

    # ── Year-by-year revenue schedule ────────
    # For each year in the hold period, calculate each tenant's revenue
    # accounting for lease expiry, downtime, and re-leasing
    revenue_schedule = {}   # {year: {tenant: revenue}}
    analysis_date = today

    for yr in range(1, int(hold_yrs) + 1):
        # What date is the start/end of this analysis year?
        year_start = date(analysis_date.year + yr - 1, analysis_date.month, analysis_date.day)
        year_end   = date(analysis_date.year + yr,     analysis_date.month, analysis_date.day)
        year_rev   = {}

        for _, tenant in df.iterrows():
            lease_end_date = tenant["lease_end"]

            # ── Case 1: Lease is active for the full year ──
            # Tenant's lease end is after this year ends
            if lease_end_date >= year_end:
                # Escalate rent from today to mid-year
                years_from_today = yr - 0.5
                escalated_rent = tenant["current_rent_psf"] * (
                    1 + tenant["annual_escalation_pct"]/100
                ) ** years_from_today
                year_rev[tenant["tenant"]] = tenant["sf"] * escalated_rent

            # ── Case 2: Lease expires during this year ──
            # Tenant pays rent for part of the year, then space is vacant
            elif lease_end_date >= year_start:
                # Fraction of year tenant is still paying rent
                days_in_year = (year_end - year_start).days
                days_paying  = (lease_end_date - year_start).days
                fraction_paying = days_paying / days_in_year

                escalated_rent = tenant["current_rent_psf"] * (
                    1 + tenant["annual_escalation_pct"]/100
                ) ** (yr - 0.5)

                # Revenue = rent for portion tenant is in place
                # After expiry: downtime → $0 (handled by fraction)
                year_rev[tenant["tenant"]] = (
                    tenant["sf"] * escalated_rent * fraction_paying
                )

            # ── Case 3: Lease already expired, modeling re-lease ──
            # Space was vacant (downtime), now re-leasing at market rent
            else:
                # How many months since expiry at start of this year?
                months_since_expiry = (year_start - lease_end_date).days / 30

                if months_since_expiry < tenant["downtime_months"]:
                    # Still in downtime window — space is vacant, $0 revenue
                    year_rev[tenant["tenant"]] = 0.0
                else:
                    # Past downtime — new tenant in at market rent
                    # Apply renewal probability: some tenants don't come back
                    # We model expected revenue = prob × market_rent
                    new_rent = tenant["market_rent_psf"] * tenant["renewal_prob"]
                    # Escalate new rent forward from re-lease date
                    years_since_relet = (months_since_expiry - tenant["downtime_months"]) / 12
                    escalated_new_rent = new_rent * (1 + 0.025) ** years_since_relet
                    year_rev[tenant["tenant"]] = tenant["sf"] * escalated_new_rent

        revenue_schedule[yr] = year_rev

    # ── Expiry schedule ──────────────────────
    # How much SF expires each year? (used for the expiration chart)
    expiry_by_year = {}
    for yr in range(1, int(hold_yrs) + 1):
        yr_start = date(today.year + yr - 1, today.month, today.day)
        yr_end   = date(today.year + yr,     today.month, today.day)
        expiring_sf = df[
            (df["lease_end"] >= yr_start) & (df["lease_end"] < yr_end)
        ]["sf"].sum()
        expiry_by_year[yr] = expiring_sf

    # ── Summary metrics ──────────────────────
    summary = {
        "total_sf":          total_sf,
        "num_tenants":       len(df),
        "walt":              walt,
        "total_revenue":     df["annual_revenue"].sum(),
        "critical_sf":       df[df["risk"] == "🔴 Critical"]["sf"].sum(),
        "watch_sf":          df[df["risk"] == "🟡 Watch"]["sf"].sum(),
        "stable_sf":         df[df["risk"] == "🟢 Stable"]["sf"].sum(),
        "avg_mtm":           df["mark_to_market_pct"].mean(),
        "expiry_by_year":    expiry_by_year,
        "revenue_schedule":  revenue_schedule,
    }

    return df, summary


# ─────────────────────────────────────────────
#  PAGE HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
    <div class="page-header-left">
        <h1>{"Industrial Asset — " + address if address else "Industrial Asset Underwriting"}</h1>
        <p>{f"{square_feet:,} RSF · Built {year_built} · {cap_rate:.2f}% Cap · {ltv:.0f}% LTV"}</p>
    </div>
    <div>
        <span class="status-badge {badge_class}">{badge_text}</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TABS — Pro Forma | Rent Roll
# ─────────────────────────────────────────────
tab1, tab2 = st.tabs(["Pro Forma", "Rent Roll"])


# ═════════════════════════════════════════════
#  TAB 1 — PRO FORMA (same as Session 2)
# ═════════════════════════════════════════════
with tab1:

    section("NOI Build")
    col_noi, col_val = st.columns([1, 1])

    with col_noi:
        items = [
            ("Gross Potential Income", f"${gross_potential_income:>12,.0f}", False),
            ("Vacancy Loss",           f"(${vacancy_loss:,.0f})",            True),
            ("Other Income",           f"${other_income:>12,.0f}",           False),
            ("Effective Gross Income", f"${egi:>12,.0f}",                    False),
            ("Management Fee",         f"(${mgmt_fee:,.0f})",                True),
            ("Insurance",              f"(${insurance:,.0f})",               True),
            ("Real Estate Taxes",      f"(${re_taxes:,.0f})",                True),
            ("Maintenance & Repairs",  f"(${maintenance:,.0f})",             True),
            ("Total Expenses",         f"(${total_expenses:,.0f})",          True),
            ("Net Operating Income",   f"${noi:>12,.0f}",                    False),
        ]
        html = '<div style="background:var(--navy2);border:1px solid var(--border);padding:1rem 1.25rem;border-radius:2px;">'
        for label, val, is_neg in items:
            cls = "noi-negative" if is_neg else ""
            divider = 'border-top:1px solid var(--border);margin-top:0.4rem;padding-top:0.6rem;' if label in ("Effective Gross Income","Total Expenses","Net Operating Income") else ""
            html += f'<div class="noi-row" style="{divider}"><span class="noi-label">{label}</span><span class="noi-value {cls}">{val}</span></div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    with col_val:
        c1, c2 = st.columns(2)
        with c1:
            metric_card("NOI / SF", f"${noi/square_feet:.2f}")
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            metric_card("Implied Value", f"${value:,.0f}")
        with c2:
            metric_card("EGI", f"${egi:,.0f}")
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            metric_card("Value / SF", f"${value/square_feet:.2f}")

    section("Debt & Coverage")
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("Loan Amount", f"${loan_amount:,.0f}")
    with c2: metric_card("Annual Debt Service", f"${annual_debt_service:,.0f}")
    with c3: metric_card("DSCR", f"{dscr:.2f}x",
        "✓ Above 1.25x" if dscr_pass else "✗ Below 1.25x",
        "metric-pass" if dscr_pass else "metric-fail")
    with c4: metric_card("Equity Invested", f"${equity_invested:,.0f}")

    section("Returns Summary")
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("Cash-on-Cash", f"{cash_on_cash:.1%}",
        "✓ Above 7%" if coc_pass else "✗ Below 7%",
        "metric-pass" if coc_pass else "metric-fail")
    with c2: metric_card("IRR", f"{irr:.1%}",
        "✓ Above 12%" if irr_pass else "✗ Below 12%",
        "metric-pass" if irr_pass else "metric-fail")
    with c3: metric_card("Sale Price", f"${sale_price:,.0f}")
    with c4: metric_card("Sale Proceeds", f"${sale_proceeds:,.0f}")

    section("Cash Flow Analysis")
    col_chart1, col_chart2 = st.columns(2)

    CHART_LAYOUT = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#131929",
        font=dict(family="DM Sans", color="#9AA0B0", size=11),
        margin=dict(l=50, r=20, t=40, b=40),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.1)", tickfont=dict(family="DM Mono", size=10)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.1)", tickfont=dict(family="DM Mono", size=10))
    )

    with col_chart1:
        years       = list(range(1, int(hold_years)+1))
        noi_by_year = [noi * (1 + noi_growth/100)**yr for yr in years]
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=years, y=noi_by_year, marker_color="#C9A84C",
            marker_line_width=0, hovertemplate="Year %{x}<br>NOI: $%{y:,.0f}<extra></extra>"))
        fig1.update_layout(**CHART_LAYOUT,
            title=dict(text="Projected NOI — Hold Period", font=dict(size=12, color="#E8E8E8")),
            yaxis_tickprefix="$", yaxis_tickformat=",.0f", bargap=0.25)
        st.plotly_chart(fig1, use_container_width=True)

    with col_chart2:
        total_cf    = sum(annual_cash_flows[:-1])
        appreciation= sale_proceeds
        fig2 = go.Figure(go.Waterfall(
            orientation="v", measure=["absolute","relative","relative","total"],
            x=["Equity In","Operating CF","Sale Proceeds","Total Return"],
            y=[-equity_invested, total_cf, appreciation, None],
            connector=dict(line=dict(color="rgba(201,168,76,0.3)", width=1, dash="dot")),
            decreasing=dict(marker_color="#E74C3C"),
            increasing=dict(marker_color="#C9A84C"),
            totals=dict(marker_color="#2ECC71"),
            hovertemplate="%{x}<br>$%{y:,.0f}<extra></extra>"
        ))
        fig2.update_layout(**CHART_LAYOUT,
            title=dict(text="Return Waterfall", font=dict(size=12, color="#E8E8E8")),
            yaxis_tickprefix="$", yaxis_tickformat=",.0f", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    section("Sensitivity Analysis — IRR")
    st.markdown('<p style="font-size:0.75rem;color:#9AA0B0;margin-top:-0.5rem;margin-bottom:1rem;">Exit cap rate (rows) × NOI growth (columns)</p>', unsafe_allow_html=True)

    exit_caps    = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0]
    growth_rates = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    rows_sens = {}
    for g in growth_rates:
        row = []
        for ec in exit_caps:
            noi_s  = [noi * (1 + g/100)**yr for yr in range(1, int(hold_years)+1)]
            cf_s   = [n - annual_debt_service for n in noi_s]
            sp_s   = noi * (1 + g/100)**(hold_years+1) / (ec/100) - remaining_balance
            cf_s[-1] += sp_s
            irr_s  = npf.irr([-equity_invested] + cf_s)
            row.append(f"{irr_s:.1%}")
        rows_sens[f"{g:.1f}%"] = row

    df_sens = pd.DataFrame(rows_sens, index=[f"{ec:.1f}%" for ec in exit_caps])
    th_cells = "".join(f"<th>{col}</th>" for col in df_sens.columns)
    tbl = f'<div style="overflow-x:auto;"><table class="rr-table"><thead><tr><th>Exit Cap \\ Growth</th>{th_cells}</tr></thead><tbody>'
    for idx, row in df_sens.iterrows():
        cells = ""
        for val in row:
            try:
                v = float(val.strip('%'))/100
                color = "#2ECC71" if v >= 0.12 else ("#F39C12" if v >= 0.08 else "#E74C3C")
                cells += f'<td style="color:{color}">{val}</td>'
            except:
                cells += f"<td>{val}</td>"
        tbl += f"<tr><td>{idx}</td>{cells}</tr>"
    tbl += "</tbody></table></div>"
    st.markdown(tbl, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    section("Deal Verdict")
    c1, c2, c3 = st.columns(3)
    with c1: metric_card("DSCR", f"{dscr:.2f}x",
        "✓ Pass (≥1.25x)" if dscr_pass else "✗ Fail (<1.25x)",
        "metric-pass" if dscr_pass else "metric-fail")
    with c2: metric_card("Cash-on-Cash", f"{cash_on_cash:.1%}",
        "✓ Pass (≥7%)" if coc_pass else "✗ Fail (<7%)",
        "metric-pass" if coc_pass else "metric-fail")
    with c3: metric_card("IRR", f"{irr:.1%}",
        "✓ Pass (≥12%)" if irr_pass else "✗ Fail (<12%)",
        "metric-pass" if irr_pass else "metric-fail")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    if all_pass:
        st.success("✅  Deal passes all thresholds — worth pursuing")
    elif hard_fail:
        st.error("❌  DSCR below 1.0 — property cannot cover debt service. Pass on this deal.")
    else:
        st.warning("⚠️  Deal passes some thresholds but not all — review assumptions")


# ═════════════════════════════════════════════
#  TAB 2 — RENT ROLL
# ═════════════════════════════════════════════
with tab2:

    section("Rent Roll Upload")

    # ── Upload widget ──────────────────────────
    # st.file_uploader returns a file-like object or None if nothing uploaded
    uploaded = st.file_uploader(
        "Upload rent roll CSV",
        type="csv",
        help="Required columns: tenant, sf, lease_start, lease_end, rent_psf, annual_escalation_pct, renewal_prob, market_rent_psf, downtime_months"
    )

    # ── Download sample ────────────────────────
    # Lets users grab the template without leaving the app
    sample_csv = """tenant,sf,lease_start,lease_end,rent_psf,annual_escalation_pct,renewal_prob,market_rent_psf,downtime_months
Amazon Fulfillment,180000,2019-01-01,2026-06-30,5.50,2.0,0.80,6.25,3
FedEx Ground,95000,2021-03-01,2028-03-01,6.25,2.5,0.75,6.50,4
Regional Distributor,40000,2020-06-01,2025-12-31,4.75,0.0,0.55,5.75,6
Midwest Auto Parts,28000,2022-09-01,2027-09-01,5.85,2.0,0.70,6.00,5
Cold Chain Logistics,12000,2023-01-01,2030-12-31,7.25,3.0,0.85,7.50,3"""

    st.download_button(
        "⬇ Download Sample Rent Roll",
        data=sample_csv,
        file_name="sample_rent_roll.csv",
        mime="text/csv"
    )

    if uploaded is not None:
        # ── Read CSV ─────────────────────────
        # pd.read_csv parses the uploaded file into a DataFrame
        df_raw = pd.read_csv(uploaded)

        # ── Run rent roll model ───────────────
        df_rr, summary = build_rent_roll(df_raw.copy(), hold_years)

        # ── Portfolio summary cards ───────────
        section("Portfolio Overview")
        c1, c2, c3, c4 = st.columns(4)
        with c1: metric_card("Total Tenants", str(summary["num_tenants"]))
        with c2: metric_card("Total SF", f"{summary['total_sf']:,.0f}")
        with c3: metric_card(
            "WALT",
            f"{summary['walt']:.1f} yrs",
            "Weighted Avg Lease Term"
        )
        with c4: metric_card(
            "In-Place Revenue",
            f"${summary['total_revenue']:,.0f}",
            f"${summary['total_revenue']/summary['total_sf']:.2f} / SF"
        )

        # ── WALT visual bar ───────────────────
        # A simple progress bar showing WALT vs hold period
        # If WALT > hold period, tenants are locked in — low rollover risk
        walt_pct = min(summary["walt"] / hold_years, 1.0) * 100
        walt_color = "#2ECC71" if summary["walt"] >= hold_years * 0.6 else (
                     "#F39C12" if summary["walt"] >= hold_years * 0.3 else "#E74C3C")
        st.markdown(f"""
        <div style="margin: 0.5rem 0 1.5rem 0;">
            <div style="font-family:DM Mono,monospace;font-size:0.62rem;color:#9AA0B0;
                        letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.3rem;">
                WALT vs Hold Period ({summary['walt']:.1f} of {hold_years:.0f} yrs)
            </div>
            <div class="walt-bar-bg">
                <div class="walt-bar-fill" style="width:{walt_pct:.0f}%;background:{walt_color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Rollover risk summary ─────────────
        section("Rollover Risk")
        c1, c2, c3 = st.columns(3)
        total_sf = summary["total_sf"]
        with c1: metric_card(
            "🔴 Critical SF",
            f"{summary['critical_sf']:,.0f}",
            f"{summary['critical_sf']/total_sf:.0%} of portfolio · expiring <12mo",
            "metric-fail" if summary["critical_sf"] > 0 else ""
        )
        with c2: metric_card(
            "🟡 Watch SF",
            f"{summary['watch_sf']:,.0f}",
            f"{summary['watch_sf']/total_sf:.0%} of portfolio · expiring 12–24mo",
            "metric-warn" if summary["watch_sf"] > 0 else ""
        )
        with c3: metric_card(
            "Avg Mark-to-Market",
            f"{summary['avg_mtm']:+.1%}",
            "Positive = below-market rents (upside on renewal)",
            "metric-pass" if summary["avg_mtm"] > 0 else "metric-fail"
        )

        # ── Tenant rent roll table ────────────
        section("Tenant Detail")

        # ── Build display DataFrame ───────────
        # st.dataframe is more reliable than HTML tables inside st.tabs
        # We format all columns as strings first so we control display exactly
        display_df = pd.DataFrame({
            "Tenant":          df_rr["tenant"],
            "SF":              df_rr["sf"].apply(lambda x: f"{x:,.0f}"),
            "Lease End":       df_rr["lease_end"].astype(str),
            "Mo. to Exp.":     df_rr["months_to_expiry"].apply(lambda x: f"{x:.0f}"),
            "Risk":            df_rr["risk"],
            "In-Place $/SF":   df_rr["current_rent_psf"].apply(lambda x: f"${x:.2f}"),
            "Market $/SF":     df_rr["market_rent_psf"].apply(lambda x: f"${x:.2f}"),
            "Mark-to-Mkt":     df_rr["mark_to_market_pct"].apply(lambda x: f"{x:+.1%}"),
            "Ann. Revenue":    df_rr["annual_revenue"].apply(lambda x: f"${x:,.0f}"),
            "Renewal Prob":    df_rr["renewal_prob"].apply(lambda x: f"{x:.0%}"),
        })

        # ── Apply row-level color styling ─────
        # Pandas Styler lets us color individual cells based on values
        # We color the Risk column and Mark-to-Market column
        def style_risk(val):
            # Returns a CSS string for the cell background
            if "Critical" in str(val):
                return "color: #E74C3C; font-weight: 600"
            elif "Watch" in str(val):
                return "color: #F39C12"
            elif "Stable" in str(val):
                return "color: #2ECC71"
            return ""

        def style_mtm(val):
            # Green for positive MTM (below-market tenant = rent upside)
            # Red for negative MTM (above-market tenant = rollover risk)
            try:
                v = float(str(val).replace("%","").replace("+",""))
                return "color: #2ECC71" if v >= 0 else "color: #E74C3C"
            except:
                return ""

        styled = (
            display_df.style
            .applymap(style_risk,  subset=["Risk"])
            .applymap(style_mtm,   subset=["Mark-to-Mkt"])
            .set_properties(**{
                "background-color": "#131929",
                "color": "#E8E8E8",
                "font-family": "DM Mono, monospace",
                "font-size": "12px",
                "border": "1px solid rgba(201,168,76,0.15)"
            })
            .set_table_styles([{
                "selector": "th",
                "props": [
                    ("background-color", "#0A0E1A"),
                    ("color", "#C9A84C"),
                    ("font-family", "DM Mono, monospace"),
                    ("font-size", "11px"),
                    ("text-transform", "uppercase"),
                    ("letter-spacing", "0.08em"),
                    ("border", "1px solid rgba(201,168,76,0.2)"),
                    ("padding", "8px 12px"),
                ]
            }])
        )

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # ── Revenue schedule chart ────────────
        section("Projected Revenue by Tenant")
        st.markdown('<p style="font-size:0.75rem;color:#9AA0B0;margin-top:-0.5rem;margin-bottom:1rem;">Shows rollover dips and re-leasing recovery year by year</p>', unsafe_allow_html=True)

        rev_sched = summary["revenue_schedule"]
        years_list = list(range(1, int(hold_years) + 1))

        # One bar trace per tenant, stacked
        # This shows which tenant's revenue drops when their lease rolls
        COLORS = ["#C9A84C", "#4C9AC9", "#2ECC71", "#E74C3C", "#9B59B6",
                  "#F39C12", "#1ABC9C", "#E67E22", "#3498DB", "#E91E63"]

        fig3 = go.Figure()
        tenants = df_rr["tenant"].tolist()

        for i, tenant_name in enumerate(tenants):
            tenant_rev = [
                rev_sched[yr].get(tenant_name, 0) for yr in years_list
            ]
            fig3.add_trace(go.Bar(
                name=tenant_name,
                x=years_list,
                y=tenant_rev,
                marker_color=COLORS[i % len(COLORS)],
                marker_line_width=0,
                hovertemplate=f"{tenant_name}<br>Year %{{x}}<br>Revenue: $%{{y:,.0f}}<extra></extra>"
            ))

        fig3.update_layout(
            **CHART_LAYOUT,
            title=dict(text="Revenue by Tenant — Hold Period", font=dict(size=12, color="#E8E8E8")),
            barmode="stack",
            yaxis_tickprefix="$",
            yaxis_tickformat=",.0f",
            legend=dict(
                font=dict(family="DM Sans", size=10, color="#9AA0B0"),
                bgcolor="rgba(0,0,0,0)",
                orientation="h",
                yanchor="bottom", y=1.02,
                xanchor="left",   x=0
            ),
            bargap=0.2
        )
        st.plotly_chart(fig3, use_container_width=True)

        # ── Lease expiration schedule ─────────
        section("Lease Expiration Schedule")

        expiry_sf   = [summary["expiry_by_year"].get(yr, 0) for yr in years_list]
        expiry_pct  = [sf / total_sf for sf in expiry_sf]

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=years_list,
            y=expiry_sf,
            marker_color=[
                "#E74C3C" if p > 0.30 else ("#F39C12" if p > 0.15 else "#C9A84C")
                for p in expiry_pct
            ],
            marker_line_width=0,
            hovertemplate="Year %{x}<br>Expiring SF: %{y:,.0f}<extra></extra>"
        ))
        fig4.update_layout(
            **CHART_LAYOUT,
            title=dict(text="SF Expiring by Year", font=dict(size=12, color="#E8E8E8")),
            yaxis_tickformat=",.0f",
            bargap=0.3
        )
        st.plotly_chart(fig4, use_container_width=True)

    else:
        # ── Empty state ───────────────────────
        # Shows when no CSV has been uploaded yet
        st.markdown("""
        <div style="background:var(--navy2);border:1px solid var(--border);
                    padding:2.5rem;border-radius:2px;text-align:center;margin-top:1rem;">
            <div style="font-size:2rem;margin-bottom:0.75rem;">📋</div>
            <div style="font-weight:600;margin-bottom:0.5rem;color:var(--white);">
                No rent roll uploaded
            </div>
            <div style="font-size:0.8rem;color:var(--white-dim);max-width:400px;margin:0 auto;">
                Upload a CSV with your tenant lease data to model rollover risk,
                mark-to-market, and tenant-level revenue projections.
                Download the sample above to see the required format.
            </div>
        </div>
        """, unsafe_allow_html=True)
