from pathlib import Path
import csv
from datetime import datetime

import matplotlib.pyplot as plt

dataFileNames = ["data/sitka_weather_07-2018_simple.csv", "data/death_valley_2018_simple.csv"]

place_names = []

# Create a figure and a grid of 1 row and 2 columns
fig, axes = plt.subplots(2, 1, figsize=(12, 6))  # Adjust the figsize for better visualization

# Loop through the data files and corresponding axes
for dataFile, ax in zip(dataFileNames, axes):
    path = Path(dataFile)
    lines = path.read_text().splitlines()

    reader = csv.reader(lines)
    header_row = next(reader)

    date_index = header_row.index('DATE')
    high_index = header_row.index('TMAX')
    low_index = header_row.index('TMIN')
    name_index = header_row.index('NAME')

    # Extract dates, and high and low temperatures.
    dates, highs, lows = [], [], []
    place_name = ""
    for row in reader:
        # Grab the station name, if it's not already set.
        if not place_name:
            place_name = row[name_index]
            place_names.append(row[name_index])

        current_date = datetime.strptime(row[date_index], '%Y-%m-%d')
        try:
            high = int(row[high_index])
            low = int(row[low_index])
        except ValueError:
            print(f"Missing data for {current_date}")
        else:
            dates.append(current_date)
            highs.append(high)
            lows.append(low)

    # Plot the high and low temperatures.
    plt.style.use('seaborn-v0_8')
    # Plot the data for each location on its corresponding subplot
    ax.plot(dates, highs, color='red', alpha=0.5, label='Highs')
    ax.plot(dates, lows, color='blue', alpha=0.5, label='Lows')
    ax.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)

    # Set common labels and title
    ax.set_title(place_name, fontsize=12)
    ax.set_ylabel("Temperature (F)", fontsize=10)
    ax.legend(fontsize=8)
    ax.tick_params(labelsize=8)

# Adjust the layout and display the plot
fig.suptitle(f"Temperature comparison between {place_names[0]} and {place_names[1]}", fontsize=14)
plt.tight_layout()
plt.show()