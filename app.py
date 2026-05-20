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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --bg:        #F5F5F7;
    --surface:   #FFFFFF;
    --surface2:  #F5F5F7;
    --border:    #D2D2D7;
    --border2:   #E8E8ED;
    --navy:      #1D1D1F;
    --navy2:     #3A3A3C;
    --mid:       #6E6E73;
    --blue:      #0071E3;
    --blue-dim:  #EBF3FD;
    --green:     #1A7A4A;
    --green-dim: #EAFAF1;
    --red:       #C0392B;
    --red-dim:   #FDEDEC;
    --amber:     #9A6700;
    --amber-dim: #FEF9E7;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg);
    color: var(--navy);
    -webkit-font-smoothing: antialiased;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

[data-testid="stSidebar"] {
    background-color: var(--surface);
    border-right: 1px solid var(--border);
}
.sidebar-section {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--mid);
    padding: 1rem 0 0.4rem 0;
    border-top: 1px solid var(--border2);
    margin-top: 0.5rem;
}
.sidebar-section:first-child { border-top: none; margin-top: 0; }

.page-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding: 0.25rem 0 1.25rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.page-header-left h1 {
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--navy);
    margin: 0 0 0.2rem 0;
    letter-spacing: -0.02em;
}
.page-header-left p {
    font-size: 0.75rem;
    color: var(--mid);
    margin: 0;
    font-family: 'IBM Plex Mono', monospace;
}
.status-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0.3rem 0.85rem;
    border-radius: 20px;
    display: inline-block;
}
.badge-pass   { background: var(--green-dim); color: var(--green); border: 1px solid rgba(26,122,74,0.25); }
.badge-fail   { background: var(--red-dim);   color: var(--red);   border: 1px solid rgba(192,57,43,0.25); }
.badge-review { background: var(--amber-dim); color: var(--amber); border: 1px solid rgba(154,103,0,0.25); }

.section-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--mid);
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border2);
    margin: 1.75rem 0 1rem 0;
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: 2px solid var(--blue);
    padding: 1rem 1.25rem;
    border-radius: 8px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--mid);
    margin-bottom: 0.4rem;
}
.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--navy);
    line-height: 1;
    margin-bottom: 0.3rem;
    letter-spacing: -0.02em;
}
.metric-sub { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; color: var(--mid); }
.metric-pass { color: var(--green) !important; }
.metric-fail { color: var(--red)   !important; }
.metric-warn { color: var(--amber) !important; }

.noi-row {
    display: flex;
    justify-content: space-between;
    padding: 0.45rem 0;
    border-bottom: 1px solid var(--border2);
    font-size: 0.82rem;
}
.noi-row:last-child {
    border-bottom: none;
    font-weight: 700;
    color: var(--blue);
    padding-top: 0.6rem;
    margin-top: 0.25rem;
    border-top: 2px solid var(--border);
}
.noi-label { color: var(--navy2); }
.noi-value { font-family: 'IBM Plex Mono', monospace; color: var(--navy); }
.noi-negative { color: var(--red) !important; }

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid var(--border);
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--mid);
    background: transparent;
    border: none;
    padding: 0.65rem 1.25rem;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--blue) !important;
    border-bottom: 2px solid var(--blue) !important;
    background: transparent !important;
}

[data-testid="stExpander"] {
    background: var(--surface);
    border: 1px solid var(--border) !important;
    border-radius: 8px;
}

[data-testid="stDownloadButton"] button {
    background: var(--blue) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}

.walt-bar-bg  { background: var(--border2); border-radius: 4px; height: 6px; margin-top: 0.4rem; }
.walt-bar-fill { border-radius: 4px; height: 6px; }
.gold-divider  { height: 1px; background: var(--border); margin: 1.75rem 0; }

[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--navy);
    border-radius: 6px;
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
    occupancy_pct  = st.slider("Occupancy (%)", min_value=0, max_value=100, value=95, step=1)
    occupancy      = occupancy_pct / 100
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

    st.markdown('<div class="sidebar-section">CapEx & Leasing Costs</div>', unsafe_allow_html=True)
    capex_psf          = st.number_input("CapEx Reserve ($/SF/yr)", min_value=0.0, value=0.35, step=0.05)
    ti_new_psf         = st.number_input("TI — New Lease ($/SF)", min_value=0.0, value=8.00, step=0.50)
    ti_renewal_psf     = st.number_input("TI — Renewal ($/SF)", min_value=0.0, value=3.00, step=0.50)
    lc_pct             = st.number_input("Leasing Commission (%)", min_value=0.0, max_value=10.0, value=4.0, step=0.25)
    new_lease_term_yrs = st.number_input("New Lease Term (yrs)", min_value=1, max_value=20, value=5, step=1)

    st.markdown('<div class="sidebar-section">LP / GP Waterfall</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Scenario Analysis</div>', unsafe_allow_html=True)
    bear_rent_adj   = st.number_input("Bear — Rent Growth Adj (%)", min_value=-5.0, max_value=0.0, value=-1.0, step=0.25)
    bear_cap_adj    = st.number_input("Bear — Exit Cap Adj (%)",    min_value=0.0,  max_value=3.0,  value=0.75, step=0.25)
    bear_occ_adj    = st.number_input("Bear — Occupancy Adj (%)",   min_value=-20.0, max_value=0.0, value=-5.0, step=1.0)
    bull_rent_adj   = st.number_input("Bull — Rent Growth Adj (%)", min_value=0.0,  max_value=5.0,  value=1.0,  step=0.25)
    bull_cap_adj    = st.number_input("Bull — Exit Cap Adj (%)",    min_value=-3.0, max_value=0.0,  value=-0.5, step=0.25)
    bull_occ_adj    = st.number_input("Bull — Occupancy Adj (%)",   min_value=0.0,  max_value=10.0, value=2.0,  step=1.0)

    st.markdown('<div class="sidebar-section">LP / GP Waterfall</div>', unsafe_allow_html=True)
    lp_equity_pct   = st.number_input("LP Equity (%)", min_value=50.0, max_value=99.0, value=90.0, step=5.0)
    pref_return     = st.number_input("Preferred Return (%)", min_value=0.0, max_value=15.0, value=8.0, step=0.5)
    promote_tier1   = st.number_input("Promote — Tier 1 (%)", min_value=0.0, max_value=50.0, value=20.0, step=5.0)
    hurdle_tier1    = st.number_input("Hurdle — Tier 1 IRR (%)", min_value=0.0, max_value=30.0, value=12.0, step=0.5)
    promote_tier2   = st.number_input("Promote — Tier 2 (%)", min_value=0.0, max_value=50.0, value=30.0, step=5.0)
    hurdle_tier2    = st.number_input("Hurdle — Tier 2 IRR (%)", min_value=0.0, max_value=30.0, value=15.0, step=0.5)


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

# ─────────────────────────────────────────────
#  CAPEX / TI / LC MODEL
# ─────────────────────────────────────────────
def build_capex_schedule(sq_ft, hold_yrs, cap_psf,
                         ti_new, ti_renew, lc_p, lease_term,
                         rr_df=None, today=None):
    from datetime import date as _date
    if today is None:
        today = _date.today()
    schedule = {}
    for yr in range(1, int(hold_yrs) + 1):
        yr_costs = {}
        # CapEx reserve — every year, non-discretionary
        yr_costs["CapEx Reserve"] = sq_ft * cap_psf
        if rr_df is not None:
            yr_start = today.replace(year=today.year + yr - 1)
            yr_end   = today.replace(year=today.year + yr)
            rollovers = rr_df[
                (rr_df["lease_end"] >= yr_start) &
                (rr_df["lease_end"] <  yr_end)
            ]
            ti_cost = lc_cost = 0.0
            for _, t in rollovers.iterrows():
                sf   = t["sf"]
                rp   = t["renewal_prob"]
                mkt  = t["market_rent_psf"]
                # Weighted TI: renewal_prob renew at lower TI, rest new at higher TI
                ti_cost  += sf * (rp * ti_renew + (1 - rp) * ti_new)
                # LC only on new leases
                lc_cost  += sf * mkt * lease_term * (lc_p / 100) * (1 - rp)
            yr_costs["Tenant Improvements"] = ti_cost
            yr_costs["Leasing Commissions"] = lc_cost
        else:
            # No rent roll: assume 6% annual rollover, 70% renewal prob
            annual_sf = sq_ft * 0.06
            rp = 0.70
            yr_costs["Tenant Improvements"] = annual_sf * (rp * ti_renew + (1 - rp) * ti_new)
            yr_costs["Leasing Commissions"] = annual_sf * 6.50 * lease_term * (lc_p / 100) * (1 - rp)
        schedule[yr] = yr_costs

    annual_totals = {yr: sum(c.values()) for yr, c in schedule.items()}
    total_capex = sum(v.get("CapEx Reserve", 0)        for v in schedule.values())
    total_ti    = sum(v.get("Tenant Improvements", 0)  for v in schedule.values())
    total_lc    = sum(v.get("Leasing Commissions", 0)  for v in schedule.values())
    total_cost  = total_capex + total_ti + total_lc
    return {
        "schedule": schedule,
        "annual_totals": annual_totals,
        "total_capex":  total_capex,
        "total_ti":     total_ti,
        "total_lc":     total_lc,
        "total_cost":   total_cost,
        "psf_per_year": total_cost / sq_ft / hold_yrs if sq_ft > 0 else 0,
    }

capex_summary = build_capex_schedule(
    square_feet, hold_years, capex_psf,
    ti_new_psf, ti_renewal_psf, lc_pct, new_lease_term_yrs
)

# Adjusted IRR: subtract CapEx/TI/LC from each year's levered cash flow
annual_capex_costs = [capex_summary["annual_totals"][yr] for yr in range(1, int(hold_years)+1)]
adj_cf = [-equity_invested] + [
    cf - cap for cf, cap in zip(annual_cash_flows, annual_capex_costs)
]
irr_adj = npf.irr(adj_cf)

# ─────────────────────────────────────────────
#  LP / GP WATERFALL ENGINE
#  Distributes total proceeds through the tiers
#  in strict waterfall order. Returns per-tier
#  and total LP/GP distributions.
# ─────────────────────────────────────────────
def build_waterfall(equity_invested, annual_cfs, sale_proceeds_val,
                    lp_pct, pref_pct, promote_t1, hurdle_t1,
                    promote_t2, hurdle_t2, hold_yrs):
    """
    Parameters
    ----------
    equity_invested   : total equity (LP + GP combined)
    annual_cfs        : list of annual levered cash flows (before sale)
    sale_proceeds_val : net sale proceeds at end of hold
    lp_pct            : LP equity percentage (e.g. 0.90)
    pref_pct          : preferred return rate (e.g. 0.08)
    promote_t1        : GP promote in tier 1 (e.g. 0.20)
    hurdle_t1         : IRR hurdle for tier 1 (e.g. 0.12)
    promote_t2        : GP promote in tier 2 (e.g. 0.30)
    hurdle_t2         : IRR hurdle for tier 2 (e.g. 0.15)
    hold_yrs          : hold period in years

    Returns
    -------
    dict with per-tier distributions and summary metrics
    """
    gp_pct = 1.0 - lp_pct

    # Split equity contribution
    lp_equity = equity_invested * lp_pct
    gp_equity = equity_invested * gp_pct

    # Total cash available to distribute = operating CFs + sale
    # We combine everything into a single pool for waterfall math
    # Operating CFs flow annually; sale at end
    operating_cfs = annual_cfs[:-1]  # exclude last year (already has sale)
    # Recalculate clean operating CFs (without sale proceeds)
    clean_ops = [cf for cf in operating_cfs]
    total_operating = sum(clean_ops)
    total_pool = total_operating + sale_proceeds_val

    # ── Accumulated pref owed to LP ────────────
    # Simple interest on LP equity over hold period
    # (Institutional LPAs often use compound — we use simple for clarity)
    # pref_owed = LP equity x pref rate x years
    pref_owed = lp_equity * pref_pct * hold_yrs

    # ── Results dict — tracks each tier ────────
    tiers = {
        "lp_return_of_capital":  0.0,
        "gp_return_of_capital":  0.0,
        "lp_preferred_return":   0.0,
        "gp_catchup":            0.0,
        "lp_tier1_promote":      0.0,
        "gp_tier1_promote":      0.0,
        "lp_tier2_promote":      0.0,
        "gp_tier2_promote":      0.0,
    }

    remaining = total_pool

    # ── TIER 1: Return of Capital ───────────────
    # LP and GP get their equity back pro-rata
    roc = min(remaining, equity_invested)
    tiers["lp_return_of_capital"] = roc * lp_pct
    tiers["gp_return_of_capital"] = roc * gp_pct
    remaining -= roc

    # ── TIER 2: LP Preferred Return ─────────────
    # 100% to LP until pref is satisfied
    pref_dist = min(remaining, pref_owed)
    tiers["lp_preferred_return"] = pref_dist
    remaining -= pref_dist

    # ── TIER 3: GP Catch-Up ─────────────────────
    # GP gets distributions until they've received promote_t1 %
    # of total profits distributed so far
    # Total LP profit so far = pref_dist
    # GP needs: (promote_t1 / (1 - promote_t1)) * lp_profit_so_far
    lp_profit_so_far = pref_dist
    if promote_t1 > 0 and remaining > 0:
        catchup_needed = (promote_t1 / 100) / (1 - promote_t1 / 100) * lp_profit_so_far
        catchup_dist = min(remaining, catchup_needed)
        tiers["gp_catchup"] = catchup_dist
        remaining -= catchup_dist

    # ── TIER 4: Promote Tier 1 (up to hurdle_t1 IRR) ──
    # Split remaining at (1-promote_t1) LP / promote_t1 GP
    # until LP hits hurdle_t1 IRR on their equity
    # Simplified: split all remaining at tier 1 ratio
    # then check if we've exceeded hurdle_t1
    if remaining > 0:
        lp_share_t1 = (1 - promote_t1 / 100)
        gp_share_t1 = promote_t1 / 100

        # Estimate how much LP can receive before hitting hurdle_t1
        # LP total return at hurdle_t1 = lp_equity * hurdle_t1 * hold_yrs (simple)
        lp_target_t1 = lp_equity * (hurdle_t1 / 100) * hold_yrs
        lp_still_needed_t1 = max(0, lp_target_t1 - pref_dist)

        if lp_still_needed_t1 > 0:
            # How much total to distribute so LP gets lp_still_needed_t1?
            total_for_t1 = min(remaining, lp_still_needed_t1 / lp_share_t1)
            tiers["lp_tier1_promote"] = total_for_t1 * lp_share_t1
            tiers["gp_tier1_promote"] = total_for_t1 * gp_share_t1
            remaining -= total_for_t1

    # ── TIER 5: Promote Tier 2 (above hurdle_t2) ──
    # Everything left splits at tier 2 ratio
    if remaining > 0:
        lp_share_t2 = (1 - promote_t2 / 100)
        gp_share_t2 = promote_t2 / 100
        tiers["lp_tier2_promote"] = remaining * lp_share_t2
        tiers["gp_tier2_promote"] = remaining * gp_share_t2

    # ── Summary ─────────────────────────────────
    lp_total = (tiers["lp_return_of_capital"] + tiers["lp_preferred_return"] +
                tiers["lp_tier1_promote"] + tiers["lp_tier2_promote"])
    gp_total = (tiers["gp_return_of_capital"] + tiers["gp_catchup"] +
                tiers["gp_tier1_promote"] + tiers["gp_tier2_promote"])

    lp_profit = lp_total - lp_equity
    gp_profit = gp_total - gp_equity
    total_profit = lp_profit + gp_profit

    # GP promote = GP profit as % of total profit
    gp_promote_pct = gp_profit / total_profit if total_profit > 0 else 0

    # Equity multiples
    lp_em = lp_total / lp_equity if lp_equity > 0 else 0
    gp_em = gp_total / gp_equity if gp_equity > 0 else 0

    return {
        "tiers":          tiers,
        "lp_equity":      lp_equity,
        "gp_equity":      gp_equity,
        "lp_total":       lp_total,
        "gp_total":       gp_total,
        "lp_profit":      lp_profit,
        "gp_profit":      gp_profit,
        "lp_em":          lp_em,
        "gp_em":          gp_em,
        "gp_promote_pct": gp_promote_pct,
        "pref_owed":      pref_owed,
        "pref_paid":      tiers["lp_preferred_return"],
        "pref_satisfied": tiers["lp_preferred_return"] >= pref_owed * 0.99,
        "total_pool":     total_pool,
    }

# ─────────────────────────────────────────────
#  SCENARIO ENGINE
#  Runs full calculation stack for bear/base/bull
#  Returns a dict of metrics for each scenario
# ─────────────────────────────────────────────
def run_scenario(sq_ft, rent_psf_s, occupancy_s, other_inc,
                 mgmt_pct, ins_psf, tax_psf, maint_psf,
                 cap_rate_s, ltv_s, int_rate, amort_yrs,
                 hold_yrs, noi_gr, exit_cap_s,
                 cap_psf_s, ti_new, ti_renew, lc_p, lease_term,
                 lp_pct, pref_p, prom_t1, hurd_t1, prom_t2, hurd_t2):
    """Runs the full underwriting stack for one scenario.
    Returns a dict of key metrics."""
    import numpy_financial as _npf

    # Income
    gpi  = sq_ft * rent_psf_s
    vac  = gpi * (1 - occupancy_s)
    egi  = gpi - vac + other_inc
    exp  = egi*(mgmt_pct/100) + sq_ft*(ins_psf+tax_psf+maint_psf)
    noi  = egi - exp

    # Valuation & debt
    val  = noi / (cap_rate_s / 100)
    loan = val * (ltv_s / 100)
    mr   = (int_rate / 100) / 12
    np_  = amort_yrs * 12
    pmt  = loan * (mr * (1+mr)**np_) / ((1+mr)**np_ - 1)
    ads  = pmt * 12
    dscr = noi / ads
    eq   = val - loan
    coc  = (noi - ads) / eq

    # Remaining balance
    pm   = int(hold_yrs) * 12
    rp   = (amort_yrs * 12) - pm
    rb   = pmt * (1 - (1+mr)**-rp) / mr

    # Cash flows
    noi_l = [noi*(1+noi_gr/100)**yr for yr in range(1, int(hold_yrs)+1)]
    acf   = [n - ads for n in noi_l]
    en    = noi*(1+noi_gr/100)**(hold_yrs+1)
    sp    = en/(exit_cap_s/100) - rb
    sale  = en/(exit_cap_s/100)
    acf[-1] += sp
    cfs   = [-eq] + acf
    irr   = _npf.irr(cfs)
    em    = sum(acf) / eq  # simplified EM

    # CapEx drag
    cx = build_capex_schedule(sq_ft, hold_yrs, cap_psf_s,
                               ti_new, ti_renew, lc_p, lease_term)
    adj = [-eq] + [cf - cx["annual_totals"][yr]
                   for yr, cf in enumerate(acf, 1)]
    irr_adj = _npf.irr(adj)

    # Waterfall
    wf = build_waterfall(eq, acf, sp, lp_pct, pref_p,
                         prom_t1, hurd_t1, prom_t2, hurd_t2, hold_yrs)

    return {
        "noi":      noi,
        "value":    val,
        "dscr":     dscr,
        "coc":      coc,
        "irr":      irr,
        "irr_adj":  irr_adj,
        "lp_em":    wf["lp_em"],
        "gp_em":    wf["gp_em"],
        "sale":     sale,
        "sp":       sp,
    }

# Build assumption sets
base_args = dict(
    sq_ft=square_feet, rent_psf_s=rent_psf, occupancy_s=occupancy,
    other_inc=other_income, mgmt_pct=mgmt_fee_pct, ins_psf=insurance_psf,
    tax_psf=re_taxes_psf, maint_psf=maintenance_psf,
    cap_rate_s=cap_rate, ltv_s=ltv, int_rate=interest_rate,
    amort_yrs=amort_years, hold_yrs=hold_years, noi_gr=noi_growth,
    exit_cap_s=exit_cap, cap_psf_s=capex_psf, ti_new=ti_new_psf,
    ti_renew=ti_renewal_psf, lc_p=lc_pct, lease_term=new_lease_term_yrs,
    lp_pct=lp_equity_pct/100, pref_p=pref_return/100,
    prom_t1=promote_tier1, hurd_t1=hurdle_tier1,
    prom_t2=promote_tier2, hurd_t2=hurdle_tier2,
)
bear_args = {**base_args,
    "occupancy_s": max(0.5,  occupancy  + bear_occ_adj/100),
    "noi_gr":      max(0.0,  noi_growth + bear_rent_adj),
    "exit_cap_s":  exit_cap + bear_cap_adj,
}
bull_args = {**base_args,
    "occupancy_s": min(1.0,  occupancy  + bull_occ_adj/100),
    "noi_gr":      noi_growth + bull_rent_adj,
    "exit_cap_s":  max(0.1,  exit_cap   + bull_cap_adj),
}

s_bear = run_scenario(**bear_args)
s_base = run_scenario(**base_args)
s_bull = run_scenario(**bull_args)

scenarios = {
    "Bear": s_bear,
    "Base": s_base,
    "Bull": s_bull,
}

# ─────────────────────────────────────────────
#  EXCEL EXPORT ENGINE
#  Builds a multi-sheet .xlsx workbook using
#  openpyxl with institutional formatting:
#  navy headers, gold accents, number formats.
#  Returns bytes that Streamlit can serve as
#  a download button.
# ─────────────────────────────────────────────
def build_excel_export(
    address, square_feet, year_built,
    rent_psf, occupancy, other_income,
    mgmt_fee_pct, insurance_psf, re_taxes_psf, maintenance_psf,
    gross_potential_income, vacancy_loss, egi,
    mgmt_fee, insurance, re_taxes, maintenance, total_expenses, noi,
    cap_rate, value, loan_amount, annual_debt_service, dscr,
    levered_cash_flow, equity_invested, cash_on_cash,
    irr, irr_adj, sale_price, sale_proceeds,
    hold_years, noi_growth, exit_cap,
    capex_summary, wf_data,
    s_bear, s_base, s_bull,
    bear_args, base_args, bull_args,
    lp_equity_pct, pref_return, promote_tier1, hurdle_tier1,
    promote_tier2, hurdle_tier2,
    rent_roll_df=None
):
    import openpyxl
    from openpyxl.styles import (PatternFill, Font, Alignment,
                                  Border, Side, numbers)
    from openpyxl.utils import get_column_letter
    import io

    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # remove default sheet

    # ── Style constants ──────────────────────
    NAVY    = "1B2A4A"   # title bars — dark navy bg
    NAVY2   = "FFFFFF"   # even rows — white
    NAVY3   = "F8FAFB"   # odd rows — near white
    GOLD    = "1B2A4A"   # kept for compatibility
    WHITE   = "000000"   # body text — dark navy
    GREEN   = "155724"   # dark green text
    RED     = "000000"   # dark red text
    AMBER   = "000000"   # dark amber text
    HBLU    = "D6EAFF"   # header fill — light blue
    KBLU    = "EEF6FF"   # key row fill — very light blue

    def hdr_fill(hex_color):
        return PatternFill("solid", fgColor=hex_color)

    def hdr_font(hex_color="1B2A4A", bold=True, size=10):
        return Font(name="Calibri", color=hex_color, bold=bold, size=size)

    def num_font(size=10):
        return Font(name="Calibri", color="000000", size=size)

    def thin_border():
        s = Side(style="thin", color="C8D8E8")
        return Border(left=s, right=s, top=s, bottom=s)

    def set_col_width(ws, col, width):
        ws.column_dimensions[get_column_letter(col)].width = width

    def write_header_row(ws, row, cols, fill_color="D6EAFF"):
        for c, (text, width) in enumerate(cols, 1):
            cell = ws.cell(row=row, column=c, value=text)
            cell.fill    = hdr_fill(fill_color)
            cell.font    = Font(name="Calibri", color="1B2A4A", bold=True, size=10)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border  = thin_border()
            set_col_width(ws, c, width)

    def write_data_row(ws, row, values, fmt=None, bold=False, color=WHITE):
        for c, val in enumerate(values, 1):
            cell = ws.cell(row=row, column=c, value=val)
            cell.fill   = hdr_fill("FFFFFF" if row % 2 == 0 else "F7F9FC")
            cell.font   = Font(name="Calibri", color="000000",
                               bold=bold, size=10)
            cell.border = thin_border()
            cell.alignment = Alignment(horizontal="right" if c > 1 else "left",
                                       vertical="center")
            if fmt and c < len(fmt)+1:
                cell.number_format = fmt[c-1] if fmt[c-1] else "General"

    # ════════════════════════════════════════
    #  SHEET 1 — PRO FORMA
    # ════════════════════════════════════════
    ws1 = wb.create_sheet("Pro Forma")
    ws1.sheet_view.showGridLines = False
    ws1.sheet_properties.tabColor = GOLD

    # Title block
    ws1.merge_cells("A1:D1")
    title = ws1["A1"]
    title.value = f"INDUSTRIAL ASSET UNDERWRITING — {address.upper() if address else 'UNNAMED ASSET'}"
    title.fill  = hdr_fill("B8CCE4")
    title.font  = Font(name="Calibri", color="1B2A4A", bold=True, size=13)
    title.alignment = Alignment(horizontal="left", vertical="center")
    ws1.row_dimensions[1].height = 28

    ws1.merge_cells("A2:D2")
    sub = ws1["A2"]
    sub.value = f"{square_feet:,} RSF  |  Built {year_built}  |  {cap_rate:.2f}% Cap Rate  |  {hold_years:.0f}-Year Hold"
    sub.fill  = hdr_fill(NAVY2)
    sub.font  = Font(name="Calibri", color="AABCCC", size=10)
    sub.alignment = Alignment(horizontal="left", vertical="center")

    # Section: NOI Build
    row = 4
    ws1.merge_cells(f"A{row}:D{row}")
    sec = ws1[f"A{row}"]
    sec.value = "NOI BUILD"
    sec.fill  = hdr_fill("B8CCE4")
    sec.font  = Font(name="Calibri", color="1B2A4A", bold=True, size=10)

    row += 1
    write_header_row(ws1, row,
        [("Line Item",30),("Amount ($)",18),("$/SF",12),("% of GPI",14)],
        "D6EAFF")

    noi_rows = [
        ("Gross Potential Income", gross_potential_income, gross_potential_income/square_feet, 1.0),
        ("Vacancy Loss",           -vacancy_loss,         -vacancy_loss/square_feet,          -vacancy_loss/gross_potential_income),
        ("Other Income",           other_income,           other_income/square_feet,            other_income/gross_potential_income),
        ("Effective Gross Income", egi,                    egi/square_feet,                    egi/gross_potential_income),
        ("Management Fee",         -mgmt_fee,             -mgmt_fee/square_feet,              -mgmt_fee/gross_potential_income),
        ("Insurance",              -insurance,            -insurance/square_feet,             -insurance/gross_potential_income),
        ("Real Estate Taxes",      -re_taxes,             -re_taxes/square_feet,              -re_taxes/gross_potential_income),
        ("Maintenance & Repairs",  -maintenance,          -maintenance/square_feet,           -maintenance/gross_potential_income),
        ("Total Expenses",         -total_expenses,       -total_expenses/square_feet,        -total_expenses/gross_potential_income),
        ("Net Operating Income",   noi,                    noi/square_feet,                    noi/gross_potential_income),
    ]
    SEPARATORS = {"Effective Gross Income", "Total Expenses", "Net Operating Income"}
    dollar_fmt = ['#,##0', '#,##0.00', '0.0%']
    for label, amt, psf, pct in noi_rows:
        row += 1
        is_sep = label in SEPARATORS
        color  = "000000"
        write_data_row(ws1, row, [label, amt, psf, pct],
                       fmt=["General","#,##0","#,##0.00","0.0%"],
                       bold=is_sep, color=color)

    # Section: Debt & Returns
    row += 2
    ws1.merge_cells(f"A{row}:D{row}")
    sec2 = ws1[f"A{row}"]
    sec2.value = "DEBT & RETURNS"
    sec2.fill  = hdr_fill("B8CCE4")
    sec2.font  = Font(name="Calibri", color="1B2A4A", bold=True, size=10)

    row += 1
    write_header_row(ws1, row,
        [("Metric",30),("Value",18),("Threshold",18),("Status",14)], "D6EAFF")

    debt_rows = [
        ("Implied Property Value",   value,                "—",        "—"),
        ("Loan Amount",              loan_amount,          "—",        "—"),
        ("Annual Debt Service",      annual_debt_service,  "—",        "—"),
        ("DSCR",                     f"{dscr:.2f}x",       "≥ 1.25x",  "✓ Pass" if dscr>=1.25 else "✗ Fail"),
        ("Cash-on-Cash Return",      f"{cash_on_cash:.1%}","≥ 7.0%",   "✓ Pass" if cash_on_cash>=0.07 else "✗ Fail"),
        ("IRR (Unadjusted)",         f"{irr:.1%}",         "≥ 12.0%",  "✓ Pass" if irr>=0.12 else "✗ Fail"),
        ("IRR (After CapEx/TI/LC)",  f"{irr_adj:.1%}",     "≥ 12.0%",  "✓ Pass" if irr_adj>=0.12 else "✗ Fail"),
        ("Sale Price",               sale_price,           "—",        "—"),
        ("Sale Proceeds (Net)",      sale_proceeds,        "—",        "—"),
        ("Equity Invested",          equity_invested,      "—",        "—"),
    ]
    for i, (label, val, thresh, status) in enumerate(debt_rows):
        row += 1
        cell_color = GREEN if "✓" in str(status) else (RED if "✗" in str(status) else WHITE)
        ws1.cell(row=row, column=1, value=label).fill  = hdr_fill(NAVY2 if row%2==0 else NAVY3)
        ws1.cell(row=row, column=1).font  = num_font()
        ws1.cell(row=row, column=1).border = thin_border()
        ws1.cell(row=row, column=1).alignment = Alignment(horizontal="left")
        for c, v in enumerate([val, thresh, status], 2):
            cell = ws1.cell(row=row, column=c, value=v)
            is_key = label in ("DSCR", "IRR (Unadjusted)", "IRR (After CapEx/TI/LC)", "Cash-on-Cash Return")
            bg = "EEF6FF" if is_key else ("FFFFFF" if row%2==0 else "F8FAFB")
            cell.fill   = hdr_fill(bg)
            cell.font   = Font(name="Calibri",
                               color=cell_color if c==4 else "000000",
                               size=10, bold=(c==4 or is_key))
            cell.border = thin_border()
            cell.alignment = Alignment(horizontal="right" if c>1 else "left")
            if isinstance(v, float) and v > 100:
                cell.number_format = "#,##0"

    # ════════════════════════════════════════
    #  SHEET 2 — SCENARIO ANALYSIS
    # ════════════════════════════════════════
    ws2 = wb.create_sheet("Scenario Analysis")
    ws2.sheet_view.showGridLines = False
    ws2.sheet_properties.tabColor = "4C9AC9"

    ws2.merge_cells("A1:D1")
    t2 = ws2["A1"]
    t2.value = "SCENARIO ANALYSIS — BEAR / BASE / BULL"
    t2.fill  = hdr_fill("B8CCE4")
    t2.font  = Font(name="Calibri", color="1B2A4A", bold=True, size=13)
    t2.alignment = Alignment(horizontal="left", vertical="center")
    ws2.row_dimensions[1].height = 28

    row = 3
    write_header_row(ws2, row,
        [("Metric",28),("Bear",18),("Base",18),("Bull",18)], "D6EAFF")

    scenario_rows = [
        ("Occupancy",          f"{bear_args['occupancy_s']:.0%}",   f"{base_args['occupancy_s']:.0%}",   f"{bull_args['occupancy_s']:.0%}"),
        ("NOI Growth (%/yr)",  f"{bear_args['noi_gr']:.2f}%",       f"{base_args['noi_gr']:.2f}%",       f"{bull_args['noi_gr']:.2f}%"),
        ("Exit Cap Rate (%)",  f"{bear_args['exit_cap_s']:.2f}%",   f"{base_args['exit_cap_s']:.2f}%",   f"{bull_args['exit_cap_s']:.2f}%"),
        ("—",                  "—","—","—"),
        ("NOI",                f"${s_bear['noi']:,.0f}",   f"${s_base['noi']:,.0f}",   f"${s_bull['noi']:,.0f}"),
        ("Implied Value",      f"${s_bear['value']:,.0f}", f"${s_base['value']:,.0f}", f"${s_bull['value']:,.0f}"),
        ("DSCR",               f"{s_bear['dscr']:.2f}x",  f"{s_base['dscr']:.2f}x",  f"{s_bull['dscr']:.2f}x"),
        ("Cash-on-Cash",       f"{s_bear['coc']:.1%}",    f"{s_base['coc']:.1%}",    f"{s_bull['coc']:.1%}"),
        ("IRR (Unadjusted)",   f"{s_bear['irr']:.1%}",    f"{s_base['irr']:.1%}",    f"{s_bull['irr']:.1%}"),
        ("IRR (After CapEx)",  f"{s_bear['irr_adj']:.1%}",f"{s_base['irr_adj']:.1%}",f"{s_bull['irr_adj']:.1%}"),
        ("LP Equity Multiple", f"{s_bear['lp_em']:.2f}x", f"{s_base['lp_em']:.2f}x", f"{s_bull['lp_em']:.2f}x"),
        ("GP Equity Multiple", f"{s_bear['gp_em']:.2f}x", f"{s_base['gp_em']:.2f}x", f"{s_bull['gp_em']:.2f}x"),
        ("Sale Price",         f"${s_bear['sale']:,.0f}",  f"${s_base['sale']:,.0f}",  f"${s_bull['sale']:,.0f}"),
    ]
    for i, r in enumerate(scenario_rows):
        row += 1
        for c, v in enumerate(r, 1):
            cell = ws2.cell(row=row, column=c, value=v)
            cell.fill   = hdr_fill("FFFFFF" if row%2==0 else "F8FAFB")
            cell.font   = Font(name="Calibri", color="000000", size=10)
            cell.border = thin_border()
            cell.alignment = Alignment(horizontal="left" if c==1 else "center")

    # ════════════════════════════════════════
    #  SHEET 3 — CAPEX SCHEDULE
    # ════════════════════════════════════════
    ws3 = wb.create_sheet("CapEx Schedule")
    ws3.sheet_view.showGridLines = False
    ws3.sheet_properties.tabColor = "E74C3C"

    ws3.merge_cells("A1:G1")
    t3 = ws3["A1"]
    t3.value = "CAPITAL EXPENDITURE SCHEDULE"
    t3.fill  = hdr_fill("B8CCE4")
    t3.font  = Font(name="Calibri", color="1B2A4A", bold=True, size=13)
    t3.alignment = Alignment(horizontal="left", vertical="center")
    ws3.row_dimensions[1].height = 28

    row = 3
    write_header_row(ws3, row, [
        ("Year",10), ("CapEx Reserve",18), ("Tenant Improvements",22),
        ("Leasing Commissions",20), ("Total Capital Cost",20),
        ("Levered CF",18), ("Adj. CF (after CapEx)",22)
    ], "D6EAFF")

    yrs = list(range(1, int(hold_years)+1))
    noi_by_yr  = [noi*(1+noi_growth/100)**yr for yr in yrs]
    lev_cf_yr  = [n - annual_debt_service for n in noi_by_yr]
    cap_yr     = [capex_summary["annual_totals"][yr] for yr in yrs]
    adj_cf_yr  = [l - c for l, c in zip(lev_cf_yr, cap_yr)]

    for yr in yrs:
        row += 1
        s = capex_summary["schedule"][yr]
        vals = [
            yr,
            s.get("CapEx Reserve", 0),
            s.get("Tenant Improvements", 0),
            s.get("Leasing Commissions", 0),
            capex_summary["annual_totals"][yr],
            lev_cf_yr[yr-1],
            adj_cf_yr[yr-1],
        ]
        write_data_row(ws3, row, vals,
                       fmt=["General","#,##0","#,##0","#,##0","#,##0","#,##0","#,##0"])

    # Totals row
    row += 1
    totals = [
        "TOTAL",
        capex_summary["total_capex"],
        capex_summary["total_ti"],
        capex_summary["total_lc"],
        capex_summary["total_cost"],
        sum(lev_cf_yr),
        sum(adj_cf_yr),
    ]
    for c, v in enumerate(totals, 1):
        cell = ws3.cell(row=row, column=c, value=v)
        cell.fill   = hdr_fill("D6EAFF")
        cell.font   = Font(name="Calibri", color="000000", bold=True, size=10)
        cell.border = thin_border()
        cell.alignment = Alignment(horizontal="right" if c>1 else "left")
        if c > 1 and isinstance(v, float):
            cell.number_format = "#,##0"

    # ════════════════════════════════════════
    #  SHEET 4 — WATERFALL
    # ════════════════════════════════════════
    ws4 = wb.create_sheet("LP-GP Waterfall")
    ws4.sheet_view.showGridLines = False
    ws4.sheet_properties.tabColor = "C9A84C"

    ws4.merge_cells("A1:D1")
    t4 = ws4["A1"]
    t4.value = "LP / GP WATERFALL DISTRIBUTION"
    t4.fill  = hdr_fill("B8CCE4")
    t4.font  = Font(name="Calibri", color="1B2A4A", bold=True, size=13)
    t4.alignment = Alignment(horizontal="left", vertical="center")
    ws4.row_dimensions[1].height = 28

    row = 3
    write_header_row(ws4, row,
        [("Item",30),("LP",18),("GP",18),("Total",18)], "D6EAFF")

    t = wf_data["tiers"]
    wf_rows = [
        ("Return of Capital",   t["lp_return_of_capital"], t["gp_return_of_capital"],
         t["lp_return_of_capital"]+t["gp_return_of_capital"]),
        ("Preferred Return",    t["lp_preferred_return"],  0,
         t["lp_preferred_return"]),
        ("GP Catch-Up",         0, t["gp_catchup"],        t["gp_catchup"]),
        ("Promote Tier 1",      t["lp_tier1_promote"],     t["gp_tier1_promote"],
         t["lp_tier1_promote"]+t["gp_tier1_promote"]),
        ("Promote Tier 2",      t["lp_tier2_promote"],     t["gp_tier2_promote"],
         t["lp_tier2_promote"]+t["gp_tier2_promote"]),
        ("TOTAL",               wf_data["lp_total"],       wf_data["gp_total"],
         wf_data["lp_total"]+wf_data["gp_total"]),
    ]
    for label, lp_v, gp_v, tot in wf_rows:
        row += 1
        is_total = label == "TOTAL"
        for c, v in enumerate([label, lp_v, gp_v, tot], 1):
            cell = ws4.cell(row=row, column=c, value=v)
            cell.fill   = hdr_fill("D6EAFF" if is_total else (NAVY2 if row%2==0 else NAVY3))
            cell.font   = Font(name="Calibri",
                               color="000000",
                               bold=is_total, size=10)
            cell.border = thin_border()
            cell.alignment = Alignment(horizontal="left" if c==1 else "right")
            if c > 1 and isinstance(v, (int, float)):
                cell.number_format = "#,##0"

    # ── Key metrics block ────────────────────
    row += 2
    summary_rows = [
        ("LP Equity Invested",  wf_data["lp_equity"]),
        ("GP Equity Invested",  wf_data["gp_equity"]),
        ("LP Equity Multiple",  f"{wf_data['lp_em']:.2f}x"),
        ("GP Equity Multiple",  f"{wf_data['gp_em']:.2f}x"),
        ("GP Promote % of Profits", f"{wf_data['gp_promote_pct']:.1%}"),
        ("Pref Return Satisfied", "Yes" if wf_data["pref_satisfied"] else "No"),
    ]
    for label, val in summary_rows:
        row += 1
        ws4.cell(row=row, column=1, value=label).fill = hdr_fill("F8FAFB")
        ws4.cell(row=row, column=1).font   = num_font()
        ws4.cell(row=row, column=1).border = thin_border()
        ws4.cell(row=row, column=1).alignment = Alignment(horizontal="left")
        cell = ws4.cell(row=row, column=2, value=val)
        cell.fill   = hdr_fill(NAVY3)
        cell.font   = Font(name="Calibri", color="FFFFFF", bold=True, size=10)
        cell.border = thin_border()
        cell.alignment = Alignment(horizontal="right")
        if isinstance(val, float):
            cell.number_format = "#,##0"

    # ════════════════════════════════════════
    #  SHEET 5 — 10-YEAR CASH FLOW
    # ════════════════════════════════════════
    ws_cf = wb.create_sheet("10-Year Pro Forma")
    ws_cf.sheet_view.showGridLines = False
    ws_cf.sheet_properties.tabColor = "4C9AC9"
    ws_cf.merge_cells("A1:H1")
    t_cf = ws_cf["A1"]
    t_cf.value = "10-YEAR CASH FLOW PROJECTION"
    t_cf.fill  = hdr_fill("B8CCE4")
    t_cf.font  = Font(name="Calibri", color="1B2A4A", bold=True, size=13)
    t_cf.alignment = Alignment(horizontal="left", vertical="center")
    ws_cf.row_dimensions[1].height = 28
    row = 3
    write_header_row(ws_cf, row, [
        ("Year",8),("NOI",16),("NOI/SF",10),
        ("Debt Service",16),("Levered CF",16),
        ("CapEx/TI/LC",16),("Adj. CF",16),("Cum. Adj. CF",16)
    ])
    _noi_l = [noi*(1+noi_growth/100)**yr for yr in range(1,int(hold_years)+1)]
    _lev_l = [n - annual_debt_service for n in _noi_l]
    _cap_l = [capex_summary["annual_totals"][yr] for yr in range(1,int(hold_years)+1)]
    _adj_l = [l - c for l,c in zip(_lev_l,_cap_l)]
    _cum = 0
    for i,yr in enumerate(range(1,int(hold_years)+1)):
        row += 1
        _cum += _adj_l[i]
        is_last = (i == int(hold_years)-1)
        bg = "EEF6FF" if is_last else ("FFFFFF" if row%2==0 else "F8FAFB")
        vals = [yr, _noi_l[i], _noi_l[i]/square_feet, annual_debt_service,
                _lev_l[i]+(sale_proceeds if is_last else 0),
                _cap_l[i], _adj_l[i]+(sale_proceeds if is_last else 0),
                _cum+(sale_proceeds if is_last else 0)]
        fmts = ["General","#,##0","#,##0.00","#,##0","#,##0","#,##0","#,##0","#,##0"]
        for c,(v,f) in enumerate(zip(vals,fmts),1):
            cell = ws_cf.cell(row=row, column=c, value=v)
            cell.fill = hdr_fill(bg)
            cell.font = Font(name="Calibri", color="000000", bold=is_last, size=10)
            cell.border = thin_border()
            cell.number_format = f
            cell.alignment = Alignment(
                horizontal="right" if c>1 else "center", vertical="center")

    # ════════════════════════════════════════
    #  SHEET 6 — RENT ROLL (if uploaded)
    # ════════════════════════════════════════
    if rent_roll_df is not None:
        ws5 = wb.create_sheet("Rent Roll")
        ws5.sheet_view.showGridLines = False
        ws5.sheet_properties.tabColor = "2ECC71"

        ws5.merge_cells("A1:J1")
        t5 = ws5["A1"]
        t5.value = "RENT ROLL"
        t5.fill  = hdr_fill("B8CCE4")
        t5.font  = Font(name="Calibri", color="1B2A4A", bold=True, size=13)
        t5.alignment = Alignment(horizontal="left", vertical="center")
        ws5.row_dimensions[1].height = 28

        row = 3
        write_header_row(ws5, row, [
            ("Tenant",22), ("SF",12), ("Lease End",14),
            ("Mo. to Exp.",12), ("Risk",12),
            ("In-Place $/SF",14), ("Market $/SF",14),
            ("Mark-to-Mkt",14), ("Ann. Revenue",16),
            ("Renewal Prob",14)
        ], "D6EAFF")

        for _, t_row in rent_roll_df.iterrows():
            row += 1
            mtm = t_row["mark_to_market_pct"]
            risk_str = str(t_row["risk"])
            if "Critical" in risk_str:   risk_color = RED
            elif "Watch" in risk_str:    risk_color = AMBER
            else:                        risk_color = GREEN
            mtm_color = GREEN if mtm >= 0 else RED

            vals = [
                t_row["tenant"],
                t_row["sf"],
                str(t_row["lease_end"]),
                round(t_row["months_to_expiry"]),
                risk_str,
                t_row["current_rent_psf"],
                t_row["market_rent_psf"],
                t_row["mark_to_market_pct"],
                t_row["annual_revenue"],
                t_row["renewal_prob"],
            ]
            fmts = ["General","#,##0","General","General","General",
                    "#,##0.00","#,##0.00","0.0%","#,##0","0%"]
            colors = [WHITE,WHITE,WHITE,WHITE,risk_color,
                      WHITE,WHITE,mtm_color,WHITE,WHITE]
            for c, (v, f, col) in enumerate(zip(vals, fmts, colors), 1):
                cell = ws5.cell(row=row, column=c, value=v)
                cell.fill   = hdr_fill(NAVY2 if row%2==0 else NAVY3)
                cell.font   = Font(name="Calibri", color=col, size=10)
                cell.border = thin_border()
                cell.alignment = Alignment(
                    horizontal="left" if c==1 else "right",
                    vertical="center"
                )
                cell.number_format = f

    # ── Save to bytes buffer ─────────────────
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.getvalue()

# Run waterfall with current inputs
# Use the operating cash flows (exclude sale, which we pass separately)
wf = build_waterfall(
    equity_invested   = equity_invested,
    annual_cfs        = annual_cash_flows,
    sale_proceeds_val = sale_proceeds,
    lp_pct            = lp_equity_pct / 100,
    pref_pct          = pref_return / 100,
    promote_t1        = promote_tier1,
    hurdle_t1         = hurdle_tier1,
    promote_t2        = promote_tier2,
    hurdle_t2         = hurdle_tier2,
    hold_yrs          = hold_years,
)

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
# ── Build export (runs every time inputs change) ──
# We pass rent_roll_df only if the user has uploaded one
# st.session_state stores it between reruns
_rr_export = st.session_state.get("rent_roll_df_export", None)
excel_bytes = build_excel_export(
    address=address, square_feet=square_feet, year_built=year_built,
    rent_psf=rent_psf, occupancy=occupancy, other_income=other_income,
    mgmt_fee_pct=mgmt_fee_pct, insurance_psf=insurance_psf,
    re_taxes_psf=re_taxes_psf, maintenance_psf=maintenance_psf,
    gross_potential_income=gross_potential_income, vacancy_loss=vacancy_loss,
    egi=egi, mgmt_fee=mgmt_fee, insurance=insurance, re_taxes=re_taxes,
    maintenance=maintenance, total_expenses=total_expenses, noi=noi,
    cap_rate=cap_rate, value=value, loan_amount=loan_amount,
    annual_debt_service=annual_debt_service, dscr=dscr,
    levered_cash_flow=levered_cash_flow, equity_invested=equity_invested,
    cash_on_cash=cash_on_cash, irr=irr, irr_adj=irr_adj,
    sale_price=sale_price, sale_proceeds=sale_proceeds,
    hold_years=hold_years, noi_growth=noi_growth, exit_cap=exit_cap,
    capex_summary=capex_summary, wf_data=wf,
    s_bear=s_bear, s_base=s_base, s_bull=s_bull,
    bear_args=bear_args, base_args=base_args, bull_args=bull_args,
    lp_equity_pct=lp_equity_pct, pref_return=pref_return,
    promote_tier1=promote_tier1, hurdle_tier1=hurdle_tier1,
    promote_tier2=promote_tier2, hurdle_tier2=hurdle_tier2,
    rent_roll_df=_rr_export,
)

# ── Page header with export button ──────────
header_col, btn_col = st.columns([4, 1])
with header_col:
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
with btn_col:
    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
    fname = f"underwriting_{address.replace(' ','_').replace(',','')[:30]}.xlsx" if address else "underwriting_export.xlsx"
    st.download_button(
        label="⬇ Export to Excel",
        data=excel_bytes,
        file_name=fname,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )


# ─────────────────────────────────────────────
#  TABS — Pro Forma | Rent Roll
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Pro Forma", "Rent Roll", "CapEx & Returns", "LP/GP Waterfall", "Scenarios"])


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
        html = '<div style="background:var(--surface);border:1px solid var(--border);padding:1rem 1.25rem;border-radius:2px;">'
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
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter", color="#6E6E73", size=11),
        margin=dict(l=50, r=20, t=40, b=40),
        xaxis=dict(gridcolor="#E8E8ED", zerolinecolor="#D2D2D7", tickfont=dict(family="IBM Plex Mono", size=10)),
        yaxis=dict(gridcolor="#E8E8ED", zerolinecolor="#D2D2D7", tickfont=dict(family="IBM Plex Mono", size=10))
    )

    with col_chart1:
        years       = list(range(1, int(hold_years)+1))
        noi_by_year = [noi * (1 + noi_growth/100)**yr for yr in years]
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=years, y=noi_by_year, marker_color="#0071E3",
            marker_line_width=0, hovertemplate="Year %{x}<br>NOI: $%{y:,.0f}<extra></extra>"))
        fig1.update_layout(**CHART_LAYOUT,
            title=dict(text="Projected NOI — Hold Period", font=dict(size=12, color="#1D1D1F")),
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
            decreasing=dict(marker_color="#C0392B"),
            increasing=dict(marker_color="#0071E3"),
            totals=dict(marker_color="#1A7A4A"),
            hovertemplate="%{x}<br>$%{y:,.0f}<extra></extra>"
        ))
        fig2.update_layout(**CHART_LAYOUT,
            title=dict(text="Return Waterfall", font=dict(size=12, color="#1D1D1F")),
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
                color = "#1A7A4A" if v >= 0.12 else ("#9A6700" if v >= 0.08 else "#E74C3C")
                cells += f'<td style="color:{color}">{val}</td>'
            except:
                cells += f"<td>{val}</td>"
        tbl += f"<tr><td>{idx}</td>{cells}</tr>"
    tbl += "</tbody></table></div>"
    st.markdown(tbl, unsafe_allow_html=True)

    # ── 10-Year Cash Flow Projection ──────────
    section("10-Year Cash Flow Projection")
    st.markdown('<p style="font-size:0.75rem;color:#9AA0B0;margin-top:-0.5rem;margin-bottom:1rem;">Year-by-year pro forma including debt service and capital costs</p>', unsafe_allow_html=True)

    cf_years     = list(range(1, int(hold_years)+1))
    cf_noi       = [noi * (1 + noi_growth/100)**yr for yr in cf_years]
    cf_ds        = [annual_debt_service] * len(cf_years)
    cf_lev       = [n - annual_debt_service for n in cf_noi]
    cf_capex     = [capex_summary["annual_totals"][yr] for yr in cf_years]
    cf_adj       = [l - c for l, c in zip(cf_lev, cf_capex)]
    cf_noi_psf   = [n / square_feet for n in cf_noi]

    # Add sale proceeds to final year
    cf_lev_disp  = cf_lev.copy()
    cf_adj_disp  = cf_adj.copy()
    cf_lev_disp[-1] += sale_proceeds
    cf_adj_disp[-1] += sale_proceeds

    cf_df = pd.DataFrame({
        "Year":           cf_years,
        "NOI":            [f"${v:,.0f}" for v in cf_noi],
        "NOI / SF":       [f"${v:.2f}"  for v in cf_noi_psf],
        "Debt Service":   [f"(${v:,.0f})" for v in cf_ds],
        "Levered CF":     [f"${v:,.0f}" for v in cf_lev],
        "CapEx / TI / LC":[f"(${v:,.0f})" for v in cf_capex],
        "Adj. CF":        [f"${v:,.0f}" for v in cf_adj],
        "Cum. Adj. CF":   [f"${sum(cf_adj[:i+1]):,.0f}" for i in range(len(cf_adj))],
    })
    # Mark final year
    cf_df.loc[cf_df.index[-1], "Levered CF"] += " + Sale"
    cf_df.loc[cf_df.index[-1], "Adj. CF"]   += " + Sale"

    st.dataframe(cf_df, use_container_width=True, hide_index=True)

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
        # Store enriched df in session state so Excel export can use it
        # st.session_state persists values across Streamlit reruns

        # ── Run rent roll model ───────────────
        df_rr, summary = build_rent_roll(df_raw.copy(), hold_years)
        # Save to session state for Excel export
        st.session_state["rent_roll_df_export"] = df_rr

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
        walt_color = "#1A7A4A" if summary["walt"] >= hold_years * 0.6 else (
                     "#9A6700" if summary["walt"] >= hold_years * 0.3 else "#E74C3C")
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
            .map(style_risk,  subset=["Risk"])
            .map(style_mtm,   subset=["Mark-to-Mkt"])
            .set_properties(**{
                "background-color": "#FFFFFF",
                "color": "#E8E8E8",
                "font-family": "DM Mono, monospace",
                "font-size": "12px",
                "border": "1px solid rgba(201,168,76,0.15)"
            })
            .set_table_styles([{
                "selector": "th",
                "props": [
                    ("background-color", "#F5F5F7"),
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
        COLORS = ["#C9A84C", "#4C9AC9", "#1A7A4A", "#E74C3C", "#9B59B6",
                  "#9A6700", "#1ABC9C", "#E67E22", "#3498DB", "#E91E63"]

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
            title=dict(text="Revenue by Tenant — Hold Period", font=dict(size=12, color="#1D1D1F")),
            barmode="stack",
            yaxis_tickprefix="$",
            yaxis_tickformat=",.0f",
            legend=dict(
                font=dict(family="Inter", size=10, color="#6E6E73"),
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
                "#E74C3C" if p > 0.30 else ("#9A6700" if p > 0.15 else "#C9A84C")
                for p in expiry_pct
            ],
            marker_line_width=0,
            hovertemplate="Year %{x}<br>Expiring SF: %{y:,.0f}<extra></extra>"
        ))
        fig4.update_layout(
            **CHART_LAYOUT,
            title=dict(text="SF Expiring by Year", font=dict(size=12, color="#1D1D1F")),
            yaxis_tickformat=",.0f",
            bargap=0.3
        )
        st.plotly_chart(fig4, use_container_width=True)

    else:
        # ── Empty state ───────────────────────
        # Shows when no CSV has been uploaded yet
        st.markdown("""
        <div style="background:var(--surface);border:1px solid var(--border);
                    padding:2.5rem;border-radius:2px;text-align:center;margin-top:1rem;">
            <div style="font-size:2rem;margin-bottom:0.75rem;">📋</div>
            <div style="font-weight:600;margin-bottom:0.5rem;color:var(--white);">
                No rent roll uploaded
            </div>
            <div style="font-size:0.8rem;color:var(--mid);max-width:400px;margin:0 auto;">
                Upload a CSV with your tenant lease data to model rollover risk,
                mark-to-market, and tenant-level revenue projections.
                Download the sample above to see the required format.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
#  TAB 3 — CAPEX & ADJUSTED RETURNS
# ═════════════════════════════════════════════
with tab3:

    section("Capital Cost Summary")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card(
            "Total CapEx Reserve",
            f"${capex_summary['total_capex']:,.0f}",
            f"${capex_psf:.2f}/SF/yr × {hold_years:.0f} yrs"
        )
    with c2:
        metric_card(
            "Total TI Cost",
            f"${capex_summary['total_ti']:,.0f}",
            "Across all rollover events"
        )
    with c3:
        metric_card(
            "Total Leasing Commissions",
            f"${capex_summary['total_lc']:,.0f}",
            f"{lc_pct:.1f}% of new lease value"
        )
    with c4:
        metric_card(
            "Total Capital Cost",
            f"${capex_summary['total_cost']:,.0f}",
            f"${capex_summary['psf_per_year']:.2f}/SF/yr all-in"
        )

    # ── IRR comparison: unadjusted vs adjusted ─
    section("IRR Impact — Before vs After Capital Costs")

    c1, c2, c3 = st.columns(3)
    irr_delta = irr_adj - irr
    with c1:
        metric_card(
            "IRR — Before CapEx",
            f"{irr:.1%}",
            "Excludes TI, LC, and CapEx reserve"
        )
    with c2:
        metric_card(
            "IRR — After CapEx",
            f"{irr_adj:.1%}",
            "True levered IRR after all capital costs",
            "metric-pass" if irr_adj >= 0.12 else "metric-fail"
        )
    with c3:
        metric_card(
            "IRR Drag",
            f"{irr_delta:.1%}",
            "Capital costs erode this much IRR",
            "metric-warn" if abs(irr_delta) < 0.03 else "metric-fail"
        )

    st.markdown("""
    <div style="background:var(--surface);border:1px solid var(--border);border-left:3px solid var(--gold);
                padding:0.75rem 1rem;border-radius:2px;font-size:0.78rem;color:var(--mid);margin:0.5rem 0 1rem 0;">
        <strong style="color:var(--white);">Why this matters:</strong>
        The unadjusted IRR (Pro Forma tab) only reflects NOI growth and exit value.
        The adjusted IRR above is what your equity actually earns after writing checks for
        tenant improvements, broker commissions, and capital reserves every time a lease rolls.
        This is the number that goes in the IC memo.
    </div>
    """, unsafe_allow_html=True)

    # ── Year-by-year CapEx schedule ────────────
    section("Annual Capital Cost Schedule")

    years_list = list(range(1, int(hold_years) + 1))
    capex_by_yr  = [capex_summary["schedule"][yr].get("CapEx Reserve", 0)        for yr in years_list]
    ti_by_yr     = [capex_summary["schedule"][yr].get("Tenant Improvements", 0)  for yr in years_list]
    lc_by_yr     = [capex_summary["schedule"][yr].get("Leasing Commissions", 0)  for yr in years_list]
    total_by_yr  = [capex_summary["annual_totals"][yr]                            for yr in years_list]

    CHART_LAYOUT = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter", color="#6E6E73", size=11),
        margin=dict(l=50, r=20, t=40, b=40),
        xaxis=dict(
            gridcolor="#E8E8ED",
            zerolinecolor="#D2D2D7",
            tickfont=dict(family="IBM Plex Mono", size=10)
        ),
        yaxis=dict(
            gridcolor="#E8E8ED",
            zerolinecolor="#D2D2D7",
            tickfont=dict(family="IBM Plex Mono", size=10)
        )
    )

    fig_capex = go.Figure()

    # Stacked bars: CapEx + TI + LC by year
    # Spikes show rollover years — makes the timing of capital calls visual
    fig_capex.add_trace(go.Bar(
        name="CapEx Reserve",
        x=years_list, y=capex_by_yr,
        marker_color="#5AC8FA",
        marker_line_width=0,
        hovertemplate="Year %{x}<br>CapEx Reserve: $%{y:,.0f}<extra></extra>"
    ))
    fig_capex.add_trace(go.Bar(
        name="Tenant Improvements",
        x=years_list, y=ti_by_yr,
        marker_color="#0071E3",
        marker_line_width=0,
        hovertemplate="Year %{x}<br>TI: $%{y:,.0f}<extra></extra>"
    ))
    fig_capex.add_trace(go.Bar(
        name="Leasing Commissions",
        x=years_list, y=lc_by_yr,
        marker_color="#E74C3C",
        marker_line_width=0,
        hovertemplate="Year %{x}<br>LC: $%{y:,.0f}<extra></extra>"
    ))

    fig_capex.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Capital Costs by Year", font=dict(size=12, color="#1D1D1F")),
        barmode="stack",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        legend=dict(
            font=dict(family="Inter", size=10, color="#6E6E73"),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="left",   x=0
        ),
        bargap=0.25
    )
    st.plotly_chart(fig_capex, use_container_width=True)

    # ── Cash flow bridge: NOI → Levered CF → Adjusted CF ──
    section("Cash Flow Bridge")
    st.markdown('<p style="font-size:0.75rem;color:#9AA0B0;margin-top:-0.5rem;margin-bottom:1rem;">How each cost layer erodes your cash flow year by year</p>', unsafe_allow_html=True)

    fig_bridge = go.Figure()

    noi_by_yr = [noi * (1 + noi_growth/100)**yr for yr in years_list]
    lev_cf_by_yr = [n - annual_debt_service for n in noi_by_yr]
    adj_cf_by_yr = [l - c for l, c in zip(lev_cf_by_yr, total_by_yr)]

    fig_bridge.add_trace(go.Scatter(
        name="NOI", x=years_list, y=noi_by_yr,
        mode="lines+markers",
        line=dict(color="#1A7A4A", width=2),
        marker=dict(size=5),
        hovertemplate="Year %{x}<br>NOI: $%{y:,.0f}<extra></extra>"
    ))
    fig_bridge.add_trace(go.Scatter(
        name="Levered Cash Flow", x=years_list, y=lev_cf_by_yr,
        mode="lines+markers",
        line=dict(color="#C9A84C", width=2),
        marker=dict(size=5),
        hovertemplate="Year %{x}<br>Levered CF: $%{y:,.0f}<extra></extra>"
    ))
    fig_bridge.add_trace(go.Scatter(
        name="Adj. CF (after CapEx/TI/LC)", x=years_list, y=adj_cf_by_yr,
        mode="lines+markers",
        line=dict(color="#E74C3C", width=2, dash="dot"),
        marker=dict(size=5),
        hovertemplate="Year %{x}<br>Adj. CF: $%{y:,.0f}<extra></extra>"
    ))

    fig_bridge.update_layout(
        **CHART_LAYOUT,
        title=dict(text="NOI → Levered CF → Adjusted CF", font=dict(size=12, color="#1D1D1F")),
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        legend=dict(
            font=dict(family="Inter", size=10, color="#6E6E73"),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="left",   x=0
        )
    )
    st.plotly_chart(fig_bridge, use_container_width=True)

    # ── Detailed year-by-year table ────────────
    section("Detailed Capital Cost Schedule")

    capex_table = pd.DataFrame({
        "Year":              years_list,
        "CapEx Reserve":     [f"${v:,.0f}" for v in capex_by_yr],
        "Tenant Improvements": [f"${v:,.0f}" for v in ti_by_yr],
        "Leasing Commissions": [f"${v:,.0f}" for v in lc_by_yr],
        "Total Capital Cost":  [f"${v:,.0f}" for v in total_by_yr],
        "Levered CF":          [f"${v:,.0f}" for v in lev_cf_by_yr],
        "Adj. CF":             [f"${v:,.0f}" for v in adj_cf_by_yr],
    })
    st.dataframe(capex_table, use_container_width=True, hide_index=True)


# ═════════════════════════════════════════════
#  TAB 4 — LP / GP WATERFALL
# ═════════════════════════════════════════════
with tab4:

    section("Partnership Structure")

    # ── Equity split summary ───────────────────
    gp_equity_pct = 100 - lp_equity_pct
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("LP Equity", f"${wf['lp_equity']:,.0f}",
                    f"{lp_equity_pct:.0f}% of total equity")
    with c2:
        metric_card("GP Equity", f"${wf['gp_equity']:,.0f}",
                    f"{gp_equity_pct:.0f}% of total equity")
    with c3:
        metric_card("Preferred Return",
                    f"{pref_return:.1f}%",
                    f"${wf['pref_owed']:,.0f} owed to LP")
    with c4:
        pref_color = "metric-pass" if wf["pref_satisfied"] else "metric-fail"
        metric_card("Pref Satisfied?",
                    "✓ Yes" if wf["pref_satisfied"] else "✗ No",
                    f"${wf['pref_paid']:,.0f} paid of ${wf['pref_owed']:,.0f}",
                    pref_color)

    # ── Returns comparison ─────────────────────
    section("LP vs GP Returns")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("LP Total Distributions", f"${wf['lp_total']:,.0f}",
                    f"{wf['lp_em']:.2f}x equity multiple")
    with c2:
        metric_card("GP Total Distributions", f"${wf['gp_total']:,.0f}",
                    f"{wf['gp_em']:.2f}x equity multiple")
    with c3:
        metric_card("LP Profit", f"${wf['lp_profit']:,.0f}",
                    f"Above return of capital")
    with c4:
        metric_card("GP Promote Earned",
                    f"{wf['gp_promote_pct']:.1%}",
                    f"${wf['gp_profit']:,.0f} GP profit on {gp_equity_pct:.0f}% equity",
                    "metric-pass")

    # ── Waterfall tier breakdown table ─────────
    section("Waterfall Distribution by Tier")

    t = wf["tiers"]
    tier_data = {
        "Tier": [
            "1 — Return of Capital",
            "1 — Return of Capital",
            "2 — Preferred Return (8%)",
            "3 — GP Catch-Up",
            "4 — Promote Tier 1",
            "4 — Promote Tier 1",
            "5 — Promote Tier 2",
            "5 — Promote Tier 2",
        ],
        "Recipient": ["LP", "GP", "LP", "GP", "LP", "GP", "LP", "GP"],
        "Amount": [
            t["lp_return_of_capital"],
            t["gp_return_of_capital"],
            t["lp_preferred_return"],
            t["gp_catchup"],
            t["lp_tier1_promote"],
            t["gp_tier1_promote"],
            t["lp_tier2_promote"],
            t["gp_tier2_promote"],
        ]
    }

    df_tiers = pd.DataFrame(tier_data)
    df_tiers["Amount"] = df_tiers["Amount"].apply(lambda x: f"${x:,.0f}")
    df_tiers["% of Pool"] = [
        wf["tiers"][k] / wf["total_pool"] * 100
        for k in [
            "lp_return_of_capital", "gp_return_of_capital",
            "lp_preferred_return", "gp_catchup",
            "lp_tier1_promote", "gp_tier1_promote",
            "lp_tier2_promote", "gp_tier2_promote",
        ]
    ]
    df_tiers["% of Pool"] = df_tiers["% of Pool"].apply(lambda x: f"{x:.1f}%")

    def color_recipient(val):
        if val == "LP":
            return "color: #4C9AC9"
        elif val == "GP":
            return "color: #0071E3"
        return ""

    styled_tiers = (
        df_tiers.style
        .map(color_recipient, subset=["Recipient"])
        .set_properties(**{
            "background-color": "#FFFFFF",
            "color": "#E8E8E8",
            "font-family": "DM Mono, monospace",
            "font-size": "12px",
        })
        .set_table_styles([{
            "selector": "th",
            "props": [
                ("background-color", "#F5F5F7"),
                ("color", "#C9A84C"),
                ("font-family", "DM Mono, monospace"),
                ("font-size", "11px"),
                ("text-transform", "uppercase"),
                ("letter-spacing", "0.08em"),
                ("padding", "8px 12px"),
            ]
        }])
    )
    st.dataframe(df_tiers, use_container_width=True, hide_index=True)

    # ── Waterfall bar chart ────────────────────
    section("Waterfall Visualization")

    CHART_LAYOUT_WF = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter", color="#6E6E73", size=11),
        margin=dict(l=50, r=20, t=40, b=80),
        xaxis=dict(
            gridcolor="#E8E8ED",
            tickfont=dict(family="IBM Plex Mono", size=9),
            tickangle=-20,
        ),
        yaxis=dict(
            gridcolor="#E8E8ED",
            tickfont=dict(family="IBM Plex Mono", size=10),
        )
    )

    # Grouped bar: LP vs GP at each tier
    tier_labels = [
        "Return of\nCapital",
        "Preferred\nReturn",
        "GP\nCatch-Up",
        "Promote\nTier 1",
        "Promote\nTier 2",
    ]
    lp_amounts = [
        t["lp_return_of_capital"],
        t["lp_preferred_return"],
        0,
        t["lp_tier1_promote"],
        t["lp_tier2_promote"],
    ]
    gp_amounts = [
        t["gp_return_of_capital"],
        0,
        t["gp_catchup"],
        t["gp_tier1_promote"],
        t["gp_tier2_promote"],
    ]

    fig_wf = go.Figure()
    fig_wf.add_trace(go.Bar(
        name="LP Distribution",
        x=tier_labels, y=lp_amounts,
        marker_color="#0071E3",
        marker_line_width=0,
        hovertemplate="%{x}<br>LP: $%{y:,.0f}<extra></extra>"
    ))
    fig_wf.add_trace(go.Bar(
        name="GP Distribution",
        x=tier_labels, y=gp_amounts,
        marker_color="#0071E3",
        marker_line_width=0,
        hovertemplate="%{x}<br>GP: $%{y:,.0f}<extra></extra>"
    ))
    fig_wf.update_layout(
        **CHART_LAYOUT_WF,
        title=dict(text="LP vs GP Distribution by Waterfall Tier",
                   font=dict(size=12, color="#1D1D1F")),
        barmode="group",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        legend=dict(
            font=dict(family="Inter", size=10, color="#6E6E73"),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="left", x=0
        ),
        bargap=0.25,
        bargroupgap=0.05
    )
    st.plotly_chart(fig_wf, use_container_width=True)

    # ── LP vs GP profit pie chart ──────────────
    col_pie, col_em = st.columns([1, 1])

    with col_pie:
        fig_pie = go.Figure(go.Pie(
            labels=["LP Profit", "GP Promote"],
            values=[wf["lp_profit"], wf["gp_profit"]],
            hole=0.55,
            marker=dict(colors=["#0071E3", "#1A7A4A"],
                        line=dict(color="#F5F5F7", width=2)),
            textfont=dict(family="IBM Plex Mono", size=11),
            hovertemplate="%{label}<br>$%{value:,.0f}<br>%{percent}<extra></extra>"
        ))
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#6E6E73"),
            margin=dict(l=20, r=20, t=40, b=20),
            title=dict(text="Profit Split", font=dict(size=12, color="#1D1D1F")),
            legend=dict(font=dict(family="Inter", size=10, color="#6E6E73"),
                        bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_em:
        st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
        metric_card("LP Equity Multiple", f"{wf['lp_em']:.2f}x",
                    f"On ${wf['lp_equity']:,.0f} invested")
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        metric_card("GP Equity Multiple", f"{wf['gp_em']:.2f}x",
                    f"On ${wf['gp_equity']:,.0f} invested — promote effect",
                    "metric-pass")
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        metric_card("GP Effective Ownership",
                    f"{wf['gp_promote_pct']:.1%}",
                    f"Of total profits vs {gp_equity_pct:.0f}% equity contribution",
                    "metric-pass")


# ═════════════════════════════════════════════
#  TAB 5 — SCENARIO ANALYSIS
# ═════════════════════════════════════════════
with tab5:

    section("Scenario Assumptions")

    # Show what changed between scenarios
    assump_df = pd.DataFrame({
        "Assumption":    ["Occupancy", "NOI Growth (%/yr)", "Exit Cap Rate (%)"],
        "Bear":       [
            f"{max(0.5, occupancy + bear_occ_adj/100):.0%}",
            f"{max(0.0, noi_growth + bear_rent_adj):.2f}%",
            f"{exit_cap + bear_cap_adj:.2f}%",
        ],
        "Base":       [
            f"{occupancy:.0%}",
            f"{noi_growth:.2f}%",
            f"{exit_cap:.2f}%",
        ],
        "Bull":       [
            f"{min(1.0, occupancy + bull_occ_adj/100):.0%}",
            f"{noi_growth + bull_rent_adj:.2f}%",
            f"{max(0.1, exit_cap + bull_cap_adj):.2f}%",
        ],
    })
    st.dataframe(assump_df, use_container_width=True, hide_index=True)

    # ── Returns comparison table ───────────────
    section("Returns Comparison — Bear / Base / Bull")

    metrics_df = pd.DataFrame({
        "Metric": [
            "NOI", "Implied Value", "DSCR",
            "Cash-on-Cash", "IRR (Unadjusted)",
            "IRR (After CapEx)", "LP Equity Multiple",
            "GP Equity Multiple", "Sale Price", "Sale Proceeds",
        ],
        "Bear": [
            f"${s_bear['noi']:,.0f}",
            f"${s_bear['value']:,.0f}",
            f"{s_bear['dscr']:.2f}x",
            f"{s_bear['coc']:.1%}",
            f"{s_bear['irr']:.1%}",
            f"{s_bear['irr_adj']:.1%}",
            f"{s_bear['lp_em']:.2f}x",
            f"{s_bear['gp_em']:.2f}x",
            f"${s_bear['sale']:,.0f}",
            f"${s_bear['sp']:,.0f}",
        ],
        "Base": [
            f"${s_base['noi']:,.0f}",
            f"${s_base['value']:,.0f}",
            f"{s_base['dscr']:.2f}x",
            f"{s_base['coc']:.1%}",
            f"{s_base['irr']:.1%}",
            f"{s_base['irr_adj']:.1%}",
            f"{s_base['lp_em']:.2f}x",
            f"{s_base['gp_em']:.2f}x",
            f"${s_base['sale']:,.0f}",
            f"${s_base['sp']:,.0f}",
        ],
        "Bull": [
            f"${s_bull['noi']:,.0f}",
            f"${s_bull['value']:,.0f}",
            f"{s_bull['dscr']:.2f}x",
            f"{s_bull['coc']:.1%}",
            f"{s_bull['irr']:.1%}",
            f"{s_bull['irr_adj']:.1%}",
            f"{s_bull['lp_em']:.2f}x",
            f"{s_bull['gp_em']:.2f}x",
            f"${s_bull['sale']:,.0f}",
            f"${s_bull['sp']:,.0f}",
        ],
    })

    def color_scenario_row(row):
        # Color IRR rows green/amber/red based on thresholds
        styles = [""] * len(row)
        if "IRR" in str(row.get("Metric", "")):
            for i, col in enumerate(["Bear", "Base", "Bull"]):
                if col in row.index:
                    try:
                        v = float(str(row[col]).replace("%","")) / 100
                        if v >= 0.12:
                            styles[row.index.get_loc(col)] = "color: #2ECC71"
                        elif v >= 0.08:
                            styles[row.index.get_loc(col)] = "color: #F39C12"
                        else:
                            styles[row.index.get_loc(col)] = "color: #E74C3C"
                    except:
                        pass
        return styles

    st.dataframe(metrics_df, use_container_width=True, hide_index=True)

    # ── IRR bar chart — bear/base/bull ─────────
    section("IRR Across Scenarios")

    CHART_LAYOUT_S = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter", color="#6E6E73", size=11),
        margin=dict(l=50, r=20, t=40, b=40),
        xaxis=dict(
            gridcolor="#E8E8ED",
            tickfont=dict(family="IBM Plex Mono", size=11)
        ),
        yaxis=dict(
            gridcolor="#E8E8ED",
            tickfont=dict(family="IBM Plex Mono", size=10),
        )
    )

    col_irr, col_em = st.columns(2)

    with col_irr:
        scenario_names  = ["Bear", "Base", "Bull"]
        irr_vals        = [s_bear["irr_adj"], s_base["irr_adj"], s_bull["irr_adj"]]
        irr_colors      = [
            "#E74C3C" if v < 0.08 else ("#9A6700" if v < 0.12 else "#1A7A4A")
            for v in irr_vals
        ]

        fig_irr = go.Figure()
        fig_irr.add_trace(go.Bar(
            x=scenario_names, y=[v*100 for v in irr_vals],
            marker_color=irr_colors,
            marker_line_width=0,
            text=[f"{v:.1%}" for v in irr_vals],
            textposition="outside",
            textfont=dict(family="IBM Plex Mono", size=11, color="#E8E8E8"),
            hovertemplate="%{x}<br>IRR: %{y:.2f}%<extra></extra>"
        ))
        # Hurdle line at 12%
        fig_irr.add_hline(
            y=12, line_dash="dot",
            line_color="rgba(0,113,227,0.5)",
            annotation_text="12% hurdle",
            annotation_font=dict(family="IBM Plex Mono", size=9, color="#C9A84C"),
            annotation_position="right"
        )
        fig_irr.update_layout(
            **CHART_LAYOUT_S,
            title=dict(text="IRR After CapEx — Scenario Comparison",
                       font=dict(size=12, color="#1D1D1F")),
            yaxis_ticksuffix="%",
            showlegend=False,
            bargap=0.4
        )
        st.plotly_chart(fig_irr, use_container_width=True)

    with col_em:
        # LP equity multiple across scenarios
        lp_ems = [s_bear["lp_em"], s_base["lp_em"], s_bull["lp_em"]]
        em_colors = [
            "#E74C3C" if v < 1.5 else ("#9A6700" if v < 1.8 else "#1A7A4A")
            for v in lp_ems
        ]

        fig_em = go.Figure()
        fig_em.add_trace(go.Bar(
            x=scenario_names, y=lp_ems,
            marker_color=em_colors,
            marker_line_width=0,
            text=[f"{v:.2f}x" for v in lp_ems],
            textposition="outside",
            textfont=dict(family="IBM Plex Mono", size=11, color="#E8E8E8"),
            hovertemplate="%{x}<br>LP EM: %{y:.2f}x<extra></extra>"
        ))
        fig_em.add_hline(
            y=1.8, line_dash="dot",
            line_color="rgba(0,113,227,0.5)",
            annotation_text="1.8x target",
            annotation_font=dict(family="IBM Plex Mono", size=9, color="#C9A84C"),
            annotation_position="right"
        )
        fig_em.update_layout(
            **CHART_LAYOUT_S,
            title=dict(text="LP Equity Multiple — Scenario Comparison",
                       font=dict(size=12, color="#1D1D1F")),
            showlegend=False,
            bargap=0.4
        )
        st.plotly_chart(fig_em, use_container_width=True)

    # ── NOI & Value waterfall across scenarios ─
    section("NOI & Value Bridge — Bear to Bull")

    fig_bridge = go.Figure()
    metrics_bridge = ["NOI", "Implied Value", "Sale Price"]
    bear_vals = [s_bear["noi"], s_bear["value"], s_bear["sale"]]
    base_vals = [s_base["noi"], s_base["value"], s_base["sale"]]
    bull_vals = [s_bull["noi"], s_bull["value"], s_bull["sale"]]

    fig_bridge.add_trace(go.Bar(
        name="Bear", x=metrics_bridge, y=bear_vals,
        marker_color="#E74C3C", marker_line_width=0,
        hovertemplate="%{x}<br>Bear: $%{y:,.0f}<extra></extra>"
    ))
    fig_bridge.add_trace(go.Bar(
        name="Base", x=metrics_bridge, y=base_vals,
        marker_color="#0071E3", marker_line_width=0,
        hovertemplate="%{x}<br>Base: $%{y:,.0f}<extra></extra>"
    ))
    fig_bridge.add_trace(go.Bar(
        name="Bull", x=metrics_bridge, y=bull_vals,
        marker_color="#1A7A4A", marker_line_width=0,
        hovertemplate="%{x}<br>Bull: $%{y:,.0f}<extra></extra>"
    ))
    fig_bridge.update_layout(
        **CHART_LAYOUT_S,
        title=dict(text="Key Metrics Across Scenarios",
                   font=dict(size=12, color="#1D1D1F")),
        barmode="group",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        legend=dict(
            font=dict(family="Inter", size=10, color="#6E6E73"),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom", y=1.02, xanchor="left", x=0
        ),
        bargap=0.2, bargroupgap=0.05
    )
    st.plotly_chart(fig_bridge, use_container_width=True)

    # ── IC memo verdict box ────────────────────
    section("Investment Committee Summary")

    bear_irr = s_bear["irr_adj"]
    bull_irr = s_bull["irr_adj"]
    base_irr = s_base["irr_adj"]

    if bear_irr >= 0.08 and base_irr >= 0.12:
        ic_color = "#1A7A4A"
        ic_border = "rgba(46,204,113,0.3)"
        ic_bg     = "rgba(46,204,113,0.08)"
        ic_verdict = "✅ RECOMMEND — Deal holds above hurdle in base and bear cases"
    elif base_irr >= 0.10 and bear_irr >= 0.06:
        ic_color = "#9A6700"
        ic_border = "rgba(243,156,18,0.3)"
        ic_bg     = "rgba(243,156,18,0.08)"
        ic_verdict = "⚠️ CONDITIONAL — Base case acceptable; bear case needs work"
    else:
        ic_color = "#E74C3C"
        ic_border = "rgba(231,76,60,0.3)"
        ic_bg     = "rgba(231,76,60,0.08)"
        ic_verdict = "❌ PASS — Returns insufficient across scenarios"

    st.markdown(f"""
    <div style="background:{ic_bg};border:1px solid {ic_border};
                border-left:4px solid {ic_color};
                padding:1.25rem 1.5rem;border-radius:2px;margin-top:0.5rem;">
        <div style="font-family:DM Mono,monospace;font-size:0.7rem;
                    letter-spacing:0.1em;text-transform:uppercase;
                    color:{ic_color};margin-bottom:0.5rem;">
            IC Verdict
        </div>
        <div style="font-size:1rem;font-weight:600;color:#E8E8E8;margin-bottom:0.75rem;">
            {ic_verdict}
        </div>
        <div style="font-size:0.78rem;color:#9AA0B0;font-family:DM Mono,monospace;">
            Bear IRR: {bear_irr:.1%} &nbsp;|&nbsp;
            Base IRR: {base_irr:.1%} &nbsp;|&nbsp;
            Bull IRR: {bull_irr:.1%} &nbsp;|&nbsp;
            LP EM (Base): {s_base['lp_em']:.2f}x
        </div>
    </div>
    """, unsafe_allow_html=True)
