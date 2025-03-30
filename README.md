# Data Engineering Zoomcamp Project - London Cycling Analytics (2021-2024)

## ✨ Problem Statement

- This project analyzes London's Santander Cycles data to identify usage patterns, high-demand areas, and temporal trends to support better resource allocation and infrastructure planning. Understanding these patterns will help support data-driven decisions for expanding cycling infrastructure in London and promote sustainable transportation options.

## ✨ Business Value

- Track bicycle usage pattern changes from 2021-2024 to inform infrastructure adaptation for evolving commuting behaviors, particularly important given the pandemic's global impact
- Identify high-demand areas for additional docking stations
- Optimize bicycle rebalancing operations by identifying stations with significant net flow imbalances

## ✨ Data Source 

- [Transport for London's (TfL) Santander Cycles](https://cycling.data.tfl.gov.uk/) data
- Documentation of methodology available [here](https://cycling.data.tfl.gov.uk/ActiveTravelCountsProgramme/0.5%20Strategic%20cycling%20estimates%20-%20methodology%20note.pdf)
- Strategic sampling of multiple time periods from 2021-2024 to provide comprehensive insights over critical post-pandemic years
- Following TfL's recommended approach by focusing on relative changes over time rather than absolute values

## ✨ Methodological Approach

- This project uses a strategic sampling approach rather than processing the complete dataset, selecting specific weeks across each season and year from 2021-2024. This approach was chosen for the following reasons:

	- **Alignment with Industry Standards:** TfL's methodology notes that they collect cycling data "once a year in spring (April to July), on weekdays (preferably Tuesdays to Thursdays) that are 'neutral'" (TfL Cycling Methodology Document, 2022). This project expands on this approach by sampling across multiple seasons.
	  
	- **Computational Efficiency:** Processing the complete dataset would require significant computational resources without proportional analytical gain. The sampling approach provides an efficient analytic overview while maintaining statistical relevance.
	  
	- **Representative Coverage:** The sampling strategy ensures:
	  1. **Coverage across all seasons** (Winter, Spring, Summer, Fall)
	  2. **Representation** of both weekday and weekend usage patterns
	  3. **Post-pandemic trends** captured from multiple years (2021-2024)

- As noted in the TfL documentation, *"cycling is a mode with characteristics that make monitoring its use more challenging than the monitoring of other modes."* This project addresses these limitations by focusing on relative changes over time rather than absolute values.

## ✨ Data Infrastructure Overview

- **Data Lake:** Google Cloud Storage (GCS) for storing raw and processed datasets
- **Data Warehouse:** BigQuery with partitioned tables by date to optimize query performance and reduce costs
- **Workflow Orchestration:** Semi-automated batch processing for workflow orchestration
- **Transformations:** dbt and Python (pandas, numpy) for cleaning, transforming, creating, and standardizing metrics
- **Dashboard Visualization:** Plotly (Python) for interactive visualizations with multiple dashboard tiles and standalone HTML files

## ✨ Pipeline Workflow 

1. **Data Ingestion:**
   - Batch processing with semi-automated workflow orchestration
   - Downloaded and preprocessed London bicycle data (Python)
   - Cleaned and standardized data (Python)
   - Uploaded data into GCS bucket
   - Loaded data into BigQuery

2. **Data Warehouse:**
   - Created optimized tables in BigQuery
   - Implemented date-based partitioning to improve query performance and reduce costs
   - Established table structure for both raw data and aggregated views
   - Tables are partitioned by `trip_date` to optimize performance for date-range queries, which are the most common in this analysis

3. **Data Transformation:**
   - Implemented **dbt models** with three layers:
     - **Staging**: clean and standardize raw data
     - **Intermediate**: create aggregated metrics
     - **Analytics**: business-ready output tables for dashboards
   - Created **station popularity** metrics using dbt transformations
   - Calculated **day-of-week** metrics by day of week and year with dbt transformations
   - Normalized data across different time periods with Python

4. **Dashboard Creation:**
   - Generated interactive dashboards for station popularity and day of week usage
   - Exported interactive HTML dashboards for easy viewing and sharing

## ✨ Dataset and Variable Descriptions 

### Station Popularity 
| Variable        | Description                                            | Data Type |
| --------------- | ------------------------------------------------------ | --------- |
| `station_id`    | Unique identifier for bicycle docking station          | Integer   |
| `station_name`  | Name and location of the station                       | String    |
| `total_starts`  | Number of trips that began at this station             | Integer   |
| `total_ends`    | Number of trips that ended at this station             | Integer   |
| `total_traffic` | Sum of starts and ends (overall usage)                 | Integer   |
| `net_flow`      | Difference between starts and ends (starts minus ends) | Integer   |
### Day of Week Usage
| Variable          | Description                                | Data Type |
|-------------------|--------------------------------------------|-----------|
| `year`            | Year of observation (2021-2024)            | Integer   |
| `day_of_week`     | Day of the week (Monday-Sunday)            | String    |
| `total_trips`     | Total number of bicycle trips              | Integer   |
| `num_days`        | Number of days sampled                     | Integer   |
| `avg_daily_trips` | Average daily trips (total_trips/num_days) | Float     |

## ✨ Dashboards and Insights
- Dashboards in html format available [here](https://github.com/wangjenn/london-cycling-analytics/tree/main/dashboards) 
### 🚴 Station Popularity
- Key Metrics: 
	1. **Total Traffic:** The sum of all trips starting and ending at each station
	2. **Start vs. End Imbalance (Net flow):** The difference between trips starting and ending at each station 

#### Top Stations by Total Traffic

![Top 20 Most Popular Stations](https://i.imgur.com/1dDylpf.png)
![](https://i.imgur.com/CakXXgO.png)
- **Preliminary Analysis**: 
	- The top stations by total traffic are predominantly located near major transit hubs, parks, and tourist attractions. *Hyde Park Corner, Waterloo Station*, and *The Borough* consistently rank among the busiest stations, suggesting these are key integration points with other transportation modes (e.g., subway stations). 

#### Station Net Flow Analysis
 - **Negative values**: more people **end** trips there (destinations) than **start** them (origins).
 - **Positive values**: more people **start** trips there (origins) than **end** them (destinations).
 - **Values close to zero** indicate balanced usage (people start and end trips in equal numbers). 
![Net Flow Analysis](https://i.imgur.com/2z3oVFg.png)

- **Preliminary Analysis:** 
	- **Destination Stations (Negative Net Flow):** Stations like *Hop Exchange* and *Liverpool Street Station* have significantly more trips ending than starting, indicating they are primarily **destinations** rather than origins.
	- **Origin Stations (Positive Net Flow):** Stations like *Hyde Park Corner* and *St. James's Park* have more trips **starting** than ending, suggesting they are popular starting points for trips (origins). 
	- **Balanced Stations:** Stations with net flow values close to zero have roughly equal numbers of trips starting and ending, indicating balanced usage patterns.

#### Top Origin and Destination Stations
- Using **net flows** to identify top origin stations and top destination stations.
![Top 5 Origin and Destination Stations](https://i.imgur.com/3MYVFQf.png)

- **Preliminary Analysis**: 
	- The stark contrast between origin and destination stations suggests distinct usage patterns tied to commuting behaviors, with **residential areas** serving as origins and **commercial** or **business districts** serving as destinations. 
	- This information is particularly valuable for bicycle rebalancing operations, as it highlights which stations require more attention and will likely need more bicycles added throughout the day.

### 🚴 Day of Week Usage Patterns
- Daily use patterns to provide insights into how bicycle usage varies throughout the week and how these patterns have changed from 2021 to 2024.
#### Daily and Weekly Usage Patterns by Year

![Daily Usage By Year](https://i.imgur.com/pMUgQHX.png)
![Weekly Pattern Analysis](https://i.imgur.com/uzd0bXC.png)

![Weekday vs. Weekend Ratio](https://p.ipic.vip/z02sy4.png)

**Preliminary Analysis**: 
- **Evolving Weekday-Weekend Patterns:** The relationship between weekday and weekend usage has changed significantly over the years, *consistent with lockdowns and return-to-office (RTO) policies*. 
    - In **2021** (immediate post-lockdown): lower overall usage with less pronounced weekday/weekend differences, though weekend usage (particularly Sunday) was relatively strong compared to weekdays. 
    - In **2022-2023**: steady growth in usage, with weekday usage became more dominant as commuting patterns and RTO policies resumed.
    - By **2024**: continuing growth with some normalization of weekday vs. weekend; balanced pattern emerged, though with weekdays still showing higher usage. 
- **Midweek Usage:** Tuesday through Thursday typically show higher usage in more recent years, aligning with common hybrid work patterns.
- **Year-over-Year Growth:** average daily trips show a steady increase from 2021 to 2024, indicating growing popularity of cycling in London post-pandemic.
- **Weekend Recovery:** weekend usage has grown alongside weekday usage, suggesting increasing recreational and leisure cycling.
- **Weekday vs. Weekend Ratio**: weekday vs. weekend ratio stabilized around 1.4-1.5 in recent years, suggests that on average, for every 10 trips on weekends, there are approximately 14-15 trips on weekdays. The trend indicates a gradual return to pre-pandemic commuting patterns while maintaining stronger weekend recreational usage

## ✨ Preliminary Key Findings and Recommendations

- Combined together, these preliminary analyses suggest the following recommendations for bicycle infrastructure planning and operations:
	1. **Rebalancing operations:** focus bicycle rebalancing efforts on the stations with extreme net flow values, particularly during peak commuting hours.
	2. **Station expansion:** consider adding capacity to the busiest stations identified in our traffic analysis, especially those that show consistent high usage.
	3. **New Station Locations:** the popularity of stations near major transit hubs suggests that future expansions should prioritize integration with the broader transportation network.
	4. **Weekend Service:** the growing weekend usage indicates a need for improved service levels on weekends, particularly around parks and recreational areas.
	5. **Weekday Capacity:** continue to maintain adequate capacity and service levels for Tuesday through Thursday, which continue to be the busiest days, consistent with hybrid company office policies. 

## ✨ Reproducibility

To reproduce this project, follow these steps:

- **1. Clone repository**
```bash
git clone https://github.com/wangjenn/london-bicycle-analysis.git
cd london-bicycle-analysis
pip install -r requirements.txt
```

- **2. Set up Google Cloud**
	- Create a Google account and signup for Google Cloud Platform
	- Create a New Project and take note of the project-id
	- Create a Service Account with the following IAM roles:
	  - Viewer
	  - Storage Admin
	  - Storage Object Admin
	  - BigQuery Admin
	- Create a new key for the service account, download as JSON, and store securely
	- Install the Google Cloud SDK
	- Authenticate using:
	  ```bash
	  gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
	  gcloud auth application-default login
	  ```
	- Close and restart your terminal
	- (Optional) Create a new virtual environment

- **3. Ingest data**
	- Download, ingest, and preprocess 2021-2024 data with Python
	- Refer to [data_ingestion.py](https://github.com/wangjenn/london-cycling-analytics/blob/main/scripts/data_ingestion.py) script

- **4. Transform data (dbt)**
	- Create all necessary aggregates and tables using dbt
	- Follow dbt's best practices (e.g., structured model hierarchy, clear model dependencies)
	- Refer to [models](https://github.com/wangjenn/london-cycling-analytics/tree/main/models) and [dbt_project.yml](https://github.com/wangjenn/london-cycling-analytics/blob/main/dbt_project.yml)

- **5. Analyze data and generate dashboards**
	- Analyze data with Python (pandas)
	- Create interactive dashboards using Plotly in Python
	- Refer to [station_popularity_dashboard.py](https://github.com/wangjenn/london-cycling-analytics/blob/main/scripts/station_popularity_dashboard.py) and [day_of_week_dashboard.py](https://github.com/wangjenn/london-cycling-analytics/blob/main/scripts/day_of_week_dashboard.py)

---

- *Thanks for taking the time to read through and review this project! 💕*
