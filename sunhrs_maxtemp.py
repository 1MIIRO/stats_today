import json
import os
import matplotlib.pyplot as plt
import calendar
from collections import defaultdict
from datetime import datetime
import shutil

# Load data from JSON file
def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Create folder if not exists, or delete and recreate if it exists
def create_folder(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)  # Delete the existing folder and its contents
    os.makedirs(folder_name)  # Create a new folder

# Load data and create folder
data = load_json_data('bar_line\\merged_data.json')  # Replace with your actual file path
create_folder('graphs_sunshine_temperature')  # Folder to store this specific plot

# Process data to get sunshine hours and temperature max
def calculate_sunshine_temperature(data):
    monthly_data = defaultdict(lambda: defaultdict(list))

    def get_sunshine_duration(sunshine_seconds):
        return sunshine_seconds / 3600

    for entry in data:
        date = entry.get('date', '')
        sunshine_seconds = entry.get('weather', {}).get('sunshine_hours', 0)
        temperature_max = entry.get('weather', {}).get('temperature_max', 0)

        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month
            monthly_data[year][month].append({
                'sunshine_hours': get_sunshine_duration(sunshine_seconds),
                'temperature_max': temperature_max,
            })
        except ValueError:
            continue  # Skip invalid date entries

    year_month_averages = defaultdict(lambda: defaultdict(dict))
    for year, months in monthly_data.items():
        for month, values in months.items():
            avg_sunshine_hours = sum(entry['sunshine_hours'] for entry in values) / len(values)
            avg_temperature_max = sum(entry['temperature_max'] for entry in values) / len(values)
            year_month_averages[year][month] = {
                'avg_sunshine_hours': avg_sunshine_hours,
                'avg_temperature_max': avg_temperature_max,
            }

    return year_month_averages

# Plot the graph
def plot_sunshine_temperature(year_month_averages):
    for year, months in year_month_averages.items():
        months_list = [calendar.month_abbr[i] for i in range(1, 13)]
        avg_sunshine_hours_list = [months.get(i, {}).get('avg_sunshine_hours', 0) for i in range(1, 13)]
        avg_temperature_max_list = [months.get(i, {}).get('avg_temperature_max', 0) for i in range(1, 13)]

        fig, ax1 = plt.subplots(figsize=(10, 6))

        ax2 = ax1.twinx()
        ax2.plot(months_list, avg_sunshine_hours_list, label='Sunshine Hours', color='orange', marker='o', linestyle='-', linewidth=2)
        ax2.set_ylabel('Sunshine Hours (h)', color='orange')
        ax2.tick_params(axis='y', labelcolor='orange')

        ax1.bar(months_list, avg_temperature_max_list, label='Max Temperature (°C)', color='purple', alpha=0.6)
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Max Temperature (°C)', color='purple')
        ax1.tick_params(axis='y', labelcolor='purple')

        plt.title(f'Sunshine Hours & Max Temperature in {year}')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        plt.savefig(f'graphs_sunshine_temperature/sunshine_temperature_{year}.png')
        plt.close()

# Calculate and plot
year_month_averages = calculate_sunshine_temperature(data)
plot_sunshine_temperature(year_month_averages)
