# Load necessary libraries
library(ggplot2)
library(dplyr)
library(tidyr)

# Set working directory
setwd("/Users/yujirokisu/Documents/devs/Paramecium_with_cyanobacteria_processing_images/final_analysis_zourimushi/P_bursaria_count")

# Read the data
data <- read.csv("/Users/yujirokisu/Documents/devs/Paramecium_with_cyanobacteria_processing_images/final_analysis_zourimushi/P_bursaria_count/P_bursaria_counting.csv")

# Reshape the data to long format for easier plotting
data_long <- data %>%
  pivot_longer(cols = c(before_dark, before_light, after_dark, after_light),
               names_to = "time",
               values_to = "value") %>%
  mutate(time = factor(time, levels = c("before_dark", "after_dark", "before_light", "after_light")))

# Calculate overall y-axis range and round limits to nearest multiple of 10
y_min <- floor(min(data_long$value, na.rm = TRUE) / 10) * 10
y_max <- ceiling(max(data_long$value, na.rm = TRUE) / 10) * 10

# Define axis interval as 10
y_interval <- 10

# Create plots for each stock
stocks <- unique(data$stock)

# Loop through each stock and create the plots
for (stock_name in stocks) {
  # Filter data for the current stock
  stock_data <- data_long %>% filter(stock == stock_name)
  
  # Calculate mean values for each time point for individual concentrations
  mean_data <- stock_data %>%
    group_by(time) %>%
    summarise(mean_value = mean(value, na.rm = TRUE))
  
  # Calculate the overall mean across all concentrations
  overall_mean_data <- stock_data %>%
    group_by(time) %>%
    summarise(overall_mean_value = mean(value, na.rm = TRUE))
  
  # Before Dark vs After Dark Plot
  plot_dark <- ggplot(stock_data %>% filter(time %in% c("before_dark", "after_dark")),
                      aes(x = time, y = value, group = factor(concentration), color = factor(concentration))) +
    geom_line(size = 1) +
    geom_point(size = 3) +
    # Add individual concentration average line
    geom_line(data = mean_data %>% filter(time %in% c("before_dark", "after_dark")),
              aes(x = time, y = mean_value, group = 1), 
              color = "black", linetype = "dashed", size = 1) +
    # Add overall average line
    geom_line(data = overall_mean_data %>% filter(time %in% c("before_dark", "after_dark")),
              aes(x = time, y = overall_mean_value, group = 1),
              color = "blue", linetype = "dashed", size = 1) +
    labs(title = paste("Before Dark vs After Dark for", stock_name),
         x = "Time",
         y = "The number of P. Bursaria",
         color = "Concentration") +
    theme_minimal() +
    theme(
      axis.title = element_text(size = 24),
      axis.text = element_text(size = 20),
      plot.title = element_text(size = 20, hjust = 0.5)
    ) +
    scale_y_continuous(limits = c(y_min, y_max), breaks = seq(y_min, y_max, by = y_interval))
  
  # Save the plot
  ggsave(filename = paste0("before_after_dark_", stock_name, ".svg"), 
         plot = plot_dark, width = 8, height = 6, dpi = 300)
  
  # Before Light vs After Light Plot
  plot_light <- ggplot(stock_data %>% filter(time %in% c("before_light", "after_light")),
                       aes(x = time, y = value, group = factor(concentration), color = factor(concentration))) +
    geom_line(size = 1) +
    geom_point(size = 3) +
    # Add individual concentration average line
    geom_line(data = mean_data %>% filter(time %in% c("before_light", "after_light")),
              aes(x = time, y = mean_value, group = 1), 
              color = "black", linetype = "dashed", size = 1) +
    # Add overall average line
    geom_line(data = overall_mean_data %>% filter(time %in% c("before_light", "after_light")),
              aes(x = time, y = overall_mean_value, group = 1),
              color = "blue", linetype = "dashed", size = 1) +
    labs(title = paste("Before Light vs After Light for", stock_name),
         x = "Time",
         y = "The number of P. Bursaria",
         color = "Concentration") +
    theme_minimal() +
    theme(
      axis.title = element_text(size = 24),
      axis.text = element_text(size = 20),
      plot.title = element_text(size = 20, hjust = 0.5)
    ) +
    scale_y_continuous(limits = c(y_min, y_max), breaks = seq(y_min, y_max, by = y_interval))
  
  # Save the plot
  ggsave(filename = paste0("before_after_light_", stock_name, ".svg"), 
         plot = plot_light, width = 8, height = 6, dpi = 300)
}