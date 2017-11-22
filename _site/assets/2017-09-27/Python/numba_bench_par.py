from __future__ import print_function
import numpy as np
import numba
import time as time

@numba.vectorize(["float64(float64,float64)"],nopython=True,target='parallel')
def add2_par(x, y):
  return x + 2 * y

# number of runs
runs = 10
# number of data points
n = np.array( [int(1e6), int(1e7), int(1e8), int(1e9)])
mean_run_times = []
for j in n:
    time_num = np.zeros(runs)
    for i in range(runs):
        # Fastest
        X = np.ones(j, dtype=np.float)
        Y = np.ones(j, dtype=np.float)
        t0 = time.time()
        add2_par(X, Y, out=X)
        t1 = time.time()
        time_num[i] = t1 - t0

    mean_run_times.append(np.mean(time_num))
    print('run:', j, '+= mean run time in seconds: ',mean_run_times[-1])
mean_run_times = np.array(mean_run_times)
np.save('numba_bench_par_times.npy',mean_run_times)
