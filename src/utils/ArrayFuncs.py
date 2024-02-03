import numpy as np


def find_closest_index(val, ar):
    ar = np.array(ar, dtype="float")
    val=float(val)
    
    closest_index = 0
    closest_diff = np.abs(ar[0] - val)
    for i, num in enumerate(ar):
        diff = np.abs(num - val)
        if diff < closest_diff:
            closest_diff = diff
            closest_index = i

    return closest_index


# Define the elegant averaging function
def average_every_n_elements(arr, n):
    averages = []  # To store the average of each chunk
    for start in range(0, len(arr), n):
        chunk = arr[start:start+n]  # Get n elements from the array
        averages.append(np.mean(chunk))  # Calculate and store the average of the chunk
    return averages

