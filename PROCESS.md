# Process

## Tools

I used Python, `requests`, CSV reading from Python's standard library,
Matplotlib, VS Code, GitHub, and Copilot. I used the Hong Kong Observatory
website and DATA.GOV.HK to find and check a real public data source. Git was
used to keep the project files organised.

## Kept

I kept the suggestion to make a blue daily rainfall chart and kept the original
bar chart as an initial version. I added a calendar because it makes seasonal
patterns easier to compare: each day has a clear place in its month, and colour
intensity shows rainfall. I also kept the suggestion to save the original
server response unchanged in `data/`, because this makes the source data easy
to inspect. Copilot helped me write the calendar layout, add the colour legend
and weekday labels, mark the three wettest days, and handle missing values.

## Rejected

I rejected the template's suggestion to use daily mean temperature and an
orange line chart, because this assignment is about rainfall. I also rejected
the idea of inventing numbers for `Trace` values: the Observatory says they
mean less than 0.05 mm, so the code does not pretend they are exact values.
The calendar uses one complete year instead of every historical day, keeping
the dates readable while leaving the original file unchanged.

## Checks and corrections

The template used a temperature API, temperature column positions, a
temperature filename, and `out/plot.png`. I corrected these to the official
Hong Kong Observatory rainfall CSV, whose actual columns are year, month, day,
value, and changed the initial bar-chart output to `out/plot.png`.
The code skips the CSV headings and explanatory notes, converts dates and
rainfall text to numbers, and explicitly counts missing `***` values instead
of silently treating them as zero. It also counts the Observatory's `Trace`
values separately because they mean less than 0.05 mm, not an exact number.
I checked the raw downloaded data and use that real data in both images. I also checked that the original bar-chart
output remains available as `out/plot.png` and that the new calendar is
`out/rainfall-calendar.png`.
