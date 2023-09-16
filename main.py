import streamlit as st
import seaborn as sns
import pandas as pd
import base64
import plotly.express as px
import plotly.graph_objects as go


# Set Streamlit theme
st.set_page_config(
    page_title="Data Science Jobs",
	page_icon="chart_with_upwards_trend",
    layout="wide",
 
)
# Set color palette for visualizations
sns.set_palette("pastel")

# Define the layout
st.title("Data Science Jobs Analysis Dashboard")

# Add CSS to set the background image for the title
st.markdown(
    """
    <style>
    h1 {
        background-repeat: no-repeat;
        background-color: lightblue;
        background-position: center;
        background-size: cover;
        color: black;
        padding: 1rem;
        text-align: center;
        font-size: 3rem;
    }

    .left-column {
        flex: 1;
        padding-right: 1rem;
        padding-top: 5rem;
    }
    .right-column {
        flex: 1;
        padding-left: 1rem;
    }
	.analytics-text {
			font-size: 1rem;
			text-align: left;
			margin-top: 1rem;
		}

    </style>
    """,
    unsafe_allow_html=True
)
# Load your data
salaries = pd.read_csv('./Salaries.csv')

tab1, tab2 = st.tabs(["Story", "Visualizations"])

with tab1:


	# Create the container with two columns
	col1, col2 = st.columns(2)

	# Add text to the left column
	with col1:
		st.markdown("<div class='left-column'>", unsafe_allow_html=True)
		#st.markdown("<h2 style='background-color: white; padding: 0rem; text-align: left;'>Story</h2>", unsafe_allow_html=True)
		st.write('***Welcome to the Data Science Jobs Analysis Dashboard*** :sunglasses: !\n')
		st.write("This tool analyzes  **4 years** (2000-2023) of different Data Science job titles at **5 countries(United States, United Kingdom, Canada,Spain and India)** and tries to uncover useful insights with respect to salary and other attributes( Employment type, Remote percentage and etc). ")
		st.write("")
		st.write("Source : https://www.kaggle.com/datasets/arnabchaki/data-science-salaries-2023?select=ds_salaries.csv")
	
		st.markdown("</div>", unsafe_allow_html=True)

	# Add an image to the right column
	with col2:
		
		st.markdown("<div class='right-column'>", unsafe_allow_html=True)
		image_path = "./datascience.jpg"  # Replace with the actual path to your image
		st.image(image_path, use_column_width=True)
		st.markdown("</div>", unsafe_allow_html=True)

	# Footer

	# Create the footer container
	with st.container():
		st.markdown("<hr style='border: 1px solid black'>", unsafe_allow_html=True)
		st.text("2023 Data Science Jobs Analysis Dashboard-Samer Bou Hamdan. All rights reserved.")



with tab2:
	
	col1, col2 = st.columns([1, 2])
	with col1:
		# Filter by Company Location
		company_location_filter = st.selectbox('Select Company Location', ['All'] + salaries['company_location'].unique().tolist())

		# Filter by Work Year
		available_work_years = salaries['work_year'].unique().tolist()
		selected_work_year = st.selectbox('Select Year', ['All'] + available_work_years)

		# Apply Filters
		filtered_salaries = salaries.copy()
		if company_location_filter != 'All':
			filtered_salaries = filtered_salaries[filtered_salaries['company_location'] == company_location_filter]
		if selected_work_year != 'All':
			filtered_salaries = filtered_salaries[filtered_salaries['work_year'] == selected_work_year]
		st.write("")
		remote_ratio_fig = px.pie(
        filtered_salaries,
        names='remote_ratio',
        title='Distribution of Remote Work',
        hole=0.4,
        color_discrete_sequence=['#FF5733', '#007acc', '#2ca02c', '#FFA500', '#e63946'],
        labels={'remote_ratio': 'Remote Work %'},
        template="plotly"
		)
		remote_ratio_fig.update_traces(textposition='inside', textinfo='percent+label')
		remote_ratio_fig.update_layout(
        showlegend=False,
        font=dict(family='Arial', size=14),
		width=400, height=400,
		title_font=dict(size=16)
		)
		st.plotly_chart(remote_ratio_fig)		
	    
	with col2:
		st.write("")
		st.write("")

		# Horizontal Stacked Bar Chart for Top 5 Job Titles with Company Size Distribution
		top_job_titles = filtered_salaries['job_title'].value_counts().head(5).index.tolist()
		df_filtered = filtered_salaries[filtered_salaries['job_title'].isin(top_job_titles)]
		pivot_df = df_filtered.pivot_table(index='job_title', columns='company_size', aggfunc='size', fill_value=0)
		company_size_distribution_fig = px.bar(
			pivot_df,
			orientation='h',
			title='',
			labels={'y': 'Job Title'},
			color_discrete_sequence=['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c'],
		)
		company_size_distribution_fig.update_xaxes(title='# of Jobs')
		company_size_distribution_fig.update_yaxes(categoryorder='total ascending')
		company_size_distribution_fig.update_layout(width=800, height=500)

		st.write('#### Top 5 Job Titles with Company Size Distribution')
		st.plotly_chart(company_size_distribution_fig)
		




	# Create filters for employment_type and work_year next to each other
	col1, col2 = st.columns(2)

	with col1:
		employment_type_filter = st.selectbox('Select Employment Type', ['All'] + salaries['employment_type'].unique().tolist())

	with col2:
		work_year_filter = st.selectbox('Select Work Year', ['All'] + salaries['work_year'].unique().tolist())

	# Apply filters
	filtered_salaries = salaries.copy()
	if employment_type_filter != 'All':
		filtered_salaries = filtered_salaries[filtered_salaries['employment_type'] == employment_type_filter]
	if work_year_filter != 'All':
		filtered_salaries = filtered_salaries[filtered_salaries['work_year'] == work_year_filter]

	# Calculate the mean salary per Country
	average_salary = filtered_salaries.groupby('company_location')['salary_in_usd'].mean().reset_index()

	# Calculate the count of rows per Country
	location_count = filtered_salaries['company_location'].value_counts().reset_index()
	location_count.columns = ['company_location', 'count']

	# Merge the two DataFrames on 'company_location'
	location_stats = average_salary.merge(location_count, on='company_location')

	# Create Plotly figure for the combo chart
	fig = go.Figure()

	# Add bar chart for the count
	fig.add_trace(go.Bar(
		x=location_stats['company_location'],
		y=location_stats['count'],
		text=location_stats['count'],
		textposition='auto',
		name='Number of jobs',
		marker_color='#1f77b4'
	))

	# Add line chart for average salary on the second y-axis
	fig.add_trace(go.Scatter(
		x=location_stats['company_location'],
		y=location_stats['salary_in_usd'],
		mode='lines+markers',
		name='Average Salary',
		yaxis='y2',
		line=dict(color='orange', width=2),
		marker=dict(color='orange', size=8)
	))

	# Update layout
	fig.update_layout(
		title='Number of Jobs and Average Salary per Country',
		xaxis=dict(title='Country'),
		yaxis=dict(title='Number of jobs'),
		yaxis2=dict(title='Average Salary', overlaying='y', side='right', showgrid=False, tickformat='$,.2f'),
		legend=dict(x=0.02, y=0.95),  # Adjust the legend position
	)

	# Use st.plotly_chart to display the Plotly figure
	st.plotly_chart(fig, use_container_width=True)

	st.subheader("Some useful insights:")
	st.write("")
	st.write("1- Data Science jobs were more common among large size companies in 2020 and 2021,However, a dramatic increase happened in medium size companies after 2022")
	st.write("2- Data science job opportunities are increasing with time")
	st.write("3- Data Scientist,Data Egineer, Data Analyst, Machine Learning Engineer are the top job titles since 2020")
	st.write("4- Remote work decreased from 68.9% in 2020 during covid into 33% in 2023 and it is more common in canada")
	st.write("5- United States has the highest average salary and then Canada come afterwards")
	st.write("6- Currently, United states has the largest number of data science jobs followed by United Kingdom")
	st.write("7- Data science jobs are decreasing in india with time unlike the other countries")

	
	
	with st.container():
		st.markdown("<hr style='border: 1px solid black'>", unsafe_allow_html=True)
		st.text("2023 Data Science Jobs Analysis Dashboard-Samer Bou Hamdan. All rights reserved.")
		
