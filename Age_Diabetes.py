import matplotlib.pyplot as plt
import numpy as np

def age_diabetes_plot(df):
    # Age ranges
    age_ranges = ['[0, 20)', '[20, 40)', '[40, 60)', '[60, 80)', '[80, 100)']

    # Data for each age range (diabetes=1)
    diabetes_1_original = [106, 604, 2858, 3908, 1023]
    diabetes_1_k_anonymity = [102, 569, 2786, 3836, 1023]
    diabetes_1_random_deletion_average = [47.9, 280.7, 1395.0, 1920.8, 512.1]

    # Set the width of the bars
    bar_width = 0.2

    # Create an array of age range positions for the x-axis
    age_range_positions = np.arange(len(age_ranges))

    # Create the grouped bar chart for diabetes=1
    plt.figure(figsize=(12, 6))
    diabetes_1_original_bars = plt.bar(age_range_positions - bar_width, diabetes_1_original, bar_width, label='Original')
    diabetes_1_k_anonymity_bars = plt.bar(age_range_positions, diabetes_1_k_anonymity, bar_width, label='Anonymized')
    diabetes_1_random_deletion_average_bars = plt.bar(age_range_positions + bar_width, diabetes_1_random_deletion_average, bar_width, label='Sampling50')

    # Calculate the centers of the bars for diabetes=1
    diabetes_1_original_centers = [rect.get_x() + rect.get_width() / 2 for rect in diabetes_1_original_bars]
    diabetes_1_k_anonymity_centers = [rect.get_x() + rect.get_width() / 2 for rect in diabetes_1_k_anonymity_bars]
    diabetes_1_random_deletion_average_centers = [rect.get_x() + rect.get_width() / 2 for rect in diabetes_1_random_deletion_average_bars]

    # Draw lines connecting the centers of bars for diabetes=1
    plt.plot(diabetes_1_original_centers, diabetes_1_original, marker='o', color='blue')
    plt.plot(diabetes_1_k_anonymity_centers, diabetes_1_k_anonymity, marker='o', color='orange')
    plt.plot(diabetes_1_random_deletion_average_centers, diabetes_1_random_deletion_average, marker='o', color='green')

    # Set x-axis labels
    plt.xticks(age_range_positions, age_ranges, fontsize=12)

    # Set the chart labels and title for diabetes=1
    plt.xlabel('Age Ranges', fontsize=12)
    plt.ylabel('Number of people with diabetes', fontsize=12)
    #plt.title('Grouped Bar Chart (Diabetes=1) by Age Ranges')

    # Add a legend for diabetes=1
    plt.legend(loc='upper left', fontsize=12)

    # Show the plot for diabetes=1
    plt.show()
