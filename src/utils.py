def load_data(file_path):
    """Load well log data from a specified file path."""
    import pandas as pd
    return pd.read_csv(file_path)

def save_data(data, file_path):
    """Save data to a specified file path."""
    import pandas as pd
    data.to_csv(file_path, index=False)

def normalize_data(data):
    """Normalize the well log data."""
    return (data - data.min()) / (data.max() - data.min())

def split_data(data, train_size=0.8):
    """Split the data into training and testing sets."""
    from sklearn.model_selection import train_test_split
    return train_test_split(data, train_size=train_size)