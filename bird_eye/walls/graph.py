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
