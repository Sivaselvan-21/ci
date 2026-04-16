vertices=[[0 for _ in range(15)] for _ in range(15)]
noofverts=int(input("Enter the no. of vertices:"))
noofedges=int(input("Enter the no. of edges:"))
nodes=[]
for i in range(noofverts):
   n=int(input("Enter the vertex:"))
   nodes.append(n)
start=int(input("Enter the start node:"))
goal=int(input("Enter the goal node:"))
for i in range(noofedges):
   u=int(input("From:"))
   v=int(input("To:"))
   vertices[u][v].append(1)
   vertices[v][u].append(1)
def addnode(node):
   noofverts+=1
   nodes.append(node)
def deletenode(node):
   nodes.remove(node)
   noofverts-=1
   for i in nodes:
      vertices[node][i].append(0)
      vertices[i][node].append(0)
   noofedges-=1
def BFS(start,goal):
   visited=[]
   queue=[]
   front=0
   rear=0
   queue[front].append(start)
   visited[start].append(1)
   while front<rear:
      v=queue[front]
      front+=1
      print(v,"->")
      if v==goal:
         break
      for i in nodes:
         if vertices[v][i]==1 and not visited[i]:
            visited[i].append(1)
            queue[rear].append(i)
            rear+=1
def printlist():
   for i in nodes:
      res=[]
      for j in nodes:
         if vertices[i][j]==1:
           res.append(j)
      print(i,":",res)
BFS(start,goal)
printlist()
