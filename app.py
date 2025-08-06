import dash
import os
from dash import dcc, html,Dash
from dash.dependencies import Input, Output
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from styles import css_styles, insight_styles


# read data
df = pd.read_csv("refined_adult.csv")
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
                color_continuous_scale='Viridis',
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
             barmode='stack',
             text='count')
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
                       title='Distribution of Occupation by Income, Workclass',
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


def workclass_workhour_tree():
    fig = px.treemap(
    df,
    path=['income', 'workclass'],
    values='hours.per.week',
    color='income',
    title="Distribution of Hours Per Week by Income and Workclass",
    color_discrete_map={'>50K': "#e27c7c", '<=50K': "#a86464"},
    hover_data={'hours.per.week': True}
)
    # Update Layout
    fig.update_layout(
        width=650,
        height=500,
        title_x=0.5,
        title_y=0.95
    )
    

    return fig

def count_income_workclass_sex_income():
    count_individuals = df.groupby(['workclass', 'sex', 'income']).size().reset_index(name='count')
    fig = px.bar(count_individuals, 
                               x='workclass', 
                               y='count', 
                               color='workclass',
                               facet_col='sex',
                               facet_row='income',
                               text='count',
                               title='Count of Individuals by Work Class, Sex, and Income',
                               labels={'workclass': 'Work Class', 'count': 'Count of Individuals'}
                               )
    fig.update_layout(
        autosize=False,
        width=800,  # Adjust the width as needed
        height=600  # Adjust the height as needed
    )

    #fig_count_individuals.update_xaxes(title_text='Work Class')
    #fig_count_individuals.update_yaxes(title_text='Count of Individuals')
    #fig.for_each_annotation(lambda a: a.update(text=f"<b>{a.text.split('=')[-1]}</b>"))  # Clean and bold facet titles

    return fig


def proportion_count(df):
    # Group by race, sex, and income, then calculate the proportion of individuals earning >50K
    income_race_gender = df.groupby(['race', 'sex', 'income']).size().unstack(fill_value=0)
    income_race_gender['proportion_>50K'] = income_race_gender['>50K'] / (income_race_gender['<=50K'] + income_race_gender['>50K'])
    income_race_gender_proportions = income_race_gender[['proportion_>50K']].reset_index()

    color_discrete_map = {
        'White': '#CCD3CA',
        'Black': '#B5C0D0',
        'Asian-Pac-Islander': '#E2BFB3',
        'Amer-Indian-Eskimo': '#EED3D9',
        'Other': '#AEABAA',
    }

    fig = px.pie(income_race_gender_proportions, 
                 names='race', 
                 values='proportion_>50K', 
                 color='race', 
                 color_discrete_map=color_discrete_map,
                 title='Proportion of Individuals Earning > 50K by Race and Gender',
                 facet_col='sex')

    # Clean and bold facet titles
    fig.for_each_annotation(lambda a: a.update(text=f"<b>{a.text.split('=')[-1]}</b>"))
    fig.update_layout(
        autosize=False,
        width=600,  # Adjust the width as needed
        height=400  # Adjust the height as needed
    )

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
    html.Div([
        html.Div([
            html.H2("Objective", className='subheader', style={'color': '#1E4C6A'}),
            html.P("The objective of this dashboard is to provide a comprehensive analysis of income variations across different demographic groups, education levels, and occupations. It aims to uncover significant differences in income based on marital status, highest education level, and work hours. Additionally, the dashboard explores the distribution of individuals by work class, gender, and income, as well as the relationship between capital gains/losses and various demographic factors. The visualizations are designed to inform and support data-driven decision-making by highlighting key patterns and insights.")
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
        # Displaying the selected question
        html.Div(id='question-output', style={'font-size': '1.25rem', 'font-weight': 'bold', 'margin-bottom': '20px'}),

    html.Div([
        html.Div([
            dcc.Graph(id='graph-output', style={'height': '450px', 'width': '800px'}),
            html.Div(id='insights-output', style={'width': '30%', 'display': 'inline-block', 'margin-left': '30px', 'font-size': '1.15rem', 'font-weight': 'bold'})
        ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '20px'}),
    ]),
    ], className='container'),

    html.Div([
        html.Div([
            html.H2("Demographic Distribution and Income Proportions", className='subheader', style={'color': '#1E4C6A'}),
        ], className='container p-3 bg-custom rounded shadow-sm mb-4'),
        # Display the question
        html.Div([
        html.P("What are the gender-based distributions across different work classes?", 
               style={'font-size': '1.25rem', 'font-weight': 'bold', 'margin-bottom': '20px', 'margin-top': '20px'})
    ], className='container', style={'margin-bottom': '20px'}),
          html.Div([
        # Visualization
        html.Div([
            dcc.Graph(
                figure=workclass_gender_distribution()
            )
        ], style={'flex': '3'}),  # Flex: 3 for visualization, with margin-right for spacing

        # Insights
        html.Div([
            html.Ul([
                html.Li("Most people work in the Private sector, with a significant number of males compared to females.", style={'color': '#54aeb1', 'font-size': '1.15rem', 'font-weight': 'bold'}),
                html.Li("Other work classes have relatively balanced gender distributions but much lower counts.", style={'color': '#54aeb1', 'font-size': '1.15rem', 'font-weight': 'bold'})
            ], className='flex-item')
        ], style={'margin-left': '70'})  # Flex: 1 for insights
    ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'flex-start','margin-bottom': '30px'}),
    html.Div([
        html.P("Count of Individuals by Work Class, Sex, and Income", 
               style={'font-size': '1.25rem', 'font-weight': 'bold', 'margin-bottom': '20px', 'margin-top': '20px'})
    ], className='container', style={'margin-bottom': '20px'}),
    html.Div([
        # Visualization
        html.Div([
            dcc.Graph(
                figure=count_income_workclass_sex_income()
            )
        ], style={'flex': '3'}),  # Flex: 3 for visualization, with margin-right for spacing

        # Insights
        html.Div([
            html.Ul([
                html.Li([
                html.Span("Female (<=50K)", style={'color': '#C70039 '}),  # Highlighting "Female (≤50K)" in blue
                ": The majority of women earning ≤50K are in the Private sector, with 5010 individuals. Other work classes like Local-gov, Self-employed, and State-gov have significantly fewer women."
            ], style={'color': '#BD7F37FF', 'font-size': '1.15rem', 'font-weight': 'bold'}),
            html.Li([
                html.Span("Female (>50K)", style={'color': '#C70039 '}),  # Highlighting "Female (≤50K)" in blue
                ":For women earning >50K, the highest count is again in the Private sector (623), followed by Self-employed (145)."
            ], style={'color': '#BD7F37FF', 'font-size': '1.15rem', 'font-weight': 'bold'}),
             html.Li([
                html.Span("Male (<=50K)", style={'color': '#C70039 '}),  # Highlighting "Female (≤50K)" in blue
                ":Men in the ≤50K category are also predominantly in the Private sector (7592), followed by Self-employed and Local-gov."
            ], style={'color': '#BD7F37FF', 'font-size': '1.15rem', 'font-weight': 'bold'}),
            html.Li([
                html.Span("Male (>50K)", style={'color': '#C70039 '}),  # Highlighting "Female (≤50K)" in blue
                ":In the >50K category, men are mainly in the Private sector (3470), with significant counts in Self-employed,State-gov and Local-gov."
            ], style={'color': '#BD7F37FF', 'font-size': '1.15rem', 'font-weight': 'bold'}),
            ], className='flex-item')
        ], style={'margin-left': '70'})  # Flex: 1 for insights
    ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'flex-start','margin-bottom': '30px'}),
    html.Div([
        html.P("Proportion of Individuals Earning > $50K by Race and Gender", 
               style={'font-size': '1.25rem', 'font-weight': 'bold', 'margin-bottom': '20px', 'margin-top': '20px'})
    ], className='container', style={'margin-bottom': '20px'}),
    html.Div([
        # Visualization
        html.Div([
            dcc.Graph(
                figure=proportion_count(df)
            )
        ], style={'flex': '3'}),  # Flex: 3 for visualization, with margin-right for spacing

        # Insights
        html.Div([
            html.Ul([
                html.Li([
                html.Span("Female", style={'color': '#f1948a '}),  # Highlighting "Female (≤50K)" in blue
                ":Among females, the largest proportion of those earning >50K is  Amer-Indian-Eskimo (26.3%), followed by White(24.3%) and Asian-Pac-Islander (23.5%)."
            ], style={'color': '#616a6b', 'font-size': '1.15rem', 'font-weight': 'bold'}),
            html.Li([
                html.Span("Male", style={'color': '#f1948a'}),  # Highlighting "Female (≤50K)" in blue
                ":Among males, Asian-Pac-Islander constitute the largest proportion (32%), followed by White (29.6%) and Black (17%)."
            ], style={'color': '#616a6b', 'font-size': '1.15rem', 'font-weight': 'bold'}),
            ], className='flex-item')
        ], style={'margin-left': '70'})  # Flex: 1 for insights
    ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'flex-start','margin-bottom': '30px'}),

], className='container'),

    html.Div([
        html.Div([
            html.H2("Variation in Work Hours Across Occupations and Work Classes", className='subheader', style={'color': '#1E4C6A'}),
        ], className='p-3 bg-custom rounded shadow-sm mb-4'),
        html.Div([
        html.P("How do work hours differ across various workclass?", 
               style={'font-size': '1.25rem', 'font-weight': 'bold', 'margin-bottom': '20px', 'margin-top': '20px'})
    ], className='container', style={'margin-bottom': '20px'}),
        html.Div([
            dcc.Graph(figure=workclass_workhour_tree()),
            html.Div([
                html.Ul([
                html.Li([
                html.Span("<=50k", style={'color': '#f1948a '}),  
                ":The largest segment in this category is for individuals in the Private sector, indicating they work the most hours but earn ≤50K. The Self-employed and Local-gov also occupy smaller portions."
            ], style={'color': '#616a6b', 'font-size': '1.15rem', 'font-weight': 'bold'}),
            html.Li([
                html.Span(">50k", style={'color': '#f1948a'}), 
                ":For individuals earning >50K, the Private sector remains the largest, though other work classes like Self-employed and Local-gov also have a presence."
            ], style={'color': '#616a6b', 'font-size': '1.15rem', 'font-weight': 'bold'})
                ], className='flex-item')
            ])
        ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '30px'}),
        html.Div([
        html.P("How do work hours differ across various oocupation?", 
               style={'font-size': '1.25rem', 'font-weight': 'bold', 'margin-bottom': '20px', 'margin-top': '20px'})
    ], className='container', style={'margin-bottom': '20px'}),
    html.Div([
            dcc.Graph(figure=sunburst()),
            html.Div([
                html.Ul([
                    html.Li("Individuals earning <=50K tend to be in Prof-specialty , Craft repair,Adm-clerical,and Sales roles, working longer hours.", style={'color': '#cc6666', 'font-size': '1.15rem', 'font-weight': 'bold'}),
                    html.Li("The largest segment of >50K income earners work in various occupations with smaller average work hours.", style={'color': '#cc6666', 'font-size': '1.15rem', 'font-weight': 'bold'})
                ], className='flex-item')
            ])
        ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '30px'})
    ], className='container'),

    
    html.Div([
        html.Div([
            html.H2("Average Capital Gain by Work Class, Race, and Native Country", className='subheader', style={'color': '#1E4C6A'}),
        ], className='p-3 bg-custom rounded shadow-sm mb-4'),

        html.Div([
            dcc.Graph(figure=multivariate2(df)),
            html.Div([
                html.Ul([
                    html.Li("Self-employed individuals tend to have the highest average capital gains across the U.S. and other countries.", style={'color': '#534b4f', 'font-size': '1.15rem', 'font-weight': 'bold'}),
                    html.Li("Private, Federal-gov, Local-gov, and State-gov work classes generally show much lower average capital gains compared to the self-employed group.", style={'color': '#534b4f', 'font-size': '1.15rem', 'font-weight': 'bold'}),
                    html.Li("The Other native country category shows a higher capital gain in the self-employed sector compared to the United States.", style={'color': '#534b4f', 'font-size': '1.15rem', 'font-weight': 'bold'})
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
    [Output('question-output', 'children'),
     Output('graph-output', 'figure'),
     Output('insights-output', 'children')],
    [Input('analysis-options', 'value')]
)
def update_main_analysis(selected_option):
    if selected_option == 'hours_worked':
        question = "How does income vary across different work hours?"
        fig = hours_worked_plot()  # Ensure this function returns a Plotly figure
        insights = html.Ul([
            html.Li("The median hours worked per week for both income groups is 40 hours.", style={'color': '#86608e'}),
            html.Li("People earning greater than 50K tend to work slightly more hours per week compared to those earning less than or equal to 50K.", style={'color': '#86608e'}),
            html.Li("The interquartile range (IQR) for the less than or equal to 50K group is narrower compared to the greater than 50K group, suggesting that hours worked per week is more consistent among lower earners.", style={'color': '#86608e'})
        ])

    elif selected_option == 'age_distribution':
        question = "How does income vary across different age groups?"
        fig = age_distribution_plot()  # Ensure this function returns a Plotly figure
        insights = html.Ul([
            html.Li("The distribution of age for people earning less than or equal to 50K is wider compared to those earning greater than 50K.", style={'color': '#86608e'}),
            html.Li("There are more younger individuals (20-40 years) in the less than or equal to 50K group.", style={'color': '#86608e'}),
            html.Li("The greater than 50K group has a tighter age distribution, indicating that higher earners are often within a more specific age range.", style={'color': '#86608e'})
        ])

    elif selected_option == 'marital_status':
        question = "Are there significant differences in income between married individuals and those who are divorced, widowed, or never married?"
        fig = marital_status_plot()  # Ensure this function returns a Plotly figure
        insights = html.Ul([
            html.Li("Individuals who have never married or are divorced show a higher count of individuals earning less than or equal to 50K.", style={'color': '#5f9ea0'}),
            html.Li("Married individuals show a higher count of individuals earning greater than 50K.", style={'color': '#5f9ea0'}),
            html.Li("The income disparity based on marital status is evident, with married individuals having a higher likelihood of earning more.", style={'color': '#5f9ea0'})
        ])

    elif selected_option == 'racial_group':
        question = "What is the distribution of income by racial group?"
        fig = racial_status_stacked_plot()  # Ensure this function returns a Plotly figure
        insights = html.Ul([
            html.Li("Most of the individuals in the dataset are White, with a higher count earning less than or equal to 50K.", style={'color': '#26619c'}),
            html.Li("Other races, such as Black and Asian-Pac-Islander, also have significant counts but with fewer individuals earning greater than 50K.", style={'color': '#26619c'}),
            html.Li("The disparity in income distribution is evident across different races, with a noticeable difference in the counts of higher earners.", style={'color': '#26619c'})
        ])

    elif selected_option == 'education_level':
        question = "Is there a significant difference in income based on the highest level of education completed?"
        fig = education_level_plot()  # Ensure this function returns a Plotly figure
        insights = html.Ul([
            html.Li("Most individuals have education levels around high school graduation (HS-grad).", style={'color': '#739073'}),
            html.Li("Higher education levels like Bachelors, Masters, and Doctorate show a higher proportion of individuals earning greater than 50K.", style={'color': '#739073'}),
            html.Li("Lower education level like High school grad,High school incomplete show a higher proportion of individuals earning less than or equal to 50K.", style={'color': '#739073'})
        ])

    return question, fig, insights

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
    app.run(debug=True)  # runs on http://127.0.0.1:8050
