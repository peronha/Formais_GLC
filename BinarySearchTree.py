class Node:
    def __init__(self, val):
        self.val = val
        self.leftChild = None
        self.rightChild = None

    def get(self):
        return self.val

    def set(self, val):
        self.val = val

    def getChildren(self):
        children = []
        if (self.leftChild != None):
            children.append(self.leftChild)
        if (self.rightChild != None):
            children.append(self.rightChild)
        return children


class BinaryTree:
    def __init__(self):
        self.root = None

    def setRoot(self, val):
        self.root = Node(val)

    # Insere um nó à esquerda.
    def InsertLeftNode(self, currentNode, val):
        novoNodo = None
        if currentNode.leftChild is None:
            novoNodo = Node(val)
            currentNode.leftChild = novoNodo
        return novoNodo

    # Insere um nó à direita.
    def InsertRightNode(self, currentNode, val):
        novoNodo = None
        if currentNode.rightChild is None:
            novoNodo = Node(val)
            currentNode.rightChild = novoNodo
        return novoNodo

    def Print(self):
        return self.PrintNodes(self.root)

    def PrintNodes(self, currentNode):
        if currentNode.leftChild is not None:
            self.PrintNodes(currentNode.leftChild)
        print("Valor do nodo: " + str(currentNode.val))
        if currentNode.rightChild is not None:
            self.PrintNodes(currentNode.rightChild)

    def GetHeight(self):
        return self.Height(self.root)

    def Height(self, root):
        if root is None:
            return -1
        else:
            return max(self.Height(root.leftChild), self.Height(root.rightChild)) + 1