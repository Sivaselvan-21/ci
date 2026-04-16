graph = {}

def addnode(node):
    if node in graph:
        print(f"Node '{node}' already exists.")
    else:
        graph[node] = set()
        print(f"Node '{node}' added.")

def removenode(node):
    if node not in graph:
        print(f"Node '{node}' does not exist.")
        return
    # Remove node from neighbors' adjacency sets
    for neighbor in graph[node]:
        graph[neighbor].remove(node)
    # Remove the node itself
    del graph[node]
    print(f"Node '{node}' and associated edges removed.")

def addedge(node1, node2):
    if node1 not in graph or node2 not in graph:
        print("Both nodes must exist before adding an edge.")
        return
    graph[node1].add(node2)
    graph[node2].add(node1)
    print(f"Edge added between '{node1}' and '{node2}'.")

def displayadjacency():
    print("\nAdjacency List:")
    for node in graph:
        neighbors = ', '.join(sorted(graph[node]))
        print(f"{node}: {neighbors if neighbors else 'No neighbors'}")

def BFS(start, goal, order='L'):
    if start not in graph or goal not in graph:
        print("Start or goal node not found.")
        return
    visited = set()
    fringe = [start]
    path = []

    print("\nINITIAL FRINGE:", fringe)

    while fringe:
        current = fringe.pop(0)
        print("\nPOP", current)
        print("FRINGE:", fringe)

        if current in visited:
            continue

        path.append(current)
        print("\nPath:", "->".join(path))

        visited.add(current)

        if current == goal:
            print("\nGOAL FOUND")
            return

        neighbors = sorted(graph[current])
        if order == 'R':
            neighbors.reverse()

        for neighbor in neighbors:
            if neighbor not in visited and neighbor not in fringe:
                fringe.append(neighbor)
                print("PUSH", neighbor)
                print("FRINGE:", fringe)

    print("\nGOAL NOT REACHABLE")

noofverts = int(input("Enter number of vertices: "))
for _ in range(noofverts):
    node = input("Enter vertex: ")
    addnode(node)

noofedges = int(input("Enter number of edges: "))
for _ in range(noofedges):
    u = input("From: ")
    v = input("To: ")
    addedge(u, v)

start = input("Enter start node: ")
goal = input("Enter goal node: ")
order = input("Traversal order (L/R): ").upper()

BFS(start, goal, order)

# Menu-driven interaction
while True:
    print("\nMenu:")
    print("1. Add node")
    print("2. Add edge")
    print("3. Remove node")
    print("4. Display adjacency list")
    print("5. BFS")
    print("6. Exit")

    choice = input("Enter the choice: ")

    if choice == '1':
        u = input("Enter the node to add: ")
        addnode(u)
    elif choice == '2':
        u = input("Enter node 1: ")
        v = input("Enter node 2: ")
        addedge(u, v)
    elif choice == '3':
        u = input("Enter the node to remove: ")
        removenode(u)
    elif choice == '4':
        displayadjacency()
    elif choice == '5':
        start = input("Enter start node: ")
        goal = input("Enter goal node: ")
        order = input("Traversal order (L/R): ").upper()
        BFS(start, goal, order)
    elif choice == '6':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
