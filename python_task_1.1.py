import pandas as pd
import numpy as np

# Question 1
def generate_car_matrix(df):
    unique_ids_1 = sorted(df['id_1'].unique())
    unique_ids_2 = sorted(df['id_2'].unique())

    car_matrix = pd.pivot_table(df, values='car', index='id_1', columns='id_2', fill_value=0)
    car_matrix = car_matrix.reindex(index=unique_ids_1, columns=unique_ids_2, fill_value=0)

    np.fill_diagonal(car_matrix.values, 0)
    return car_matrix

# Question 2
def get_type_count(df):
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])
    type_count = df['car_type'].value_counts().sort_index().to_dict()
    return type_count

# Question 3
def get_bus_indexes(df):
    mean_bus = 2 * df['bus'].mean()
    bus_indexes = df[df['bus'] > mean_bus].index.to_list()
    return sorted(bus_indexes)

# Question 4
def filter_routes(df):
    avg_truck_routes = df.groupby('route')['truck'].mean()
    selected_routes = avg_truck_routes[avg_truck_routes > 7].index.to_list()
    return sorted(selected_routes)

# Question 5
def multiply_matrix(df):
    modified_df = df.copy()
    modified_df[df > 20] *= 0.75
    modified_df[df <= 20] *= 1.25
    return modified_df.round(1)

# Question 6
def time_check(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['day_of_week'] = df['timestamp'].dt.day_name()

    completeness_check = df.groupby(['id', 'id_2'])['timestamp'].agg(lambda x: (x.max() - x.min()).total_seconds() == 7 * 24 * 3600).reset_index()
    return completeness_check.set_index(['id', 'id_2'])['timestamp']

# Sample usage
if __name__ == "__main__":
    # Read dataset-1.csv
    dataset_1 = pd.read_csv('datasets/dataset-1.csv')

    # Question 1
    car_matrix_result = generate_car_matrix(dataset_1)
    print("Question 1 Result:")
    print(car_matrix_result)

    # Question 2
    type_count_result = get_type_count(dataset_1)
    print("\nQuestion 2 Result:")
    print(type_count_result)

    # Question 3
    bus_indexes_result = get_bus_indexes(dataset_1)
    print("\nQuestion 3 Result:")
    print(bus_indexes_result)

    # Question 4
    routes_result = filter_routes(dataset_1)
    print("\nQuestion 4 Result:")
    print(routes_result)

    # Question 5 (Assuming car_matrix_result is the result from Question 1)
    modified_matrix_result = multiply_matrix(car_matrix_result)
    print("\nQuestion 5 Result:")
    print(modified_matrix_result)

    # Question 6
    # Assuming dataset-2.csv is available
    dataset_2 = pd.read_csv('datasets/dataset-2.csv')
    time_check_result = time_check(dataset_2)
    print("\nQuestion 6 Result:")
    print(time_check_result)
