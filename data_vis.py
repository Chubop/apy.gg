import matplotlib.pyplot as plt
import random  # Used to simulate scraper results
import numpy as np


# Define the scraper function (replace this with your actual scraper function)
def map_scraper(accuracy_values: list = [1 / 1, 2 / 2, 3 / 3, 4 / 5, 5 / 6, 5 / 7, 5 / 8, 6 / 9, 7 / 10]):
    # Define the x-values (independent variable)
    x_values = list(range(1, len(accuracy_values) + 1))

    # Calculate the trendline
    z = np.polyfit(x_values, accuracy_values, 1)
    trendline = np.poly1d(z)

    # Plot the graph
    plt.plot(x_values, accuracy_values, label='Accuracy')
    plt.plot(x_values, trendline(x_values), 'r--', label='Trendline')
    plt.xlabel("Number of Tests")
    plt.ylabel("Accuracy (%)")
    plt.title("Scraper Accuracy vs Number of Tests")
    plt.legend()
    plt.grid()

    # Display the graph
    plt.show()


if __name__ == '__main__':
    map_scraper()
