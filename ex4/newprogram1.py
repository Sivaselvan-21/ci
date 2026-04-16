import math

def safe_log2(x: float) -> float:
    return math.log(x, 2) if x > 0 else 0.0

def print_dataset_table(rows, headers):
    """Prints the dataset in a formatted table."""
    print("\n DATASET PREVIEW")
    # Calculate column widths
    widths = {h: len(h) for h in headers}
    for row in rows:
        for h in headers:
            widths[h] = max(widths[h], len(str(row[h])))
    
    # Print Header
    header_line = " | ".join(f"{h:<{widths[h]}}" for h in headers)
    print(header_line)
    print("-" * len(header_line))
    
    # Print Rows
    for row in rows:
        print(" | ".join(f"{str(row[h]):<{widths[h]}}" for h in headers))
    print()

def entropy(rows, target):
    label_counts = {}
    for row in rows:
        y = row[target]
        label_counts[y] = label_counts.get(y, 0) + 1
    total = len(rows)
    H = 0.0
    probs = []
    for c in label_counts.values():
        p = c / total
        probs.append(p)
        H += -p * safe_log2(p)
    return H, label_counts, probs

def unique_values(rows, attr):
    seen = set()
    vals = []
    for row in rows:
        v = row[attr]
        if v not in seen:
            seen.add(v)
            vals.append(v)
    return vals

def split_by_value(rows, attr):
    groups = {}
    for row in rows:
        v = row[attr]
        groups.setdefault(v, []).append(row)
    return groups

def step_by_step_report(rows, attributes, target):
    # --- NEW: Print the dataset table first ---
    all_headers = attributes + [target]
    print_dataset_table(rows, all_headers)
    
    n = len(rows)
    H_S, label_counts, _ = entropy(rows, target)
    
    print(f"Total examples: {n}")
    labels_sorted = sorted(label_counts.keys())
    parts = []
    for L in labels_sorted:
        c = label_counts[L]
        p = c / n
        parts.append(f"-({c}/{n})*log2({c}/{n})")
    
    print("Entropy H(S) = " + " + ".join(parts) + f" = {H_S:.4f}")
    print("Class counts: " + ", ".join([f"{L}={label_counts[L]}" for L in labels_sorted]))
    print()

    ig_results = []
    for attr in attributes:
        print(f"Attribute: {attr}")
        groups = split_by_value(rows, attr)
        weighted_terms = []
        H_after = 0.0
        
        for v in unique_values(rows, attr):
            subset = groups[v]
            n_v = len(subset)
            H_v, counts_v, _ = entropy(subset, target)
            weight = n_v / n
            H_after += weight * H_v
            
            parts_v = []
            for L in labels_sorted:
                c = counts_v.get(L, 0)
                if c == 0: continue
                parts_v.append(f"-({c}/{n_v})*log2({c}/{n_v})")
            
            print(f"  Value {v}: |S_{v}|={n_v} -> counts: " + ", ".join([f"{L}={counts_v.get(L,0)}" for L in labels_sorted]))
            if parts_v:
                print(f"    H(S_{v}) = " + " + ".join(parts_v) + f" = {H_v:.4f}")
            else:
                print(f"    H(S_{v}) = 0.0000")
            weighted_terms.append(f"({n_v}/{n})*{H_v:.4f}")
        
        print("  Weighted entropy H(S|{0}) = {1} = {2:.4f}".format(attr, " + ".join(weighted_terms), H_after))
        IG = H_S - H_after
        print(f"  Information Gain IG(S, {attr}) = {H_S:.4f} - {H_after:.4f} = {IG:.4f}\n")
        ig_results.append((attr, IG))

    print("=" * 40)
    print(" SUMMARY OF INFORMATION GAIN ")
    print("=" * 40)
    for attr, IG in ig_results:
        print(f"- {attr:15s} -> IG = {IG:.4f}")
    
    best_attr, best_IG = max(ig_results, key=lambda x: x[1])
    print(f"\nBest Attribute (Root Node) = {best_attr} (IG = {best_IG:.4f})")
    print("=" * 40 + "\n")

def load_dataset_from_txt(filename):
    data = []
    with open(filename, 'r') as f:
        lines = f.read().strip().splitlines()
        headers = [h.strip() for h in lines[0].split(',')]
        for line in lines[1:]:
            values = [v.strip() for v in line.split(',')]
            row = {headers[i]: values[i] for i in range(len(headers))}
            data.append(row)
    return data, headers[:-1], headers[-1]

if __name__ == "__main__":
    try:
        filename = input("Enter dataset filename (e.g., dataset.txt): ").strip()
        data, attributes, target = load_dataset_from_txt(filename)
        step_by_step_report(data, attributes, target)
    except FileNotFoundError:
        print("File not found. Please ensure the filename is correct.")

