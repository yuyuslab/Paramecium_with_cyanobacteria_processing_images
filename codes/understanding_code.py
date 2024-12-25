import cv2
import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

def main():
    dir_dark = "../input_images/zourimushi_data/1030/dark"
    process_images(dir_dark, 0, 50)


def process_images(dir, min_r, max_r):
    image_folders = [f for f in os.listdir(dir)]

    for stock_dir in image_folders:
        stock = os.path.join(dir, stock_dir)
        con_dir = [c for c in os.listdir(stock)]

        # **MODIFIED**: Create lists to store concentrations and their mean values for plotting.
        concentrations = []
        mean_values = []

        for con in con_dir:
            concentration = os.path.join(stock, con)
            image_files = [f for f in os.listdir(concentration) if f.endswith('.jpg')]

            for filename in tqdm(image_files, desc=f"Processing range {min_r}-{max_r}", leave=False):
                file_path = os.path.join(concentration, filename)

                # Load the image
                image = cv2.imread(file_path)
                if image is None:
                    continue

                height, width, _ = image.shape
                valid_samples = []

                while len(valid_samples) < 10:
                    x = random.randint(0, width - 10)
                    y = random.randint(0, height - 10)
                    region = image[y:y+10, x:x+10]
                    red_channel = region[:, :, 2]

                    if np.all(red_channel == 0):
                        continue

                    valid_samples.append(red_channel)

            extracted_values = [red[(red >= min_r) & (red < max_r)] for red in valid_samples]
            extracted_values = np.concatenate(extracted_values)
            mean_value = np.mean(extracted_values) if len(extracted_values) > 0 else 0

            # **MODIFIED**: Collect concentration and mean value.
            concentrations.append(float(con))
            mean_values.append(mean_value)

            print(f"A stock of {stock_dir} and concentration of {con}. The mean value is {mean_value}.")

        # **MODIFIED**: Generate scatter plot for the stock.
        plot_stock(stock_dir, concentrations, mean_values)


def plot_stock(stock_name, concentrations, mean_values):
    """
    Generates and saves a scatter plot for the given stock.
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(concentrations, mean_values, color="blue", label="Mean Values")
    plt.plot(concentrations, mean_values, color="red", linestyle="dashed", label="Trend Line")
    plt.xlabel("Concentration")
    plt.ylabel("Mean Value")
    plt.title(f"Scatter Plot for Stock: {stock_name}")
    plt.legend()
    plt.grid(False)

    # Save the plot as an image.
    output_directory = "../output_images/all_analysis_data"
    # if not os.path.exists(output_directory):
    #     os.makedirs(output_directory)

    output_path = os.path.join(output_directory, f"{stock_name}_scatter.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Saved scatter plot for {stock_name} at {output_path}")