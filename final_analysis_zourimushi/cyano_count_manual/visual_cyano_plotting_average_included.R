# Loop through each stock and create the plots
for (stock_name in stocks) {
  # Filter data for the current stock
  stock_data <- data_long %>% filter(stock == stock_name)
  
  ## Calculate regression equation for "dark" condition
  overall_mean_dark <- stock_data %>%
    filter(time %in% c("before", "after_dark")) %>%
    group_by(time) %>%
    summarise(overall_mean = mean(value, na.rm = TRUE)) %>%
    mutate(time_numeric = as.numeric(time))
  
  regression_dark <- lm(overall_mean ~ time_numeric, data = overall_mean_dark)
  coef_dark <- coefficients(regression_dark)
  slope_dark <- round(coef_dark["time_numeric"], 2)
  intercept_dark <- round(coef_dark["(Intercept)"], 2)
  equation_dark <- paste0("y = ", slope_dark, "x + ", intercept_dark)
  
  ## Calculate regression equation for "light" condition
  overall_mean_light <- stock_data %>%
    filter(time %in% c("before", "after_light")) %>%
    group_by(time) %>%
    summarise(overall_mean = mean(value, na.rm = TRUE)) %>%
    mutate(time_numeric = as.numeric(time))
  
  regression_light <- lm(overall_mean ~ time_numeric, data = overall_mean_light)
  coef_light <- coefficients(regression_light)
  slope_light <- round(coef_light["time_numeric"], 2)
  intercept_light <- round(coef_light["(Intercept)"], 2)
  equation_light <- paste0("y = ", slope_light, "x + ", intercept_light)
  
  # Before vs After Dark Plot
  plot_dark <- ggplot(stock_data %>% filter(time %in% c("before", "after_dark")),
                      aes(x = time, y = value, group = factor(concentration), color = factor(concentration))) +
    geom_line(size = 1) +
    geom_point(size = 3) +
    # Add overall average line
    geom_line(data = overall_mean_dark,
              aes(x = time, y = overall_mean, group = 1),
              color = "blue", linetype = "dashed", size = 1) +
    # Annotate with the regression equation
    annotate("text", x = 1.5, y = y_max - 10, label = equation_dark, color = "black", size = 6, hjust = 0) +
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
    # Add overall average line
    geom_line(data = overall_mean_light,
              aes(x = time, y = overall_mean, group = 1),
              color = "blue", linetype = "dashed", size = 1) +
    # Annotate with the regression equation
    annotate("text", x = 1.5, y = y_max - 10, label = equation_light, color = "black", size = 6, hjust = 0) +
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