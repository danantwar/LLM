#load the library and check its version, just to make sure we aren't using an older version
import numpy as np

#L = np.eye(5)
#print(L)
x1 = np.random.randint(10,100)
print(x1)

x = np.array([1, 2, 3])
y = np.array([3, 2, 1])
z = np.array([[9],[9]])
grid = np.array([[1,2,3],[17,18,19]])
print(np.vstack([y,grid]))

