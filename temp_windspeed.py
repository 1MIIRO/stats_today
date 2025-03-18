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
create_folder('graphs_temp_wind_speed')  # Folder to store this specific plot

# Process data to get monthly temperature and wind speed
def calculate_temperature_wind_speed(data):
    monthly_data = defaultdict(lambda: defaultdict(list))

    for entry in data:
        date = entry.get('date', '')
        temperature_mean = entry.get('weather', {}).get('temperature_mean', 0)
        wind_speed = entry.get('weather', {}).get('wind_speed_max', 0)

        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month
            monthly_data[year][month].append({
                'temperature_mean': temperature_mean,
                'wind_speed': wind_speed,
            })
        except ValueError:
            continue  # Skip invalid date entries

    year_month_averages = defaultdict(lambda: defaultdict(dict))
    for year, months in monthly_data.items():
        for month, values in months.items():
            avg_temperature_mean = sum(entry['temperature_mean'] for entry in values) / len(values)
            avg_wind_speed = sum(entry['wind_speed'] for entry in values) / len(values)
            year_month_averages[year][month] = {
                'avg_temperature_mean': avg_temperature_mean,
                'avg_wind_speed': avg_wind_speed,
            }

    return year_month_averages

# Plot the graph
def plot_temperature_wind_speed(year_month_averages):
    for year, months in year_month_averages.items():
        months_list = [calendar.month_abbr[i] for i in range(1, 13)]
        avg_temperature_mean_list = [months.get(i, {}).get('avg_temperature_mean', 0) for i in range(1, 13)]
        avg_wind_speed_list = [months.get(i, {}).get('avg_wind_speed', 0) for i in range(1, 13)]

        fig, ax1 = plt.subplots(figsize=(10, 6))

        ax2 = ax1.twinx()
        ax2.plot(months_list, avg_temperature_mean_list, label='Average Temperature (°C)', color='red', marker='o', linestyle='-', linewidth=2)
        ax2.set_ylabel('Temperature (°C)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        ax1.bar(months_list, avg_wind_speed_list, label='Avg Wind Speed (km/h)', color='blue', alpha=0.6)
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Avg Wind Speed (km/h)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        plt.title(f'Average Temperature & Wind Speed in {year}')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        plt.savefig(f'graphs_temp_wind_speed/temp_wind_speed_{year}.png')
        plt.close()

# Calculate and plot
year_month_averages = calculate_temperature_wind_speed(data)
plot_temperature_wind_speed(year_month_averages)
