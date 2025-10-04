#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
)

# App
app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"

# -------------------------------------------------------------------
# Dropdown options
dropdown_options = [
    {"label": "Select Statistics", "value": "Select Statistics"},
    {"label": "Yearly Statistics", "value": "Yearly Statistics"},
    {"label": "Recession Period Statistics", "value": "Recession Period Statistics"},
]

year_list = [i for i in range(1980, 2024, 1)]

# -------------------------------------------------------------------
# Layout
app.layout = html.Div(
    [
        # TASK 2.1: Title
        html.H1(
            "Automobile Sales Statistics Dashboard",
            style={"textAlign": "center", "color": "#503D36", "fontSize": 24},
        ),

        # TASK 2.2: Two dropdowns
        html.Div(
            [
                html.Label("Select Statistics:"),
                dcc.Dropdown(
                    id="dropdown-statistics",
                    options=dropdown_options,
                    value="Select Statistics",
                    placeholder="Select a report type",
                    style={
                        "width": "80%",
                        "padding": "3px",
                        "font-size": "20px",
                        "text-align-last": "center",
                    },
                ),
            ]
        ),

        html.Div(
            dcc.Dropdown(
                id="select-year",
                options=[{"label": i, "value": i} for i in year_list],
                placeholder="Select Year",
                value=None,
            )
        ),

        Output container
        html.Div(
            id="output-container",
            className="chart-grid",
            style={"display": "flex", "flexWrap": "wrap"},
        ),
    ]
)

# -------------------------------------------------------------------
Callbacks

# Enable year dropdown only for Yearly Statistics
@app.callback(
    Output("select-year", "disabled"),
    Input("dropdown-statistics", "value"),
)
def update_input_container(selected_statistics):
    return False if selected_statistics == "Yearly Statistics" else True


# Plotting callback
@app.callback(
    Output("output-container", "children"),
    [
        Input("dropdown-statistics", "value"),
        Input("select-year", "value"),
    ],
)
def update_output_container(report_type, year_selected):
    # ---------------- Recession report ----------------
    if report_type == "Recession Period Statistics":
        recession_data = data[data["Recession"] == 1]

        # Plot 1: line avg sales by year
        yearly_rec = (
            recession_data.groupby("Year")["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                title="Average Automobile Sales During Recession (Year-wise)",
            )
        )

        # Plot 2: bar avg vehicles sold by vehicle type
        average_sales = (
            recession_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Average Vehicles Sold by Vehicle Type (Recession)",
            )
        )

        # Plot 3: pie advertising expenditure share by vehicle type
        exp_rec = (
            recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Advertising Expenditure Share by Vehicle Type (Recession)",
            )
        )

        # Plot 4: bar effect of unemployment rate on sales, by vehicle type
        unemp_data = (
            recession_data.groupby(["unemployment_rate", "Vehicle_Type"])["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x="unemployment_rate",
                y="Automobile_Sales",
                color="Vehicle_Type",
                labels={
                    "unemployment_rate": "Unemployment Rate",
                    "Automobile_Sales": "Average Automobile Sales",
                },
                title="Effect of Unemployment Rate on Vehicle Type and Sales",
            )
        )

        return [
            html.Div(
                className="chart-item",
                children=[html.Div(children=R_chart1), html.Div(children=R_chart2)],
                style={"display": "flex"},
            ),
            html.Div(
                className="chart-item",
                children=[html.Div(children=R_chart3), html.Div(children=R_chart4)],
                style={"display": "flex"},
            ),
        ]

    # ---------------- Yearly report ----------------
    elif year_selected and report_type == "Yearly Statistics":
        yearly_data = data[data["Year"] == year_selected]

        # Plot 1: line avg yearly automobile sales (whole period)
        yas = (
            data.groupby("Year")["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x="Year",
                y="Automobile_Sales",
                title="Average Yearly Automobile Sales",
            )
        )

        # Plot 2: line total monthly sales (sum across years)
        mas = (
            data.groupby("Month")["Automobile_Sales"]
            .sum()
            .reset_index()
        )
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x="Month",
                y="Automobile_Sales",
                title="Total Monthly Automobile Sales",
            )
        )

        # Plot 3: bar avg vehicles sold by vehicle type in selected year
        avr_vdata = (
            yearly_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title=f"Average Vehicles Sold by Vehicle Type in the year {year_selected}",
            )
        )

        # Plot 4: pie total ad expenditure by vehicle type in selected year
        exp_data = (
            yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title=f"Total Advertisement Expenditure by Vehicle Type in {year_selected}",
            )
        )

        return [
            html.Div(
                className="chart-item",
                children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)],
                style={"display": "flex"},
            ),
            html.Div(
                className="chart-item",
                children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)],
                style={"display": "flex"},
            ),
        ]


    else:
        return []


if __name__ == "__main__":
    
    app.run(debug=True)             


