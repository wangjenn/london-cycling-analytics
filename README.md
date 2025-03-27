# Data Engineering Zoomcamp Project- London Cycling Analytics (2021-2024)

## ✨ Problem Statement
- This project analyzes London's Santander Cycles data to identify usage patterns, high-demand areas, and temporal trends to support better resource allocation and infrastructure planning. Understanding these data will help support data-driven decisions for expanding cycling infrastructure in London and help its promotion of sustainability options. 

## ✨ Business Value
- Track bicycle usage pattern changes from 2021-2024 to help inform insights on how to adapt infrastructure to evolving commuting behaviors. This is especially important given the pandemic's significant global impact on societies. 
- Help identify high-demand areas for additional docking stations.
- Optimize bicycle rebalancing operations by identifying stations with significant net flow imbalances.

## ✨ Data Source 
- This project uses data from [Transport for London's (TfL) Santander Cycles](https://cycling.data.tfl.gov.uk/). Documentation of methodology can be found [here](https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/0.5%20Strategic%20cycling%20estimates%20-%20methodology%20note.pdf)
- This project samples multiple time periods from 2021-2024 to provide more comprehensive insights over critical pandemic years. 
- Based on TfL's recommended approach, this project focuses on relative changes over time rather than absolute values.

## ✨ Methodological Approach
- This project uses a strategic sampling approach rather than the complete dataset, selecting specific weeks across each season and year from 2021-2024. This approach was chosen for the following reasons:
  - **Alignment with Industry Standards:** TfL documentation notes that they collect cycling data "once a year in spring (April to July), on weekdays (preferably Tuesdays to Thursdays) that are 'neutral'" (TfL Cycling Methodology Document, 2022-- refer to methodology documentation for more information)). This project expands on this approach by sampling across multiple seasons to capture more comprehensive patterns.
  - **Computational Efficiency**: Processing the complete dataset would require significant computational resources without significant proportional analytical gain. This project aims to provide an efficient analytic overview while maintaining statistical relevance. Balancing resource constraints and efficiency is an important consideration across most companies and organizations.  
  - **Representative Coverage:** this project's sampling strategy ensures:
    - 1. **Coverage across all seasons** (Winter, Spring, Summer, Fall).
    - 2. **Representation of both weekday and weekend usage patterns**
    - 3. **Post-pandemic trends**: data collected from multiple years (2021-2024) to capture post-pandemic trends
- As noted in the TfL documentation, "cycling is a mode with characteristics that make monitoring its use more challenging than the monitoring of other modes" -- this project aims to address these limitations by focusing on relative changes over time rather than absolute values.

---
## ✨ Data Infrastructure Overview
- **Data Lake**: Google Cloud Storage (GCS)-- cloud storage to store raw and processed datasets
- **Data Warehouse**: BigQuery-- serverless data warehouse for analytics. **Partitioned tables** by date to optimize query performance and reduce costs 
- **Workflow Orchestration**: semi-automated **batch processing** for workflow orchestration
- **Transformations**: dbt, Python-- dbt and various packages in Python (e.g., pandas, numpy) to clean, transform, create, and standardize metrics. 
- **Dashboard Visualization**: Plotly (Python)-- interactive visualizations with multiple dashboard tiles and standalone HTML files for easy sharing and deployment

## ✨ Pipeline Workflow 
1. **Data Ingestion**:
   - Batch processing (semi-automated workflow orchestration) 
   - Downloaded and preprocessed London bicycle data (Python)
   - Cleaned and standardized data (Python) 
   - Uploaded data into GCS bucket
   - Loaded data into BigQuery

3. **Data Warehouse**:
   - Created optimized tables in BigQuery 
   - Implemented date-based partitioning to improve query performance
   - Established table structure for both raw data and aggregated views

4. **Data Transformation**:
   - Implemented **dbt models** with three layers:
     - Staging: clean and standardize raw data
     - Intermediate: create aggregated metrics
     - Analytics: business-ready output tables for dashboards 
   - Created **station popularity metrics** using dbt transformations
   - Calculated **day_of_week metrics** by day of week and year with dbt dbt transformations 
   - Normalized data across different time periods with **Python**

5. **Dashboard Creation**:
   - Generated interactive dashboards for **station popularity** and **day of week usage**
   - Exported interactive HTML dashboards for easy viewing and sharing

---

## ✨ Dataset and Variable Descriptions 

### Day of Week Usage
| Variable          | Description                                | Data Type |
| ----------------- | ------------------------------------------ | --------- |
| `year`            | Year of observation (2021-2024)            | Integer   |
| `day_of_week`     | Day of the week (Monday-Sunday)            | String    |
| `total_trips`     | Total number of bicycle trips              | Integer   |
| `num_days`        | Number of days sampled                     | Integer   |
| `avg_daily_trips` | Average daily trips (total_trips/num_days) | Float     |
|                   |                                            |           |

## Station Popularity
| Variable        | Description                                            | Data Type |    
| --------------- | ------------------------------------------------------ | --------- |
| `station_id`    | Unique identifier for bicycle docking station          | Integer   |
| `station_name`  | Name and location of the station                       | String    |
| `total_starts`  | Number of trips that began at this station             | Integer   |
| `total_ends`    | Number of trips that ended at this station             | Integer   |
| `total_traffic` | Sum of starts and ends (overall usage)                 | Integer   | 
| `net_flow`      | Difference between starts and ends (starts minus ends) | Integer   |  


---

## ✨ Dashboards and Insights
- Refer to dashboards [here](https://github.com/wangjenn/london-cycling-analytics/tree/main/dashboards)

### 🚴🏻‍♂️ Station Popularity

#### **Top Bicycle Stations by Total Traffic:** wwe
![](https://i.imgur.com/1dDylpf.png)
![](https://i.imgur.com/IKNxQWK.png)
![](https://i.imgur.com/1uFTmZ9.png)



![](https://i.imgur.com/tuIWbyv.png)

![](https://i.imgur.com/2z3oVFg.png)

![](https://i.imgur.com/dMclvGW.png)
- The net_flow column is particularly interesting:
	- **Negative values** (like Hop Exchange at -4876) mean more people end trips there than start them - these are "destination stations"
	- **Positive values** (like Hyde Park Corner ID 1075 at +1190) mean more people start trips there than end them - these are "origin stations"
	- **Values close to zero** indicate balanced usage (people start and end trips in equal numbers)

#### **Top 5 Origin and Destination Stations** 
![](https://i.imgur.com/3MYVFQf.png)

### 🚴🏻‍♂️ Day of Week Usage
![](https://i.imgur.com/pMUgQHX.png)
### Week day vs. weekend usage by year

![[yearly_weekday_weekend 1.png]]

- **Week day vs. Weekend Ratio by Year**
![ScreenFloat Shot of Preview at Mar 26, 2025 at 4_41_34 PM](https://p.ipic.vip/z02sy4.png)

- **NOTES**: 
	- Commuting** patterns make sense 
---

## ✨ Reproducibility
- First, ensure everything is set up (e.g., GCP, BigQuery, Python, dbt) and all required packages are installed! Refer to [requirements.txt](https://github.com/wangjenn/london-cycling-analytics/blob/main/requirements.txt)
  

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

**3. Ingest data:** download, ingest, and preprocess 2021-2024 data with Python. Refer to [data_ingestion](https://github.com/wangjenn/london-cycling-analytics/blob/main/scripts/data_ingestion.py) script

**4. Transform data (dbt)**: create all necessary aggregates and tables using **dbt**. Make sure to follow dbt's best practices (e.g., following structured model hierarchy, defining clear model dependencies). Refer to [models](https://github.com/wangjenn/london-cycling-analytics/tree/main/models) and [dbt_project.yml](https://github.com/wangjenn/london-cycling-analytics/blob/main/dbt_project.yml) 

**5. Analyze data and generate interactive dashboards (Python):** analyze data with Python (e.g., pandas) and create interactive dashboards using Plotly in Python
 - Refer to [station_popularity_dashboard.py](https://github.com/wangjenn/london-cycling-analytics/blob/main/scripts/station_popularity_dashboard.py) for **Station Popularity** dashboard
 - Refer to [day_of_week_dashboard.py](https://github.com/wangjenn/london-cycling-analytics/blob/main/scripts/day_of_week_dashboard.py) for **Day of Week Usage** dashboard 


---
### Thanks for taking the time to read through and review this project! 💕

