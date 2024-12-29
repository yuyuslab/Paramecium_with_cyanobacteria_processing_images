setwd("/Users/yujirokisu/Documents/devs/Paramecium_with_cyanobacteria_processing_images/final_analysis_zourimushi")

# Load necessary libraries
library(ggplot2)
library(dplyr)
library(tidyr)

# Read the data
data <- read.csv("/Users/yujirokisu/Documents/devs/Paramecium_with_cyanobacteria_processing_images/final_analysis_zourimushi/cyano_ratio_all_long_format.csv")

# Reshape the data to long format for easier plotting
data_long <- data %>%
  pivot_longer(cols = c(before, after_dark, after_light),
               names_to = "time",
               values_to = "value") %>%
  mutate(time = factor(time, levels = c("before", "after_dark", "after_light")))

# Create plots for each stock
stocks <- unique(data$stock)

# Loop through each stock and create the plots
for (stock_name in stocks) {
  # Filter data for the current stock
  stock_data <- data_long %>% filter(stock == stock_name)
  
  # Before vs After Dark Plot
  plot_dark <- ggplot(stock_data %>% filter(time %in% c("before", "after_dark")),
                      aes(x = time, y = value, group = factor(concentration), color = factor(concentration))) +
    geom_line(size = 1) +
    geom_point(size = 3) +
    labs(title = paste("Before vs After Dark for Stock:", stock_name),
         x = "Time",
         y = "Value",
         color = "Concentration") +
    theme_minimal()
  
  # Save the plot
  ggsave(filename = paste0("before_after_dark_", stock_name, ".png"), plot = plot_dark, width = 8, height = 6)
  
  # Before vs After Light Plot
  plot_light <- ggplot(stock_data %>% filter(time %in% c("before", "after_light")),
                       aes(x = time, y = value, group = factor(concentration), color = factor(concentration))) +
    geom_line(size = 1) +
    geom_point(size = 3) +
    labs(title = paste("Before vs After Light for Stock:", stock_name),
         x = "Time",
         y = "Value",
         color = "Concentration") +
    theme_minimal()
  
  # Save the plot
  ggsave(filename = paste0("before_after_light_", stock_name, ".png"), plot = plot_light, width = 8, height = 6)
}

