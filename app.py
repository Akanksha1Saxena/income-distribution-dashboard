import dash
from dash import dcc, html,Dash
from dash.dependencies import Input, Output
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from styles import css_styles, insight_styles


# read data
file_read = "C:/Users/Akanksha/Downloads/Refined_csv/refined_adult.csv"
df = pd.read_csv(file_read)
# Initialize the Dash app
app = dash.Dash(__name__,suppress_callback_exceptions=True, external_stylesheets=[{'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
    'rel': 'stylesheet',
    'async': True }])

def age_distribution_plot():
    fig = px.violin(df, x='income', y='age', 
                    title='Distribution of Age by Income Level',
                    labels={'income': 'Income Level', 'age': 'Age'}, 
                    box=True, points='all') # Box=True adds a mini box plot inside the violin plot
    return fig

def hours_worked_plot():
    fig = px.box(df, x='income', y='hours.per.week',
             title='Distribution of Hours Worked per Week by Income Group',
             labels={'income': 'Income Group', 'hours.per.week': 'Hours per Week'},
             points='outliers', ) # Show outliers
             
    return fig

def marital_status_plot():
    color_map = {
    '<=50K': '#008080',
    '>50K': '#4EBCBA'
}   

    counts = df.groupby(['marital.status', 'income']).size().reset_index(name='count')
    fig = px.bar(counts, x='marital.status', y='count', color='income',
             title='Income Distribution by Marital Status',
             labels={'marital.status': 'Marital Status', 'count': 'Count', 'income': 'Income Level'},
             color_discrete_map=color_map,
             barmode='group')
    return fig


def racial_status_stacked_plot():
    # Aggregate the data
    aggregated_df = df.groupby(['race', 'income']).size().reset_index(name='count')
    heatmap_df = aggregated_df.pivot(index='race', columns='income', values='count')
    fig = px.imshow(heatmap_df,
                color_continuous_scale='Blues',
                labels={'x': 'Income', 'y': 'Race', 'color': 'Count of People'},
                title='Income Distribution by Race',
                text_auto=True)
    fig.update_layout(
        autosize=False,
        width=800,  # Adjust the width as needed
        height=450,  # Adjust the height as needed
    )
    return fig

def workclass_gender_distribution():
    color_map = {
    '<=50K': '#FFD6A5',
    '>50K': '#FFADAD'
}

    counts = df.groupby(['workclass', 'sex']).size().reset_index(name='count')
    fig = px.bar(counts, x='workclass', y='count', color='sex',
             title='Distribution of Work Class Across Different Gender',
             labels={'workclass': 'Workclass', 'count': 'Count', 'sex': 'Gender'},
             color_discrete_map=color_map,
             barmode='stack')
    fig.update_layout(
        width=700,
        height=400,
        title_x=0.5,
        title_y=0.95
    )

    return fig

def education_level_plot():
    
    education_mapping = df[['education.num', 'education']].drop_duplicates().sort_values('education.num')
    education_mapping_dict = dict(zip(education_mapping['education.num'], education_mapping['education']))

  # Create an ordered list of education levels based on education.num
    ordered_education_levels = [education_mapping_dict[num] for num in sorted(education_mapping_dict.keys())]


    color_map = {
    '<=50K': '#99BAB9',
    '>50K': '#CCD5AE'
    }

    counts = df.groupby(['education', 'income']).size().reset_index(name='count')
    fig = px.bar(counts, x='education', y='count', color='income',
             title='Distribution of Work Class Across Different Gender',
             labels={'education': 'edu', 'income': 'income'},
             category_orders={'education': ordered_education_levels},
             color_discrete_map=color_map,
             barmode='group')
    return fig

def hour_captial_gain_plot():
    fig = px.scatter(df, x='hours.per.week', y='capital.gain',
                 title='Relationship between Hours Worked per Week and Capital Gain',
                 labels={'hours.per.week': 'Hours per Week', 'capital.gain': 'Capital gain'},
                 trendline='ols',
                 trendline_color_override="red",
                 color='hours.per.week'
                  )
    return fig

 
def sunburst() : 
    fig = px.sunburst(
    df,
    path=['income', 'occupation'],
    values='hours.per.week',
    color='income',
    color_discrete_map={'>50K': "#e27c7c", '<=50K': "#a86464"},
    hover_data={'hours.per.week': True}
)


    # Update Layout
    fig.update_layout(
        title='Distribution of Hours Per Week by Income and Occupation',
        width=550,
        height=500,
        title_x=0.5,
        title_y=0.95
    )

    # Add Annotation
    fig.add_annotation(
        text="Size of each segment represents the average hours per week.",
        xref='paper',
        yref='paper',
        x=0.5,
        y=-0.1,
        showarrow=False,
        font=dict(size=14, color="black"),
        align='center'
    )

    return fig

def multivariate1():
    color_map = {
        '<=50K': '#ffb400',
        '>50K': '#a57c1b'
    }

    # Create the histogram
    fig = px.histogram(df, x='occupation', color='income', 
                       facet_col='workclass', barmode='group',
                       color_discrete_map=color_map,
                       title='Distribution of Occupation by Income, Workclass, and Education',
                       labels={'occupation': 'Occupation', 'income': 'Income Level'})
    
    # Update layout properties
    fig.update_layout(
        width=2500,       # Increase width
        height=500,       # Increase height
        title_x=0.5,      # Center the title
        title_y=0.95,     # Position the title slightly below the top
        xaxis_title='Occupation',  # X-axis title
        yaxis_title='Count',       # Y-axis title
        margin=dict(t=70, l=75, r=75, b=80),  # Set margins

    )
    return fig
def aggregate_countries(df):
    df_copy = df.copy() 
    threshold = 1000
    country_counts = df_copy['native.country'].value_counts()
    countries_to_keep = country_counts[country_counts >= threshold].index
    df_copy['native.country'] = df_copy['native.country'].apply(lambda x: x if x in countries_to_keep else 'Other')
    return df_copy

def multivariate2(df):

    # Apply the function to the DataFrame
    df_filtered  = aggregate_countries(df)

    # Aggregate data to calculate average capital gain
    df_aggregated = df_filtered .groupby(['native.country', 'race', 'workclass']).agg({
        'capital.gain': 'mean'
    }).reset_index()

    color_map = {
        'White': '#f3a8c2',
        'Black': '#f6d1de',
        'Asian-Pac-Islander': '#f74fd0',
        'Amer-Indian-Eskimo': '#a2a0a1',
        'Other': "#75c2f9"
    }

    fig = px.bar(df_aggregated, x='workclass', y='capital.gain', color='race', 
                facet_col='native.country', barmode='group',
                title='Average Capital Gain by Work Class, Race, and Native Country',
                labels={'workclass': 'Work Class', 'capital.gain': 'Average Capital Gain'},
                color_discrete_map=color_map)

    # Update layout
    fig.update_layout(width=900, height=500, margin=dict(t=70, l=25, r=25, b=25))
    return fig



app.layout = html.Div([
    # Header Section
    html.Div([
        html.H1("Exploring Income Trends by Demographic Factors", 
                className='text-center my-4 header', 
                style={'color': '#50748B', 'font-size': '2.5rem', 'font-weight': 'bold', 'text-shadow': '1px 1px 2px rgba(0,0,0,0.1)'}),
    ], className='container'),

    # Introduction Section
       html.Div([
        html.Div([
            html.H2("Introduction", className='subheader', style={'color': '#1E4C6A'}),
            html.Div([
                "Welcome to the interactive dashboard for analyzing how income varies based on demographic factors. This ",
                html.A("dataset", href='https://www.kaggle.com/datasets/priyamchoksi/adult-census-income-dataset/data', target='_blank', style={'color': '#008ae6'}),
                " was retrieved from the UCI Machine Learning Repository and extracted from the 1994 Census bureau database by Ronny Kohavi and Barry Becker from Silicon Graphics. The goal is to explore and visualize the relationships between various demographic factors and income levels."
            ], style={'color': 'black', 'font-size': '1.15rem'}),
        ], className='p-3 bg-custom rounded shadow-sm mb-4')
    ], className='container'),

    # Dataset Overview, Data Characteristics, Data Preprocessing Sections
    html.Div([
        html.Div([
            html.H3("Dataset Overview", className='subheader', style={'color': '#1E4C6A'}),
            html.P("The dataset includes the following attributes:"),
            html.Ul([
                html.Li("Age: Individual's age."),
                html.Li("Work Class: Type of employment."),
                html.Li("Education: Highest level of education."),
                html.Li("Hours Worked per Week: Average hours worked weekly."),
                html.Li("Capital Gain: Amount of capital gains."),
                html.Li("Capital Loss: Amount of capital losses."),
                html.Li("Income Level: Income above or below $50K."),
                html.Li("Final Weight (fnlwgt): Sampling weight."),
                html.Li("Education Number (education-num): Ordinal education level."),
                html.Li("Marital Status: Individual’s marital status."),
                html.Li("Occupation: Type of occupation."),
                html.Li("Relationship: Family relationship status."),
                html.Li("Race: Racial group."),
                html.Li("Sex: Gender."),
                html.Li("Native Country: Country of origin.")
            ]),
            html.H3("Data Characteristics", className='subheader', style={'color': '#1E4C6A'}),
            html.P([
                "The dataset contains approximately ",
                html.Span("32,561", style={'font-weight': 'bold'}),
                " rows and ",
                html.Span("15", style={'font-weight': 'bold'}),
                " columns. It features a diverse representation of work classes, education levels, and income levels, providing a robust basis for predictive analysis."
            ]),
            html.H3("Data Preprocessing", className='subheader', style={'color': '#1E4C6A'}),
            html.P("To prepare the data for analysis, we performed several preprocessing steps, including handling missing values, normalizing numerical features, and encoding categorical variables."),
        ], className='p-3 bg-custom rounded shadow-sm mb-4')
    ], className='container'),

    # Existing Content Sections
    html.Div([
        html.Div([
            html.H2("Age Distribution Analysis", className='subheader', style={'color': '#1E4C6A'}),
            html.P("The age column is an important feature in our dataset. To understand its distribution, we use a histogram and a box plot.", style={'color': '#05395a', 'font-size': '1.15rem'}),
            html.Img(src='/assets/histogram_age.png', className='img-fluid rounded mx-auto d-block', style={'width': '50%', 'height': 'auto'}),
            html.P("The histogram shows that the age distribution is not normally distributed. There is a higher frequency of individuals in the younger age groups, with a decreasing number of individuals as age increases.",
                   style={'color': '#05395a', 'font-size': '1.15rem', 'font-weight': 'bold'}),
            html.Img(src='/assets/outlier.png', className='img-fluid rounded mx-auto d-block', style={'width': '50%', 'height': 'auto'}),
            html.P("The box plot reveals the presence of outliers in the age data, indicating that some individuals fall outside the typical age range for the majority of the dataset.", style={'color': '#05395a', 'font-size': '1.15rem', 'font-weight': 'bold'}),
            html.P("Understanding the income and work patterns of older individuals can provide insights into retirement age, post-retirement income sources, and economic contributions of the elderly.", style={'color': '#05395a', 'font-size': '1.15rem', 'font-weight': 'bold'}),
            html.H4("Statistical Test Selection", className='subheader', style={'color': '#1E4C6A'}),
            html.P("Due to the non-normal distribution of the age column and the presence of outliers, we opted for non-parametric statistical tests, which do not assume normality. These tests include the Mann-Whitney U Test, Kruskal-Wallis H Test, Chi-Square Test of Independence, and Spearman's Rank Correlation.", style={'color': '#05395a', 'font-size': '1.15rem'})
        ], className='p-3 bg-custom rounded shadow-sm mb-4')
    ], className='container'),

    html.Div([
        html.Div([
            html.H2("Explore Key Factors Affecting Income Distribution", className='subheader', style={'color': '#1E4C6A'}),
            dcc.RadioItems(
                id='analysis-options',
                options=[
                    {'label': 'Income Distribution by Age ', 'value': 'age_distribution'},
                    {'label': 'Income Distribution by Hours Worked Per Week', 'value': 'hours_worked'},
                    {'label': 'Income Distribution by Marital Status', 'value': 'marital_status'},
                    {'label': 'Income Distribution by Racial Group', 'value': 'racial_group'},
                    {'label': 'Income Distribution by Education Level', 'value': 'education_level'},
                ],
                value='age_distribution',
                labelStyle={'display': 'block'}
            )
        ], className='p-3 bg-custom rounded shadow-sm mb-4')
    ], className='container'),

    html.Div([
        html.Div([
            dcc.Graph(id='graph-output', style={'height': '450px', 'width': '800px'}),
            html.Div(id='insights-output', style={'width': '30%', 'display': 'inline-block', 'margin-left': '30px', 'font-size': '1.15rem', 'font-weight': 'bold'})
        ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),
    ], className='container'),

    html.Div([
        html.Div([
            html.H2("Gender-Based Analysis of Workclass", className='subheader', style={'color': '#1E4C6A'}),
        ], className='container p-3 bg-custom rounded shadow-sm mb-4'),
        html.Div([
            dcc.Graph(
                figure=workclass_gender_distribution()
            ),
            html.Div([
                html.Ul([
                    html.Li("Most people work in the Private sector, with a significant number of males compared to females.", style={'color': '#54aeb1', 'font-size': '1.15rem', 'font-weight': 'bold'}),
                    html.Li("Other work classes have relatively balanced gender distributions but much lower counts.", style={'color': '#54aeb1', 'font-size': '1.15rem', 'font-weight': 'bold'})
                ], className='flex-item')
            ])
        ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '30px'})
    ], className='container'),

    html.Div([
        html.Div([
            html.H2("Analysis of Age Distribution Across Workclass", className='subheader', style={'color': '#1E4C6A'}),
        ], className='container p-3 bg-custom rounded shadow-sm mb-4'),
        html.Div([
            html.Img(src='/assets/age_workclass.png', style={'width': '48%'}),
            html.Div([
                html.Ul([
                    html.Li("The Private sector has the widest age distribution, indicating a diverse age group.", style={'color': '#778899', 'font-size': '1.15rem', 'font-weight': 'bold'}),
                    html.Li("The Never-worked category has a very narrow age range, with most individuals being quite young.", style={'color': '#778899', 'font-size': '1.15rem', 'font-weight': 'bold'}),
                    html.Li("Other work classes have varying age distributions, highlighting the diversity in age across different types of employment.", style={'color': '#778899', 'font-size': '1.15rem', 'font-weight': 'bold'})
                ], className='flex-item')
            ])
        ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'})
    ], className='container'),

    html.Div([
        html.Div([
            html.H2("Distribution of Hours Per Week by Income and Occupation", className='subheader', style={'color': '#1E4C6A'}),
        ], className='p-3 bg-custom rounded shadow-sm mb-4'),

        html.Div([
            dcc.Graph(figure=sunburst()),
            html.Div([
                html.Ul([
                    html.Li("Individuals earning >50K tend to be in Adm-clerical, Craft repair and Prof-specialty roles, working longer hours.", style={'color': '#cc6666', 'font-size': '1.15rem', 'font-weight': 'bold'}),
                    html.Li("The largest segment of <=50K income earners work in various occupations with smaller average work hours.", style={'color': '#cc6666', 'font-size': '1.15rem', 'font-weight': 'bold'}),
                    html.Li("Other work classes have varying age distributions, highlighting the diversity in age across different types of employment.", style={'color': '#cc6666', 'font-size': '1.15rem', 'font-weight': 'bold'})
                ], className='flex-item')
            ])
        ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '30px'})
    ], className='container'),

    html.Div([
        html.Div([
            html.H2("Distribution of Occupation by Income, Workclass, and Education", className='subheader', style={'color': '#1E4C6A'}),
        ], className='p-3 bg-custom rounded shadow-sm mb-4'),

        html.Div([
            dcc.Graph(figure=multivariate1(), style={'overflowX': 'auto'}),
            html.Div([
                html.Ul([
                    html.Li("The Private work class has a diverse range of occupations, with more individuals in lower income brackets.", style={'color': '#da9100', 'font-size': '1.15rem', 'font-weight': 'bold'}),
                    html.Li("State-gov and Federal-gov work classes show a limited range of occupations, with a balanced income distribution.", style={'color': '#da9100', 'font-size': '1.15rem', 'font-weight': 'bold'}),
                    html.Li("Self-employed individuals in the Self-emp-inc category show a notable number of higher-income occupations.", style={'color': '#da9100', 'font-size': '1.15rem', 'font-weight': 'bold'})
                ], className='flex-item')
            ])
        ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),
    ], className='container'),

    html.Div([
        html.Div([
            html.H2("Average Capital Gain by Work Class, Race, and Native Country", className='subheader', style={'color': '#1E4C6A'}),
        ], className='p-3 bg-custom rounded shadow-sm mb-4'),

        html.Div([
            dcc.Graph(figure=multivariate2(df)),
            html.Div([
                html.Ul([
                    html.Li("Self-emp-inc work class shows significantly higher average capital gains in United States", style={'color': '#534b4f', 'font-size': '1.15rem', 'font-weight': 'bold'}),
                    html.Li("There is a noticeable capital gain difference among racial groups within the same work class.", style={'color': '#534b4f', 'font-size': '1.15rem', 'font-weight': 'bold'})
                ], className='flex-item')
            ])
        ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'})
    ], className='container'),

    html.Div([
        html.Div([
        html.H1("Global Analysis of Average Capital Gain/Loss", className='subheader', style={'color': '#1E4C6A'}),
        ], className='p-3 bg-custom rounded shadow-sm mb-4'),
        dcc.Dropdown(
            id='filter-dropdown',
            options=[
                {'label': 'Capital Gain', 'value': 'capital.gain'},
                {'label': 'Capital Loss', 'value': 'capital.loss'}
            ],
            value='capital.gain',  # Default value
            style={'width': '50%'}
        ),

        dcc.Graph(id='map-graph')
    ], className='container')

])  # Set background color and text color




#Updated Callback Functions
#Update the callback to handle the combined analyses:

@app.callback(
    [Output('graph-output', 'figure'),
     Output('insights-output', 'children')],
    [Input('analysis-options', 'value')]
)
def update_main_analysis(selected_option):
    if selected_option == 'hours_worked':
        fig = hours_worked_plot()
        insights = html.Ul([
    html.Li("The median hours worked per week for both income groups is 40 hours.",style={'color': '#86608e'}),
    html.Li("People earning greater than 50K tend to work slightly more hours per week compared to those earning less than or equal to 50K.",style={'color': '#86608e'}),
    html.Li("There are more outliers in the greater than 50K group, indicating some individuals work significantly more hours (up to 100 hours per week).",style={'color': '#86608e'}),
    html.Li("The interquartile range (IQR) for the less than or equal to 50K group is narrower compared to the greater than 50K group, suggesting that hours worked per week is more consistent among lower earners.",style={'color': '#86608e'})
])

    elif selected_option == 'age_distribution':
        fig = age_distribution_plot()
        insights = html.Ul([
    html.Li("The distribution of age for people earning less than or equal to 50K is wider compared to those earning greater than 50K.",style={'color': '#86608e'}),
    html.Li("There are more younger individuals (20-40 years) in the less than or equal to 50K group.",style={'color': '#86608e'}),
    html.Li("The greater than 50K group has a tighter age distribution, indicating that higher earners are often within a more specific age range.",style={'color': '#86608e'})
])

    elif selected_option == 'marital_status':
        fig = marital_status_plot()
        insights =html.Ul([
    html.Li("Individuals who have never married or are divorced show a higher count of individuals earning less than or equal to 50K.",style={'color': '#5f9ea0'}),
    html.Li("Married individuals, especially those with spouses, show a higher count of individuals earning greater than 50K.",style={'color': '#5f9ea0'}),
    html.Li("The income disparity based on marital status is evident, with married individuals having a higher likelihood of earning more.",style={'color': '#5f9ea0'})
])


    elif selected_option == 'racial_group':
        fig = racial_status_stacked_plot()
        insights = html.Ul([
    html.Li("Most of the individuals in the dataset are White, with a higher count earning less than or equal to 50K.",style={'color': '#26619c'}),
    html.Li("Other races, such as Black and Asian-Pac-Islander, also have significant counts but with fewer individuals earning greater than 50K.",style={'color': '#26619c'}),
    html.Li("The disparity in income distribution is evident across different races, with a noticeable difference in the counts of higher earners.",style={'color': '#26619c'})
])


    elif selected_option == 'education_level':
        fig = education_level_plot()
        insights = html.Ul([
    html.Li("Most individuals have education levels around high school graduation (HS-grad) and some college education.",style={'color': '#739073'}),
    html.Li("Higher education levels like Bachelors, Masters,HS-grad and Doctorate show a higher proportion of individuals earning greater than 50K.",style={'color': '#739073'}),
    html.Li("Lower education levels (like 1st-4th grade, 5th-6th grade) show a higher proportion of individuals earning less than or equal to 50K.",style={'color': '#739073'})
])

    return fig, insights

# Callback to handle page navigation


# Callback to update the map based on the selected filter
@app.callback(
    Output('map-graph', 'figure'),
    Input('filter-dropdown', 'value'),
   
)
def update_map(selected_filter):
    df_avg = df.groupby('native.country')[selected_filter].mean().reset_index()
    
    fig = px.choropleth(
        df_avg,
        locations='native.country',
        locationmode='country names',
        color=selected_filter,
        hover_name="native.country",
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f'Average {selected_filter.replace(".", " ").title()} by Country'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)