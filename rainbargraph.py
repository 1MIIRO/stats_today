import json
import matplotlib.pyplot as plt
import os
import calendar
from collections import defaultdict
from datetime import datetime
import shutil

# Function to load data from a JSON file
def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Function to classify rainfall into categories
def classify_rainfall(rain_sum):
    if rain_sum <= 5:
        return 'Low_rainfall'
    elif 6 <= rain_sum <= 10:
        return 'Medium_rainfall'
    elif rain_sum >= 10:
        return 'High_rainfall'
    return None  # If there's no valid data for rainfall

# Function to count the frequency of rainfall categories per month and year
def count_rainfall_categories(data):
    rainfall_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # Year -> Month -> Category -> Count

    for entry in data:
        date = entry.get('date', '')
        rain_sum = entry.get('weather', {}).get('rain_sum', 0)

        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            month = year_month.month

            category = classify_rainfall(rain_sum)
            if category:
                rainfall_counts[year][month][category] += 1
        except ValueError:
            continue  # Skip invalid date entries
    
    return rainfall_counts

# Function to create folder if it doesn't exist
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Function to plot the rainfall frequency bar graph for each year
def plot_rainfall_categories(rainfall_counts, save_folder):
    categories = ['Low_rainfall', 'Medium_rainfall', 'High_rainfall']
    
    # Loop over all years
    for year, months in rainfall_counts.items():
        months_list = [calendar.month_abbr[i] for i in range(1, 13)]
        
        # Prepare data for plotting
        low_rainfall = []
        medium_rainfall = []
        high_rainfall = []

        for month in range(1, 13):
            low_rainfall.append(months.get(month, {}).get('Low_rainfall', 0))
            medium_rainfall.append(months.get(month, {}).get('Medium_rainfall', 0))
            high_rainfall.append(months.get(month, {}).get('High_rainfall', 0))

        # Create the bar graph
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Bar width
        bar_width = 0.25
        index = range(12)

        # Plot the bars
        ax.bar(index, low_rainfall, bar_width, label='Low Rainfall', color='green')
        ax.bar([i + bar_width for i in index], medium_rainfall, bar_width, label='Medium Rainfall', color='orange')
        ax.bar([i + bar_width * 2 for i in index], high_rainfall, bar_width, label='High Rainfall', color='red')

        # Set labels and title
        ax.set_xlabel('Month')
        ax.set_ylabel('Frequency')
        ax.set_title(f'Rainfall Categories Frequency in {year}')
        ax.set_xticks([i + bar_width for i in index])
        ax.set_xticklabels(months_list)
        
        # Add legends
        ax.legend()

        # Save the plot to the specified folder
        save_path = os.path.join(save_folder, f'rainfall_categories_{year}.png')
        plt.savefig(save_path)
        plt.close()  # Close the plot to avoid memory issues

        print(f"Histogram for {year} saved to {save_path}")

# Main function
def main():
    # Load earthquake and weather data from JSON file
    data = load_json_data('bar_graphs\\merged_data.json')  # Replace with your actual file path

    # Count rainfall categories
    rainfall_counts = count_rainfall_categories(data)

    # Folder to save the bar graphs
    save_folder = 'rainfall_histograms'  # Folder name where the histogram will be saved

    # Create the folder if it doesn't exist
    create_folder(save_folder)

    # Plot and save the rainfall frequency bar graphs
    plot_rainfall_categories(rainfall_counts, save_folder)

# Run the main function
if __name__ == "__main__":
    main()
