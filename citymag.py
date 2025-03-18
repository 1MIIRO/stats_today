import json
import matplotlib.pyplot as plt
import os
from collections import defaultdict
from datetime import datetime

# Function to load data from a JSON file
def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Function to classify earthquake magnitudes into categories
def classify_magnitude(magnitude):
    if magnitude <= 2:
        return 'Low_Magnitude'
    elif 3 <= magnitude <= 5:
        return 'Medium_Magnitude'
    elif magnitude >= 5:
        return 'High_Magnitude'
    return None  # If there's no valid data for magnitude

# Function to count the frequency of magnitude categories per city, month, and year
def count_magnitude_categories_by_year(data):
    # Initialize defaultdict to store magnitude category counts by year, city
    magnitude_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # Year -> City -> Category -> Count

    for entry in data:
        date = entry.get('date', '')
        magnitude = entry.get('magnitude', 0)
        city = entry.get('city', None)  # Get city, default to None if it doesn't exist

        # Skip entry if city is missing or not a valid string
        if not city or not isinstance(city, str):
            continue

        try:
            year_month = datetime.strptime(date, "%Y-%m-%d")
            year = year_month.year
            category = classify_magnitude(magnitude)
            if category:
                magnitude_counts[year][city][category] += 1
        except ValueError:
            continue  # Skip invalid date entries
    
    return magnitude_counts

# Function to create a folder to store the graphs
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Function to plot and save the bar graph for magnitude categories by year (10 cities per graph)
def plot_magnitude_frequency_by_year(magnitude_counts, folder_name):
    # Define colors for the categories
    category_colors = {
        'Low_Magnitude': 'blue',
        'Medium_Magnitude': 'orange',
        'High_Magnitude': 'green'
    }

    for year, cities_data in magnitude_counts.items():
        cities = list(cities_data.keys())  # Get all cities for this year
        
        # Split cities into chunks of 10
        chunks = [cities[i:i + 10] for i in range(0, len(cities), 10)]

        for chunk_index, chunk in enumerate(chunks):
            low_counts = []
            medium_counts = []
            high_counts = []

            # Get the magnitude category counts for each city in this chunk
            for city in chunk:
                low_counts.append(cities_data[city].get('Low_Magnitude', 0))
                medium_counts.append(cities_data[city].get('Medium_Magnitude', 0))
                high_counts.append(cities_data[city].get('High_Magnitude', 0))

            # Set up the figure for the bar graph
            bar_width = 0.25  # Width of the bars
            index = range(len(chunk))  # X positions for each city

            fig, ax = plt.subplots(figsize=(12, 8))

            # Create bars for the 3 categories (Low, Medium, High) for each city
            ax.bar(index, low_counts, bar_width, label='Low Magnitude', color=category_colors['Low_Magnitude'])
            ax.bar([i + bar_width for i in index], medium_counts, bar_width, label='Medium Magnitude', color=category_colors['Medium_Magnitude'])
            ax.bar([i + 2 * bar_width for i in index], high_counts, bar_width, label='High Magnitude', color=category_colors['High_Magnitude'])

            # Set labels and title
            ax.set_xlabel('Cities')
            ax.set_ylabel('Frequency of Earthquakes')
            ax.set_title(f'Earthquake Magnitude Frequency in {year} - Part {chunk_index + 1}')
            ax.set_xticks([i + bar_width for i in index])  # Position the x-ticks between the bars
            ax.set_xticklabels(chunk, rotation=45, ha='right')
            ax.legend(title="Magnitude Categories")

            # Save the plot
            save_path = f'{folder_name}/earthquake_frequency_{year}_{chunk_index + 1}.png'
            plt.tight_layout()  # Ensure everything fits nicely
            plt.savefig(save_path)
            plt.close()  # Close the plot to avoid memory issues

# Main function to load data, process, and generate the graphs
def main():
    # Load the data (replace with your actual file path)
    data = load_json_data('bar_line\\merged_data.json')  # Your actual data file path
    
    # Count magnitude categories by year
    magnitude_counts = count_magnitude_categories_by_year(data)

    # Create the folder for storing graphs
    create_folder('earthquake_histograms_by_year')

    # Plot the earthquake magnitude frequency graph for each year (with 10 cities per graph)
    plot_magnitude_frequency_by_year(magnitude_counts, 'earthquake_histograms_by_year')

    print("Graphs have been saved in the 'earthquake_histograms_by_year' folder.")

# Execute the main function
if __name__ == "__main__":
    main()
