# Set working directory
setwd("/Users/yujirokisu/Documents/devs/Paramecium_with_cyanobacteria_processing_images/final_analysis_zourimushi/cyano_count_manual")

# Load necessary libraries
library(ggplot2)
library(dplyr)
library(tidyr)

# Read the data
data <- read.csv("/Users/yujirokisu/Documents/devs/Paramecium_with_cyanobacteria_processing_images/final_analysis_zourimushi/cyano_count_manual/cyano_cout_manual.csv")

# Reshape the data to long format for easier plotting
data_long <- data %>%
  pivot_longer(cols = c(before, after_dark, after_light),
               names_to = "time",
               values_to = "value") %>%
  mutate(time = factor(time, levels = c("before", "after_dark", "after_light")))

# Calculate overall y-axis range and round limits to nearest multiple of 10
y_min <- floor(min(data_long$value, na.rm = TRUE) / 10) * 10
y_max <- ceiling(max(data_long$value, na.rm = TRUE) / 10) * 10

# Define axis interval as 20
y_interval <- 20

# Create plots for each stock
stocks <- unique(data$stock)

# Loop through each stock and create the plots
for (stock_name in stocks) {
  # Filter data for the current stock
  stock_data <- data_long %>% filter(stock == stock_name)
  
  # Calculate mean values for each time point
  mean_data <- stock_data %>%
    group_by(time) %>%
    summarise(mean_value = mean(value, na.rm = TRUE))
  
  # Calculate overall average across all concentrations for the stock
  overall_mean_data <- stock_data %>%
    group_by(time) %>%
    summarise(overall_mean = mean(value, na.rm = TRUE))
  
  # Before vs After Dark Plot
  plot_dark <- ggplot(stock_data %>% filter(time %in% c("before", "after_dark")),
                      aes(x = time, y = value, group = factor(concentration), color = factor(concentration))) +
    geom_line(size = 1) +
    geom_point(size = 3) +
    # Add average line for individual concentrations
    geom_line(data = mean_data %>% filter(time %in% c("before", "after_dark")),
              aes(x = time, y = mean_value, group = 1), 
              color = "black", linetype = "dashed", size = 1) +
    # Add overall average line
    geom_line(data = overall_mean_data %>% filter(time %in% c("before", "after_dark")),
              aes(x = time, y = overall_mean, group = 1),
              color = "blue", linetype = "dashed", size = 1) +
    labs(title = paste("Before vs After Dark for Stock:", stock_name),
         x = "Time",
         y = "The number of cyanobacteria (/400 µm^2)",
         color = "Concentration") +
    theme_minimal() +
    theme(
      axis.title = element_text(size = 22),
      axis.text = element_text(size = 20),
      plot.title = element_text(size = 20, hjust = 0.5)
    ) +
    scale_y_continuous(limits = c(y_min, y_max), breaks = seq(y_min, y_max, by = y_interval))
  
  # Save the plot
  ggsave(filename = paste0("average_before_after_dark_", stock_name, ".svg"), plot = plot_dark, width = 8, height = 8)
  
  # Before vs After Light Plot
  plot_light <- ggplot(stock_data %>% filter(time %in% c("before", "after_light")),
                       aes(x = time, y = value, group = factor(concentration), color = factor(concentration))) +
    geom_line(size = 1) +
    geom_point(size = 3) +
    # Add average line for individual concentrations
    geom_line(data = mean_data %>% filter(time %in% c("before", "after_light")),
              aes(x = time, y = mean_value, group = 1), 
              color = "black", linetype = "dashed", size = 1) +
    # Add overall average line
    geom_line(data = overall_mean_data %>% filter(time %in% c("before", "after_light")),
              aes(x = time, y = overall_mean, group = 1),
              color = "blue", linetype = "dashed", size = 1) +
    labs(title = paste("Before vs After Light for Stock:", stock_name),
         x = "Time",
         y = "The number of cyanobacteria (/400 µm^2)",
         color = "Concentration") +
    theme_minimal() +
    theme(
      axis.title = element_text(size = 22),
      axis.text = element_text(size = 20),
      plot.title = element_text(size = 20, hjust = 0.5)
    ) +
    scale_y_continuous(limits = c(y_min, y_max), breaks = seq(y_min, y_max, by = y_interval))
  
  # Save the plot
  ggsave(filename = paste0("average_before_after_light_", stock_name, ".svg"), plot = plot_light, width = 8, height = 8)
}