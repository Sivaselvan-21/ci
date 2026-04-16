vertices = [[0 for _ in range(15)] for _ in range(15)]

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
    vertices[u][v] = 1
    vertices[v][u] = 1

def DFS(start, goal):
    visited = [0]*15
    fringe = []

    print("\nINITIAL FRINGE:", fringe)

    fringe.append(start)
    print("PUSH ", start)
    print("FRINGE:", fringe)

    while fringe:
        current = fringe.pop()
        print("\nPOP ", current)
        print("FRINGE:", fringe)

        if visited[current]:
            continue

        visited[current] = 1

        if current == goal:
            print("\nGOAL FOUND")
            return

        if order == 'L':
            neighbors = nodes
        else:
            neighbors = reversed(nodes)

        for i in neighbors:
            if vertices[current][i] == 1 and not visited[i]:
                fringe.append(i)
                print("PUSH ", i)
                print("FRINGE:", fringe)

    print("\nGOAL NOT REACHABLE")

DFS(start, goal)
