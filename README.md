# Data Engineering Zoomcamp Project- London Cycling Analytics (2021-2024)

## Problem Statement
- This project analyzes London's Santander Cycles data to identify usage patterns, high-demand areas, and temporal trends to support better resource allocation and infrastructure planning. Understanding these data will help support data-driven decisions for expanding cycling infrastructure in London and help its promotion of sustainability options. 

## Business Value
- Track bicycle usage pattern changes from 2021-2024 to help inform insights on how to adapt infrastructure to evolving commuting behaviors. This is especially important given the pandemic's significant global impact on societies. 
- Help identify high-demand areas for additional docking stations.
- Optimize bicycle rebalancing operations by identifying stations with significant net flow imbalances.

## Data Source 
- This project uses data from [Transport for London's (TfL) Santander Cycles](https://cycling.data.tfl.gov.uk/). Documentation of methodology can be found [here](https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/0.5%20Strategic%20cycling%20estimates%20-%20methodology%20note.pdf)
- This project samples multiple time periods from 2021-2024 to provide more comprehensive insights over critical pandemic years. 
- Based on TfL's recommended approach, this project focuses on relative changes over time rather than absolute values.

## Methodological Approach
- This project uses a strategic sampling approach rather than the complete dataset, selecting specific weeks across each season and year from 2021-2024. This approach was chosen for the following reasons:
  - **Alignment with Industry Standards:** TfL documentation notes that they collect cycling data "once a year in spring (April to July), on weekdays (preferably Tuesdays to Thursdays) that are 'neutral'" (TfL Cycling Methodology Document, 2022-- refer to methodology documentation for more information)). This project expands on this approach by sampling across multiple seasons to capture more comprehensive patterns.
  - **Computational Efficiency**: Processing the complete dataset would require significant computational resources without significant proportional analytical gain. This project aims to provide an efficient analytic overview while maintaining statistical relevance. Balancing resource constraints and efficiency is an important consideration across most companies and organizations.  
  - **Representative Coverage:** this project's sampling strategy ensures:
    - 1. **Coverage across all seasons** (Winter, Spring, Summer, Fall).
    - 2. **Representation of both weekday and weekend usage patterns**
    - 3. **Post-pandemic trends**: data collected from multiple years (2021-2024) to capture post-pandemic trends
- As noted in the TfL documentation, "cycling is a mode with characteristics that make monitoring its use more challenging than the monitoring of other modes" -- this project aims to address these limitations by focusing on relative changes over time rather than absolute values.

---
## Data Infrastructure Overview
- **Data Lake**: Google Cloud Storage (GCS)-- cloud storage to store raw and processed datasets
- **Data Warehouse**: BigQuery-- serverless data warehouse for analytics. **Partitioned tables** by date to optimize query performance and reduce costs 
- **Workflow Orchestration**: semi-automated **batch processing** for workflow orchestration
- **Transformations**: dbt/Python-- dbt and various packages in Python (e.g., pandas, numpy) to clean, transform, create, and standardize metrics. 
- **Dashboard Visualization**: Plotly (Python)-- interactive visualizations with multiple dashboard tiles and standalone HTML files for easy sharing and deployment

## Pipeline Workflow 
1. **Data Ingestion**: **batch processing** (semi-automated workflow orchestration) 
   - Downloaded and preprocessed London bicycle data (Python)
   - Cleaned and standardized data (Python) 
   - Uploaded data into GCS bucket
   - Loaded data into BigQuery

2. **Data Warehouse Setup**:
   - Created optimized tables (e.g., daily_trips, station_popularity) in BigQuery 
   - Implemented date-based partitioning to improve query performance
   - Established table structure for both raw data and aggregated views

3. **Data Transformation**:
   - Created **station popularity metrics** (e.g., total_traffic, net_flow)
   - Calculated **temporal patterns** by day of week and year
   - Normalized data across different time periods
   - Implemented aggregation transformations for analytics

4. **Dashboard Creation**:
   - Generated interactive dashboards for **station popularity** and **temporal usage patterns**
   - Exported interactive HTML dashboards for easy viewing and sharing
  
## Data Transformations with dbt
This project uses dbt (data build tool) to transform the raw bicycle data into analytics-ready tables:
- **Staging models**: Clean and standardize raw data
- **Intermediate models**: Create aggregated daily metrics
- **Analytics models**: Generate final tables for dashboards

**Key transformations include:**
- Daily trip aggregation by day of week
- Station popularity metrics (total_traffic, net_flow)
- Standardized time-based analysis

---

## Dataset Descriptions 

### Day of Week Usage (`daily_trips`)
| Variable          | Description                                | Data Type |
| ----------------- | ------------------------------------------ | --------- |
| `year`            | Year of observation (2021-2024)            | Integer   |
| `day_of_week`     | Day of the week (Monday-Sunday)            | String    |
| `total_trips`     | Total number of bicycle trips              | Integer   |
| `num_days`        | Number of days sampled                     | Integer   |
| `avg_daily_trips` | Average daily trips (total_trips/num_days) | Float     |
|                   |                                            |           |

## Station Popularity (`station_popularity`) 
| Variable        | Description                                            | Data Type |     |     |
| --------------- | ------------------------------------------------------ | --------- | --- | --- |
| `station_id`    | Unique identifier for bicycle docking station          | Integer   |     |     |
| `station_name`  | Name and location of the station                       | String    |     |     |
| `total_starts`  | Number of trips that began at this station             | Integer   |     |     |
| `total_ends`    | Number of trips that ended at this station             | Integer   |     |     |
| `total_traffic` | Sum of starts and ends (overall usage)                 | Integer   |     |     |
| `net_flow`      | Difference between starts and ends (starts minus ends) | Integer   |     |     |


--- 

## Dashboards and Insights

--- 

## Reproducibility
- First, ensure everything is set up (e.g., Docker, GCP, BigQuery, Python, Jupyter Notebook) properly and all required packages are installed!
  
**1. Clone repository**
 ```git clone https://github.com/wangjenn/london-bicycle-analysis.git``` 

**2. Set up Google Cloud**
  - Create a Google account and signup for Google Cloud Platform
  - Create a New Project and take note of the project-id
  - Create a Service Account and configure its Identity and Access Management (IAM) policy:
    - Viewer
    - Storage Admin
    - Storage Object Admin
    - BigQuery Admin
  - Create a new key for the service account, and download the key as JSON credentials. Store the key in a secure location.
  -  Install the Google Cloud SDK
  - Replace the GCP key location in the following codes and execute the codes on terminal:
  
    ```gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS```
    
    ```gcloud auth application-default login```
    
  - Close and restart your terminal
  - (_Optional_) Create a new virtual environment

**3. Ingest data (Python):** download, ingest, and preprocess data for 2021-2024. See [SEE HERE] 

**4. Transform data (dbt, Python)**: create necessary aggregates and tables (**daily_trips, station_popularity**). See [SQL SCRIPTS] and [PYTHON JUPYTER NOTEBOOK] 

**5. Analyze data and generate interactive dashboards (Python):** analyze data with Python (e.g., pandas) and create interactive dashboards using Plotly in Python [NOTEBOOK HERE]-- analysis notebook. 


--- 
### Thanks for taking the time to read through and review this project! 💕_

