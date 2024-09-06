import pandas as pd

def json_flatton_data(data):
    def flatten_json(y):
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], a + '_')
            else:
                out[name[:-1]] = x

        flatten(y)
        return out

    flattened_data = []
    try:
        for entry in data:
            for date, nested_data in entry.items():
                # Flatten the nested data
                flat_data = flatten_json(nested_data)
                # Add the date to the flattened data
                flat_data['date'] = date
                flattened_data.append(flat_data)
        flattened_data = pd.DataFrame(flattened_data)
        flattened_data = flattened_data.set_index('date')
    except KeyError: 
        pass
    return flattened_data


def transform_to_percentage(df, columns =  None):
    """
    Transforms specified columns in a DataFrame to percentage based on their row-wise sum.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data
    columns (list): List of column names to transform

    Returns:
    pd.DataFrame: DataFrame with transformed percentage columns
    """
    df_copy = df.copy()
    if columns is None:
        columns = df_copy.columns
    total = df_copy[columns].sum(axis=1)
    for column in columns:
        df_copy[column] = df_copy[column] / total * 100
    return df_copy

