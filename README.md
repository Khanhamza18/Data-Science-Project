# Data Processor and Visualizer

> **Project Goal**  
> This project aims to process and visualize training data, ideal functions, and test data using Python. The application is structured around three key components.

## Key Components

| Component | Description |
| --- | --- |
| DataProcessor | - Loads data from CSV files.- Stores data in an SQLite database.- Processes test data to find best-fitting ideal functions. |
| DataVisualizer | - Provides visualizations of processed data through Bokeh plots. |
| Unit Tests | - Ensures functionality of the DataProcessor class through a series of test cases. |

* * *

## Contents

1.  **[Project Structure](#project-structure)**
2.  **[Dependencies](#dependencies)**
3.  **[Installation Guide](#installation-guide)**
4.  **[Usage Instructions](#usage-instructions)**
5.  **[Testing](#testing)**

* * *


## Dependencies

This project requires several libraries for proper functionality:

*   **pandas**: Data manipulation and CSV handling.
*   **sqlalchemy**: SQLite database interaction.
*   **numpy**: Numerical operations support.
*   **sklearn**: Mean squared error calculations for function fitting.
*   **bokeh**: For creating interactive visualizations.
*   **unittest**: To facilitate unit testing.

### Installation Command

To install all required dependencies, run:




`pip install pandas sqlalchemy numpy scikit-learn bokeh`

* * *

## Installation Guide

### Steps to Set Up

1.  **Clone the Repository**:
    
    
    `git clone https://github.com/your-repo/data-processor-visualizer.git  cd data-processor-visualizer`
    
2.  **Prepare Your CSV Files**:
    
    Ensure you have the following files in the root directory:
    
    *   **`train.csv`**: Contains training data.
        
    *   **`ideal.csv`**: Contains ideal functions.
        
    *   **`test.csv`**: Contains test data.
        
    
    > **Note:** You can create your own CSV files if necessary.
    
3.  **Run the Main Script**:
    
    Execute the following command to load data, process it, and visualize results:

    
    `python main.py`
    

* * *

## Usage Instructions

### 1\. Data Processing:

*   The `DataProcessor` class manages the loading of data, creating the SQLite database, and processing the test data.
*   You can specify the file paths for the training data, ideal functions, and test data in `main.py` when initializing the `DataProcessor`.

> The processed results are saved in the `test_data` table of the SQLite database.

### 2\. Data Visualization:

*   The `DataVisualizer` class (found in `visualizer.py`) is responsible for creating visual representations of the data.
*   It generates plots to compare training data and ideal functions, as well as visualizing test data mappings.

### 3\. Output:

*   After executing `main.py`, the visualizations are saved in an HTML file, which will automatically open in your default web browser.

* * *

## Testing

The `test.py` file includes unit tests designed to validate the functionality of the `DataProcessor` class.

### To Run Tests:

1.  Ensure the `unittest` library is available (part of Python's standard library).
    
2.  Execute the tests with the following command:
    
    
    `python test.py`
    

> **Tests Include:**
> 
> *   Successful loading of CSV files into pandas DataFrames.
> *   Accurate processing of test data, ensuring that results are populated.