# Creating dashboard for Station Popularity using Plotly in Python 

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from google.cloud import bigquery

class StationPopularityDashboard:
    def __init__(self, project_id, dataset, mart_table='mart_station_popularity'):
        """
        Initialize dashboard for station popularity
        
        :param project_id: Google Cloud Project ID
        :param dataset: Dataset containing dbt mart model
        :param mart_table: Name of the mart table
        """
        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id
        self.dataset = dataset
        self.mart_table = mart_table
        
    def fetch_station_data(self, limit=15):
        """
        Fetch station popularity data from dbt mart model
        
        :param limit: Number of top stations to retrieve
        :return: pandas DataFrame with station data
        """
        query = f"""
        SELECT
          station_id,
          station_name,
          total_starts,
          total_ends,
          total_traffic,
          net_flow
        FROM `{self.project_id}.{self.dataset}.{self.mart_table}`
        ORDER BY total_traffic DESC
        LIMIT {limit}
        """
        
        # Execute query and convert to DataFrame
        df = self.client.query(query).to_dataframe()
        return df
    
    def create_dashboards(self, output_dir='dashboards/outputs'):
        """
        Generate and save station popularity dashboards
        
        :param output_dir: Directory to save dashboard files
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Fetch data
        df = self.fetch_station_data()
        
        # 1. Total Traffic Dashboard
        fig_total_traffic = px.bar(
            df.sort_values('total_traffic', ascending=False),
            x='station_name',
            y='total_traffic',
            title='Top Bicycle Stations by Total Traffic',
            labels={'total_traffic': 'Total Trips', 'station_name': 'Station Name'}
        )
        fig_total_traffic.update_layout(
            xaxis_tickangle=-45,
            height=600,
            width=1000
        )
        
        # 2. Starts vs Ends Composition
        df_melted = pd.melt(
            df, 
            id_vars=['station_name', 'station_id'],
            value_vars=['total_starts', 'total_ends'],
            var_name='trip_type',
            value_name='trips'
        )
        
        fig_starts_ends = px.bar(
            df_melted.sort_values(by=['trips'], ascending=False),
            x='station_name',
            y='trips',
            color='trip_type',
            title='Station Usage Composition: Starts vs. Ends',
            labels={'trips': 'Number of Trips', 'station_name': 'Station Name', 'trip_type': 'Trip Type'},
            color_discrete_map={'total_starts': 'royalblue', 'total_ends': 'lightcoral'},
            barmode='group'
        )
        fig_starts_ends.update_layout(
            xaxis_tickangle=-45,
            height=600,
            width=1000,
            legend_title_text='Trip Type'
        )
        
        # 3. Net Flow Dashboard
        fig_net_flow = px.bar(
            df.sort_values('net_flow'),
            x='station_name',
            y='net_flow',
            color='net_flow',
            color_continuous_scale='RdBu',
            title='Station Net Flow (Starts minus Ends)',
            labels={'net_flow': 'Net Flow', 'station_name': 'Station Name'}
        )
        fig_net_flow.update_layout(
            xaxis_tickangle=-45,
            height=600,
            width=1000
        )
        fig_net_flow.add_shape(
            type="line",
            x0=-0.5,
            y0=0,
            x1=len(df)-0.5,
            y1=0,
            line=dict(color="black", width=1, dash="dash")
        )
        
        # 4. Comprehensive Flow Patterns
        fig_flow_patterns = make_subplots(
            rows=2, cols=1,
            subplot_titles=(
                'Top 5 Origin Stations (Positive Net Flow)',
                'Top 5 Destination Stations (Negative Net Flow)'
            ),
            vertical_spacing=0.15,
            specs=[[{"type": "bar"}], [{"type": "bar"}]]
        )
        
        # Top origin stations (positive net flow)
        origin_stations = df[df['net_flow'] > 0].sort_values('net_flow', ascending=False).head(5)
        fig_flow_patterns.add_trace(
            go.Bar(
                x=origin_stations['station_name'],
                y=origin_stations['net_flow'],
                marker_color='royalblue',
                text=origin_stations['net_flow'],
                textposition='auto',
                name='Net Outflow'
            ),
            row=1, col=1
        )
        
        # Top destination stations (negative net flow)
        destination_stations = df[df['net_flow'] < 0].sort_values('net_flow').head(5)
        fig_flow_patterns.add_trace(
            go.Bar(
                x=destination_stations['station_name'],
                y=destination_stations['net_flow'].abs(),
                marker_color='lightcoral',
                text=destination_stations['net_flow'].abs(),
                textposition='auto',
                name='Net Inflow'
            ),
            row=2, col=1
        )
        
        fig_flow_patterns.update_layout(
            height=800,
            width=1000,
            title_text="London Bicycle Station Flow Patterns",
            showlegend=True
        )
        fig_flow_patterns.update_xaxes(tickangle=-45, row=1, col=1)
        fig_flow_patterns.update_xaxes(tickangle=-45, row=2, col=1)
        
        # Save dashboards
        dashboards = [
            ('total_traffic', fig_total_traffic),
            ('starts_ends', fig_starts_ends),
            ('net_flow', fig_net_flow),
            ('flow_patterns', fig_flow_patterns)
        ]
        
        for name, fig in dashboards:
            # Save interactive HTML
            html_path = os.path.join(output_dir, f'station_popularity_{name}_dashboard.html')
            fig.write_html(html_path)
            print(f"Saved interactive dashboard: {html_path}")
            
            # Save static image
            png_path = os.path.join(output_dir, f'station_popularity_{name}_dashboard.png')
            fig.write_image(png_path)
            print(f"Saved static dashboard: {png_path}")

def main():
    dashboard = StationPopularityDashboard(
        project_id='your-project-id',
        dataset='your_dataset'
    )
    
    # Generate all dashboards
    dashboard.create_dashboards()

if __name__ == '__main__':
    main()