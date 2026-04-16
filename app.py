import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Load processed data
df = pd.read_csv("output.csv", parse_dates=["date"])

# Aggregate total sales per day across all regions
daily_sales = df.groupby("date", as_index=False)["sales"].sum()

# Build line chart
fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    labels={"date": "Date", "sales": "Total Sales ($)"},
)

# Mark the price increase on 15 Jan 2021
fig.add_shape(
    type="line",
    x0="2021-01-15", x1="2021-01-15",
    y0=0, y1=1,
    xref="x", yref="paper",
    line={"dash": "dash", "color": "red"},
)
fig.add_annotation(
    x="2021-01-15", y=1,
    xref="x", yref="paper",
    text="Price Increase (15 Jan 2021)",
    showarrow=False,
    xanchor="left",
    yanchor="top",
    font={"color": "red"},
)

fig.update_layout(margin={"t": 40})

# Build app
app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        "Pink Morsel Sales Visualiser",
        style={"textAlign": "center", "fontFamily": "Arial, sans-serif"}
    ),
    dcc.Graph(id="sales-chart", figure=fig),
])

if __name__ == "__main__":
    app.run(debug=True)
