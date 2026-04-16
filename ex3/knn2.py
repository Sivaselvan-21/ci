import math
import csv
import random # 1. Import random
from collections import defaultdict

# ================= FILE PATH =================
# Ensure this path is correct
FILE_PATH = './Employee_Attrition_DataSet.csv'

# ================= LOAD DATASET =================
def load_dataset():
    data = []
    labels = []
    try:
        with open(FILE_PATH, mode='r') as f:
            reader = csv.DictReader(f, delimiter='\t') 
            field_map = {name.strip().lower(): name for name in reader.fieldnames}
            
            
            attr_col = field_map.get('attrition') 
            age_col = field_map.get('age')
            job_col = field_map.get('joblevel')
            
            if not all([attr_col, age_col, job_col]):
                print(f"Error: Could not find columns. Found: {reader.fieldnames}")
                return [], []
            
            for row in reader:
                labels.append(row[attr_col])
                data.append([float(row[age_col]), float(row[job_col])])
                
    except FileNotFoundError:
        print(f"Error: File not found at {FILE_PATH}")
        return [], []
        
    return data, labels

# ================= NORMALIZATION =================
def min_max_normalize(data):
    if not data: return []
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

# ================= DISTANCE FUNCTION =================
def distance_metric(p1, p2, r):
    if r == 1:
        return sum(abs(a - b) for a, b in zip(p1, p2))
    # Euclidean distance (r=2)
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

# ================= KNN FUNCTION =================
def knn(train_data, train_labels, test_point, k, r):
    distances = []
    for i in range(len(train_data)):
       
        d = distance_metric(train_data[i], test_point, r)
        distances.append((d, train_labels[i]))
    
    
    distances.sort(key=lambda x: x[0])
    
    
    neighbors = distances[:k]
    
    
    unweighted_votes = defaultdict(int)
    for d, cls in neighbors:
        unweighted_votes[cls] += 1
        
    return neighbors, unweighted_votes

# ================= PRINT DATASET =================
def print_dataset(data, labels, title):
    print(f"\n--- {title} ---")
    print(f" Idx | [Age, JobLevel] | Class ")
    
    for i in range(min(len(data), 10)):
        formatted = list(map(lambda x: f"{x:.4f}", data[i]))
        print(f"{i+1:3} | {formatted} | {labels[i]}")
    if len(data) > 10: print("...")

# ================= MAIN EXECUTION =================


raw_data, raw_labels = load_dataset()
if not raw_data:
    exit()

data_norm = min_max_normalize(raw_data)
combined = list(zip(data_norm, raw_labels))
random.shuffle(combined) 
data_norm, raw_labels = zip(*combined)
data_norm = list(data_norm)
raw_labels = list(raw_labels)
split_idx = 250
train_data = data_norm[:split_idx]
train_labels = raw_labels[:split_idx]
# Pick a random point from th REMAINING data to ensure it's not in training
test_point = data_norm[split_idx + 1] 
actual_class = raw_labels[split_idx + 1]

print(f"Dataset Size: {len(data_norm)}")
print(f"Training Size: {len(train_data)}")
print(f"Test Point Features: {[f'{x:.4f}' for x in test_point]}")
print(f"Actual Test Class: {actual_class}")

# 5. Ask user for k
while True:
    try:
        k = int(input(f"\nEnter the value of k (1-{len(train_data)-1}): "))
        if k <= 0 or k >= len(train_data):
            print(f"k must be positive and less than {len(train_data)}. Try again.")
            continue
        break
    except ValueError:
        print("Please enter a valid integer for k.")

r = 2 # Euclidean distance
neighbors, unweighted = knn(train_data, train_labels, test_point, k, r)

print(f"\nResults for Test Point (Randomly Selected):")

# ---------------- NEIGHBOR RANKING ----------------
print("\n--- NEIGHBOR RANKING ---")
print(f"{'Rank':<5} | {'Distance':<10} | {'Class':<10}")
print("-" * 35)
for i, (d, cls) in enumerate(neighbors, start=1):
    print(f"{i:<5} | {d:<10.4f} | {cls:<10}")

# ---------------- WEIGHTED VOTING ----------------
print("\n--- WEIGHTED VOTING CALCULATION (1/d^2) ---")
print(f"{'Rank':<5} | {'Class':<10} | {'Distance':<10} | {'1/d^2 Weight':<15}")
print("-" * 65)
class_sums = defaultdict(float)


for i, (d, cls) in enumerate(neighbors, start=1):
    # If distance is extremely small, set weight to a high number
    weight = 1 / (d**2)
    class_sums[cls] += weight
    print(f"{i:<5} | {cls:<10} | {d:<10.4f} | {weight:<15.4f}")

print("\n--- SUMMED WEIGHTS PER CLASS ---")
for cls, total in class_sums.items():
    print(f"Class {cls:<10} | Total Weight = {total:.4f}")

# ---------------- FINAL RESULT ----------------
print("\n" + "="*35)
print("FINAL UNWEIGHTED CLASS:", max(unweighted, key=unweighted.get))
print("FINAL WEIGHTED CLASS:", max(class_sums, key=class_sums.get))
print("Actual Class:", actual_class)
print("="*35)

