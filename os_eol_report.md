# OS End of Life Device Report

## Summary Report

### Total Devices Analyzed
- Total Devices: 23

### Device Breakdown by Type
- iPad: 21 devices (91.3%)
- iPhone: 1 device (4.3%)
- Other: 1 device (4.3%)

### Device Support Status
- Active Devices: 17 (73.9%)
- End of Support Devices: 6 (26.1%)

### Newly Added Devices (Through March 2025)
1. iPad Pro (M4, 11"/13")
2. iPad Air (M2, 11"/13")
3. iPad (11th generation)
4. iPad Mini (7th generation)

### Key Insights about Discontinued Devices
- Earliest End of Support: iPad Mini 4 (2021-09-13)
- Most Recent End of Support: iPad (6th generation) (2024-10-01)
- 10 devices marked as "Discontinued BUT supported"

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
     REGEXMATCH(E2, "\d{4}-\d{2}-\d{2}"),
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
     REGEXMATCH(E2, "\d{4}-\d{2}-\d{2}"),
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
       REGEXMATCH(E2, "\d{4}-\d{2}-\d{2}"),
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
       REGEXMATCH(E2, "\d{4}-\d{2}-\d{2}"),
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

Note: This report was generated on 2025-04-07 based on the provided data.
