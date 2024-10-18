from collections import deque
from .path import Path
import cv2

class Graph:
    def __init__(self, vertexes, matrix):
        self.__vertexes = vertexes
        self.__matrix = matrix

    def neighbours(self, idx):
        return self.__matrix[idx]

    def __getitem__(self, index):
        return self.__vertexes[index]

    def vertexes(self):
        return self.__vertexes

    def matrix(self):
        return self.__matrix

    def size(self):
        return len(self.__vertexes)

    def draw(self, frame):
        for v in self.vertexes():
            x, y = v
            cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

        for i, line in enumerate(self.matrix()):
            for j in line:
                cv2.line(frame, self[i], self[j], (0, 255, 0), 2)

    def get_path(self, start, goal) -> Path:
        visited = set()
        queue = deque([start])
        if start == goal:
            return Path([start])
        back = [0] * self.size()
        find = False
        while queue:
            cur = queue.popleft()
            neighbors = self.neighbours(cur)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
                    back[neighbor] = cur

                    if neighbor == goal:
                        find = True
                        break
            visited.add(cur)
        if find:
            path = []
            cur = goal
            while cur != start:
                path.append(self[cur])
                cur = back[cur]
            path.append(self[start])
            return Path(path[::-1])
        raise RuntimeError("Path doesn't exist ")
