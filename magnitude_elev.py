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

# Function to classify elevation into categories
def classify_elevation(elevation):
    if elevation <= 10:
        return 'Below_Sea_Level'
    elif 11 <= elevation <= 30:
        return 'Sea_Level'
    elif 31 <= elevation <= 60:
        return 'Ground_Level'
    elif 61 <= elevation <= 90:
        return 'Ground_Level_Mid'
    elif elevation > 90:
        return 'Ground_Level_High'
    return None

# Function to process the data and calculate the magnitude and classified elevation for each year and month
def calculate_magnitude_and_elevation_per_year_and_month(data):
    magnitude_elevation_per_year_month = defaultdict(lambda: defaultdict(list))

    # List of elevation classifications
    elevation_classes = [
        'Below_Sea_Level', 'Sea_Level', 'Ground_Level', 'Ground_Level_Mid', 'Ground_Level_High'
    ]

    # Create a dictionary to map elevation categories to numerical values (for plotting)
    elevation_categories = {
        'Below_Sea_Level': 1,
        'Sea_Level': 2,
        'Ground_Level': 3,
        'Ground_Level_Mid': 4,
        'Ground_Level_High': 5
    }

    for entry in data:
        date = entry.get('date', '')
        magnitude = entry.get('magnitude', 0)
        elevation = entry.get('elevation', 0)

        # Classify elevation
        elevation_class = classify_elevation(elevation)

        # Extract year and month from the date
        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month
            magnitude_elevation_per_year_month[year][month].append((magnitude, elevation_class))
        except ValueError:
            continue  # Skip invalid date entries

    # Calculate the magnitude and elevation classification for each month of each year
    magnitude_elevation_data = defaultdict(lambda: defaultdict(dict))
    for year, months in magnitude_elevation_per_year_month.items():
        for month, values in months.items():
            # Calculate the average magnitude for the month
            avg_magnitude = sum(magnitude for magnitude, _ in values) / len(values)
            # Take the mode (most frequent) elevation category for the month
            elevation_classes_in_month = [elevation_class for _, elevation_class in values]
            most_common_elevation = max(set(elevation_classes_in_month), key=elevation_classes_in_month.count)

            magnitude_elevation_data[year][month]['avg_magnitude'] = avg_magnitude
            magnitude_elevation_data[year][month]['elevation_class'] = most_common_elevation

    return magnitude_elevation_data, elevation_classes

# Function to create the 'magnitude_elevation_graphs' folder (delete if exists)
def create_magnitude_elevation_graph_folder():
    folder_path = 'magnitude_elevation_graphs'
    
    # If the folder exists, delete it and recreate it
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    # Create a new folder to store graphs
    os.makedirs(folder_path)
    return folder_path

# Function to plot and save the earthquake magnitude and elevation classification for each month in a year
def plot_and_save_magnitude_elevation(magnitude_elevation_data, elevation_classes, folder_path):
    for year, months in magnitude_elevation_data.items():
        # Prepare the data for the plot
        months_list = []
        avg_magnitude_list = []
        elevation_class_list = []

        # Get the short name of the months (Jan, Feb, Mar, etc.) and magnitude and elevation data
        for month in range(1, 13):
            months_list.append(calendar.month_abbr[month])  # Short name of the month
            avg_magnitude_list.append(months.get(month, {}).get('avg_magnitude', 0))
            elevation_class_list.append(months.get(month, {}).get('elevation_class', ''))

        # Map the elevation classifications to corresponding numerical values for plotting
        elevation_numeric = [elevation_classes.index(elevation_class) + 1 if elevation_class else 0 for elevation_class in elevation_class_list]

        # Create a new figure for the year
        fig, ax1 = plt.subplots(figsize=(10, 6))
        bar_width = 0.35  # Set the width of the bars
        index = range(len(months_list))

        # Plot the bars for elevation class (using categorical names)
        ax1.bar(index, elevation_numeric, bar_width, label='Elevation Classification', color='blue', alpha=0.6)
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Elevation Classification', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.set_xticks([i for i in index])
        ax1.set_xticklabels(months_list)

        # Create a secondary y-axis to plot the magnitude
        ax2 = ax1.twinx()
        ax2.plot(index, avg_magnitude_list, label='Average Magnitude', color='red', marker='o', linestyle='-', linewidth=2)
        ax2.set_ylabel('Average Magnitude', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Title and legend
        plt.title(f'Earthquake Magnitude and Elevation Classification in {year}')
        
        # Add custom ticks for elevation y-axis (show the actual categories)
        ax1.set_yticks([1, 2, 3, 4, 5])  # Set the ticks based on the categories
        ax1.set_yticklabels(elevation_classes)  # Use category names for y-tick labels

        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Save the figure as a PNG file
        graph_filename = f"{folder_path}/magnitude_elevation_{year}.png"
        plt.savefig(graph_filename)
        plt.close()  # Close the plot to avoid memory issues

# Main function
def main():
    # Load data (replace 'data.json' with your file path)
    data = load_json_data('bar_line\\merged_data.json')

    # Calculate the magnitude and elevation classification per year and month
    magnitude_elevation_data, elevation_classes = calculate_magnitude_and_elevation_per_year_and_month(data)

    # Create the 'magnitude_elevation_graphs' folder
    folder_path = create_magnitude_elevation_graph_folder()

    # Generate and save magnitude and elevation graphs for each year
    plot_and_save_magnitude_elevation(magnitude_elevation_data, elevation_classes, folder_path)

    print(f"Earthquake magnitude and elevation graphs saved in '{folder_path}'")

if __name__ == "__main__":
    main()
