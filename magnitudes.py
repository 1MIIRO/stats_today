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

# Function to process the data and calculate the highest and lowest magnitude per year and month
def calculate_highest_lowest_magnitude_per_year_and_month(data):
    mag_per_year_month = defaultdict(lambda: defaultdict(list))

    for entry in data:
        date = entry.get('date', '')
        magnitude = entry.get('magnitude', 0)

        # Extract year and month from the date
        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month
            mag_per_year_month[year][month].append(magnitude)
        except ValueError:
            continue  # Skip invalid date entries

    # Calculate the highest and lowest magnitude for each month of each year
    highest_lowest_magnitude = defaultdict(lambda: defaultdict(dict))
    for year, months in mag_per_year_month.items():
        for month, magnitudes in months.items():
            highest_lowest_magnitude[year][month]['max_magnitude'] = max(magnitudes)
            highest_lowest_magnitude[year][month]['min_magnitude'] = min(magnitudes)

    return highest_lowest_magnitude

# Function to create the 'magnitude_graphs' folder (delete if exists)
def create_magnitude_graph_folder():
    folder_path = 'magnitude_graphs'
    
    # If the folder exists, delete it and recreate it
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    # Create a new folder to store graphs
    os.makedirs(folder_path)
    return folder_path

# Function to plot the highest and lowest magnitudes for all 12 months in one graph for each year
def plot_and_save_magnitude(highest_lowest_magnitude, folder_path):
    for year, months in highest_lowest_magnitude.items():
        # Prepare the data for the plot
        months_list = []
        max_magnitude_list = []
        min_magnitude_list = []

        # Get the short name of the months (Jan, Feb, Mar, etc.) and magnitude data
        for month in range(1, 13):
            months_list.append(calendar.month_abbr[month])  # Short name of the month
            max_magnitude_list.append(months.get(month, {}).get('max_magnitude', 0))
            min_magnitude_list.append(months.get(month, {}).get('min_magnitude', 0))

        # Create a new figure for the year
        plt.figure(figsize=(10, 6))
        bar_width = 0.35  # Set the width of the bars
        index = range(len(months_list))

        # Plot the bars for max and min magnitude
        plt.bar(index, max_magnitude_list, bar_width, label='Max Magnitude', color='red')
        plt.bar([i + bar_width for i in index], min_magnitude_list, bar_width, label='Min Magnitude', color='blue')

        plt.xlabel('Month')
        plt.ylabel('Magnitude')
        plt.title(f'Highest and Lowest Magnitudes in {year}')
        plt.xticks([i + bar_width / 2 for i in index], months_list)  # Center the ticks between the bars
        plt.legend()

        # Save the figure as a PNG file
        graph_filename = f"{folder_path}/magnitude_{year}.png"
        plt.savefig(graph_filename)
        plt.close()  # Close the plot to avoid memory issues

# Main function
def main():
    # Load data (replace 'data.json' with your file path)
    data = load_json_data('bar_graphs\\merged_data.json')

    # Calculate highest and lowest magnitude per year and month
    highest_lowest_magnitude = calculate_highest_lowest_magnitude_per_year_and_month(data)

    # Create the 'magnitude_graphs' folder
    folder_path = create_magnitude_graph_folder()

    # Generate and save magnitude graphs for each year
    plot_and_save_magnitude(highest_lowest_magnitude, folder_path)

    print(f"Magnitude graphs saved in '{folder_path}'")

if __name__ == "__main__":
    main()
