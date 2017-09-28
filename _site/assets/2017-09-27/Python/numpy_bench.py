from __future__ import print_function
import numpy as np
import time as time

# number of runs
runs = 10
# number of data points
n = np.array( [int(1e6), int(1e7), int(1e8), int(1e9)])
mean_run_times = []
for j in n:
    time_plus_eq = np.zeros(runs)
    for i in range(runs):
        # Fastest
        X = np.ones(j, dtype=np.float)
        Y = np.ones(j, dtype=np.float)
        t0 = time.time()
        X += Y; X += Y
        # np.add(X, Y, out=X); np.add(X, Y, out=X)
        t1 = time.time()
        time_plus_eq[i] = t1 - t0

    mean_run_times.append(np.mean(time_plus_eq))
    print('run:', j, '+= mean run time in seconds: ',mean_run_times[-1])
mean_run_times = np.array(mean_run_times)
np.save('numpy_bench_run_times.npy',mean_run_times)
