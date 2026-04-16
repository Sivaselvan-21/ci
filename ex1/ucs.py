import heapq

vertices = [[0 for _ in range(15)] for _ in range(15)]
cost = [[0 for _ in range(15)] for _ in range(15)]

noofverts = int(input("Enter number of vertices: "))
noofedges = int(input("Enter number of edges: "))

nodes = []
for _ in range(noofverts):
    nodes.append(int(input("Enter vertex: ")))

start = int(input("Enter start node: "))
goal = int(input("Enter goal node: "))

order = input("Traversal order (L/R): ").upper()

for _ in range(noofedges):
    u = int(input("From: "))
    v = int(input("To: "))
    w = int(input("Cost: "))
    vertices[u][v] = 1
    vertices[v][u] = 1
    cost[u][v] = w
    cost[v][u] = w

def UCS(start, goal):
    fringe = []
    explored = set()
    best_cost = {start: 0}

    heapq.heappush(fringe, (0, start))
    print("\nINITIAL FRINGE:", fringe)

    while fringe:
        curr_cost, current = heapq.heappop(fringe)
        print(f"\nPOP  → {current} (Cost = {curr_cost})")

        if current in explored:
            continue

        if current == goal:
            print("\n🎯 GOAL FOUND WITH COST:", curr_cost)
            return

        explored.add(current)

        if order == 'L':
            neighbors = nodes
        else:
            neighbors = reversed(nodes)

        for i in neighbors:
            if cost[current][i] > 0 and i not in explored:
                new_cost = curr_cost + cost[current][i]

                if i not in best_cost or new_cost < best_cost[i]:
                    best_cost[i] = new_cost
                    heapq.heappush(fringe, (new_cost, i))
                    print(f"PUSH {i} (Cost = {new_cost})")
                    print("FRINGE:", fringe)

    print("\nGOAL NOT REACHABLE")

UCS(start, goal)
