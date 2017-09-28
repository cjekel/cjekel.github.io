import numpy as np
#A = np.ones([10000,10000])
#B = np.ones([10000,10000])
#C = np.dot(A,B)
# np.dot automatically solves in parallel

# F*a = c
F = np.random.random([10000,10000])
a = np.random.random([10000,1])
c = np.dot(F,a)
print('solve')

aHat = np.linalg.solve(F,c)

# np.linalg.solve automatically uses parallel processing :o
