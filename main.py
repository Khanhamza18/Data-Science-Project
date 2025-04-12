from database import DataProcessor
from visualizer import DataVisualizer
import pandas as pd

def main():
    """
    Main function to run the data processing and visualization.

    This function initializes the DataProcessor with paths to the training data,
    ideal functions, and test data CSV files. It then creates the database, loads
    the data, processes the test data, and visualizes the results.
    """
    # Initialize DataProcessor with file paths
    processor = DataProcessor(
        training_file='train.csv',
        ideal_functions_file='ideal.csv',
        test_file='test.csv'
    )

    # Create the database and load data
    processor.initialize_database()
    processor.load_data_to_db()

    # Map test data to ideal functions
    test_results = processor.map_test_data()

    # Initialize DataVisualizer and visualize data
    visualizer = DataVisualizer()
    
    # Load training and ideal functions data from the database
    training_data = pd.read_sql('SELECT * FROM training_data', processor.engine)
    ideal_functions = pd.read_sql('SELECT * FROM ideal_functions', processor.engine)

    # Pass the loaded data to the visualize_data method
    visualizer.visualize_data(training_data, ideal_functions, test_results)  

if __name__ == "__main__":
    main()
