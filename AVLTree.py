#Name: AVL Tree
#Description:
#Date Created: 03/22/2019
#Date Last Modified:

class Node (object):
   def __init__(self, data):
      self.data = data
      self.lchild = None
      self.rchild = None
      self.height = 0

   def getHeight(self):
      return self.height

   def getValue(self):
      return self.data

class Tree(object):
   def __init__(self):
      self.root = None

   def insertNode(self, data):
      #create new node
      newNode = Node(data)

      #case when root is empty
      if (self.root is None):
         self.root = newNode
      else:
         current = self.root
         parent = self.root
         while not(current is None):
            parent = current
            if (data < current.data):
               current = current.lchild
            else:
               current = current.rchild
         if (data < parent.data):
            parent.lchild = newNode
         else:
            parent.rchild = newNode

      #update height of all nodes in the tree.
      self.updatetHeight(self.root)

      #balance tree
      self.balanceTree(self.root, self.root)

   def deleteNode(self, data):
      #Check if tree is empty
      if (self.root is None):
         return None

      parent = self.root
      current = self.root
      is_left = False

      #Check if Node exists
      while ( not(current is None) and (current.data != data) ):
         parent = current
         if ( data < current.data ):
            current = current.lchild
            is_left = True
         else:
            current = current.rchild
            is_left = False

      # If node does not exist.
      if (current is None):
         return None

      #check if the node is leaf node.
      if ((current.lchild is None) and (current.rchild is None)):
         #check if node is the root of the tree.
         if (current is self.root):
            self.root = None
         elif (is_left):
            parent.lchild = None
         else:
            parent.rchild = None

      #check if node has only left child
      elif (current.rchild is None):
         #check if node is the root of the tree.
         if (current is self.root):
            self.root = current.lchild
         elif (is_left):
            parent.lchild = current.lchild
         else:
            parent.rchild = current.lchild

      #check if node has only right child
      elif (current.lchild is None):
         #check if node is the root of the tree
         if (current is self.root):
            self.root = current.rchild
         elif (is_left):
            parent.lchild = current.rchild
         else:
            parent.rchild = current.rchild

      #check if node has both right and left children.
      else:
         succesor = current.rchild
         pSuccesor = current

         while (succesor.lchild != None):
            pSuccesor = succesor
            succesor = succesor.lchild

         #check if node is the root of the tree.
         if (current is self.root):
            self.root = succesor
         elif (is_left):
            parent.lchild = succesor
         else:
            parent.rchild = succesor

         #connect delete node's left child to be succesor's left child.
         succesor.lchild = current.lchild

         #succesor node left descendant of deleted node.
         if (succesor != current.rchild):
            pSuccesor.lchild = succesor.lchild
            succesor.rchild = current.rchild

      self.updatetHeight(self.root)
      self.balanceTree(self.root, self.root)

   #use post-order traversal to visit all nodes of the tree/subtree and check if balanced.
   def balanceTree(self, aNode, prevNode):
      if not(aNode is None):
         self.balanceTree(aNode.lchild, aNode)
         self.balanceTree(aNode.rchild, aNode)

         #get balance factor of the node
         bf = self.getBalanceFactor(aNode)

         if ((bf < -1) or (bf > 1)):
            if (bf > 1):
               bf_lchild = self.getBalanceFactor(aNode.lchild)
               if ( bf_lchild > 0 ): #case 1: rotate right
                  print("srr, aNode: {0}, bf_lchild:{1}".format(aNode.getValue(), bf_lchild))
                  self.simpleRightRotation(aNode, prevNode)
               else: # case 3: rotate left, then rotate right.
                  self.case3(aNode, prevNode)
                  print("case 3, aNode: {0}, bf_lchild:{1}".format(aNode.getValue(), bf_lchild))
            else:
               bf_rchild = self.getBalanceFactor(aNode.rchild)
               if ( bf_rchild < 0 ): # case 2: rotate left.
                  print("slr, aNode: {0}, bf_rchild:{1}".format(aNode.getValue(), bf_rchild))
                  self.simpleLeftRotation(aNode, prevNode)
               else: # case 4: rotate right, then rotate left.
                  print("doubleRotationRL, aNode: {0}, bf_rchild:{1}".format(aNode.getValue(), bf_rchild))
                  self.doubleRotationRL(aNode, prevNode)

   #Rotates aNode to the right.
   def simpleRightRotation(self, aNode, prevNode):
      print("rotating right")
      print("aNode: {0}".format(aNode.getValue()))
      print("prevNode: {0}".format(prevNode.getValue()))

      successor = aNode.lchild #successor of aNode.
      print("succ: {0}".format(successor.getValue()))

      #check if aNode is self.root.
      if (aNode is self.root):
         self.root = successor
      else:
         if (aNode.getValue() < prevNode.getValue()):
            print("value <")
            prevNode.lchild = successor
         else:
            print("value >")
            prevNode.rchild = successor

      aNode.lchild = successor.rchild
      successor.rchild = aNode

      self.updatetHeight(self.root)

   #Rotates aNode to the left.
   def simpleLeftRotation(self, aNode, prevNode):
      print("rotating left")
      print("aNode: {0}".format(aNode.getValue()))
      print("prevNode: {0}".format(prevNode.getValue()))

      successor = aNode.rchild #succesor of aNode
      print("succ: {0}".format(successor.getValue()))

      #check if aNode is self.root
      if (aNode is self.root):
         self.root = successor
      else:
         if (aNode.getValue() > prevNode.getValue()):
            print("value >")
            prevNode.rchild = successor
         else:
            print("value <")
            prevNode.lchild = successor

      aNode.rchild = successor.lchild
      # print("new rchild {0}".format(aNode.rchild.getValue()))
      successor.lchild = aNode
      # print("new lchild {0}".format(successor.lchild.getValue()))

      self.updatetHeight(self.root)

   #Rotates aNode.lchild to the left, then rotates aNode right.
   def case3(self, aNode, prevNode):
      print("rotating left, then right")
      print("aNode: {0}".format(aNode.getValue()))
      print("prevNode: {0}".format(prevNode.getValue()))

      successor = aNode.lchild
      print("succ: {0}".format(successor.getValue()))
      #Left rotation
      self.simpleLeftRotation(successor, aNode)

      #Right rotation
      self.simpleRightRotation(aNode, prevNode)

      self.updatetHeight(self.root)

   #Rotates aNode.rchild to the right, then rotates aNode left.
   def doubleRotationRL(self, aNode, prevNode):
      print("rotating right, then left")
      print("aNode: {0}".format(aNode.getValue()))
      print("prevNode: {0}".format(prevNode.getValue()))

      successor = aNode.rchild
      print("succ: {0}".format(successor.getValue()))
      #Rotate right
      self.simpleRightRotation(successor,aNode)

      #Rotate left
      self.simpleLeftRotation(aNode, prevNode)

      self.updatetHeight(self.root)

   def getBalanceFactor(self, aNode):
      if aNode.height == 1:
         return 0
      else:
         if not(aNode.lchild is None):
            lchild = (aNode.lchild).getHeight()
         else:
            lchild = 0

         if not(aNode.rchild is None):
            rchild = (aNode.rchild).getHeight()
         else:
            rchild = 0
         return (lchild - rchild)

   #use post-order traversal to visit all nodes of the tree/subtree and check if balanced.
   def isBalanced(self, aNode):
      if not(aNode is None):
         self.isBalanced(aNode.lchild)
         self.isBalanced(aNode.rchild)
         if ((self.getBalanceFactor(aNode) > -2) and (self.getBalanceFactor(aNode) < 2) ):
            return True
         else:
            return False

   # use post-order traversal- left, right, center- to visit all nodes of the
   #tree and update their height.
   def updatetHeight(self, aNode):
      if not(aNode is None):
         self.updatetHeight(aNode.lchild)
         self.updatetHeight(aNode.rchild)
         aNode.height = self.updateHeightHelper(aNode)

   def updateHeightHelper(self, aNode):
      if aNode is None:
         return 0
      else:
         return (1 + max(self.updateHeightHelper(aNode.lchild),
                        self.updateHeightHelper(aNode.rchild)))

   def printTree(self):
      nLevels = self.root.getHeight()

      for i in range(nLevels + 1):
         print(self.print_level(i))

   # Prints out all nodes at the given level
   def print_level (self, level):
      s = ""
      level = level - 1
      queue = self.print_level_helper()

      for i in range(len(queue)):
         if i == level:
            for element in queue[level]:
               s += str(element.data) + " "
      return s

   def print_level_helper(self):
      queue = []
      lev = []

      lev.append(self.root)
      queue.append(lev)

      for l in queue:
         lev = []
         for current in l:
            if not(current.lchild is None):
               lev.append(current.lchild)
            if not(current.rchild is None):
               lev.append(current.rchild)
         if not(len(lev) == 0):
            queue.append(lev)
      return queue


import random

def main():
   # mylist = [25,50,75, 90,100]
   # myTree = Tree()
   # for i in mylist:
   #    myTree.insertNode(i)
   # myTree.printTree()
   #
   # mylist2 = [100, 90, 75, 50, 25]
   # myTree2 = Tree()
   # for i in mylist2:
   #    myTree2.insertNode(i)
   # myTree2.printTree()
   #
   # mylist3 = [5, 10, 8]
   # myTree3 = Tree()
   # for i in mylist3:
   #    myTree3.insertNode(i)
   # myTree3.printTree()
   #
   # mylist4 = [10,5,15,20,17]
   # myTree4 = Tree()
   # for i in mylist4:
   #    myTree4.insertNode(i)
   # myTree4.printTree()
   #
   # mylist5 = [10,5,8]
   # myTree5 = Tree()
   # for i in mylist5:
   #    myTree5.insertNode(i)
   # myTree5.printTree()
   # mylist5 = [10,5,8]
   #
   # mylist6 = [15, 10, 20, 5, 7]
   # myTree6 = Tree()
   # for i in mylist6:
   #    myTree6.insertNode(i)
   # myTree6.printTree()
   #
   # myTree = Tree()
   # x = [1, 2, 3, 4, 5, 6, 10, 11, 12, 19, 20]
   # for i in x:
   #    print("Insert: ", i, "type: ", type(i))
   #    myTree.insertNode(i)
   # myTree.printTree()

   testCount = 1000
   maxElements = 20
   for test in range(testCount):
      print("Test: ", test)
      elems = random.randint(1, maxElements)
      insert = []
      remove = []
      for i in range(elems):
         newElem = random.randint(1, 10*maxElements)
         while newElem in insert:
            newElem = random.randint(1, 10*maxElements)
         insert.append(newElem)
      print("Inserting values: ", insert)

      tree = Tree()
      for i in insert:
         print("Insert: ", i)
         remove.append(i)
         tree.insertNode(i)


         willRemove = random.randint(1, 100)
         if willRemove > 95:
            randomRemove = random.randint(0, len(remove))
            elem = remove[randomRemove]
            print("Remove: ", elem)
            del remove[randomRemove]
            tree.deleteNode(elem)

      while len(remove) > 0:
         randomRemove = random.randint(0, len(remove))
         elem = remove[randomRemove]
         del remove[randomRemove]
         tree.deleteNode(elem)
main()
