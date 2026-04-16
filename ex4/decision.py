import csv
import math
from collections import Counter

# 🔹 CHANGE THIS PATH TO YOUR CSV FILE
FILE_PATH = "Employee_Attrition_DataSet.csv"

# ================= LOAD DATASET =================
def load_dataset():
    data = []
    labels = []

    with open(FILE_PATH, newline='') as f:
        reader = csv.DictReader(f)

        # Remove target and ID column
        feature_names = [name for name in reader.fieldnames
                         if name != 'Attrition' and name != 'EmployeeID']

        for row in reader:
            row_data = {}

            for feature in feature_names:
                try:
                    row_data[feature] = float(row[feature])
                except:
                    row_data[feature] = row[feature]

            data.append(row_data)
            labels.append(row['Attrition'])

    return data, labels, feature_names


# ================= ENTROPY =================
def entropy(labels):
    total = len(labels)
    counts = Counter(labels)

    ent = 0.0
    for label, count in counts.items():
        p = count / total
        print(f"    Probability({label}) = {count}/{total} = {p:.4f}")
        ent -= p * math.log2(p)

    print(f"    Entropy = {ent:.4f}")
    return ent


# ================= CATEGORICAL GAIN =================
def gain_categorical(data, labels, feature):

    print("\n================================================")
    print(f"Feature: {feature}")
    print("================================================")

    subsets = {}

    for i, row in enumerate(data):
        val = row[feature]
        if val not in subsets:
            subsets[val] = []
        subsets[val].append(labels[i])

    print("\nTotal Dataset Entropy:")
    total_entropy = entropy(labels)

    weighted_entropy = 0

    for val, subset_labels in subsets.items():
        print(f"\n--- Value: {val} ---")
        count = len(subset_labels)
        yes_count = subset_labels.count("Yes")
        no_count = subset_labels.count("No")

        print(f"    Total samples = {count}")
        print(f"    Yes = {yes_count}")
        print(f"    No = {no_count}")

        subset_entropy = entropy(subset_labels)

        weight = count / len(labels)
        weighted_entropy += weight * subset_entropy

        print(f"    Weight = {count}/{len(labels)} = {weight:.4f}")
        print(f"    Weighted Entropy Contribution = {weight * subset_entropy:.4f}")

    gain = total_entropy - weighted_entropy

    print(f"\nWeighted Entropy = {weighted_entropy:.4f}")
    print(f"Information Gain for {feature} = {gain:.4f}")

    return gain


# ================= NUMERIC GAIN =================
def gain_numeric(data, labels, feature):

    print("\n================================================")
    print(f"Feature: {feature} (Numeric)")
    print("================================================")

    values = sorted(set(row[feature] for row in data))
    base_entropy = entropy(labels)

    best_gain = -1
    best_threshold = None

    for i in range(len(values) - 1):
        threshold = (values[i] + values[i + 1]) / 2

        left_labels = [labels[j] for j, row in enumerate(data)
                       if row[feature] <= threshold]
        right_labels = [labels[j] for j, row in enumerate(data)
                        if row[feature] > threshold]

        if not left_labels or not right_labels:
            continue

        print(f"\nTrying Threshold = {threshold:.2f}")

        print("\n  LEFT SIDE (<= threshold)")
        left_entropy = entropy(left_labels)

        print("\n  RIGHT SIDE (> threshold)")
        right_entropy = entropy(right_labels)

        weighted_entropy = (len(left_labels)/len(labels)) * left_entropy + \
                           (len(right_labels)/len(labels)) * right_entropy

        gain = base_entropy - weighted_entropy

        print(f"  Weighted Entropy = {weighted_entropy:.4f}")
        print(f"  Information Gain = {gain:.4f}")

        if gain > best_gain:
            best_gain = gain
            best_threshold = threshold

    print(f"\nBest Threshold for {feature} = {best_threshold}")
    print(f"Best Information Gain = {best_gain:.4f}")

    return best_gain, best_threshold


# ================= FIND ROOT =================
def find_root_node(data, labels, features):

    print("\n#############################")
    print("FINDING ROOT NODE")
    print("#############################\n")

    gains = {}
    thresholds = {}

    for feature in features:

        if isinstance(data[0][feature], float):
            gain, threshold = gain_numeric(data, labels, feature)
            thresholds[feature] = threshold
        else:
            gain = gain_categorical(data, labels, feature)
            thresholds[feature] = None

        gains[feature] = gain

    print("\n======================================")
    print("FINAL INFORMATION GAIN VALUES")
    print("======================================")

    for f, g in gains.items():
        print(f"{f} : {g:.4f}")

    root = max(gains, key=gains.get)

    print("\n======================================")
    print(f"ROOT NODE SELECTED: {root}")
    if thresholds[root] is not None:
        print(f"Best Threshold: {thresholds[root]:.2f}")
    print("======================================")

    return root


# ================= MAIN =================
data, labels, features = load_dataset()
root_node = find_root_node(data, labels, features)
