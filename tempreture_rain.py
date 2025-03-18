import json
import matplotlib.pyplot as plt
import os
import shutil
from collections import defaultdict
from datetime import datetime
import calendar

# Function to load data from a JSON file
def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Function to process the data and calculate the total rain_sum, and average temperature_mean per year and month
def calculate_temperature_rainfall_per_year_and_month(data):
    temperature_rainfall_per_year_month = defaultdict(lambda: defaultdict(list))

    for entry in data:
        date = entry.get('date', '')
        temperature_mean = entry.get('weather', {}).get('temperature_mean', 0)
        rain_sum = entry.get('weather', {}).get('rain_sum', 0)

        # Extract year and month from the date
        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month
            temperature_rainfall_per_year_month[year][month].append((temperature_mean, rain_sum))
        except ValueError:
            continue  # Skip invalid date entries

    # Calculate the total rain_sum, and average temperature_mean for each month of each year
    total_temperature_rainfall = defaultdict(lambda: defaultdict(dict))
    for year, months in temperature_rainfall_per_year_month.items():
        for month, values in months.items():
            total_rain_sum = sum(rain_sum for _, rain_sum in values)  # Total rain sum
            avg_temperature_mean = sum(temperature_mean for temperature_mean, _ in values) / len(values)
            
            total_temperature_rainfall[year][month]['total_rain_sum'] = total_rain_sum
            total_temperature_rainfall[year][month]['avg_temperature_mean'] = avg_temperature_mean

    return total_temperature_rainfall

# Function to create the 'temperature_rainfall_graphs' folder (delete if exists)
def create_temperature_rainfall_graph_folder():
    folder_path = 'temperature_rainfall_graphs'
    
    # If the folder exists, delete it and recreate it
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    # Create a new folder to store graphs
    os.makedirs(folder_path)
    return folder_path

# Function to plot and save the total rainfall and average temperature_mean for each month in a year
def plot_and_save_temperature_rainfall(total_temperature_rainfall, folder_path):
    for year, months in total_temperature_rainfall.items():
        # Prepare the data for the plot
        months_list = []
        avg_temperature_mean_list = []
        total_rain_sum_list = []

        # Get the short name of the months (Jan, Feb, Mar, etc.) and temperature and rainfall data
        for month in range(1, 13):
            months_list.append(calendar.month_abbr[month])  # Short name of the month
            avg_temperature_mean_list.append(months.get(month, {}).get('avg_temperature_mean', 0))
            total_rain_sum_list.append(months.get(month, {}).get('total_rain_sum', 0))

        # Create a new figure for the year
        fig, ax1 = plt.subplots(figsize=(10, 6))
        bar_width = 0.35  # Set the width of the bars
        index = range(len(months_list))

        # Plot the bars for total rainfall (total_rain_sum)
        ax1.bar(index, total_rain_sum_list, bar_width, label='Total Rainfall (mm)', color='blue', alpha=0.6)
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Total Rainfall (mm)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.set_xticks([i for i in index])
        ax1.set_xticklabels(months_list)

        # Create a secondary y-axis to plot the temperature_mean
        ax2 = ax1.twinx()
        ax2.plot(index, avg_temperature_mean_list, label='Average Temperature (°C)', color='red', marker='o', linestyle='-', linewidth=2)
        ax2.set_ylabel('Temperature (°C)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Title and legend
        plt.title(f'Total Rainfall and Average Temperature in {year}')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Save the figure as a PNG file
        graph_filename = f"{folder_path}/temperature_rainfall_{year}.png"
        plt.savefig(graph_filename)
        plt.close()  # Close the plot to avoid memory issues

# Main function
def main():
    # Load data (replace 'data.json' with your file path)
    data = load_json_data('bar_line\\merged_data.json')

    # Calculate total rain_sum, and average temperature_mean per year and month
    total_temperature_rainfall = calculate_temperature_rainfall_per_year_and_month(data)

    # Create the 'temperature_rainfall_graphs' folder
    folder_path = create_temperature_rainfall_graph_folder()

    # Generate and save temperature and rainfall graphs for each year
    plot_and_save_temperature_rainfall(total_temperature_rainfall, folder_path)

    print(f"Temperature and rainfall graphs saved in '{folder_path}'")

if __name__ == "__main__":
    main()
