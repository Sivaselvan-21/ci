def activation(yin):
    if yin > 0:
        return 1
    elif yin < 0:
        return -1
    else:
        return 0

# ----------- INPUT -----------

n = int(input("Enter number of inputs: "))
m = int(input("Enter number of samples: "))

X = []
T = []

print("\nEnter input values:")
for i in range(m):
    row = list(map(float, input(f"Sample {i+1}: ").split()))
    X.append(row)

print("\nEnter target values:")
for i in range(m):
    T.append(int(input(f"t{i+1}: ")))

weights = list(map(float, input(f"\nEnter {n} initial weights: ").split()))
bias = float(input("Enter bias: "))
alpha = float(input("Enter learning rate: "))
epochs = int(input("Enter number of epochs: "))

# ----------- TRAINING -----------

for epoch in range(epochs):
    print("\n" + "="*60)
    print(f"                    EPOCH {epoch+1}")
    print("="*60)

    # Header
    header = ""
    for i in range(n):
        header += f"{'x'+str(i+1):>8}"
    header += f"{'t':>8}{'yin':>10}{'y':>8}"

    for i in range(n):
        header += f"{'w'+str(i+1):>10}"
    header += f"{'bias':>10}"

    print(header)
    print("-" * len(header))

    all_correct = True

    for i in range(m):
        # Calculate yin
        yin = sum(X[i][j] * weights[j] for j in range(n)) + bias

        # Activation
        y = activation(yin)

        # Check correctness
        if y != T[i]:
            all_correct = False

        # Print row (BEFORE update)
        row = ""
        for val in X[i]:
            row += f"{val:>8.2f}"

        row += f"{T[i]:>8}{yin:>10.3f}{y:>8}"

        for w in weights:
            row += f"{w:>10.3f}"

        row += f"{bias:>10.3f}"

        print(row)

        # ----------- UPDATE RULE -----------
        for j in range(n):
            weights[j] += alpha * X[i][j] * T[i]

        bias += alpha * T[i]

    # Stop if all outputs correct
    if all_correct:
        print("\nAll outputs matched targets TRAINING STOPPED")
        break

# ----------- FINAL RESULT -----------

print("\n" + "="*40)
print("FINAL WEIGHTS AND BIAS")
print("="*40)

for i in range(n):
    print(f"w{i+1} = {weights[i]:.3f}")
print(f"bias = {bias:.3f}")
