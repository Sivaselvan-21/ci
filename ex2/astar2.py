import heapq
def create_graph():
    graph = {}
    heuristic = {}

    n = int(input("Enter number of vertices: "))

    print("\nEnter vertex name and heuristic value")
    for _ in range(n):
        node = input("Vertex: ")
        h = float(input(f"Heuristic h({node}): "))
        graph[node] = []
        heuristic[node] = h

    e = int(input("\nEnter number of directed edges: "))
    print("Enter edges (source destination cost):")

    for _ in range(e):
        u = input("Source: ")
        v = input("Destination: ")
        cost = float(input("Cost: "))

        if u in graph and v in graph:
            graph[u].append((v, cost))
        else:
            print("Invalid edge skipped")

    return graph, heuristic

def astar_all_paths(graph, heuristic, start, goal):
    open_list = []
    heapq.heappush(open_list, (heuristic[start], 0, start, [start]))

    goal_paths = []

    print("\n--- PATH-BASED A* SEARCH (ALL PATHS SHOWN) ---")

    step = 1
    while open_list:
        print(f"\nSTEP {step}")
        print("OPEN LIST:")
        for f, g, node, path in open_list:
            print(f"  Path: {'->'.join(path)}, g={g}, f={f}")

        f, g, current, path = heapq.heappop(open_list)

        print("\nEXPANDING:")
        print(f"  Path: {'->'.join(path)}")
        print(f"  g({current}) = {g}")
        print(f"  h({current}) = {heuristic[current]}")
        print(f"  f({current}) = {f}")

        if current == goal:
            print("  Goal reached ")
            goal_paths.append((path, g))
            step += 1
            continue

        for neighbor, cost in graph[current]:
            if neighbor in path:
                continue  # avoid cycles

            new_g = g + cost
            new_f = new_g + heuristic[neighbor]
            new_path = path + [neighbor]

            print(
                f"    Exploring {current}->{neighbor} | "
                f"g={new_g}, h={heuristic[neighbor]}, f={new_f}"
            )

            heapq.heappush(open_list, (new_f, new_g, neighbor, new_path))

        step += 1

    print("\n--- ALL GOAL PATHS FOUND ---")
    for p, c in goal_paths:
        print(f"Path: {'->'.join(p)}, Cost = {c}")

    if not goal_paths:
        print("No path exists")
        return None, float('inf')

    best = min(goal_paths, key=lambda x: x[1])

    print("\nBEST (MINIMUM COST) PATH")
    print(f"Path: {'->'.join(best[0])}")
    print(f"Final Cost = {best[1]}")

    return best

graph, heuristic = create_graph()

start = input("\nEnter START node: ")
goal = input("Enter GOAL node: ")

if start not in graph or goal not in graph:
    print("Invalid start or goal node")
else:
    astar_all_paths(graph, heuristic, start, goal)
      

