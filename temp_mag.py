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

# Function to process the data and calculate the average temperature_mean and magnitude per year and month
def calculate_temperature_and_magnitude_per_year_and_month(data):
    temperature_and_magnitude_per_year_month = defaultdict(lambda: defaultdict(list))

    for entry in data:
        date = entry.get('date', '')
        temperature_mean = entry.get('weather', {}).get('temperature_mean', 0)
        magnitude = entry.get('magnitude', 0)

        # Extract year and month from the date
        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month
            temperature_and_magnitude_per_year_month[year][month].append((temperature_mean, magnitude))
        except ValueError:
            continue  # Skip invalid date entries

    # Calculate the average temperature_mean and magnitude for each month of each year
    average_temperature_and_magnitude = defaultdict(lambda: defaultdict(dict))
    for year, months in temperature_and_magnitude_per_year_month.items():
        for month, values in months.items():
            avg_temperature_mean = sum(temperature_mean for temperature_mean, _ in values) / len(values)
            avg_magnitude = sum(magnitude for _, magnitude in values) / len(values)
            average_temperature_and_magnitude[year][month]['avg_temperature_mean'] = avg_temperature_mean
            average_temperature_and_magnitude[year][month]['avg_magnitude'] = avg_magnitude

    return average_temperature_and_magnitude

# Function to create the 'temperature_magnitude_graphs' folder (delete if exists)
def create_temperature_magnitude_graph_folder():
    folder_path = 'temperature_magnitude_graphs'
    
    # If the folder exists, delete it and recreate it
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    # Create a new folder to store graphs
    os.makedirs(folder_path)
    return folder_path

# Function to plot the average temperature_mean and magnitude for all 12 months in one graph for each year
def plot_and_save_temperature_magnitude(average_temperature_and_magnitude, folder_path):
    for year, months in average_temperature_and_magnitude.items():
        # Prepare the data for the plot
        months_list = []
        avg_temperature_mean_list = []
        avg_magnitude_list = []

        # Get the short name of the months (Jan, Feb, Mar, etc.) and temperature and magnitude data
        for month in range(1, 13):
            months_list.append(calendar.month_abbr[month])  # Short name of the month
            avg_temperature_mean_list.append(months.get(month, {}).get('avg_temperature_mean', 0))
            avg_magnitude_list.append(months.get(month, {}).get('avg_magnitude', 0))

        # Create a new figure for the year
        fig, ax1 = plt.subplots(figsize=(10, 6))
        bar_width = 0.35  # Set the width of the bars
        index = range(len(months_list))

        # Plot the bars for average temperature
        ax1.bar(index, avg_temperature_mean_list, bar_width, label='Average Temperature (°C)', color='blue')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Average Temperature (°C)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.set_xticks([i for i in index])
        ax1.set_xticklabels(months_list)

        # Create a secondary y-axis to plot the magnitude
        ax2 = ax1.twinx()
        ax2.plot(index, avg_magnitude_list, label='Average Magnitude', color='red', marker='o', linestyle='-', linewidth=2)
        ax2.set_ylabel('Average Magnitude', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Title and legend
        plt.title(f'Average Temperature and Magnitude in {year}')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Save the figure as a PNG file
        graph_filename = f"{folder_path}/temperature_magnitude_{year}.png"
        plt.savefig(graph_filename)
        plt.close()  # Close the plot to avoid memory issues

# Main function
def main():
    # Load data (replace 'data.json' with your file path)
    data = load_json_data('bar_line\\merged_data.json')

    # Calculate average temperature_mean and magnitude per year and month
    average_temperature_and_magnitude = calculate_temperature_and_magnitude_per_year_and_month(data)

    # Create the 'temperature_magnitude_graphs' folder
    folder_path = create_temperature_magnitude_graph_folder()

    # Generate and save temperature and magnitude graphs for each year
    plot_and_save_temperature_magnitude(average_temperature_and_magnitude, folder_path)

    print(f"Temperature and magnitude graphs saved in '{folder_path}'")

if __name__ == "__main__":
    main()
