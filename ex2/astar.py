import heapq

# ---------------- INITIAL GRAPH CREATION ----------------

def create_initial_graph():
    graph = {}
    heuristic = {}

    n = int(input("Enter number of vertices: "))

    print("\nEnter vertex names and heuristic values:")
    for _ in range(n):
        node = input("Vertex name: ")
        h = float(input(f"Heuristic value for {node}: "))
        graph[node] = []
        heuristic[node] = h

    e = int(input("\nEnter number of edges: "))
    print("Enter edges (source destination cost):")

    for _ in range(e):
        u = input("Source: ")
        v = input("Destination: ")
        cost = float(input("Cost: "))

        if u in graph and v in graph:
            graph[u].append((v, cost))
        else:
            print("Invalid nodes, edge skipped")

    return graph, heuristic

# ---------------- GRAPH OPERATIONS ----------------

def add_node(graph, heuristic):
    node = input("Enter new node name: ")
    if node in graph:
        print("Node already exists")
        return

    h = float(input("Enter heuristic value: "))
    graph[node] = []
    heuristic[node] = h
    print("Node added")

def remove_node(graph, heuristic):
    node = input("Enter node to remove: ")
    if node not in graph:
        print("Node does not exist")
        return

    graph.pop(node)
    heuristic.pop(node, None)

    for n in graph:
        graph[n] = [(nbr, c) for nbr, c in graph[n] if nbr != node]

    print("Node and associated edges removed")

def add_edge(graph):
    u = input("Enter source node: ")
    v = input("Enter destination node: ")
    cost = float(input("Enter edge cost: "))

    if u in graph and v in graph:
        graph[u].append((v, cost))
        print("Edge added")
    else:
        print("Invalid nodes")

def display_graph(graph):
    print("\nAdjacency List:")
    for node in graph:
        print(f"{node} : {graph[node]}")

# ---------------- A* SEARCH ----------------

def astar(graph, heuristic, start, goal):
    open_list = []
    heapq.heappush(open_list, (heuristic[start], start))

    g_cost = {start: 0}
    parent = {start: None}

    print("\n--- A* SEARCH TRACE ---")

    while open_list:
        f_current, current = heapq.heappop(open_list)

        print(f"\nExpanding node: {current}")
        print(f"g({current}) = {g_cost[current]}")
        print(f"h({current}) = {heuristic[current]}")
        print(f"f({current}) = {f_current}")

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1], g_cost[goal]

        print("Exploring neighbors:")

        for neighbor, cost in graph[current]:
            new_g = g_cost[current] + cost
            h = heuristic[neighbor]
            f = new_g + h

            print(
                f"  Neighbor: {neighbor}, "
                f"Edge cost: {cost}, "
                f"g({neighbor}) = {new_g}, "
                f"h({neighbor}) = {h}, "
                f"f({neighbor}) = {f}"
            )

            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                parent[neighbor] = current
                heapq.heappush(open_list, (f, neighbor))
                print(f"Updated & added to OPEN list")
            else:
                print(f" Not updated (higher cost)")

        print("\nCurrent OPEN list:")
        for item in open_list:
            print(f"  Node: {item[1]}, f(n): {item[0]}")

    return None, float('inf')


def run_astar(graph, heuristic):
    start = input("Enter start node: ")
    goal = input("Enter goal node: ")

    if start not in graph or goal not in graph:
        print("Invalid start or goal node")
        return

    path, cost = astar(graph, heuristic, start, goal)

    if path is None:
        print("No path found")
    else:
        print("Path:", path)
        print("Final Cost:", cost)

def menu(graph, heuristic):
    while True:
        print("\n--- MENU ---")
        print("1. Add Node")
        print("2. Remove Node")
        print("3. Add Edge")
        print("4. Display Adjacency List")
        print("5. A* Search")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_node(graph, heuristic)
        elif choice == '2':
            remove_node(graph, heuristic)
        elif choice == '3':
            add_edge(graph)
        elif choice == '4':
            display_graph(graph)
        elif choice == '5':
            run_astar(graph, heuristic)
        elif choice == '6':
            print("Program terminated")
            break
        else:
            print("Invalid choice")


graph, heuristic = create_initial_graph()
menu(graph, heuristic)
