import streamlit as st
import numpy as np
import numpy_financial as npf
import pandas as pd
import plotly.graph_objects as go

# ─────────────────────────────────────────────
#  PAGE CONFIG — must be first Streamlit call
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Industrial RE Underwriter",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — Goldman-deck aesthetic
#  Injected once at the top; applies everywhere
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import institutional font ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* ── Root variables ── */
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

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--navy);
    color: var(--white);
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--navy2);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .block-container { padding-top: 1rem; }

/* ── Sidebar section headers ── */
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

/* ── Page header ── */
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
.badge-fail   { background: rgba(231,76,60,0.15);  color: var(--red);   border: 1px solid rgba(231,76,60,0.3);  }
.badge-review { background: rgba(243,156,18,0.15); color: var(--amber); border: 1px solid rgba(243,156,18,0.3); }

/* ── Section headers ── */
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

/* ── Metric cards ── */
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
.metric-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: var(--white-dim);
}
.metric-pass { color: var(--green) !important; }
.metric-fail { color: var(--red)   !important; }
.metric-warn { color: var(--amber) !important; }

/* ── Data table ── */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.8rem;
}
.styled-table th {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--gold);
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid var(--border);
    text-align: right;
}
.styled-table th:first-child { text-align: left; }
.styled-table td {
    padding: 0.45rem 0.75rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    color: var(--white);
    text-align: right;
}
.styled-table td:first-child { text-align: left; color: var(--white-dim); font-family: 'DM Mono', monospace; font-size: 0.72rem; }
.styled-table tr:hover td { background: rgba(201,168,76,0.04); }

/* ── NOI waterfall row ── */
.noi-row { display: flex; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.82rem; }
.noi-row:last-child { border-bottom: none; font-weight: 600; color: var(--gold); }
.noi-label { color: var(--white-dim); }
.noi-value { font-family: 'DM Mono', monospace; color: var(--white); }
.noi-negative { color: var(--red) !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--navy2);
    border: 1px solid var(--border) !important;
    border-radius: 2px;
}

/* ── Inputs ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: var(--navy3);
    border: 1px solid rgba(255,255,255,0.1);
    color: var(--white);
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
}
[data-testid="stSlider"] { padding-top: 0.25rem; }

/* ── Divider ── */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, var(--gold) 0%, transparent 100%);
    margin: 1.5rem 0;
    opacity: 0.4;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPER: render a metric card
#  label     — small caps label above the number
#  value     — the big formatted number string
#  sub       — small line below (pass/fail, etc.)
#  sub_class — "metric-pass", "metric-fail", or "metric-warn"
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


# ─────────────────────────────────────────────
#  HELPER: section header
# ─────────────────────────────────────────────
def section(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR — all inputs live here
#  Main page becomes outputs-only
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏭 Deal Inputs")

    st.markdown('<div class="sidebar-section">Property</div>', unsafe_allow_html=True)
    address      = st.text_input("Address", placeholder="123 Industrial Pkwy, Memphis, TN")
    square_feet  = st.number_input("Rentable SF", min_value=0, value=50000, step=1000)
    year_built   = st.number_input("Year Built", min_value=1900, max_value=2030, value=1995, step=1)

    st.markdown('<div class="sidebar-section">Income</div>', unsafe_allow_html=True)
    rent_psf     = st.number_input("Base Rent ($/SF/yr)", min_value=0.0, value=6.50, step=0.25)
    occupancy    = st.slider("Occupancy", min_value=0.0, max_value=1.0, value=0.95, step=0.01, format="%.0f%%")
    other_income = st.number_input("Other Income ($/yr)", min_value=0.0, value=0.0, step=500.0)

    st.markdown('<div class="sidebar-section">Expenses</div>', unsafe_allow_html=True)
    mgmt_fee_pct   = st.number_input("Mgmt Fee (% EGI)", min_value=0.0, max_value=20.0, value=3.0, step=0.5)
    insurance_psf  = st.number_input("Insurance ($/SF/yr)", min_value=0.0, value=0.15, step=0.05)
    re_taxes_psf   = st.number_input("RE Taxes ($/SF/yr)", min_value=0.0, value=0.80, step=0.05)
    maintenance_psf= st.number_input("Maintenance ($/SF/yr)", min_value=0.0, value=0.25, step=0.05)

    st.markdown('<div class="sidebar-section">Valuation & Debt</div>', unsafe_allow_html=True)
    cap_rate      = st.number_input("Market Cap Rate (%)", min_value=0.1, max_value=20.0, value=6.0, step=0.25)
    ltv           = st.number_input("LTV (%)", min_value=0.0, max_value=95.0, value=65.0, step=5.0)
    interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=15.0, value=6.5, step=0.25)
    amort_years   = st.number_input("Amortization (yrs)", min_value=1, max_value=30, value=25, step=1)

    st.markdown('<div class="sidebar-section">Returns</div>', unsafe_allow_html=True)
    hold_years  = st.number_input("Hold Period (yrs)", min_value=1, max_value=20, value=10, step=1)
    noi_growth  = st.number_input("NOI Growth (%/yr)", min_value=0.0, max_value=10.0, value=2.0, step=0.25)
    exit_cap    = st.number_input("Exit Cap Rate (%)", min_value=0.0, max_value=20.0, value=7.0, step=0.25)


# ─────────────────────────────────────────────
#  CALCULATIONS — pure math, no UI here
#  Same formulas as your original app.py
# ─────────────────────────────────────────────

# Income
gross_potential_income = square_feet * rent_psf
vacancy_loss           = gross_potential_income * (1 - occupancy)
egi                    = gross_potential_income - vacancy_loss + other_income

# Expenses
mgmt_fee       = egi * (mgmt_fee_pct / 100)
insurance      = square_feet * insurance_psf
re_taxes       = square_feet * re_taxes_psf
maintenance    = square_feet * maintenance_psf
total_expenses = mgmt_fee + insurance + re_taxes + maintenance

# NOI
noi = egi - total_expenses

# Valuation
value = noi / (cap_rate / 100)

# Debt
loan_amount       = value * (ltv / 100)
monthly_rate      = (interest_rate / 100) / 12
n_payments        = amort_years * 12
monthly_payment   = loan_amount * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)
annual_debt_service = monthly_payment * 12
dscr              = noi / annual_debt_service

# Levered returns
levered_cash_flow = noi - annual_debt_service
equity_invested   = value - loan_amount
cash_on_cash      = levered_cash_flow / equity_invested

# IRR
payments_made      = int(hold_years) * 12
remaining_payments = (amort_years * 12) - payments_made
remaining_balance  = monthly_payment * (1 - (1 + monthly_rate)**-remaining_payments) / monthly_rate

noi_list           = [noi * (1 + noi_growth/100)**yr for yr in range(1, int(hold_years)+1)]
annual_cash_flows  = [n - annual_debt_service for n in noi_list]

exit_noi           = noi * (1 + noi_growth/100)**(hold_years + 1)
sale_price         = exit_noi / (exit_cap / 100)
sale_proceeds      = sale_price - remaining_balance
annual_cash_flows[-1] += sale_proceeds

cash_flows = [-equity_invested] + annual_cash_flows
irr        = npf.irr(cash_flows)

# Pass/fail thresholds
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
#  MAIN PAGE LAYOUT
# ─────────────────────────────────────────────

# ── Deal header ──────────────────────────────
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


# ── NOI Waterfall ─────────────────────────────
section("NOI Build")

col_noi, col_val = st.columns([1, 1])

with col_noi:
    # Line-by-line NOI build — reads like an Argus output
    items = [
        ("Gross Potential Income",  f"${gross_potential_income:>12,.0f}", False),
        ("Vacancy Loss",            f"(${vacancy_loss:,.0f})",            True),
        ("Other Income",            f"${other_income:>12,.0f}",           False),
        ("Effective Gross Income",  f"${egi:>12,.0f}",                    False),
        ("Management Fee",          f"(${mgmt_fee:,.0f})",                True),
        ("Insurance",               f"(${insurance:,.0f})",               True),
        ("Real Estate Taxes",       f"(${re_taxes:,.0f})",                True),
        ("Maintenance & Repairs",   f"(${maintenance:,.0f})",             True),
        ("Total Expenses",          f"(${total_expenses:,.0f})",          True),
        ("Net Operating Income",    f"${noi:>12,.0f}",                    False),
    ]
    html = '<div style="background:var(--navy2);border:1px solid var(--border);padding:1rem 1.25rem;border-radius:2px;">'
    for label, val, is_neg in items:
        cls = "noi-negative" if is_neg else ""
        divider = 'border-top:1px solid var(--border);margin-top:0.4rem;padding-top:0.6rem;' if label in ("Effective Gross Income","Total Expenses","Net Operating Income") else ""
        html += f'<div class="noi-row" style="{divider}"><span class="noi-label">{label}</span><span class="noi-value {cls}">{val}</span></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

with col_val:
    # Key valuation metrics in card grid
    c1, c2 = st.columns(2)
    with c1:
        metric_card("NOI / SF", f"${noi/square_feet:.2f}")
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        metric_card("Implied Value", f"${value:,.0f}")
    with c2:
        metric_card("EGI", f"${egi:,.0f}")
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        metric_card("Value / SF", f"${value/square_feet:.2f}")


# ── Debt ─────────────────────────────────────
section("Debt & Coverage")

c1, c2, c3, c4 = st.columns(4)
with c1: metric_card("Loan Amount", f"${loan_amount:,.0f}")
with c2: metric_card("Annual Debt Service", f"${annual_debt_service:,.0f}")
with c3: metric_card(
    "DSCR",
    f"{dscr:.2f}x",
    "✓ Above 1.25x" if dscr_pass else "✗ Below 1.25x",
    "metric-pass" if dscr_pass else "metric-fail"
)
with c4: metric_card("Equity Invested", f"${equity_invested:,.0f}")

with st.expander("DSCR Reference"):
    st.markdown("""
    | Range | Interpretation |
    |---|---|
    | Below 1.0x | Property can't cover debt — lender will decline |
    | 1.0x – 1.25x | Breaking even — most lenders won't touch this |
    | 1.25x – 1.35x | Minimum acceptable for most commercial lenders |
    | Above 1.35x | Comfortable — strong from a lender's perspective |
    """)


# ── Returns ──────────────────────────────────
section("Returns Summary")

c1, c2, c3, c4 = st.columns(4)
with c1: metric_card(
    "Cash-on-Cash",
    f"{cash_on_cash:.1%}",
    "✓ Above 7%" if coc_pass else "✗ Below 7%",
    "metric-pass" if coc_pass else "metric-fail"
)
with c2: metric_card(
    "IRR",
    f"{irr:.1%}",
    "✓ Above 12%" if irr_pass else "✗ Below 12%",
    "metric-pass" if irr_pass else "metric-fail"
)
with c3: metric_card("Sale Price", f"${sale_price:,.0f}")
with c4: metric_card("Sale Proceeds", f"${sale_proceeds:,.0f}")


# ── Charts ───────────────────────────────────
section("Cash Flow Analysis")

col_chart1, col_chart2 = st.columns(2)

# Shared Plotly layout config — institutional dark theme
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",  # transparent background
    plot_bgcolor="#131929",          # navy2 plot area
    font=dict(family="DM Sans", color="#9AA0B0", size=11),
    margin=dict(l=50, r=20, t=40, b=40),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        zerolinecolor="rgba(255,255,255,0.1)",
        tickfont=dict(family="DM Mono", size=10)
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        zerolinecolor="rgba(255,255,255,0.1)",
        tickfont=dict(family="DM Mono", size=10)
    )
)

with col_chart1:
    # NOI growth bar chart
    years       = list(range(1, int(hold_years)+1))
    noi_by_year = [noi * (1 + noi_growth/100)**yr for yr in years]

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=years,
        y=noi_by_year,
        marker_color="#C9A84C",        # gold bars
        marker_line_width=0,
        hovertemplate="Year %{x}<br>NOI: $%{y:,.0f}<extra></extra>"
    ))
    fig1.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Projected NOI — Hold Period", font=dict(size=12, color="#E8E8E8")),
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        bargap=0.25
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    # Return waterfall — where does money come from?
    total_cf   = sum(annual_cash_flows[:-1])  # operating cash flows (all but last)
    appreciation = sale_proceeds

    # Waterfall: Equity In (negative) → Cash Flow → Sale Proceeds → Total Return
    fig2 = go.Figure(go.Waterfall(
        name="Returns",
        orientation="v",
        measure=["absolute", "relative", "relative", "total"],
        x=["Equity In", "Operating CF", "Sale Proceeds", "Total Return"],
        y=[-equity_invested, total_cf, appreciation, None],
        connector=dict(line=dict(color="rgba(201,168,76,0.3)", width=1, dash="dot")),
        decreasing=dict(marker_color="#E74C3C"),
        increasing=dict(marker_color="#C9A84C"),
        totals=dict(marker_color="#2ECC71"),
        hovertemplate="%{x}<br>$%{y:,.0f}<extra></extra>"
    ))
    fig2.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Return Waterfall", font=dict(size=12, color="#E8E8E8")),
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)


# ── Sensitivity Table ─────────────────────────
section("Sensitivity Analysis — IRR")
st.markdown('<p style="font-size:0.75rem;color:#9AA0B0;margin-top:-0.5rem;margin-bottom:1rem;">Exit cap rate (rows) × NOI growth (columns)</p>', unsafe_allow_html=True)

exit_caps   = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0]
growth_rates= [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]

rows = {}
for g in growth_rates:
    row = []
    for ec in exit_caps:
        noi_s   = [noi * (1 + g/100)**yr for yr in range(1, int(hold_years)+1)]
        cf_s    = [n - annual_debt_service for n in noi_s]
        en_s    = noi * (1 + g/100)**(hold_years + 1)
        sp_s    = en_s / (ec/100) - remaining_balance
        cf_s[-1]+= sp_s
        irr_s   = npf.irr([-equity_invested] + cf_s)
        row.append(f"{irr_s:.1%}")
    rows[f"{g:.1f}%"] = row

df = pd.DataFrame(rows, index=[f"{ec:.1f}%" for ec in exit_caps])

# Build styled HTML table — gold headers, dark rows
th_cells = "".join(f"<th>{col}</th>" for col in df.columns)
table_html = f"""
<div style="overflow-x:auto;">
<table class="styled-table">
<thead><tr>
  <th>Exit Cap \\ Growth</th>
  {th_cells}
</tr></thead>
<tbody>
"""
for idx, row in df.iterrows():
    cells = ""
    for val in row:
        # color-code: green above 12%, amber 8-12%, red below 8%
        try:
            v = float(val.strip('%')) / 100
            if v >= 0.12:
                color = "#2ECC71"
            elif v >= 0.08:
                color = "#F39C12"
            else:
                color = "#E74C3C"
            cells += f'<td style="color:{color};font-family:DM Mono,monospace;font-size:0.75rem;">{val}</td>'
        except:
            cells += f"<td>{val}</td>"
    table_html += f"<tr><td>{idx}</td>{cells}</tr>"

table_html += "</tbody></table></div>"
st.markdown(table_html, unsafe_allow_html=True)


# ── Deal Verdict ──────────────────────────────
st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
section("Deal Verdict")

c1, c2, c3 = st.columns(3)
with c1: metric_card(
    "DSCR",
    f"{dscr:.2f}x",
    "✓ Pass (≥1.25x)" if dscr_pass else "✗ Fail (<1.25x)",
    "metric-pass" if dscr_pass else "metric-fail"
)
with c2: metric_card(
    "Cash-on-Cash",
    f"{cash_on_cash:.1%}",
    "✓ Pass (≥7%)" if coc_pass else "✗ Fail (<7%)",
    "metric-pass" if coc_pass else "metric-fail"
)
with c3: metric_card(
    "IRR",
    f"{irr:.1%}",
    "✓ Pass (≥12%)" if irr_pass else "✗ Fail (<12%)",
    "metric-pass" if irr_pass else "metric-fail"
)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

if all_pass:
    st.success("✅  Deal passes all thresholds — worth pursuing")
elif hard_fail:
    st.error("❌  DSCR below 1.0 — property cannot cover debt service. Pass on this deal.")
else:
    st.warning("⚠️  Deal passes some thresholds but not all — review assumptions")
