class RingBuffer:

    def __init__(self, size = 5):

        self.__size = size
        self.__currentPtr = 0
        self.__valueCount = 0
        self.__buffer = [0]*5

    def incrementPtr(self):
        self.__currentPtr = (self.__currentPtr + 1) % self.__size
        self.__valueCount = min(self.__valueCount + 1, self.__size)

    def putValue(self, value):
        self.__buffer[self.__currentPtr] = value
        self.incrementPtr()

    def getAverage(self):
        if self.__valueCount == 0:
            return 0
        return sum(self.__buffer) / float(self.__valueCount)