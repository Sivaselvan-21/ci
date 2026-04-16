import heapq
def create_initial_graph():
   
    graph = {}

    n = int(input("Enter number of vertices: "))

    print("\nEnter vertex names:")
    for _ in range(n):
        node = input("Vertex name: ")
        graph[node] = []

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

    return graph

def add_node(graph):
    node = input("Enter new node name: ")
    if node in graph:
        print("Node already exists")
        return
    graph[node] = []
    print("Node added")

def remove_node(graph):
    node = input("Enter node to remove: ")
    if node not in graph:
        print("Node does not exist")
        return

    graph.pop(node)

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


# ---------------- UNIFORM COST SEARCH ----------------

def ucs(graph, start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))

    g_cost = {start: 0}
    parent = {start: None}

    print("\n--- UCS TRACE ---")

    while open_list:
        current_cost, current = heapq.heappop(open_list)

        print(f"\nExpanding node: {current}")
        print(f"g({current}) = {current_cost}")

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1], g_cost[goal]

        print("Exploring neighbors:")

        for neighbor, cost in graph[current]:
            new_cost = g_cost[current] + cost

            print(
                f"  Neighbor: {neighbor}, "
                f"Edge cost: {cost}, "
                f"g({neighbor}) = {new_cost}"
            )

            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(open_list, (new_cost, neighbor))
                print("Updated & added to OPEN list")
            else:
                print("Not updated (higher cost)")

        print("\nCurrent OPEN list:")
        for cost, node in open_list:
            print(f"  Node: {node}, g(n): {cost}")

    return None, float('inf')


def run_ucs(graph):
    start = input("Enter start node: ")
    goal = input("Enter goal node: ")

    if start not in graph or goal not in graph:
        print("Invalid start or goal node")
        return

    path, cost = ucs(graph, start, goal)

    if path is None:
        print("No path found")
    else:
        print("\n--- RESULT ---")
        print("Path:", path)
        print("Final Cost:", cost)


def menu(graph):
    while True:
        print("\n--- MENU ---")
        print("1. Add Node")
        print("2. Remove Node")
        print("3. Add Edge")
        print("4. Display Adjacency List")
        print("5. Uniform Cost Search (UCS)")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_node(graph)
        elif choice == '2':
            remove_node(graph)
        elif choice == '3':
            add_edge(graph)
        elif choice == '4':
            display_graph(graph)
        elif choice == '5':
            run_ucs(graph)
        elif choice == '6':
            print("Program terminated")
            break
        else:
            print("Invalid choice")


graph = create_initial_graph()
menu(graph)
