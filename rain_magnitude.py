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

# Function to process the data and calculate the total rain_sum and magnitude per year and month
def calculate_rain_and_magnitude_per_year_and_month(data):
    rain_and_magnitude_per_year_month = defaultdict(lambda: defaultdict(list))

    for entry in data:
        date = entry.get('date', '')
        rain_sum = entry.get('weather', {}).get('rain_sum', 0)
        magnitude = entry.get('magnitude', 0)

        # Extract year and month from the date
        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month
            rain_and_magnitude_per_year_month[year][month].append((rain_sum, magnitude))
        except ValueError:
            continue  # Skip invalid date entries

    # Calculate the total rain_sum and magnitude for each month of each year
    total_rain_and_magnitude = defaultdict(lambda: defaultdict(dict))
    for year, months in rain_and_magnitude_per_year_month.items():
        for month, values in months.items():
            total_rain_sum = sum(rain_sum for rain_sum, _ in values)
            average_magnitude = sum(magnitude for _, magnitude in values) / len(values)
            total_rain_and_magnitude[year][month]['total_rain_sum'] = total_rain_sum
            total_rain_and_magnitude[year][month]['average_magnitude'] = average_magnitude

    return total_rain_and_magnitude

# Function to create the 'rain_magnitude_graphs' folder (delete if exists)
def create_rain_magnitude_graph_folder():
    folder_path = 'rain_magnitude_graphs'
    
    # If the folder exists, delete it and recreate it
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    # Create a new folder to store graphs
    os.makedirs(folder_path)
    return folder_path

# Function to plot the total rain_sum and average magnitude for all 12 months in one graph for each year
def plot_and_save_rain_magnitude(total_rain_and_magnitude, folder_path):
    for year, months in total_rain_and_magnitude.items():
        # Prepare the data for the plot
        months_list = []
        total_rain_sum_list = []
        average_magnitude_list = []

        # Get the short name of the months (Jan, Feb, Mar, etc.) and rain and magnitude data
        for month in range(1, 13):
            months_list.append(calendar.month_abbr[month])  # Short name of the month
            total_rain_sum_list.append(months.get(month, {}).get('total_rain_sum', 0))
            average_magnitude_list.append(months.get(month, {}).get('average_magnitude', 0))

        # Create a new figure for the year
        fig, ax1 = plt.subplots(figsize=(10, 6))
        bar_width = 0.35  # Set the width of the bars
        index = range(len(months_list))

        # Plot the bars for total rain sum
        ax1.bar(index, total_rain_sum_list, bar_width, label='Total Rain Sum (mm)', color='blue')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Total Rain Sum (mm)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.set_xticks([i for i in index])
        ax1.set_xticklabels(months_list)

        # Create a secondary y-axis to plot the magnitude
        ax2 = ax1.twinx()
        ax2.plot(index, average_magnitude_list, label='Average Magnitude', color='red', marker='o', linestyle='-', linewidth=2)
        ax2.set_ylabel('Average Magnitude', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Set the y-axis range for magnitude from 0 to 8
        ax2.set_ylim(0, 8)

        # Title and legend
        plt.title(f'Total Rain Sum and Average Magnitude in {year}')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Save the figure as a PNG file
        graph_filename = f"{folder_path}/rain_magnitude_{year}.png"
        plt.savefig(graph_filename)
        plt.close()  # Close the plot to avoid memory issues

# Main function
def main():
    # Load data (replace 'data.json' with your file path)
    data = load_json_data('bar_line\\merged_data.json')

    # Calculate total rain_sum and average magnitude per year and month
    total_rain_and_magnitude = calculate_rain_and_magnitude_per_year_and_month(data)

    # Create the 'rain_magnitude_graphs' folder
    folder_path = create_rain_magnitude_graph_folder()

    # Generate and save rain sum and magnitude graphs for each year
    plot_and_save_rain_magnitude(total_rain_and_magnitude, folder_path)

    print(f"Rain sum and magnitude graphs saved in '{folder_path}'")

if __name__ == "__main__":
    main()
