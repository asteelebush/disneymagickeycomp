import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.colors as pcolors
import math
import uuid

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Disneyland Magic Key Breakeven Calculator"

def make_input_group(label, input_id, value, symbol="$", step=1):
    prepend = [dbc.InputGroupText(symbol)] if symbol else []
    return dbc.Row([
        dbc.Label(label, width=7, className="text-muted small mb-0"),
        dbc.Col(
            dbc.InputGroup(
                prepend + [dbc.Input(id=input_id, type="number", value=value, step=step)], 
                size="sm"
            ),
            width=5
        )
    ], className="mb-2 align-items-center")

# Default Data for the Table
default_table_data = [{
    "id": str(uuid.uuid4()),
    "Name": "Family of 5 (Explore)",
    "Inspire": 0, "Believe": 0, "Explore": 5, "Imagine": 0,
    "Vehicles": 1
}]

# UI Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("🏰 Magic Key Breakeven Calculator", className="mt-4 mb-3 text-primary")),
    ]),
    
    # Global Settings
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Global Assumptions (Out of Pocket Costs)", className="fw-bold"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([make_input_group("Avg Single-Day Ticket", "global-ticket", 160)], md=4),
                        dbc.Col([make_input_group("Standard Daily Parking", "global-parking", 40)], md=4),
                        dbc.Col([make_input_group("Est. Food/Merch (Per Person)", "global-spend", 10)], md=4)
                    ])
                ])
            ]), width=12, className="mb-4"
        )
    ]),

    # Pass Tier Settings (Configuration Only)
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Inspire Key", className="bg-info text-white fw-bold"),
            dbc.CardBody([
                make_input_group("Pass Cost", "inspire-cost", 1899),
                make_input_group("Parking Discount", "inspire-park-disc", 100, "%"),
                make_input_group("Food/Merch Discount", "inspire-food-disc", 20, "%"),
            ])
        ]), width=12, md=6, lg=3, className="mb-3"),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader("Believe Key", className="bg-success text-white fw-bold"),
            dbc.CardBody([
                make_input_group("Pass Cost", "believe-cost", 1474),
                make_input_group("Parking Discount", "believe-park-disc", 50, "%"),
                make_input_group("Food/Merch Discount", "believe-food-disc", 10, "%"),
            ])
        ]), width=12, md=6, lg=3, className="mb-3"),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader("Explore Key", className="bg-warning text-white fw-bold"),
            dbc.CardBody([
                make_input_group("Pass Cost", "explore-cost", 999),
                make_input_group("Parking Discount", "explore-park-disc", 0, "%"),
                make_input_group("Food/Merch Discount", "explore-food-disc", 10, "%"),
            ])
        ]), width=12, md=6, lg=3, className="mb-3"),
        
        dbc.Col(dbc.Card([
            dbc.CardHeader("Imagine Key", className="bg-danger text-white fw-bold"),
            dbc.CardBody([
                make_input_group("Pass Cost", "imagine-cost", 599),
                make_input_group("Parking Discount", "imagine-park-disc", 0, "%"),
                make_input_group("Food/Merch Discount", "imagine-food-disc", 10, "%"),
            ])
        ]), width=12, md=6, lg=3, className="mb-3"),
    ]),

    # ---------------------------------------------------------
    # NEW: Scenario Builder & Comparison Table
    # ---------------------------------------------------------
    html.H4("Group Scenario Builder", className="mt-4 mb-3 border-bottom pb-2"),
    dbc.Row([
        # Scenario Input Form
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Add a New Scenario", className="fw-bold bg-light"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Label("Scenario Name", width=5, className="small fw-bold"),
                        dbc.Col(dbc.Input(id="scen-name", type="text", value="Scenario 2", size="sm"), width=7)
                    ], className="mb-2"),
                    dbc.Row([
                        dbc.Label("Vehicles", width=5, className="small fw-bold text-muted"),
                        dbc.Col(dbc.Input(id="scen-v", type="number", value=1, min=1, step=1, size="sm"), width=7)
                    ], className="mb-3"),
                    html.Hr(className="my-2"),
                    dbc.Row([
                        dbc.Col([dbc.Label("Inspire Qty", className="small text-info"), dbc.Input(id="scen-i", type="number", value=0, min=0, size="sm")], width=6),
                        dbc.Col([dbc.Label("Believe Qty", className="small text-success"), dbc.Input(id="scen-b", type="number", value=0, min=0, size="sm")], width=6),
                    ], className="mb-2"),
                    dbc.Row([
                        dbc.Col([dbc.Label("Explore Qty", className="small text-warning"), dbc.Input(id="scen-e", type="number", value=0, min=0, size="sm")], width=6),
                        dbc.Col([dbc.Label("Imagine Qty", className="small text-danger"), dbc.Input(id="scen-im", type="number", value=0, min=0, size="sm")], width=6),
                    ], className="mb-3"),
                    dbc.Button("Add to Comparison", id="add-scenario-btn", color="primary", className="w-100", n_clicks=0)
                ])
            ]), width=12, lg=3, className="mb-4"
        ),
        
        # Scenario Data Table
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    dash_table.DataTable(
                        id='scenario-table',
                        data=default_table_data,
                        columns=[
                            {"name": "Name", "id": "Name"},
                            {"name": "Vehicles", "id": "Vehicles"},
                            {"name": "Inspire", "id": "Inspire"},
                            {"name": "Believe", "id": "Believe"},
                            {"name": "Explore", "id": "Explore"},
                            {"name": "Imagine", "id": "Imagine"},
                            {"name": "Total Upfront", "id": "Upfront", "type": "numeric", "format": dash_table.FormatTemplate.money(0)},
                            {"name": "Breakeven", "id": "Breakeven", "type": "numeric"}
                        ],
                        row_deletable=True,
                        style_cell={'textAlign': 'center', 'fontFamily': 'sans-serif', 'padding': '10px'},
                        style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
                        style_data_conditional=[
                            {'if': {'column_id': 'Name'}, 'textAlign': 'left', 'fontWeight': 'bold'},
                            {'if': {'column_id': 'Breakeven'}, 'fontWeight': 'bold', 'backgroundColor': '#e9ecef'}
                        ]
                    )
                ])
            ]), width=12, lg=9, className="mb-4"
        )
    ]),

    # Scenario Chart
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id="line-chart-group")), width=12, className="mb-5"),
    ]),

    # Individual Metrics 
    html.H4("Individual Pass Baselines", className="mt-4 mb-3 border-bottom pb-2"),
    dbc.Row(id="kpi-cards-container", className="mb-3"),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id="bar-chart")), width=12, lg=4, className="mb-4"),
        dbc.Col(dbc.Card(dcc.Graph(id="line-chart-individual")), width=12, lg=8, className="mb-4"),
    ])

], fluid=True, className="p-4")

# Helper to prevent UI freezing on empty fields
def safe_val(val, default=0.0):
    try:
        return float(val) if val is not None else float(default)
    except (ValueError, TypeError):
        return float(default)

@app.callback(
    [Output("scenario-table", "data"),
     Output("line-chart-group", "figure"),
     Output("kpi-cards-container", "children"),
     Output("bar-chart", "figure"),
     Output("line-chart-individual", "figure")],
    
    # Triggers (Any change to configs OR pressing the add button OR deleting a row)
    [Input("add-scenario-btn", "n_clicks"),
     Input("scenario-table", "data_previous"),
     Input("global-ticket", "value"), Input("global-parking", "value"), Input("global-spend", "value"),
     Input("inspire-cost", "value"), Input("inspire-park-disc", "value"), Input("inspire-food-disc", "value"),
     Input("believe-cost", "value"), Input("believe-park-disc", "value"), Input("believe-food-disc", "value"),
     Input("explore-cost", "value"), Input("explore-park-disc", "value"), Input("explore-food-disc", "value"),
     Input("imagine-cost", "value"), Input("imagine-park-disc", "value"), Input("imagine-food-disc", "value")],
    
    # State (Data we need to read but shouldn't trigger recalculations on their own)
    [State("scenario-table", "data"), State("scen-name", "value"), State("scen-v", "value"), 
     State("scen-i", "value"), State("scen-b", "value"), State("scen-e", "value"), State("scen-im", "value")]
)
def update_master(n_clicks, table_prev, 
                  t_cost, p_cost, s_cost,
                  i_c, i_p, i_f,
                  b_c, b_p, b_f,
                  e_c, e_p, e_f,
                  im_c, im_p, im_f,
                  table_data, scen_name, scen_v, scen_i, scen_b, scen_e, scen_im):
    
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'] if ctx.triggered else ""

    # Sanitize global inputs
    t_cost, p_cost, s_cost = safe_val(t_cost, 160), safe_val(p_cost, 40), safe_val(s_cost, 50)
    table_data = table_data or []

    # Map current tier definitions
    tiers = {
        "Inspire": {"color": "#17a2b8", "cost": safe_val(i_c), "p_disc": safe_val(i_p)/100, "f_disc": safe_val(i_f)/100},
        "Believe": {"color": "#28a745", "cost": safe_val(b_c), "p_disc": safe_val(b_p)/100, "f_disc": safe_val(b_f)/100},
        "Explore": {"color": "#ffc107", "cost": safe_val(e_c), "p_disc": safe_val(e_p)/100, "f_disc": safe_val(e_f)/100},
        "Imagine": {"color": "#dc3545", "cost": safe_val(im_c), "p_disc": safe_val(im_p)/100, "f_disc": safe_val(im_f)/100}
    }

    # 1. ADD SCENARIO LOGIC
    if "add-scenario-btn" in trigger:
        qty_sum = safe_val(scen_i) + safe_val(scen_b) + safe_val(scen_e) + safe_val(scen_im)
        if qty_sum > 0:
            new_row = {
                "id": str(uuid.uuid4()),
                "Name": scen_name if scen_name else f"Scenario {len(table_data)+1}",
                "Inspire": int(safe_val(scen_i)), "Believe": int(safe_val(scen_b)),
                "Explore": int(safe_val(scen_e)), "Imagine": int(safe_val(scen_im)),
                "Vehicles": max(1, int(safe_val(scen_v, 1)))
            }
            table_data.append(new_row)

    # 2. GROUP SCENARIO MATH & CHARTING
    group_fig = go.Figure()
    visits_range = list(range(26))  # 0 to 25 visits    
    colors = pcolors.qualitative.G10 # Color palette for scenarios

    for idx, row in enumerate(table_data):
        i_q = safe_val(row.get("Inspire", 0))
        b_q = safe_val(row.get("Believe", 0))
        e_q = safe_val(row.get("Explore", 0))
        im_q = safe_val(row.get("Imagine", 0))
        v_count = safe_val(row.get("Vehicles", 1))
        
        group_size = i_q + b_q + e_q + im_q
        if group_size == 0: continue

        # Calculate Upfront
        total_upfront = (i_q * tiers["Inspire"]["cost"]) + (b_q * tiers["Believe"]["cost"]) + \
                        (e_q * tiers["Explore"]["cost"]) + (im_q * tiers["Imagine"]["cost"])
        
        # Calculate max food discount in this group
        f_discs = []
        if i_q > 0: f_discs.append(tiers["Inspire"]["f_disc"])
        if b_q > 0: f_discs.append(tiers["Believe"]["f_disc"])
        if e_q > 0: f_discs.append(tiers["Explore"]["f_disc"])
        if im_q > 0: f_discs.append(tiers["Imagine"]["f_disc"])
        max_f_disc = max(f_discs) if f_discs else 0

        # Calculate parking discounts applied to vehicles
        p_discs = []
        p_discs.extend([tiers["Inspire"]["p_disc"]] * int(i_q))
        p_discs.extend([tiers["Believe"]["p_disc"]] * int(b_q))
        p_discs.extend([tiers["Explore"]["p_disc"]] * int(e_q))
        p_discs.extend([tiers["Imagine"]["p_disc"]] * int(im_q))
        p_discs.sort(reverse=True)

        group_pass_parking_cost = 0
        for i in range(int(v_count)):
            if i < len(p_discs):
                group_pass_parking_cost += p_cost * (1 - p_discs[i])
            else:
                group_pass_parking_cost += p_cost

        # Standard ticket-based "No Pass" baseline for this specific group
        group_ticket_cost_total = (i_q * t_cost) + (b_q * t_cost) + (e_q * t_cost) + (im_q * t_cost)

        group_no_pass_per_visit = group_ticket_cost_total + (v_count * p_cost) + (group_size * s_cost)
        group_pass_per_visit = group_pass_parking_cost + (group_size * s_cost * (1 - max_f_disc))
        
        group_savings = group_no_pass_per_visit - group_pass_per_visit
        group_breakeven = math.ceil(total_upfront / group_savings) if group_savings > 0 else float('inf')

        # Update Table Data Row
        row["Upfront"] = total_upfront
        row["Savings"] = group_savings
        row["Breakeven"] = group_breakeven if group_breakeven != float('inf') else "Never"

        # Chart the lines for this scenario
        c = colors[idx % len(colors)]
        scen_name_disp = row["Name"]
        
        group_pass_costs = [total_upfront + (v * group_pass_per_visit) for v in visits_range]

        group_fig.add_trace(go.Scatter(
            x=visits_range, y=group_pass_costs, mode='lines+markers', 
            name=f'{scen_name_disp}', line=dict(color=c, width=3)
        ))

    group_fig.update_layout(
        title="Comparison Chart: Cumulative Costs", xaxis_title="Number of Group Visits", yaxis_title="Total Cost ($)",
        template="plotly_white", hovermode="x unified", margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )


    # 3. INDIVIDUAL CALCULATIONS (Bottom Section)
    ind_results = []
    for name, t in tiers.items():
        cost_no_pass = t_cost + p_cost + s_cost
        cost_pass = (p_cost * (1 - t["p_disc"])) + (s_cost * (1 - t["f_disc"]))
        savings = cost_no_pass - cost_pass
        
        b_even = math.ceil(t["cost"] / savings) if savings > 0 else float('inf')
        ind_results.append({"name": name, "color": t["color"], "cost": t["cost"], "breakeven": b_even, "cost_pass": cost_pass})

    # Individual KPI Cards
    kpi_cards = []
    for r in ind_results:
        kpi_cards.append(dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6(f"{r['name']} Key", className="text-muted text-uppercase mb-1"),
                html.H3(f"{r['breakeven']} Visits" if r['breakeven'] != float('inf') else "Never", className="fw-bold mb-0"),
                html.Small(f"Upfront: ${r['cost']:,.0f}", className="text-muted")
            ])
        ], style={"borderLeft": f"5px solid {r['color']}"}), width=12, md=6, lg=3, className="mb-2"))

    # Individual Bar Chart
    bar_fig = go.Figure(data=[go.Bar(
        x=[r["name"] for r in ind_results], 
        y=[r["breakeven"] if r["breakeven"] != float('inf') else 0 for r in ind_results], 
        marker_color=[r["color"] for r in ind_results], 
        text=[f"{r['breakeven']}" if r["breakeven"] != float('inf') else "N/A" for r in ind_results], textposition='auto'
    )])
    bar_fig.update_layout(title="Individual Breakeven Visits", yaxis_title="Number of Visits", template="plotly_white", margin=dict(l=40, r=40, t=50, b=40))

    # Individual Line Chart
    line_fig_ind = go.Figure()
    no_pass_costs_base = [v * (t_cost + p_cost + s_cost) for v in visits_range]
    line_fig_ind.add_trace(go.Scatter(x=visits_range, y=no_pass_costs_base, mode='lines+markers', name='No Pass (Base Rate)', line=dict(color='black', width=3, dash='dash')))

    for r in ind_results:
        tier_costs = [r["cost"] + (v * r["cost_pass"]) for v in visits_range]
        line_fig_ind.add_trace(go.Scatter(x=visits_range, y=tier_costs, mode='lines', name=f"{r['name']} Key", line=dict(color=r["color"], width=2)))

    line_fig_ind.update_layout(title="Individual Trajectory", xaxis_title="Visits", yaxis_title="Total Cost ($)", template="plotly_white", hovermode="x unified", margin=dict(l=40, r=40, t=50, b=40), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

    return table_data, group_fig, kpi_cards, bar_fig, line_fig_ind

if __name__ == '__main__':
    app.run(debug=True)