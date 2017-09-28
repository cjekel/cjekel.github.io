from __future__ import print_function
import numpy as np
import time as time

# the above line is equivalent to the following line
# X += Y; X += Y
# the reason why this is faster is because it doesn't need to create a copy of X
# when performing the math.

runs = 10

#100 loops, run time 3.9 seconds
n = int(1e9)
time_np_add = np.zeros(runs)
for i in range(runs):
    # Fastest
    X = np.ones(n, dtype=np.float)
    Y = np.ones(n, dtype=np.float)
    t0 = time.time()
    np.add(X, Y, out=X); np.add(X, Y, out=X)
    t1 = time.time()
    time_np_add[i] = t1 - t0
time_2x = np.zeros(runs)
for i in range(runs):
    # Fastest
    X = np.ones(n, dtype=np.float)
    Y = np.ones(n, dtype=np.float)
    t0 = time.time()
    X = X + 2.0 * Y
    t1 = time.time()
    time_2x[i] = t1 - t0
time_plus_eq = np.zeros(runs)
for i in range(runs):
    # Fastest
    X = np.ones(n, dtype=np.float)
    Y = np.ones(n, dtype=np.float)
    t0 = time.time()
    X += Y; X += Y
    # np.add(X, Y, out=X); np.add(X, Y, out=X)
    t1 = time.time()
    time_plus_eq[i] = t1 - t0

print('*2 mean run time in seconds: ',np.mean(time_2x))
print('np.add mean run time in seconds: ',np.mean(time_np_add))
print('+= mean run time in seconds: ',np.mean(time_plus_eq))
