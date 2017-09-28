import time as time
import numpy as np
import numba

# generate 1 billion samples
n = 1000000000

# Add 2 * Y to X, element by element:

# Slowest
# Create two int arrays, each filled with with one billion 1's.
X = np.ones(n, dtype=np.int)
Y = np.ones(n, dtype=np.int)
t0 = time.time()
X = X + 2.0 * Y
t1 = time.time()
print('run time',t1-t0,'seconds')
#100 loops, run time 5.9 seconds

# A bit faster
X = np.ones(n, dtype=np.int)
Y = np.ones(n, dtype=np.int)
t0 = time.time()
X = X + 2 * Y
t1 = time.time()
print('run time',t1-t0,'seconds')
#100 loops, run time 4.5 sconds

# Much faster
X = np.ones(n, dtype=np.int)
Y = np.ones(n, dtype=np.int)
t0 = time.time()
X += 2 * Y
t1 = time.time()
print('run time',t1-t0,'seconds')
#100 loops, run time 4.5 seconds

# Fastest
X = np.ones(n, dtype=np.int)
Y = np.ones(n, dtype=np.int)
t0 = time.time()
np.add(X, Y, out=X); np.add(X, Y, out=X)
# the above line is equivalent to the following line
# X += Y; X += Y
# the reason why this is faster is because it doesn't need to create a copy of X
# when performing the math.
t1 = time.time()
print('run time',t1-t0,'seconds')
#100 loops, run time 3.9 seconds

# Much faster...
X = np.ones(n, dtype=np.int)
Y = np.ones(n, dtype=np.int)
t0 = time.time()
@numba.vectorize(nopython=True)
def add2(x, y):
  return x + 2 * y
add2(X, Y, out=X)
t1 = time.time()
print('run time',t1-t0,'seconds')
# run time 1.94 seconds

# Slightly faster by declaring data type ... on average ...
# single threaded 
X = np.ones(n, dtype=np.int)
Y = np.ones(n, dtype=np.int)
t0 = time.time()
@numba.vectorize(["int64(int64,int64)"],nopython=True,target='cpu')
def add2_par(x, y):
  return x + 2 * y
add2_par(X, Y, out=X)
t1 = time.time()
print('run time',t1-t0,'seconds')
# run time 1.90 seconds

# Slightly faster in parallel...
X = np.ones(n, dtype=np.int)
Y = np.ones(n, dtype=np.int)
t0 = time.time()
@numba.vectorize(["int64(int64,int64)"],nopython=True,target='parallel')
def add2_par(x, y):
  return x + 2 * y
add2_par(X, Y, out=X)
t1 = time.time()
print('run time',t1-t0,'seconds')
# run time 1.53 seconds
