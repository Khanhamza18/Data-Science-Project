import pandas as pd
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import numpy as np
from sklearn.metrics import mean_squared_error

class DataLoadError(Exception):
    """Custom exception for errors encountered during data loading."""
    pass

class DataProcessor:
    """
    A class to handle training data, ideal functions, and test data processing.

    Attributes:
    -----------
    training_file : str
        Path to the training data CSV file.
    ideal_functions_file : str
        Path to the ideal functions CSV file.
    test_file : str
        Path to the test data CSV file.
    db_file : str
        Path to the SQLite database file (default is 'data.db').
    """

    def __init__(self, training_file, ideal_functions_file, test_file, db_file='data.db'):
        """
        Initializes the DataProcessor with file paths for training, ideal functions, and test data.
        """
        self.training_file = training_file
        self.ideal_functions_file = ideal_functions_file
        self.test_file = test_file
        self.db_file = db_file

    def _load_csv(self, file_path):
        """
        Loads a CSV file into a pandas DataFrame.

        Parameters:
        ----------
        file_path : str
            Path to the CSV file.

        Returns:
        -------
        DataFrame
            Loaded data as a pandas DataFrame.

        Raises:
        ------
        DataLoadError
            Raised when loading CSV fails.
        """
        try:
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.lower()  # Ensure column names are lowercase
            return df
        except Exception as e:
            raise DataLoadError(f"Failed to load {file_path}: {str(e)}")

    def initialize_database(self):
        """Creates SQLite database tables for training data, ideal functions, and test data."""
        engine = db.create_engine(f'sqlite:///{self.db_file}')
        metadata = db.MetaData()

        # Define the database schema
        self.training_data_table = db.Table(
            'training_data', metadata,
            db.Column('x', db.Float),
            *(db.Column(f'y{i+1}', db.Float) for i in range(4))
        )

        self.ideal_functions_table = db.Table(
            'ideal_functions', metadata,
            db.Column('x', db.Float),
            *(db.Column(f'y{i+1}', db.Float) for i in range(50))
        )

        self.test_data_table = db.Table(
            'test_data', metadata,
            db.Column('x', db.Float),
            db.Column('y', db.Float),
            db.Column('delta_y', db.Float),
            db.Column('ideal_func_no', db.Integer)
        )

        metadata.create_all(engine)
        self.engine = engine

    def load_data_to_db(self):
        """Loads the training and ideal function data into the SQLite database."""
        # Load training and ideal function data
        training_df = self._load_csv(self.training_file)
        ideal_df = self._load_csv(self.ideal_functions_file)

        # Rename training data columns for consistency
        training_df.columns = ['x', 'y1', 'y2', 'y3', 'y4']

        # Insert data into the database
        training_df.to_sql('training_data', self.engine, if_exists='replace', index=False)
        ideal_df.to_sql('ideal_functions', self.engine, if_exists='replace', index=False)

    def map_test_data(self):
        """
        Maps test data to the best-fitting ideal functions based on mean squared error.

        Returns:
        -------
        DataFrame
            A pandas DataFrame with test data, ideal function number, and deviation.
        """
        test_df = self._load_csv(self.test_file)
        ideal_df = pd.read_sql('SELECT * FROM ideal_functions', self.engine).set_index('x')
        training_df = pd.read_sql('SELECT * FROM training_data', self.engine)

        best_fit_funcs = []
        for i in range(1, 5):
            best_func = self._find_best_fit(training_df[f'y{i}'], ideal_df)
            best_fit_funcs.append(best_func)

        results = []
        for _, row in test_df.iterrows():
            best_fit, min_deviation = self._find_best_match(row['x'], row['y'], best_fit_funcs, ideal_df, training_df)
            results.append({'x': row['x'], 'y': row['y'], 'delta_y': min_deviation, 'ideal_func_no': best_fit})

        results_df = pd.DataFrame(results)
        results_df.to_sql('test_data', self.engine, if_exists='replace', index=False)
        return results_df

    def _find_best_fit(self, training_series, ideal_df):
        """
        Finds the best-fitting ideal function based on minimum mean squared error (MSE).

        Parameters:
        ----------
        training_series : pandas Series
            The training data for a specific 'y' column.
        ideal_df : DataFrame
            The ideal function DataFrame.

        Returns:
        -------
        str
            Column name of the ideal function with the smallest MSE.
        """
        min_mse = float('inf')
        best_func = None
        for col in ideal_df.columns:
            mse = mean_squared_error(training_series, ideal_df[col])
            if mse < min_mse:
                min_mse = mse
                best_func = col
        return best_func

    def _find_best_match(self, x_val, y_val, best_fit_funcs, ideal_df, training_df):
        """
        Finds the best-fitting ideal function for a test data point.

        Parameters:
        ----------
        x_val : float
            The x value of the test data point.
        y_val : float
            The y value of the test data point.
        best_fit_funcs : list
            List of best fit ideal functions for each training function.
        ideal_df : DataFrame
            The ideal function DataFrame.
        training_df : DataFrame
            The training data DataFrame.

        Returns:
        -------
        tuple
            Best-fitting ideal function number and the deviation.
        """
        min_deviation = float('inf')
        best_fit = None
        for idx, ideal_func in enumerate(best_fit_funcs):
            deviation = abs(y_val - ideal_df.loc[x_val, ideal_func])
            max_allowed_deviation = np.sqrt(2) * abs(training_df[f'y{idx+1}'] - ideal_df[ideal_func]).max()
            if deviation <= max_allowed_deviation and deviation < min_deviation:
                min_deviation = deviation
                best_fit = idx + 1
        return best_fit, min_deviation
