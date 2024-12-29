import cv2
import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from tqdm import tqdm

def main():
    csv_file = "../visual_count_data/cyano_visual_count.csv"
    visual_data = visual_count_data(csv_file, 5)

    directory = '../cyanos'

    # List of ranges for processing
    # ranges = [(0, 10), (11, 21), (22, 31), (32, 41), (42, 51), (52, 103), (10, 51)]
    ranges = [(0, 50), (51, 101), (102, 152), (153, 203), (204, 255)]
    num_samples = 100000
    mean_values_list = []

    print("Processing images across ranges...")
    for min_r, max_r in tqdm(ranges, desc="Overall Progress"):
        mean_values = process_images(directory, min_r, max_r, num_samples)
        mean_values_list.append(mean_values)

    # Generate plots
    # plot_titles = ["0-10", "11-21", "22-31", "32-41", "42-51", "52-103", "10-51"]
    plot_titles = ["0-50 wide", "51-101 wide", "102-152 wide", "153-203 wide", "204-254 wide"]

    for idx, mean_values in enumerate(mean_values_list):
        plot_scatter(
            x_data=visual_data,
            y_data=mean_values,
            x_label="Visual Count Data",
            y_label="Mean R Values",
            title=f"Scatter Plot of Visual Data vs. Mean R Values ({plot_titles[idx]})",
            concentration=plot_titles[idx]
        )

def process_images(directory, min_r, max_r, num_samples):
    """
    Processes images in the specified directory and computes the average R channel values within the range.
    """
    mean_values = []
    image_files = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]

    for filename in tqdm(image_files, desc=f"Processing range {min_r}-{max_r}", leave=False):
        file_path = os.path.join(directory, filename)

        # Load the image
        image = cv2.imread(file_path)
        if image is None:
            continue

        height, width, _ = image.shape
        valid_samples = []

        while len(valid_samples) < num_samples:
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
        mean_values.append(float(mean_value))

    return mean_values

def visual_count_data(csv_dir, counts):
    df = pd.read_csv(csv_dir)
    num_rows = len(df.index)

    lst_means = []
    for i in tqdm(range(1, int(num_rows / counts) + 1), desc="Calculating Visual Data Means"):
        mean_img = df[df['id'] == i]['value'].mean()
        lst_means.append(float(mean_img))

    return lst_means

def plot_scatter(x_data, y_data, x_label, y_label, title, concentration):
    # output_directory = "../output_images/tests"
    output_directory = "../output_images/tests"

    x_2D = np.array(x_data).reshape(-1, 1)
    y_2D = np.array(y_data).reshape(-1, 1)

    model_lr = LinearRegression()
    model_lr.fit(x_2D, y_2D)
    r_squared = model_lr.score(x_2D, y_2D)

    print(f"{concentration}: R-squared = {r_squared:.3f}")

    plt.rcParams["font.size"] = 16

    plt.figure(figsize=(8, 6))
    plt.scatter(x_data, y_data, color='blue')
    plt.xlabel(f"{x_label} ({concentration})", fontsize=14)
    plt.ylabel(y_label, fontsize=14)
    plt.plot(x_data, model_lr.predict(x_2D), color="red", linestyle="solid")
    plt.title(title)
        # Display R^2 value on the figure
    plt.text(
        0.05, 0.95, 
        f"$R^2$ = {r_squared:.2f}", 
        transform=plt.gca().transAxes, 
        fontsize=14, 
        verticalalignment='top', 
        horizontalalignment='left', 
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5')
    )
    plt.grid(False)

    output_filename = os.path.join(output_directory, f"valid_testing_{concentration}.png")
    plt.savefig(output_filename)
    plt.close()

if __name__ == "__main__":
    main()




'''

赤の濃度が高いところは，シアノバクテリアの面積をとりあえず２倍する
（それでも相関が出なければ，重なっている濃度の波長を探して，そこの波長の範囲を倍増する）

正方形の大きさは10 x 10 で 320くらいのサンプリング回数 -> done




'''