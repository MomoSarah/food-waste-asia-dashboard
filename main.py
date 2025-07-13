import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Provided data for food supply stages
countries = ['Bangladesh', 'Nepal', 'Sri Lanka', 'Pakistan', 'India', 'China', 'Indonesia']
stages = ['Distribution', 'Market', 'Households', 'Farm', 'Storage', 'Processing', 'Transport', 'Wholesale', 'Harvest', 'Retail', 'Food Services', 'Trader', 'Export', 'Whole supply chain', 'Post-harvest']
loss_percentages = [0.79, 1.94, 2.86, 2.94, 3.16, 3.26, 4.21, 5.64, 5.81, 6.89, 7.59, 7.95, 10.79, 12.05, 16.93]

# Create a DataFrame for food supply stages
data_fsc = {
    'country': countries * len(stages),
    'food_supply_stage': [stage for stage in stages for _ in range(len(countries))],
    'loss_percentage': loss_percentages * len(countries)
}

sub_df_cleaned_fsc = pd.DataFrame(data_fsc)

# Provided data for commodity groups
data_fw = {
    'country': ['Bangladesh', 'Bangladesh', 'Bangladesh', 'China', 'China', 'China', 'China', 'India', 'India', 'India', 'India', 'India', 'Indonesia', 'Indonesia', 'Nepal', 'Nepal', 'Pakistan', 'Pakistan', 'Pakistan', 'Sri Lanka', 'Sri Lanka', 'Sri Lanka'],
    'commodity_group': ['Cereals & Pulses', 'Fruits & Vegetables', 'Roots, Tubers & Oil crops', 'Animal Products', 'Cereals & Pulses', 'Fruits & Vegetables', 'Other', 'Animal Products', 'Cereals & Pulses', 'Fruits & Vegetables', 'Other', 'Roots, Tubers & Oil crops', 'Cereals & Pulses', 'Fruits & Vegetables', 'Cereals & Pulses', 'Fruits & Vegetables', 'Cereals & Pulses', 'Fruits & Vegetables', 'Roots, Tubers & Oil crops', 'Cereals & Pulses', 'Fruits & Vegetables', 'Roots, Tubers & Oil crops'],
    'loss_percentage': [5.311894, 8.789755, 20.000000, 2.983333, 3.104124, 8.980694, 4.930000, 1.463529, 2.657143, 4.229673, 2.396522, 1.749622, 4.277069, 30.000000, 5.166000, 14.048857, 4.791750, 10.166522, 3.190000, 12.968000, 12.179821, 10.808000]
}

# Create DataFrame for commodity groups
sub_df_cleaned_fw = pd.DataFrame(data_fw)

# Group by country and commodity group and calculate the mean loss percentage
avg_loss_per_country_commodity = sub_df_cleaned_fw.groupby(['country', 'commodity_group'])['loss_percentage'].mean().reset_index()

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'])

# App layout
app.layout = html.Div([
    html.H1("Food Loss Dashboard"),

    html.Div([
        html.Div([
            html.H2("Food Loss Percentage by Food Supply Stage and Country"),
            dcc.Dropdown(
                id='food_supply_stage_dropdown',
                options=[{'label': stage, 'value': stage} for stage in sub_df_cleaned_fsc['food_supply_stage'].unique()],
                value=sub_df_cleaned_fsc['food_supply_stage'].unique()[0],
                clearable=False
            ),
            dcc.Graph(id='bar_chart_fsc'),
            html.Div(id='avg_loss_text_fsc')
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            html.H2("Average Loss Percentage by Commodity Group and Country"),
            dcc.Dropdown(
                id='commodity_group_dropdown',
                options=[{'label': group, 'value': group} for group in avg_loss_per_country_commodity['commodity_group'].unique()],
                value=avg_loss_per_country_commodity['commodity_group'].unique()[0],
                clearable=False
            ),
            dcc.Graph(id='bar_chart_fw'),
            html.Div(id='avg_loss_text_fw')
        ], style={'width': '48%', 'display': 'inline-block'})
    ])
])

# Callback to update the bar chart and average loss text for food supply stages
@app.callback(
    [Output('bar_chart_fsc', 'figure'),
     Output('avg_loss_text_fsc', 'children')],
    [Input('food_supply_stage_dropdown', 'value')]
)
def update_chart_fsc(selected_stage):
    filtered_df = sub_df_cleaned_fsc[sub_df_cleaned_fsc['food_supply_stage'] == selected_stage]
    
    fig = px.bar(
        filtered_df,
        x='country',
        y='loss_percentage',
        title=f'Food Loss Percentage for {selected_stage}',
        labels={'loss_percentage': 'Loss Percentage', 'country': 'Country'},
        template='plotly_white',
        text='loss_percentage'
    )
    
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    
    avg_loss = filtered_df['loss_percentage'].mean()
    avg_loss_text = f'Average loss percentage for {selected_stage}: {avg_loss:.2f}%'
    
    return fig, avg_loss_text

# Callback to update the bar chart and average loss text for commodity groups
@app.callback(
    [Output('bar_chart_fw', 'figure'),
     Output('avg_loss_text_fw', 'children')],
    [Input('commodity_group_dropdown', 'value')]
)
def update_chart_fw(selected_group):
    filtered_df = avg_loss_per_country_commodity[avg_loss_per_country_commodity['commodity_group'] == selected_group]
    
    fig = px.bar(
        filtered_df,
        x='country',
        y='loss_percentage',
        title=f'Average Loss Percentage for {selected_group}',
        labels={'loss_percentage': 'Loss Percentage', 'country': 'Country'},
        template='plotly_white',
        text='loss_percentage'
    )
    
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    
    avg_loss = filtered_df['loss_percentage'].mean()
    avg_loss_text = f'Average loss percentage for {selected_group}: {avg_loss:.2f}%'
    
    return fig, avg_loss_text

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
