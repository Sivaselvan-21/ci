import math

def safe_log2(x: float) -> float:
    return math.log(x, 2) if x > 0 else 0.0

def print_dataset_table(rows, headers, title="DATASET PREVIEW"):
    print(f"\n--- {title} ---")
    widths = {h: len(h) for h in headers}
    for row in rows:
        for h in headers:
            widths[h] = max(widths[h], len(str(row[h])))
    
    header_line = " | ".join(f"{h:<{widths[h]}}" for h in headers)
    print(header_line)
    print("-" * len(header_line))
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
    for c in label_counts.values():
        p = c / total
        H += -p * safe_log2(p)
    return H, label_counts

def step_by_step_report(rows, attributes, target):
    all_headers = attributes + [target]
    print_dataset_table(rows, all_headers)
    
    n_total = len(rows)
    H_S, total_label_counts = entropy(rows, target)
    labels_sorted = sorted(total_label_counts.keys())

    print(f"Total examples: {n_total}")
    print(f"Entropy H(S) = {H_S:.4f}")
    print("-" * 40)

    ig_results = []

    for attr in attributes:
        print(f"\nATTRIBUTE: {attr}")
        groups = {}
        for row in rows:
            v = row[attr]
            groups.setdefault(v, []).append(row)

        # Print Distribution Table for the Attribute ---
        tbl_headers = [attr] + labels_sorted + ["Total"]
        attr_table_data = []
        
        for val in sorted(groups.keys()):
            subset = groups[val]
            _, counts_v = entropy(subset, target)
            row_data = {attr: val}
            for L in labels_sorted:
                row_data[L] = counts_v.get(L, 0)
            row_data["Total"] = len(subset)
            attr_table_data.append(row_data)
        
        print_dataset_table(attr_table_data, tbl_headers, title=f"Split Table for {attr}")
        print("Column wise total:",n_total)
        # --- Calculation Logic ---
        weighted_terms = []
        H_after = 0.0
        
        for val in sorted(groups.keys()):
            subset = groups[val]
            n_v = len(subset)
            H_v, counts_v = entropy(subset, target)
            
            weight = n_v / n_total
            H_after += weight * H_v
            parts_v = [f"-({counts_v.get(L,0)}/{n_v})*log2({counts_v.get(L,0)}/{n_v})" 
                       for L in labels_sorted if counts_v.get(L,0) > 0]
            
            print(f"H(S_{val}) = {' + '.join(parts_v) if parts_v else '0'} = {H_v:.4f}")
            weighted_terms.append(f"({n_v}/{n_total})*{H_v:.4f}")

        IG = H_S - H_after
        print(f"\nWeighted Entropy H(S|{attr}) = {' + '.join(weighted_terms)} = {H_after:.4f}")
        print(f"Information Gain IG(S, {attr}) = {H_S:.4f} - {H_after:.4f} = {IG:.4f}")
        ig_results.append((attr, IG))
        print("=" * 60)
    print("\n" + "="*40)
    print("SUMMARY OF INFORMATION GAIN")
    print("="*40)
    for attr, IG in ig_results:
        print(f"- {attr:15s} -> IG = {IG:.4f}")
    
    best_attr, best_IG = max(ig_results, key=lambda x: x[1])
    print(f"\nBest Attribute (Root Node) = {best_attr} (IG = {best_IG:.4f})")
def load_dataset_from_txt(filename):
    with open(filename, 'r') as f:
        lines = f.read().strip().splitlines()
    headers = [h.strip() for h in lines[0].split(',')]
    data = []
    for line in lines[1:]:
        values = [v.strip() for v in line.split(',')]
        data.append({headers[i]: values[i] for i in range(len(headers))})
    return data[:25], headers[:-1], headers[-1]

if __name__ == "__main__":
    try:
        filename = input("Enter dataset filename: ").strip()
        data, attributes, target = load_dataset_from_txt(filename)
        step_by_step_report(data, attributes, target)
    except Exception as e:
        print(f"Error: {e}")

