import json
import matplotlib.pyplot as plt
import os
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

# Function to count the frequency of rainfall categories per city, month, and year
def count_rainfall_categories_by_year(data):
    # Initialize defaultdict to store rainfall category counts by year, city
    rainfall_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # Year -> City -> Category -> Count

    for entry in data:
        date = entry.get('date', '')
        rain_sum = entry.get('weather', {}).get('rain_sum', 0)
        city = entry.get('city', None)  # Get city, default to None if it doesn't exist

        # Skip entry if city is missing or not a valid string
        if not city or not isinstance(city, str):
            continue

        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            category = classify_rainfall(rain_sum)
            if category:
                rainfall_counts[year][city][category] += 1
        except ValueError:
            continue  # Skip invalid date entries
    
    return rainfall_counts

# Function to create a folder to store the graphs
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Function to plot and save the bar graph for rainfall categories by year (10 cities per graph)
def plot_rainfall_frequency_by_year(rainfall_counts, folder_name):
    # Define colors for the categories
    category_colors = {
        'Low_rainfall': 'blue',
        'Medium_rainfall': 'orange',
        'High_rainfall': 'green'
    }

    for year, cities_data in rainfall_counts.items():
        cities = list(cities_data.keys())  # Get all cities for this year
        
        # Split cities into chunks of 10
        chunks = [cities[i:i + 10] for i in range(0, len(cities), 10)]

        for chunk_index, chunk in enumerate(chunks):
            low_counts = []
            medium_counts = []
            high_counts = []

            # Get the rainfall category counts for each city in this chunk
            for city in chunk:
                low_counts.append(cities_data[city].get('Low_rainfall', 0))
                medium_counts.append(cities_data[city].get('Medium_rainfall', 0))
                high_counts.append(cities_data[city].get('High_rainfall', 0))

            # Set up the figure for the bar graph
            bar_width = 0.25  # Width of the bars
            index = range(len(chunk))  # X positions for each city

            fig, ax = plt.subplots(figsize=(12, 8))

            # Create bars for the 3 categories (Low, Medium, High) for each city
            ax.bar(index, low_counts, bar_width, label='Low Rainfall', color=category_colors['Low_rainfall'])
            ax.bar([i + bar_width for i in index], medium_counts, bar_width, label='Medium Rainfall', color=category_colors['Medium_rainfall'])
            ax.bar([i + 2 * bar_width for i in index], high_counts, bar_width, label='High Rainfall', color=category_colors['High_rainfall'])

            # Set labels and title
            ax.set_xlabel('Cities')
            ax.set_ylabel('Frequency of Rainfall')
            ax.set_title(f'Rainfall Frequency by Category in {year} - Part {chunk_index + 1}')
            ax.set_xticks([i + bar_width for i in index])  # Position the x-ticks between the bars
            ax.set_xticklabels(chunk, rotation=45, ha='right')
            ax.legend(title="Rainfall Categories")

            # Save the plot
            save_path = f'{folder_name}/rainfall_frequency_{year}_{chunk_index + 1}.png'
            plt.tight_layout()  # Ensure everything fits nicely
            plt.savefig(save_path)
            plt.close()  # Close the plot to avoid memory issues

# Main function to load data, process, and generate the graphs
def main():
    # Load the data (replace with your actual file path)
    data = load_json_data('bar_line\\merged_data.json')  # Your actual data file path
    
    # Count rainfall categories by year
    rainfall_counts = count_rainfall_categories_by_year(data)

    # Create the folder for storing graphs
    create_folder('rainfall_histograms_by_year')

    # Plot the rainfall frequency graph for each year (with 10 cities per graph)
    plot_rainfall_frequency_by_year(rainfall_counts, 'rainfall_histograms_by_year')

    print("Graphs have been saved in the 'rainfall_histograms_by_year' folder.")

# Execute the main function
if __name__ == "__main__":
    main()
