import random
from Block import Block

class Board:
    def __init__(self, size, prob):
        self.size = size
        self.prob = prob
        self.numClicked = 0
        self.numNoBombs = 0
        self.lost = False
        self.won = False
        self.setBoard()

    def setBoard(self):
        self.board = []
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                hasBomb = random.random() < self.prob
                if not hasBomb:
                    self.numNoBombs += 1
                block = Block(hasBomb)
                row.append(block)
            self.board.append(row)
        self.setNeighbors()

    def setNeighbors(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                block = self.getBlock((row, col))
                neighbors = self.getListOfNeighbors((row, col))
                block.setNeighbors(neighbors)

    def getListOfNeighbors(self, index):
        neighbors = []
        for row in range(index[0] - 1, index[0] + 2):
            for col in range(index[1] - 1, index[1] + 2):
                outOfBound = row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]
                same = row == index[0] and col == index[1]
                if (same or outOfBound):
                    continue
                neighbors.append(self.getBlock((row, col)))
            return neighbors

    def getBoard(self):
        return self.board

    def getSize(self):
        return self.size

    def getBlock(self, index):
        return self.board[index[0]][index[1]]\

    def handleClick(self, block, flag):
        if block.getClicked() or (not flag and block.getFlagged()):
            return
        if flag:
            block.toggleFlag()
            return
        block.click()
        if block.getHasBomb():
            self.lost = True
            return
        self.numClicked += 1
        if block.getNumAround() != 0:
            return
        for neighbor in block.getNeighbors():
            if not neighbor.getHasBomb() and not neighbor.getClicked():
                self.handleClick(neighbor, False)

    def getLost(self):
        return self.lost

    def getWon(self):
        return self.numNoBombs == self.numClicked




