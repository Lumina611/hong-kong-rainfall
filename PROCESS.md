# Process

## Tools

I used Python, `requests`, CSV reading from Python's standard library,
Matplotlib, VS Code, GitHub, and Copilot. I used the Hong Kong Observatory
website and DATA.GOV.HK to find and check a real public data source. Git was
used to keep the project files organised.

## Kept

I kept the suggestion to make a blue daily rainfall bar chart. It is simple to
read: bar height shows the rainfall amount, and the date axis shows when it
happened. I also kept the suggestion to save the original server response
unchanged in `data/`, because this makes the source data easy to inspect.
Copilot helped me replace the temperature example, write the small CSV-reading
function, handle missing values, and create the chart.

## Rejected

I rejected the template's suggestion to use daily mean temperature and an
orange line chart, because this assignment is about rainfall. I also did not
use every historical day in one chart: that would make the date labels
unreadable, so the chart uses one complete year while leaving the original
file unchanged.

## Checks and corrections

The template used a temperature API, temperature column positions, a
temperature filename, and `out/plot.png`. I corrected these to the official
Hong Kong Observatory rainfall CSV, whose actual columns are year, month, day,
value, and data completeness, and changed the output to `out/rainfall.png`.
The code skips the CSV headings and explanatory notes, converts dates and
rainfall text to numbers, and explicitly counts missing `***` values instead
of silently treating them as zero. It also counts the Observatory's `Trace`
values separately because they mean less than 0.05 mm, not an exact number.
I checked the raw downloaded data and use that real data in the image.
