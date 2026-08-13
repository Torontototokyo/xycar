# Work Card Analysis Project

This project analyzes vehicle permit and parking data from a SaaS parking management platform.

## Project Overview

**Purpose:** Extract, process, and analyze vehicle exit/entry records and permit information from a parking management system.

**Data Flow:**
1. **web.py** - Web scraping using Selenium to login and collect data from the parking platform (登录/login to yun.jslife.com.cn)
2. **download.py** - HTTP utilities for downloading or fetching data
3. **gather.py** - ETL pipeline that reads Excel exports, connects to MySQL database, and stores processed data
4. **main.py** / **main2.py** - Data analysis functions for calculating permit hours, validating date ranges, and generating reports

## Key Conventions

### Data & Chinese Columns
The project works with Chinese-named columns in Excel exports:
- `车牌号码` - License plate number
- `开始期限` - Start date
- `截止期限` - End date
- `占用时长` - Duration occupied
- `车辆出场记录` - Vehicle exit records

### Date & Hour Calculations
- **HOUR_PER_MONTH = 360** - Standard monthly hour allocation for permits
- Calculations often distinguish between "full months" (30+ days remaining) and partial months
- `get_hours_by_dates()` computes remaining hours based on permit end date vs today
- `get_start_counting_date_arr()` generates monthly billing periods, max 6 months (platform export limit)

### Excel File Handling
- Input format: `.xlsx` files with unnamed columns (e.g., "Unnamed: 15" renamed to "占用时长")
- Output: `save_excel()` exports dataframes without index
- Common files: `车辆出场记录_[timestamp].xlsx`

### Database Setup
- **Engine:** MySQL via SQLAlchemy + pymysql
- **Credentials in gather.py:** User='root', Password='root', Host='localhost', DB='cars_db'
- **Connection pattern:** `init_engine()` creates reusable SQLAlchemy engine with connection pooling

## Common Tasks

### Data Validation
- Verify start/end dates are consistent (end - start = 1 day)
- Check for missing date fields in rows
- Use `confirm_start_date_end_date()` for validation

### Filtering & Extraction
- Filter records by license plate (e.g., `df[df['车牌号码'] == 'PLATE_ID']`)
- Export filtered subsets to new Excel files for analysis

### Calculations
- **Remaining hours:** Use `get_hours_by_dates()` to calculate hours left on a permit
- **Billing periods:** Use `get_start_counting_date_arr()` to break permit period into monthly chunks
- Handle edge cases where data older than 6 months must be excluded

## Dependencies

```
pandas           - Data manipulation
sqlalchemy       - ORM and database connection
pymysql          - MySQL driver
selenium         - Web automation
paddleocr        - OCR for character recognition
requests         - HTTP requests
dateutil         - Date arithmetic
```

## Setup

1. Ensure MySQL is running with database `cars_db`
2. Configure database credentials in `gather.py` (currently hardcoded)
3. Install Python dependencies
4. For web scraping: Ensure Chrome/Chromium is installed for Selenium

## Common Pitfalls

- **Date parsing:** Always use `'%Y-%m-%d'` format explicitly with `strptime()`
- **Excel unnamed columns:** Check for "Unnamed: X" patterns after reading
- **6-month limitation:** Exit records can only export 6 months; older periods need separate queries
- **Time zones:** No explicit timezone handling; assumes local/server time

## When Working on Analysis

- Check if you're modifying/filtering existing DataFrames or creating new analysis
- Validate date ranges before calculations
- Use `HOUR_PER_MONTH` constant for consistency
- Output results to `.xlsx` for verification before loading to database
