#Name: Topological Sort
#Description:The following program do a topological sort. The program tests if
#the graph contains a cycle and then do a topo sort on the graph. The inputs include a
# single integer numV  denoting the number of vertices; vert denoting a list
#with the vertices in alphabetical order; single integer numE denoting the number
#of edges; and edg denoting a list with the edges. The edges are in the form -
#from vertex to vertex. A weight of 1 was asigned to all edges. The program
#outputs all the vertices on a level in alphabetical order.
#Date Created: 04/25/2018
#Date Last Modified: 03/22/2019
class Stack (object):
   def __init__ (self):
      self.stack = []

   # add an item to the top of the stack
   def push (self, item):
      self.stack.append ( item )

   # remove an item from the top of the stack
   def pop (self):
      return self.stack.pop()

   # check what item is on top of the stack without removing it
   def peek (self):
      return self.stack[len(self.stack) - 1]

   # check if a stack is empty
   def isEmpty (self):
      return (len(self.stack) == 0)

   # return the number of elements in the stack
   def size (self):
      return (len(self.stack))

   def inStack(self, element):
      if element in self.stack:
         return True
      return False

class Vertex(object):
   def __init__(self, label):
      self.label = label
      self.visited = False #default value

   def wasVisited(self):
      return self.visited

   def getLabel(self):
      return self.label

   #String representation of the vertex
   def __str__(self):
      return str(self.label)

class Graph(object):
   def __init__(self):
      self.Vertices = []
      self.adjMat = []

   # Check if a vertex already exists in the graph.
   def hasVertex(self, label):
      nVert = len(self.Vertices)
      for i in range(nVert):
         if (label == (self.Vertices[i]).label):
            return True
      return False

   # Given a label get the index of a vertex.
   def getIndex(self, label):
      nVert = len(self.Vertices)
      for i in range(nVert):
         if (self.Vertices[i]).label == label:
            return i
      return -1

   # Add vertex with given label to the graph.
   def addVertex(self, label):
      # If graph does not have the vertex, add it.
      if (not self.hasVertex(label)):
         self.Vertices.append(Vertex(label))

         #add a new column for the vertex into adjacency matrix
         nVert = len(self.Vertices)
         for i in range(nVert - 1):
            (self.adjMat[i]).append(0)

         #add a new row for the vertex into the adjacency matrix.
         newRow = []
         for i in range(nVert):
            newRow.append(0)
         self.adjMat.append(newRow)

   # Add directed edge to graph with corresponding weight
   def addDirectedEdge(self, start, finish, weight = 1):
      self.adjMat[start][finish] = weight

   # Return unvisited vertex adjacent to vertex v.
   def getAdjUnvisitedVertex(self, v):
      nVert = len(self.Vertices)
      for i in range(nVert):
         if ( (self.adjMat[v][i] > 0) and not((self.Vertices[i]).wasVisited()) ):
            return i
      return -1

   # get a list of immediate neighbors that you can go to from a vertex
   # return empty list if there are none
   def getNeighbors (self, vertexLabel):
      neighbors = []
      VertexIdx = self.getIndex(vertexLabel)
      nVert = len(self.Vertices)
      for i in range(nVert):
         if self.adjMat[VertexIdx][i] > 0:
            neighbors.append((self.Vertices[i]).label)
      return neighbors

   def hasCycle(self):
      nVert = len(self.Vertices)
      theStack = Stack()

      for i in range(nVert):
         if not(self.Vertices[i].wasVisited()):
            if (self.hasCycleHelper(i, theStack)):
               #Reset the flags
               nVert = len (self.Vertices)
               for i in range (nVert):
                  (self.Vertices[i]).visited = False
               return True

      #Reset the flags
      nVert = len (self.Vertices)
      for i in range (nVert):
         (self.Vertices[i]).visited = False

      return False

   def hasCycleHelper(self, v, theStack):
      # mark vertex v as visited and push on the stack
      (self.Vertices[v]).visited = True
      theStack.push (v)

      #Get all neighbors.
      neighbors = self.getNeighbors(v)
      for neighbor in neighbors:
         #if neighbor was not visited. hasCycleHelper
         if not(self.Vertices[self.getIndex(neighbor)].wasVisited()):
            if (self.hasCycleHelper(self.getIndex(neighbor), theStack)):
               return True
         #elif neighbor in stack return true
         elif theStack.inStack( self.getIndex(neighbor) ):
            return True

      #pop v from the stack
      theStack.pop()
      return False

   def dfs(self, v, postOrder):
      theStack = Stack()

      # mark vertex v as visited and push on the stack
      (self.Vertices[v]).visited = True
      theStack.push (v)

      # vist other vertices according to depth
      while (not theStack.isEmpty()):
         # get an adjacent unvisited vertex
         u = self.getAdjUnvisitedVertex (theStack.peek())
         if (u == -1):
            #removes the last item in the list
            u = theStack.pop()
            postOrder.append(u)
         else:
            (self.Vertices[u]).visited = True
            theStack.push(u)

   def topologicalSort(self):
      postOrder = []
      nVert = len(self.Vertices)

      for i in range(nVert):
         # print(i)
         # print(self.Vertices[i].wasVisited())
         if not(self.Vertices[i].wasVisited()):
            self.dfs(i, postOrder)

      # the stack is empty let us reset the falgs
      nVert = len (self.Vertices)
      for i in range (nVert):
         (self.Vertices[i]).visited = False

      return postOrder[::-1]

def RunTopoSort(numV, vert, numE, edg):
   # create a Graph object
   cities = Graph()
   #rev_cities = Graph()

   for v in range(numV):
      cities.addVertex(vert[v])
      #rev_cities.addVertex(vert[v])

   for e in range(numE):
      edge = edg[e].split()
      start = cities.getIndex(edge[0])
      finish = cities.getIndex(edge[1])

      cities.addDirectedEdge (start, finish, 1)
      #rev_cities.addDirectedEdge(finish, start, 1)

   #test if a directed graph has a cycle
   if cities.hasCycle():
      print("Graph has cycle.")
      topo = cities.topologicalSort()
   else:
      print("Graph does not have a cycle.")
      topo = cities.topologicalSort()

   s =''
   for i in range(len(topo)):
      vertex = str(cities.Vertices[topo[i]])
      s += vertex
   print(s)

def TestTopoSort():
   verTest1 = ['0','1','2','3','4','5','6','7']
   edgTest1 = ['0 2','0 3','0 4','1 3','1 5','2 5','3 7','6 7']
   RunTopoSort(len(verTest1), verTest1, len(edgTest1), edgTest1)

   verTest4 = ['A','B','C','D','E']
   edgTest4 = ['A B','A C','B D','C D','D E']
   RunTopoSort(len(verTest4), verTest4, len(edgTest4), edgTest4)

   verTest5 = ['0','1','2','3']
   edgTest5 = ['0 1','0 2','1 2','2 0','2 3', '3 3']
   RunTopoSort(len(verTest5), verTest5, len(edgTest5), edgTest5)

   verTest6 = ['0','1','2','3']
   edgTest6 = ['0 1','0 2','1 2','2 0','2 3','3 3']
   RunTopoSort(len(verTest6), verTest6, len(edgTest6), edgTest6)

def main():
   TestTopoSort()
main()
