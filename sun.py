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

# Function to convert sunshine_seconds to hours
def get_sunshine_duration(sunshine_seconds):
    return float(sunshine_seconds) / 3600  # Convert seconds to hours

# Function to process the data and calculate the highest and lowest sunshine hours per year and month
def calculate_highest_lowest_sunshine_per_year_and_month(data):
    sunshine_per_year_month = defaultdict(lambda: defaultdict(list))

    for entry in data:
        date = entry.get('date', '')
        sunshine_seconds = entry.get('weather', {}).get('sunshine_hours', 0)

        # Convert sunshine hours from seconds to hours
        sunshine_hours = get_sunshine_duration(sunshine_seconds)

        # Extract year and month from the date
        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month
            sunshine_per_year_month[year][month].append(sunshine_hours)
        except ValueError:
            continue  # Skip invalid date entries

    # Calculate the highest and lowest sunshine hours for each month of each year
    highest_lowest_sunshine = defaultdict(lambda: defaultdict(dict))
    for year, months in sunshine_per_year_month.items():
        for month, sunshine_hours in months.items():
            highest_lowest_sunshine[year][month]['max_sunshine'] = max(sunshine_hours)
            highest_lowest_sunshine[year][month]['min_sunshine'] = min(sunshine_hours)

    return highest_lowest_sunshine

# Function to create the 'sunshine_graphs' folder (delete if exists)
def create_sunshine_graph_folder():
    folder_path = 'sunshine_graphs'
    
    # If the folder exists, delete it and recreate it
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    # Create a new folder to store graphs
    os.makedirs(folder_path)
    return folder_path

# Function to plot the highest and lowest sunshine hours for all 12 months in one graph for each year
def plot_and_save_sunshine(highest_lowest_sunshine, folder_path):
    for year, months in highest_lowest_sunshine.items():
        # Prepare the data for the plot
        months_list = []
        max_sunshine_list = []
        min_sunshine_list = []

        # Get the short name of the months (Jan, Feb, Mar, etc.) and sunshine data
        for month in range(1, 13):
            months_list.append(calendar.month_abbr[month])  # Short name of the month
            max_sunshine_list.append(months.get(month, {}).get('max_sunshine', 0))
            min_sunshine_list.append(months.get(month, {}).get('min_sunshine', 0))

        # Create a new figure for the year
        plt.figure(figsize=(10, 6))
        bar_width = 0.35  # Set the width of the bars
        index = range(len(months_list))

        # Plot the bars for max sunshine hours and min sunshine hours
        plt.bar(index, max_sunshine_list, bar_width, label='Max Sunshine Hours', color='orange')
        plt.bar([i + bar_width for i in index], min_sunshine_list, bar_width, label='Min Sunshine Hours', color='blue')

        plt.xlabel('Month')
        plt.ylabel('Sunshine Hours (hrs)')
        plt.title(f'Highest and Lowest Sunshine Hours in {year}')
        plt.xticks([i + bar_width / 2 for i in index], months_list)  # Center the ticks between the bars
        plt.legend()

        # Save the figure as a PNG file
        graph_filename = f"{folder_path}/sunshine_{year}.png"
        plt.savefig(graph_filename)
        plt.close()  # Close the plot to avoid memory issues

# Main function
def main():
    # Load data (replace 'data.json' with your file path)
    data = load_json_data('bar_graphs\\merged_data.json')

    # Calculate highest and lowest sunshine hours per year and month
    highest_lowest_sunshine = calculate_highest_lowest_sunshine_per_year_and_month(data)

    # Create the 'sunshine_graphs' folder
    folder_path = create_sunshine_graph_folder()

    # Generate and save sunshine hour graphs for each year
    plot_and_save_sunshine(highest_lowest_sunshine, folder_path)

    print(f"Sunshine hour graphs saved in '{folder_path}'")

if __name__ == "__main__":
    main()
