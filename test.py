class testing:
    def __init__(self, x):
        self.y = x

testings = [None for i in range(9)]

for i in range(len(testings)):
    testings[i] = testing(i)
check = None
check = testings[5]

testings[5] = None

for i in range(len(testings)):
    if not i == 5:
        print(str(testings[i].y))
    else:
        print(check.y)