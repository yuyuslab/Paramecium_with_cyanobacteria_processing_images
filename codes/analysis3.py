import cv2
import os
import csv
import numpy as np
import random
def main():
    # Individual images
    
    # Test
    # inputs = "/Users/yujirokisu/Desktop/cropped"
    # results = image_process_conc_grouped(inputs)
    # csv_file = "/Users/yujirokisu/Desktop/cropped_group.csv"
    # csv_write(results, csv_file)

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
    inputs_before = "../input_images/zourimushi_data/1029_cropped"
    results_before = image_process_conc_grouped(inputs_before)
    csv_file_before = "../outputs_csv/cropped_1029_grouped_by_con2.csv"
    csv_write(results_before, csv_file_before)

    inputs_after_dark = "../input_images/zourimushi_data/1030_cropped/dark"
    results_after_dark = image_process_conc_grouped(inputs_after_dark)
    csv_file_after_dark = "../outputs_csv/cropped_1030_dark_grouped_by_con2.csv"
    csv_write(results_after_dark, csv_file_after_dark)

    inputs_after_light = "../input_images/zourimushi_data/1030_cropped/light"
    results_after_light = image_process_conc_grouped(inputs_after_light)
    csv_file_after_light = "../outputs_csv/cropped_1030_light_grouped_by_con2.csv"
    csv_write(results_after_light, csv_file_after_light)

    # test_inputs = "../input_images/zourimushi_data/1029_cropped"
    # test_results = image_process_conc_grouped(test_inputs)
    # test_csv_file = "../outputs_csv/cropped_1029_grouped_by_con.csv"
    # csv_write(test_results, test_csv_file)



def image_process_individual(inputs):
    fixed_concentrations = [0.02, 0.04, 0.06, 0.08, 0.1]
    dic = {"image": "mean_red_value"}
    image_folders = [f for f in os.listdir(inputs) if f != ".DS_Store"]
    
    # Iterate over each "stock" directory
    for stock_dir in image_folders:
        stock = os.path.join(inputs, stock_dir)    
        con_dir = [c for c in os.listdir(stock) if c != ".DS_Store"]

        # Iterate over each concentration directory
        for con in con_dir:
            if con in fixed_concentrations:
                concentration = os.path.join(stock, con)
                image_files = [f for f in os.listdir(concentration) if f.endswith('.jpg' or '.png')]
                # Process each image in the concentration directory
                for filename in image_files:
                    file_path = os.path.join(concentration, filename)

                    # Load the image
                    image = cv2.imread(file_path)
                    if image is None:
                        continue

                    height, width, _ = image.shape
                    count = 0
                    # Randomly sample pixels until we have 10 valid ones
                    side_length = 10
                    while count < 10000:
                        x = random.randint(0, width - side_length)
                        y = random.randint(0, height - side_length)
                        region = image[y:y+side_length, x:x+side_length]
                        red_channel = region[:, :, 2]                        
                        if np.all(red_channel == 0):
                            continue
                        count += 1

                    mean_value = red_channel.mean()
                    red_value_ratio = mean_value / (side_length ** 2)
                    image_name = f"{stock_dir}_{con}_{filename}"
                    dic[image_name] = red_value_ratio  # Add to the dictionary directly
            else:
                image_name = f"{stock_dir}_{con}_NA"
                dic[image_name] = 0  # Add to the dictionary directly

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
            con_results = []
            concentration = os.path.join(stock, con)
            # If there is not file, assign 0 to con_mean
            if not os.path.exists(concentration):
                con_mean = 0
                con_result_name = f"{stock_dir}_{con}"
                dic[con_result_name] = con_mean
                continue
            image_files = [f for f in os.listdir(concentration) if f.endswith('.png')]
            
            # Process each image in the concentration directory
            for filename in image_files:
                file_path = os.path.join(concentration, filename)
        
                # Load the image
                image = cv2.imread(file_path)
                if image is None:
                    continue
                
                height, width, _ = image.shape
                count = 0
                # Randomly sample pixels until we have 10 valid ones
                side_length = 10
                while count < 100:
                    x = random.randint(0, width - side_length)
                    y = random.randint(0, height - side_length)
                    region = image[y:y+side_length, x:x+side_length]
                    red_channel = region[:, :, 2]
                    if np.all(red_channel == 0):
                        continue
                    count += 1
                    mean_value = red_channel.mean()
                    red_value_ratio = float(mean_value / (side_length ** 2))
                    con_results.append(red_value_ratio)
                    # np.savetxt(f"../outputs_csv/result_{con}.txt", red_channel, fmt="%.3f", delimiter=",")
           
            con_results = np.array(con_results)
            
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