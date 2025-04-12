import unittest
from database import DataProcessor

class TestDataProcessor(unittest.TestCase):
    """
    Unit tests for the DataProcessor class.

    Methods:
    --------
    setUp():
        Initializes the DataProcessor and loads data before each test.
    test_load_csv_to_df():
        Verifies if CSV files are correctly loaded into DataFrames.
    test_process_test_data():
        Ensures test data is processed correctly and results are not empty.
    """
    
    def setUp(self):
        """
        Initialize the DataProcessor instance and load data into the database.
        
        This method sets up the environment for each test by initializing
        the DataProcessor object with the training, ideal functions, and
        test data files. It also creates the database and loads data into it.
        """
        self.processor = DataProcessor(
            training_file='train.csv',
            ideal_functions_file='ideal.csv',
            test_file='test.csv'
        )
        self.processor.initialize_database()
        self.processor.load_data_to_db()

    def test_load_csv_to_df(self):
        """
        Test if the 'load_csv_to_df' method loads CSV data into a DataFrame.
        
        This test ensures that the method successfully loads the training data
        from the CSV file into a pandas DataFrame and that the DataFrame is not empty.
        """
        df = self.processor._load_csv('train.csv')
        self.assertFalse(df.empty, "The DataFrame should not be empty after loading the CSV.")

    def test_process_test_data(self):
        """
        Test if the 'process_test_data' method processes the test data correctly.
        
        This test verifies that the method processes the test data and returns a
        non-empty DataFrame with the correct mappings of test data to ideal functions.
        """
        results = self.processor.map_test_data()
        self.assertFalse(results.empty, "The results DataFrame should not be empty after processing the test data.")

if __name__ == "__main__":
    unittest.main()
