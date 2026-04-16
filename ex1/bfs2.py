vertices = [[0 for _ in range(100)] for _ in range(100)]

noofverts = int(input("Enter number of vertices: "))
noofedges = int(input("Enter number of edges: "))

nodes = []
for _ in range(noofverts):
    nodes.append((input("Enter vertex: ")))

start = int( input("Enter start node: "))
goal = int(input("Enter goal node: "))

order = input("Traversal order (L/R): ").upper()

for _ in range(noofedges):
    u =int( input("From: "))
    v = int(input("To: "))
    vertices[u][v] = 1
    vertices[v][u] = 1
def addnode(node):
   nodes.append(node)
def removenode(node):
   nodes.remove(node)
   for i in nodes:
      if i!=node:
         vertices[node][i]=-1
         vertices[i][node]=-1
def addedge(node1,node2):
   vertices[node1][node2]=1
   vertices[node2][node1]=1
def displayadjacency():
   for i in nodes:
      res=[]
      for j in nodes:
         if vertices[i][j]==1:
           res.append(j)
      print(i,": ",res)
def BFS(start, goal):
    visited = [0]*15
    fringe = []

    print("\nINITIAL FRINGE:", fringe)

    fringe.append(start)
    print("PUSH ", start)
    print("FRINGE:", fringe)
    path=[]
    while fringe:
        current = fringe.pop(0)
        print("\nPOP ", current)
        print("FRINGE:", fringe)
        path.append(current)
        sep="->"
        joined_path=sep.join(str(path))
        print("\nPath: ",joined_path)
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
BFS(start,goal)
print("\n 1.Add node\n2.Add edge\n3.Remove node\n4.Display adjacency list\n5.BFS")
choice=int(input("Enter the choice:"))
while choice:
   if choice==1:
      u=int(input("Enter the node:"))
      addnode(u)
   elif choice==2:
      u=int(input("Enter node 1:"))
      v=int(input("Enter node 2:"))
      addedge(u,v)
   elif choice==3:
      u=int(input("Enter the node to be removed:"))
      removenode(u)
   elif choice==4:
      displayadjacency()
   elif choice==5:
      start=int(input("Enter start node:"))
      goal=(input("Enter goal node:"))
      BFS(start,goal)
   choice=int(input("Enter the choice:"))
print("Exit....\n")
