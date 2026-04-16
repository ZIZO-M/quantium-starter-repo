import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

PRICE_INCREASE_DATE = "2021-01-15"

# Load processed data
df = pd.read_csv("output.csv", parse_dates=["date"])

app = Dash(__name__)

app.layout = html.Div(id="page-wrapper", children=[
    html.H1("Pink Morsel Sales Visualiser", id="header"),
    html.P("Soul Foods · Pink Morsel revenue over time", id="subheader"),

    html.Div(id="controls", children=[
        html.Span("Region", id="controls-label"),
        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "All",   "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "South", "value": "south"},
                {"label": "East",  "value": "east"},
                {"label": "West",  "value": "west"},
            ],
            value="all",
            className="radio-group",
            inputClassName="radio-input",
            labelClassName="radio-label",
        ),
    ]),

    html.Div(id="chart-container", children=[
        dcc.Graph(id="sales-chart"),
    ]),
])


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(region):
    if region == "all":
        filtered = df.groupby("date", as_index=False)["sales"].sum()
    else:
        filtered = (
            df[df["region"] == region]
            .groupby("date", as_index=False)["sales"].sum()
        )

    fig = px.line(
        filtered,
        x="date",
        y="sales",
        labels={"date": "Date", "sales": "Total Sales ($)"},
    )

    fig.update_traces(line_color="#ff6b9d", line_width=2)

    fig.add_shape(
        type="line",
        x0=PRICE_INCREASE_DATE, x1=PRICE_INCREASE_DATE,
        y0=0, y1=1,
        xref="x", yref="paper",
        line={"dash": "dash", "color": "#7986cb", "width": 1.5},
    )
    fig.add_annotation(
        x=PRICE_INCREASE_DATE, y=0.97,
        xref="x", yref="paper",
        text="Price Increase",
        showarrow=False,
        xanchor="left",
        yanchor="top",
        font={"color": "#7986cb", "size": 11},
    )

    fig.update_layout(
        plot_bgcolor="#1a1d2e",
        paper_bgcolor="#1a1d2e",
        font_color="#e8eaf6",
        margin={"t": 20, "b": 40, "l": 60, "r": 20},
        xaxis={"gridcolor": "#2a2d3e", "linecolor": "#2a2d3e"},
        yaxis={"gridcolor": "#2a2d3e", "linecolor": "#2a2d3e"},
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
