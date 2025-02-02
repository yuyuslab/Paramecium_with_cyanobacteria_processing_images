# Set working directory
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

# Calculate global min and max for y-axis
global_y_min <- floor(min(data_long$value, na.rm = TRUE))
global_y_max <- ceiling(max(data_long$value, na.rm = TRUE))  # Add a small buffer to max value

# Set a smaller interval for more detailed axis labels
y_interval <- 0.5

# Ensure range is aligned with the interval
global_y_min <- floor(global_y_min / y_interval) * y_interval
global_y_max <- ceiling(global_y_max / y_interval) * y_interval

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
  
  ## Before vs After Dark
  dark_mean_data <- mean_data %>% filter(time %in% c("before", "after_dark"))
  dark_mean_data <- dark_mean_data %>%
    mutate(time_numeric = as.numeric(time))
  
  # Perform linear regression for dark condition
  dark_regression <- lm(mean_value ~ time_numeric, data = dark_mean_data)
  dark_coef <- coefficients(dark_regression)
  dark_slope <- round(dark_coef["time_numeric"], 2)
  dark_intercept <- round(dark_coef["(Intercept)"], 2)
  dark_equation <- paste0("y = ", dark_slope, "x + ", dark_intercept)
  
  # Before vs After Dark Plot
  plot_dark <- ggplot(stock_data %>% filter(time %in% c("before", "after_dark")),
                      aes(x = time, y = value, group = factor(concentration), color = factor(concentration))) +
    geom_line(size = 1) +
    geom_point(size = 3) +
    # Add mean line for each time point (dashed)
    geom_line(data = dark_mean_data,
              aes(x = time, y = mean_value, group = 1), 
              color = "blue", linetype = "dashed", size = 1) +
    # Annotate with the regression equation
    annotate("text", x = 1.5, y = global_y_max - 0.5, label = dark_equation, color = "black", size = 6, hjust = 0) +
    labs(title = paste("Before vs After Dark for Stock:", stock_name),
         x = "Time",
         y = "The density of red fluorescence (/100 px^2)",
         color = "Concentration") +
    theme_minimal() +
    theme(
      axis.title = element_text(size = 22),
      axis.text = element_text(size = 20),
      plot.title = element_text(size = 20, hjust = 0.5)
    ) +
    scale_y_continuous(limits = c(global_y_min, global_y_max), breaks = seq(global_y_min, global_y_max, by = y_interval))
  
  # Save the plot
  ggsave(filename = paste0("average_before_after_dark_", stock_name, ".svg"), plot = plot_dark, width = 8, height = 8)
  
  ## Before vs After Light
  light_mean_data <- mean_data %>% filter(time %in% c("before", "after_light"))
  light_mean_data <- light_mean_data %>%
    mutate(time_numeric = as.numeric(time))
  
  # Perform linear regression for light condition
  light_regression <- lm(mean_value ~ time_numeric, data = light_mean_data)
  light_coef <- coefficients(light_regression)
  light_slope <- round(light_coef["time_numeric"], 2)
  light_intercept <- round(light_coef["(Intercept)"], 2)
  light_equation <- paste0("y = ", light_slope, "x + ", light_intercept)
  
  # Before vs After Light Plot
  plot_light <- ggplot(stock_data %>% filter(time %in% c("before", "after_light")),
                       aes(x = time, y = value, group = factor(concentration), color = factor(concentration))) +
    geom_line(size = 1) +
    geom_point(size = 3) +
    # Add mean line for each time point (dashed)
    geom_line(data = light_mean_data,
              aes(x = time, y = mean_value, group = 1), 
              color = "blue", linetype = "dashed", size = 1) +
    # Annotate with the regression equation
    annotate("text", x = 1.5, y = global_y_max - 0.5, label = light_equation, color = "black", size = 6, hjust = 0) +
    labs(title = paste("Before vs After Light for Stock:", stock_name),
         x = "Time",
         y = "The density of red fluorescence (/100 px^2)",
         color = "Concentration") +
    theme_minimal() +
    theme(
      axis.title = element_text(size = 22),
      axis.text = element_text(size = 20),
      plot.title = element_text(size = 20, hjust = 0.5)
    ) +
    scale_y_continuous(limits = c(global_y_min, global_y_max), breaks = seq(global_y_min, global_y_max, by = y_interval))
  
  # Save the plot
  ggsave(filename = paste0("average_before_after_light_", stock_name, ".svg"), plot = plot_light, width = 8, height = 8)
}