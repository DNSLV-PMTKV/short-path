class Point:
    '''
    Represents a point
    '''

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '({},{})'.format(self.x, self.y)

    def __repr__(self):
        return '({},{})'.format(self.x, self.y)

    # needed for set
    def __hash__(self):
        return hash((self.x, self.y))


class PathFinder:
    '''
    Find the shortest path in a grid
    '''

    def __init__(self, field):
        self._field = field

    def shortest_path(self, startPoint, endPoint, diagonals=False):
        queue = []
        visited = set()
        queue.append([startPoint])
        while queue:
            path = queue.pop(0)
            currentPoint = path[-1]
            # Path found
            if currentPoint == endPoint:
                return path

            for neighbour in self.neighbours(currentPoint, diagonals=diagonals):
                if neighbour not in visited:
                    visited.add(neighbour)
                    newPath = list(path)
                    newPath.append(neighbour)
                    queue.append(newPath)
        # Path not found
        return []

    def neighbours(self, point, diagonals=False):
        '''
        Get all adjacent point
        '''
        adjPoints = []
        if diagonals:
            for i in range(-1, 2):
                # check if neighbour x is in the grid
                neig_x = min(max(point.x+i, 0), self.rows-1)
                for j in range(-1, 2):
                    # chech if neighbour y is in the grid
                    neig_y = min(max(point.y+j, 0), self.cols-1)
                    # check if neighbour is not our point
                    if point.x == neig_x and point.y == neig_y:
                        continue
                    neigbour = Point(neig_x, neig_y)
                    # check if the neighbour is anobstacle
                    if self.is_obstacle(neigbour):
                        continue
                    adjPoints.append(neigbour)
        else:
            for i in range(-1, 2):
                neig_x = min(max(point.x+i, 0), self.cols - 1)
                for j in range(-1, 2):
                    neig_y = min(max(point.y+j, 0), self.rows - 1)
                    if point.x == neig_x:
                        if self.is_obstacle(Point(point.x, neig_y)):
                            continue
                        adjPoints.append(Point(point.x, neig_y))
                    if point.y == neig_y:
                        if self.is_obstacle(Point(neig_x, point.y)):
                            continue
                        adjPoints.append(Point(neig_x, point.y))
        return adjPoints

    def is_obstacle(self, point):
        return self._field[point.x][point.y] == '#'

    @property
    def rows(self):
        return len(self._field[0])

    @property
    def cols(self):
        return len(self._field)
