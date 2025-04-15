import json
import pandas as pd
from datetime import datetime
import re

# Load the JSON data
with open('filtered_device_eol_data.json', 'r') as f:
    device_data = json.load(f)

# Load the CSV data
csv_data = pd.read_csv('os_eol_data.csv')

# Current date for reference
current_date = datetime.now()

# Extract devices from JSON
devices = device_data['filtered_devices']
total_devices = len(devices)

# Analyze device types
device_types = {}
for device in devices:
    category = device.get('category', 'Uncategorized')
    if category in device_types:
        device_types[category] += 1
    else:
        device_types[category] = 1

# Analyze support status
active_devices = sum(1 for device in devices if device.get('status') == 'Active')
eol_devices = total_devices - active_devices

# Get newly added devices
newly_added = [device['device_name'] for device in devices if device.get('newly_added', False)]

# Find earliest and latest end of support dates from CSV for more accurate dates
eol_dates = []
for _, row in csv_data.iterrows():
    eol_date = row['End of Support Date']
    if eol_date and eol_date not in ['Current', 'Discontinued BUT supported', '(current)', '4 years from release date']:
        if re.match(r'\d{4}-\d{2}-\d{2}', eol_date):
            try:
                date_obj = datetime.strptime(eol_date, '%Y-%m-%d')
                eol_dates.append((row['Device Name'], eol_date, date_obj))
            except:
                pass

# Sort by date
if eol_dates:
    eol_dates.sort(key=lambda x: x[2])
    earliest = eol_dates[0]
    latest = eol_dates[-1]
else:
    earliest = None
    latest = None

# Generate the report content
report = f"""# OS End of Life Device Report

## Summary Report

### Total Devices Analyzed
- Total Devices: {total_devices}

### Device Breakdown by Type
"""

for device_type, count in device_types.items():
    percentage = (count / total_devices) * 100
    report += f"- {device_type}: {count} device{'s' if count > 1 else ''} ({percentage:.1f}%)\n"

report += f"""
### Device Support Status
- Active Devices: {active_devices} ({(active_devices / total_devices) * 100:.1f}%)
- End of Support Devices: {eol_devices} ({(eol_devices / total_devices) * 100:.1f}%)

### Newly Added Devices (Through March 2025)
"""

for i, device in enumerate(newly_added, 1):
    report += f"{i}. {device}\n"

report += """
### Key Insights about Discontinued Devices
"""

if earliest and latest:
    report += f"- Earliest End of Support: {earliest[0]} ({earliest[1]})\n"
    report += f"- Most Recent End of Support: {latest[0]} ({latest[1]})\n"

# Count devices with "Discontinued BUT supported" status
discontinued_but_supported = sum(1 for _, row in csv_data.iterrows() if row['End of Support Date'] == 'Discontinued BUT supported')
report += f"- {discontinued_but_supported} devices marked as \"Discontinued BUT supported\"\n"

report += """
### Notable Patterns and Trends
- Most iPads have transitioned through multiple iOS/iPadOS versions
- Newer devices (released 2022-2024) remain actively supported
- Devices from 2015-2018 have mostly reached end of support
- Latest devices run iPadOS 17 or 18

## Google Sheets Import and Management Instructions

### Importing CSV File
1. Open Google Sheets
2. Click "File" > "Import"
3. Select "Upload" tab
4. Choose the os_eol_data.csv file
5. Select "Replace spreadsheet" option
6. Click "Import data"

### Conditional Formatting Rules

To highlight devices approaching end of support (within 6 months):
1. Select all data (Ctrl+A)
2. Click "Format" > "Conditional formatting"
3. Choose "Custom formula is" and enter:
   ```
   =AND(
     NOT(ISBLANK(E2)),
     NOT(REGEXMATCH(E2, "Current|Discontinued BUT supported")),
     REGEXMATCH(E2, "\\d{4}-\\d{2}-\\d{2}"),
     DATEVALUE(E2) > TODAY(),
     DATEVALUE(E2) - TODAY() <= 180
   )
   ```
4. Set formatting style to yellow background
5. Click "Done"

To highlight devices that have reached end of support:
1. Click "Format" > "Conditional formatting"
2. Choose "Custom formula is" and enter:
   ```
   =AND(
     NOT(ISBLANK(E2)),
     NOT(REGEXMATCH(E2, "Current|Discontinued BUT supported")),
     REGEXMATCH(E2, "\\d{4}-\\d{2}-\\d{2}"),
     DATEVALUE(E2) <= TODAY()
   )
   ```
3. Set formatting style to red background
4. Click "Done"

To highlight newly added devices:
1. Click "Format" > "Conditional formatting"
2. Choose "Custom formula is" and enter:
   ```
   =G2="Yes"
   ```
3. Set formatting style to green background
4. Click "Done"

### Auto-Sorting and Filtering Options

To set up auto-sorting:
1. Select all data including headers
2. Click "Data" > "Create a filter"
3. Use the filter buttons in the header row to sort or filter data

Recommended filters:
- Filter by "Status" to see only active or end-of-support devices
- Filter by "Device Type" to focus on specific device categories
- Sort by "End of Support Date" to prioritize devices nearing end of support

### Keeping the Sheet Updated

To make the sheet self-updating:
1. Add a new column called "Days Until EOL"
2. In the first data cell of this column, enter the formula:
   ```
   =IF(
     OR(ISBLANK(E2), REGEXMATCH(E2, "Current|Discontinued BUT supported")),
     "N/A",
     IF(
       REGEXMATCH(E2, "\\d{4}-\\d{2}-\\d{2}"),
       DATEVALUE(E2) - TODAY(),
       "Date format error"
     )
   )
   ```
3. Add another column called "Support Status (Auto)"
4. In the first data cell of this column, enter the formula:
   ```
   =IF(
     OR(ISBLANK(E2), REGEXMATCH(E2, "Current|Discontinued BUT supported")),
     "Active",
     IF(
       REGEXMATCH(E2, "\\d{4}-\\d{2}-\\d{2}"),
       IF(DATEVALUE(E2) <= TODAY(), "End of Support", "Active"),
       "Check manually"
     )
   )
   ```
5. Copy these formulas down to all rows

For periodic updates:
1. Create a new sheet for each update
2. Import the latest CSV data
3. Compare with previous versions to identify changes
4. Update the "Newly Added" column manually for new devices

Note: This report was generated on {current_date.strftime('%Y-%m-%d')} based on the provided data.
"""

# Print a summary to the console
print("OS End of Life Device Report Summary:")
print(f"- Total devices analyzed: {total_devices}")
print(f"- Active devices: {active_devices}")
print(f"- End of support devices: {eol_devices}")
print(f"- Newly added devices: {len(newly_added)}")
print("Report generated successfully!")

# Save the report to a markdown file
with open('os_eol_report.md', 'w') as f:
    f.write(report)

print("Report saved to os_eol_report.md")