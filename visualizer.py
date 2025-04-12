import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.layouts import gridplot
import sqlalchemy as db

class DataVisualizer:
    """
    A class to visualize training data, ideal functions, and test data using Bokeh.
    """
    def __init__(self, db_file='data.db'):
        self.db_file = db_file

    def visualize_data(self, training_data, ideal_functions, test_data):
        """
        Visualizes the training data, ideal functions, and test data using Bokeh.
        """
        engine = db.create_engine(f'sqlite:///{self.db_file}')
        output_file("visualization.html")

        plots = []

        # Create scatter plots for training data and ideal functions
        for i in range(1, 5):
            p = figure(title=f'Training Data Y{i} and Ideal Function', 
                       x_axis_label='x', 
                       y_axis_label='y',
                       width=400, height=300)

            # Customize colors and markers for training data
            p.scatter(training_data['x'], training_data[f'y{i}'], 
                       legend_label=f'Training y{i}', 
                       color='navy', size=8, alpha=0.6, marker='circle')

            # Customize line styles for ideal functions
            p.line(ideal_functions['x'], ideal_functions[f'y{i}'], 
                   legend_label=f'Ideal y{i}', 
                   color='orange', line_width=2, line_dash='dashed')

            # Adding grid and legend
            p.grid.grid_line_alpha = 0.3
            p.legend.location = "top_left"
            p.legend.click_policy="hide"

            plots.append(p)

        # Create scatter plot for test data with assigned ideal functions
        p_test = figure(title='Test Data with Assigned Ideal Functions', 
                        x_axis_label='x', 
                        y_axis_label='y', 
                        width=400, height=300)

        # Customize test data scatter
        p_test.scatter(test_data['x'], test_data['y'], 
                       legend_label='Test Data', 
                       color='green', size=10, alpha=0.7, marker='square')

        # Differentiate the test data points based on assigned ideal functions
        for i in range(1, 5):
            subset = test_data[test_data['ideal_func_no'] == i]
            p_test.scatter(subset['x'], subset['y'], 
                           legend_label=f'Ideal Func {i}', 
                           color=('#ff9933' if i == 1 else '#33ccff' if i == 2 
                                   else '#ffcc33' if i == 3 else '#ff6699'), 
                           size=8, alpha=0.6)

        # Arrange the plots in a grid layout and display them
        grid = gridplot([[plots[0], plots[1]], [plots[2], plots[3]], [p_test]])
        show(grid)
