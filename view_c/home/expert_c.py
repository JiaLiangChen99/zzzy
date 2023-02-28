from server import app
from dash import Input, Output, html
from model.PERMISSION_EXPERT import PERMISSION_EXPERT
import dash_bootstrap_components as dbc

@app.callback(
    Output('expert_info','children'),
    Input('expert_page_store','data'),
)
def show_expert(data):
    if data:
        query_result = PERMISSION_EXPERT.select(PERMISSION_EXPERT.EXPERT_NAME, PERMISSION_EXPERT.EXPERT_DISCRIBE)
        return [
                dbc.Col(
                    html.Div(
                        [
                        html.H1(item.EXPERT_NAME),
                        html.P(item.EXPERT_DISCRIBE)
                            ]
                    ),width=12) for item in query_result
                    ]

