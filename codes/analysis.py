import cv2
import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from tqdm import tqdm

def main():
    dir_dark = "../input_images/zourimushi_data/1030/dark"
    dir_light = "../input_images/zourimushi_data/1030/light"
    # output_dir = "../output_images/all_analysis_data"  # Directory where plots will be saved
    output_dir = "../output_images/tests/12_25"
    
    process_images(dir_dark, 0, 50, output_dir, "dark")
    process_images(dir_light, 0, 50, output_dir, "light")

def process_images(dir, min_r, max_r, output_dir, condition):
    image_folders = [f for f in os.listdir(dir)]
    
    # Iterate over each "stock" directory
    for stock_dir in image_folders:
        stock = os.path.join(dir, stock_dir)    
        con_dir = [c for c in os.listdir(stock)]

        # Prepare lists for concentrations and their corresponding mean values
        concentrations = []
        mean_values = []

        # Iterate over each concentration directory
        for con in con_dir:
            concentration = os.path.join(stock, con)
            image_files = [f for f in os.listdir(concentration) if f.endswith(('.jpg'))]

            # Process each image in the concentration directory
            for filename in tqdm(image_files, desc=f"Processing range {min_r}-{max_r}", leave=False):
                file_path = os.path.join(concentration, filename)

                # Load the image
                image = cv2.imread(file_path)
                if image is None:
                    continue

                height, width, _ = image.shape
                valid_samples = []

                # Randomly sample pixels until we have 10 valid ones
                while len(valid_samples) < 10000:
                    x = random.randint(0, width - 10)
                    y = random.randint(0, height - 10)
                    region = image[y:y+10, x:x+10]
                    red_channel = region[:, :, 2]

                    # Only consider regions with non-zero red channel values
                    if np.all(red_channel == 0):
                        continue

                    valid_samples.append(red_channel)

            # Extract red channel values within the specified range
            extracted_values = [red[(red >= min_r) & (red < max_r)] for red in valid_samples]
            extracted_values = np.concatenate(extracted_values)
            mean_value = np.mean(extracted_values) if len(extracted_values) > 0 else 0

            # Collect the concentration and its corresponding mean value
            concentrations.append(float(con))
            mean_values.append(mean_value)
            print(len(mean_values))

        # **MODIFIED**: Define x-axis ticks explicitly and filter valid data for plotting
        fixed_concentrations = [0.02, 0.04, 0.06, 0.08, 0.1]
        
        # Filter out concentrations and mean values that exist in the actual data
        plot_concentrations = [c for c in fixed_concentrations if c in concentrations]
        plot_mean_values = [mean_values[concentrations.index(c)] for c in plot_concentrations]

        # Plot the data points
        plt.scatter(plot_concentrations, plot_mean_values, label="Data points")

        # Perform linear regression on the available data points
        if len(plot_concentrations) > 1:
            reg = LinearRegression().fit(np.array(plot_concentrations).reshape(-1, 1), plot_mean_values)
            y_pred = reg.predict(np.array(fixed_concentrations).reshape(-1, 1))
            plt.plot(fixed_concentrations, y_pred, color="black", label="Linear Regression")

        # Set the x-axis ticks to include all fixed concentrations
        plt.xticks(fixed_concentrations)

        # Set the labels and title
        plt.xlabel('Concentration')
        plt.ylabel('Mean Red Channel Value')
        plt.title(f"Stock: {stock_dir} in {condition}")
        plt.legend()

        # Save the plot as an image to the output directory
        output_path = os.path.join(output_dir, f"{condition}_{stock_dir}_plot.png")
        plt.savefig(output_path)
        plt.close()  # Close the plot to free memory

if __name__ == "__main__":
    main()