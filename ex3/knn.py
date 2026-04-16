import math
import csv
from collections import defaultdict
FILE_PATH = "./Smartphone_usage.csv"
def load_dataset():
    data = []
    labels = []
    with open(FILE_PATH, mode='r') as f: 
        reader = csv.DictReader(f, delimiter='\t') 
        
        for row in reader:
            try:
                # Use .strip() on keys to ignore hidden whitespace
                row = {k.strip(): v for k, v in row.items()}
                
                labels.append(row['Device_Type'])
                data.append([
                    float(row['Daily_Phone_Hours']), 
                    float(row['Social_Media_Hours'])
                ])
            except KeyError as e:
                print(f"Missing column: {e}")
                return [], []
    return data, labels

def min_max_normalize(data):
    cols = list(zip(*data))
    min_vals = [min(col) for col in cols]
    max_vals = [max(col) for col in cols]

    normalized = []
    for row in data:
        new_row = []
        for i in range(len(row)):
            if (max_vals[i] - min_vals[i]) != 0:
                val = (row[i] - min_vals[i]) / (max_vals[i] - min_vals[i])
            else:
                val = 0.0
            new_row.append(val)
        normalized.append(new_row)

    return normalized
def distance_metric(p1, p2, r):
    if r == 1:
        return sum(abs(a - b) for a, b in zip(p1, p2))
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))
def knn(train_data, train_labels, test_point, k, r):
    distances = []

    for i in range(len(train_data)):
        # Skip the test point itself
        if train_data[i] == test_point:
            continue
        d = distance_metric(train_data[i], test_point, r)
        distances.append((d, train_labels[i], i))

    distances.sort(key=lambda x: x[0])
    neighbors = distances[:k]
    unweighted_votes = defaultdict(int)
    for d, cls, idx in neighbors:
        unweighted_votes[cls] += 1

    return neighbors, unweighted_votes

def print_dataset(data, labels, title):
    print(f"\n--- {title} ---")
    print("Ind | [Daily Phone Hours,Social Media Hours] | Class")
    for i in range(len(data)):
        formatted = list(map(lambda x: f"{x:.4f}", data[i]))
        print(f"{i+1:3} | {formatted} | {labels[i]}")
data, labels = load_dataset()

if not data:
    exit()

data_norm = min_max_normalize(data)
print_dataset(data[:30], labels[:30], "ORIGINAL (SELECTED COLS)")
print_dataset(data_norm[:30], labels[:30], "NORMALIZED (SELECTED COLS)")
test_index = 251
test_point = data_norm[test_index]

while True:
    try:
        k = int(input("\nEnter the value of k (number of neighbors): "))
        if k <= 0 or k >= len(data):
            print("k must be positive and less than dataset size. Try again.")
            continue
        break
    except ValueError:
        print("Please enter a valid integer for k.")

r = 2  # Euclidean distancie

neighbors, unweighted = knn(data_norm, labels, test_point, k, r)

print(f"\nResults for Index {test_index} (Test Point: {[f'{x:.4f}' for x in test_point]}):")
print("\n--- UNWEIGHTED RANKING ---")
print(f"{'Rank':<5} | {'Distance':<10} | {'Class':<10}")
print("-" * 50)

for i, (d, cls, idx) in enumerate(neighbors, start=1):
    print(f"{i:<5} | {d:<10.4f} | {cls:<10}")
print("\n--- WEIGHTED VOTING CALCULATION (1/d^2) ---")
print(f"{'Rank':<5} | {'Class':<10} | {'Distance':<10} | {'1/d^2 Weight':<15}")
print("-" * 65)

class_sums = defaultdict(float)
epsilon = 1e-3  # To avoid division by zero

for i, (d, cls, idx) in enumerate(neighbors, start=1):
    weight = 1 / (d**2 + epsilon)
    class_sums[cls] += weight
    print(f"{i:<5} | {cls:<10} | {d:<10.4f} | {weight:<15.4f}")

print("\n--- SUMMED WEIGHTS PER CLASS ---")
for cls, total in class_sums.items():
    print(f"Class {cls:<10} | Total Weight = {total:.4f}")
print("\n" + "="*35)
print("FINAL UNWEIGHTED CLASS:", max(unweighted, key=unweighted.get))
print("FINAL WEIGHTED CLASS:  ", max(class_sums, key=class_sums.get))
print("="*35)
