# Create dashboard for Day of Week for 2021-2024 

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from google.cloud import bigquery

class DayOfWeekDashboard:
    def __init__(self, project_id, dataset, mart_table='mart_day_of_week'):
        """
        Initialize dashboard for day of week trips
        
        :param project_id: Google Cloud Project ID
        :param dataset: Dataset containing dbt mart model
        :param mart_table: Name of the mart table
        """
        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id
        self.dataset = dataset
        self.mart_table = mart_table
        
    def fetch_day_of_week_data(self):
        """
        Fetch day of week trip data from dbt mart model
        
        :return: pandas DataFrame with day of week data
        """
        query = f"""
        SELECT
          EXTRACT(year from trip_date) AS year, 
          day_of_week, 
          AVG(total_trips) AS avg_daily_trips
        FROM `{self.project_id}.{self.dataset}.{self.mart_table}`
        GROUP BY EXTRACT(year from trip_date), 
                 day_of_week
        ORDER BY year, 
                 day_of_week
        """
        
        # Execute query and convert to DataFrame
        df = self.client.query(query).to_dataframe()
        
        # Add day order for consistent sorting
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df['day_order'] = df['day_of_week'].map({day: i for i, day in enumerate(day_order)})
        df = df.sort_values(['year', 'day_order'])
        
        return df
    
    def create_dashboards(self, output_dir='dashboards/outputs'):
        """
        Generate and save day of week dashboards
        
        :param output_dir: Directory to save dashboard files
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Fetch data
        df = self.fetch_day_of_week_data()
        
        # Day Order for consistent visualization
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # 1. Day of Week by Year Dashboard
        fig_day_of_week = make_subplots(
            rows=2, cols=1,
            subplot_titles=(
                'Average Daily Bicycle Trips by Day of Week',
                'Yearly Average Daily Trips'
            ),
            vertical_spacing=0.15,
            specs=[[{"type": "bar"}], [{"type": "bar"}]]
        )
        
        # Day of Week Plot
        for year in sorted(df['year'].unique()):
            year_data = df[df['year'] == year]
            
            fig_day_of_week.add_trace(
                go.Bar(
                    x=year_data['day_of_week'],
                    y=year_data['avg_daily_trips'],
                    name=str(year),
                    text=[f"{x:.0f}" for x in year_data['avg_daily_trips']],
                    textposition='auto'
                ),
                row=1, col=1
            )
        
        # Yearly Average Plot
        yearly_avg = df.groupby('year')['avg_daily_trips'].mean().reset_index()
        yearly_avg['year'] = yearly_avg['year'].astype(str)
        
        fig_day_of_week.add_trace(
            go.Bar(
                x=yearly_avg['year'],
                y=yearly_avg['avg_daily_trips'],
                text=[f"{x:.0f}" for x in yearly_avg['avg_daily_trips']],
                textposition='auto'
            ),
            row=2, col=1
        )
        
        # Update layout for day of week plot
        fig_day_of_week.update_layout(
            height=800, 
            width=1000,
            title_text="London Bicycle Trips: Day of Week Analysis",
            barmode='group'
        )
        
        # Update x-axes
        fig_day_of_week.update_xaxes(
            categoryorder='array', 
            categoryarray=day_order, 
            row=1, col=1
        )
        
        # 2. Line Plot for Trend Analysis
        fig_trend = px.line(
            df, 
            x='day_of_week', 
            y='avg_daily_trips', 
            color='year',
            title='Average Daily Trips Trend by Day of Week',
            labels={'avg_daily_trips': 'Average Daily Trips', 'day_of_week': 'Day of Week'},
            category_orders={'day_of_week': day_order}
        )
        
        fig_trend.update_layout(
            height=600,
            width=1000,
            title_text="London Bicycle Trips: Day of Week Trend"
        )
        
        # Save dashboards
        dashboards = [
            ('day_of_week', fig_day_of_week),
            ('trend', fig_trend)
        ]
        
        for name, fig in dashboards:
            # Save interactive HTML
            html_path = os.path.join(output_dir, f'day_of_week_{name}_dashboard.html')
            fig.write_html(html_path)
            print(f"Saved interactive dashboard: {html_path}")
            
            # Save static image
            png_path = os.path.join(output_dir, f'day_of_week_{name}_dashboard.png')
            fig.write_image(png_path)
            print(f"Saved static dashboard: {png_path}")

def main():
    dashboard = DayOfWeekDashboard(
        project_id='your-project-id',
        dataset='your_dataset'
    )
    
    # Generate all dashboards
    dashboard.create_dashboards()

if __name__ == '__main__':
    main()