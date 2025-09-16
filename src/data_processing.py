def load_well_log_data(file_path):
    """Load well log data from a specified file path."""
    import pandas as pd
    
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def clean_well_log_data(data):
    """Clean the well log data by handling missing values and duplicates."""
    if data is not None:
        data = data.drop_duplicates()
        data = data.fillna(method='ffill')  # Forward fill for missing values
        return data
    return None

def normalize_well_log_data(data):
    """Normalize the well log data to a range of [0, 1]."""
    if data is not None:
        return (data - data.min()) / (data.max() - data.min())
    return None

def transform_well_log_data(data, transformation_func):
    """Apply a transformation function to the well log data."""
    if data is not None and callable(transformation_func):
        return transformation_func(data)
    return None