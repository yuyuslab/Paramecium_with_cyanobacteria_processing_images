import cv2
import os
import csv
import numpy as np

def main():
    # Individual images
    
    # inputs_before = "../input_images/zourimushi_data/1029"
    # results_before = image_process_individual(inputs_before)
    # csv_file_before = "../outputs_csv/1029.csv"
    # csv_write(results_before, csv_file_before)

    # inputs_after_dark = "../input_images/zourimushi_data/1030/dark"
    # results_after_dark = image_process_individual(inputs_after_dark)
    # csv_file_after_dark = "../outputs_csv/1030_dark.csv"
    # csv_write(results_after_dark, csv_file_after_dark)

    # inputs_after_light = "../input_images/zourimushi_data/1030/light"
    # results_after_light = image_process_individual(inputs_after_light)
    # csv_file_after_light = "../outputs_csv/1030_light.csv"
    # csv_write(results_after_light, csv_file_after_light)

    # Grouped images by concentration
    inputs_before = "../input_images/zourimushi_data/1029"
    results_before = image_process_conc_grouped(inputs_before)
    csv_file_before = "../outputs_csv/1029_grouped_by_con.csv"
    csv_write(results_before, csv_file_before)

    inputs_after_dark = "../input_images/zourimushi_data/1030/dark"
    results_after_dark = image_process_conc_grouped(inputs_after_dark)
    csv_file_after_dark = "../outputs_csv/1030_dark_grouped_by_con.csv"
    csv_write(results_after_dark, csv_file_after_dark)

    inputs_after_light = "../input_images/zourimushi_data/1030/light"
    results_after_light = image_process_conc_grouped(inputs_after_light)
    csv_file_after_light = "../outputs_csv/1030_light_grouped_by_con.csv"
    csv_write(results_after_light, csv_file_after_light)

def image_process_individual(inputs):
    dic = {"image": "mean_red_value"}
    image_folders = [f for f in os.listdir(inputs) if f != ".DS_Store"]
    
    # Iterate over each "stock" directory
    for stock_dir in image_folders:
        stock = os.path.join(inputs, stock_dir)    
        con_dir = [c for c in os.listdir(stock) if c != ".DS_Store"]

        # Iterate over each concentration directory
        for con in con_dir:
            concentration = os.path.join(stock, con)
            image_files = [f for f in os.listdir(concentration) if f.endswith('.jpg')]
            # Process each image in the concentration directory
            for filename in image_files:
                file_path = os.path.join(concentration, filename)

                # Load the image
                image = cv2.imread(file_path)
                if image is None:
                    continue
                
                # Get the red channel
                red_channel = image[:, :, 2]
                mean_value = red_channel.mean()
                image_name = f"{stock_dir}_{con}_{filename}"
                dic[image_name] = mean_value  # Add to the dictionary directly

    return dic  # Return the entire dictionary



def image_process_conc_grouped(inputs):
    dic = {"stock_conc": "con_mean_red_value"}
    image_folders = [f for f in os.listdir(inputs) if f != ".DS_Store"]
    
    # Iterate over each "stock" directory
    for stock_dir in image_folders:
        stock = os.path.join(inputs, stock_dir)    
        con_dir = [c for c in os.listdir(stock) if c != ".DS_Store"]

        # Iterate over each concentration directory
        for con in con_dir:
            concentration = os.path.join(stock, con)
            image_files = [f for f in os.listdir(concentration) if f.endswith('.jpg')]
            # Process each image in the concentration directory
            for filename in image_files:
                file_path = os.path.join(concentration, filename)

                # Load the image
                image = cv2.imread(file_path)
                if image is None:
                    continue
                
                # Get the red channel
                red_channel = image[:, :, 2]
                con_results = []
                con_results.append(red_channel)
                con_results = np.concatenate(con_results)
                con_mean = con_results.mean()
                con_result_name = f"{stock_dir}_{con}"
                dic[con_result_name] = con_mean  # Add to the dictionary directly

    return dic  # Return the entire dictionary






def csv_write(results, csv_file):
    # Specify the CSV file name
    output_dir = csv_file 

    # Ensure the output directory exists
    output_dir = os.path.dirname(csv_file)
    os.makedirs(output_dir, exist_ok=True)

    # Writing to CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for key, value in results.items():
            writer.writerow([key, value])

    print(f"Results saved to {csv_file}")

if __name__ == "__main__":
    main()