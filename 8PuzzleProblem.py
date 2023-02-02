class State:
    def __init__(self, data, level, fval):
        # initialize the node with data, level of the node and calculated fval
        self.data = data
        self.level = level
        self.fval = fval

    def generate_child(self):
        # generate child nodes from the given node by moving the blank space in
        # either of the 4 directions [up, down, left, right]
        x, y = self.find(self.data, '_')

        # contains position values for moving the blank space in either of the 4
        # directions [up, down, left, right]
        moves = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]

        children = list()
        for move in moves:
            child = self.shuffle(self.data, x, y, move[0], move[1])
            if child is not None:
                child_state = State(child, self.level+1, 0)
                children.append(child_state)
        return children

    def shuffle(self, state, x1, y1, x2, y2):
        # move the blank space in the given direction
        # if position value are out of the limits return None
        if 0 <= x2 < len(self.data) and 0 <= y2 < len(self.data):
            new_state = self.copy(state)
            new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
            return new_state
        else:
            return None

    @staticmethod
    def copy(root):
        # copy function to create a similar matrix of the given state
        new = list()
        for i in root:
            temp = list()
            for j in i:
                temp.append(j)
            new.append(temp)
        return new

    def find(self, state, x):
        # find position of blank space
        n = len(self.data)
        for i in range(n):
            for j in range(n):
                if state[i][j] == x:
                    return i, j


class Puzzle:
    def __init__(self, n):
        # Initialize the puzzle size and open & closed lists
        self.n = n
        self.open = list()
        self.closed = list()

    def state(self):
        state = list()
        for i in range(self.n):
            row = input().split(" ")
            state.append(row)
        print()
        return state

    # Heuristic value f(x) = h(x) + g(x)
    def fvalue(self, start, goal):
        return self.hvalue(start.data, goal) + start.level

    # misplaced valued / Hamming Priority function
    def hvalue(self, start, goal):
        # calculate the different between the given puzzles
        diff = 0
        for i in range(self.n):
            for j in range(self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '_':
                    diff += 1
        return diff

    def solve(self):
        # initialize Start and Goal puzzle state
        print("Enter the goal state matrix:-")
        goal = self.state()
        print("Enter the start state matrix:-")
        start = self.state()

        start = State(start, 0, 0)
        start.fval = self.fvalue(start, goal)

        # put the start node in open list
        print("Solution:- \n")
        self.open.append(start)

        step = 0
        while True:
            curr = self.open.pop(0)
            print(f'        STEP {step}')
            print(f'f(n)={curr.fval}, h(n)={curr.fval - curr.level}, g(n)={curr.level}')
            for i in curr.data:
                print("       ", end=' ')
                for j in i:
                    print(j, end=' ')
                print()

            # if the difference between current and goal node is 0 we have reached goal node
            if self.hvalue(curr.data, goal) == 0:
                break

            for i in curr.generate_child():
                i.fval = self.fvalue(i, goal)
                # if i.data not in self.closed:
                self.open.append(i)
            self.closed.append(curr)
            # del self.open[0]

            # sort the open list based on f value
            self.open.sort(key=lambda x: x.fval)

            print()
            print("          | ")
            print("          | ")
            print("         \\\'/ \n")
            step += 1


if __name__ == "__main__":
    puzzle = Puzzle(3)
    puzzle.solve()
