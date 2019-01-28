class Point:
    '''
    Represents a point
    '''

    def __init__(self, x=0, y=0):
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

    def shortest_path(self, startPoint, endPoint):
        queue = []
        visited = set()
        queue.append([startPoint])
        while queue:
            path = queue.pop(0)
            currentPoint = path[-1]
            # Path found
            if currentPoint == endPoint:
                return path

            for neighbour in self.neighbours(currentPoint, diagonals=False):
                if neighbour not in visited:
                    visited.add(neighbour)
                    newPath = list(path)
                    newPath.append(neighbour)
                    queue.append(newPath)
        # Path not found
        return []

    def neighbours(self, point, diagonals=True):
        adjPoints = []
        if diagonals:
            for i in range(point.x-1, point.x+2):
                for j in range(point.y-1, point.y+2):
                    if Point(i, j) != point:
                        adjPoints.append(Point(i, j))
        else:
            for i in range(-1, 2):
                adjPoints.append(Point(point.x + i, point.y))
                adjPoints.append(Point(point.x, point.y + i))
        return adjPoints


testField = [
    ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
]
a = PathFinder(testField)
print(a.shortest_path(Point(0, 0), Point(8, 8)))
