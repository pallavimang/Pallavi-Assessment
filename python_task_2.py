import pandas as pd
import numpy as np
from datetime import time

# Question 1
def calculate_distance_matrix(df):
    distances = df.set_index(['id_start', 'id_end'])[['distance']]
    distance_matrix = pd.pivot_table(distances, values='distance', index='id_start', columns='id_end', fill_value=0)

    # Ensure the matrix is symmetric
    distance_matrix = distance_matrix + distance_matrix.T
    np.fill_diagonal(distance_matrix.values, 0)

    return distance_matrix

# Question 2
def unroll_distance_matrix(distance_matrix):
    unrolled_df = distance_matrix.unstack().reset_index(name='distance')
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]
    unrolled_df = unrolled_df.sort_values(['id_start', 'id_end']).reset_index(drop=True)
    return unrolled_df

# Question 3
def find_ids_within_ten_percentage_threshold(unrolled_df, reference_value):
    avg_distance = unrolled_df[unrolled_df['id_start'] == reference_value]['distance'].mean()
    threshold = 0.1 * avg_distance

    selected_ids = unrolled_df[(unrolled_df['distance'] >= avg_distance - threshold) &
                               (unrolled_df['distance'] <= avg_distance + threshold)]['id_start'].unique()

    return sorted(selected_ids)

# Question 4
def calculate_toll_rate(unrolled_df):
    toll_rates = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    for vehicle_type, rate in toll_rates.items():
        unrolled_df[vehicle_type] = unrolled_df['distance'] * rate

    return unrolled_df

# Question 5
def calculate_time_based_toll_rates(unrolled_df):
    def apply_discount(row):
        if row['start_day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            if time(0, 0) <= row['start_time'] < time(10, 0):
                return row['distance'] * 0.8
            elif time(10, 0) <= row['start_time'] < time(18, 0):
                return row['distance'] * 1.2
            else:
                return row['distance'] * 0.8
        else:
            return row['distance'] * 0.7

    unrolled_df['start_day'] = pd.to_datetime(unrolled_df['start_time']).dt.day_name()
    unrolled_df['end_day'] = pd.to_datetime(unrolled_df['end_time']).dt.day_name()

    unrolled_df['distance'] = unrolled_df.apply(apply_discount, axis=1)

    return unrolled_df

# Sample usage
if __name__ == "__main__":
    # Assuming 'dataset-3.csv' file is available in the 'datasets' folder
    dataset_3 = pd.read_csv('datasets/dataset-3.csv')

    # Question 1
    distance_matrix_result = calculate_distance_matrix(dataset_3)
    print("Question 1 Result:")
    print(distance_matrix_result)

    # Question 2
    unrolled_distance_matrix_result = unroll_distance_matrix(distance_matrix_result)
    print("\nQuestion 2 Result:")
    print(unrolled_distance_matrix_result)

    # Question 3 (Assuming reference_value is 1, change it accordingly)
    reference_value = 1
    ids_within_threshold_result = find_ids_within_ten_percentage_threshold(unrolled_distance_matrix_result, reference_value)
    print("\nQuestion 3 Result:")
    print(ids_within_threshold_result)

    # Question 4
    toll_rate_result = calculate_toll_rate(unrolled_distance_matrix_result)
    print("\nQuestion 4 Result:")
    print(toll_rate_result)

    # Question 5
    time_based_toll_rates_result = calculate_time_based_toll_rates(toll_rate_result)
    print("\nQuestion 5 Result:")
    print(time_based_toll_rates_result)
    print(time_based_toll_rates_result)
