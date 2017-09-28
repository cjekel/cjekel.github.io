import numpy as np
import matplotlib.pyplot as plt
from scipy import io
n = np.array( [int(1e6), int(1e7), int(1e8), int(1e9)])

#   load machine 1 results
gfortran1 = np.array([2.2249999999999995E-003,2.0161399999999993E-002,0.19474739999999996,2.0455654000000001])
gfortranO21 = np.array([2.2550999999999990E-003,1.9526200000000001E-002, 0.19258479999999989, 1.9078102999999995])
numpy1 = np.load('numpy_bench_run_times1.npy')
numba_single_1 = np.load('numba_bench_single_times1.npy')
numba_par_1 = np.load('numba_bench_par_times1.npy')
mat = io.loadmat('matlab_single1.mat')
matlab1 = mat['mean_run_times']

plt.figure()
plt.title('Machine 1: AMD FX-8370')
plt.plot(n,matlab1, '-s', label='MATLAB')
plt.plot(n,numpy1, '-o', label='NumPy')
plt.plot(n,gfortran1, '-^', label='gfortran')
plt.plot(n, gfortranO21, '-P', label='gfortran -O2')
plt.plot(n,numba_single_1, '-x', label='Numba Single')
plt.plot(n,numba_par_1, '-D', label='Numba Parallel')
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of array elements')
plt.ylabel('Run time in seconds (higer number is worse)')
plt.legend()
plt.show()
plt.savefig('Machine1_res.png', dpi=600)

# compute the perecent slowest
percent_faster = np.zeros((4,6))
for i in range(4):
    temp = np.array([gfortran1[i], numpy1[i], numba_single_1[i], numba_par_1[i], matlab1[i], gfortranO21[i]])
    fastest = np.min(temp)
    percent_faster[i,0] = (gfortran1[i]) / fastest
    percent_faster[i,1] = (numpy1[i]) / fastest
    percent_faster[i,2] = (numba_single_1[i]) / fastest
    percent_faster[i,3] = (numba_par_1[i]) / fastest
    percent_faster[i,4] = (matlab1[i]) / fastest
    percent_faster[i,5] = (gfortranO21[i]) / fastest

    # percent_faster[i,0] = (gfortran1[i]) / numpy1[i]
    # percent_faster[i,1] = (numpy1[i]) / numpy1[i]
    # percent_faster[i,2] = (numba_single_1[i]) / numpy1[i]
    # percent_faster[i,3] = (numba_par_1[i]) / numpy1[i]
    # percent_faster[i,4] = (matlab1[i]) / numpy1[i]

plt.figure()
plt.title('Machine 1: AMD FX-8370')
plt.plot(n,percent_faster[:,4], '-s', label='MATLAB')
plt.plot(n,percent_faster[:,1], '-o', label='NumPy')
plt.plot(n,percent_faster[:,0], '-^', label='gfortran')
plt.plot(n,percent_faster[:,5], '-P', label='gfortran -O2')
plt.plot(n,percent_faster[:,2], '-x', label='Numba Single')
plt.plot(n,percent_faster[:,3], '-D', label='Numba Parallel')
plt.xlabel('Number of array elements')
plt.ylabel('Times slower than Numba Parallel (higer number is worse)')
plt.xscale('log')
plt.grid(True)
plt.legend()
plt.show()
plt.savefig('Machine1_per.png', dpi=600)

#   load machine 2 results
gfortran2 = np.array([1.2813999999999998E-003,1.1580799999999997E-002, 0.10972190000000001,1.7090401999999998])
gfortranO22 = np.array([1.2827999999999995E-003,9.9685000000000017E-003,0.10023819999999997,0.94956319999999972])
numpy2 = np.load('numpy_bench_run_times2.npy')
numba_single_2 = np.load('numba_bench_single_times2.npy')
numba_par_2 = np.load('numba_bench_par_times2.npy')
mat = io.loadmat('matlab_single2.mat')
matlab2 = mat['mean_run_times']

plt.figure()
plt.title('Machine 2: i5-6300u')
plt.plot(n,matlab2, '-s', label='MATLAB')
plt.plot(n,numpy2, '-o', label='NumPy')
plt.plot(n,gfortran2, '-^', label='gfortran')
plt.plot(n, gfortranO22, '-P', label='gfortran -O2')
plt.plot(n,numba_single_2, '-x', label='Numba Single')
plt.plot(n,numba_par_2, '-D', label='Numba Parallel')
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of array elements')
plt.ylabel('Run time in seconds (higer number is worse)')
plt.legend()
plt.show()
plt.savefig('Machine2_res.png', dpi=600)

# compute the perecent slowest
percent_faster = np.zeros((4,6))
for i in range(4):
    temp = np.array([gfortran2[i], numpy2[i], numba_single_2[i], numba_par_2[i], matlab2[i], gfortranO22[i]])
    fastest = np.min(temp)
    percent_faster[i,0] = (gfortran2[i]) / fastest
    percent_faster[i,1] = (numpy2[i]) / fastest
    percent_faster[i,2] = (numba_single_2[i]) / fastest
    percent_faster[i,3] = (numba_par_2[i]) / fastest
    percent_faster[i,4] = (matlab2[i]) / fastest
    percent_faster[i,5] = gfortranO22[i] / fastest
plt.figure()
plt.title('Machine 2: i5-6300u')
plt.plot(n,percent_faster[:,4], '-s', label='MATLAB')
plt.plot(n,percent_faster[:,1], '-o', label='NumPy')
plt.plot(n,percent_faster[:,0], '-^', label='gfortran')
plt.plot(n,percent_faster[:,5], '-P', label='gfortran -O2')

plt.plot(n,percent_faster[:,2], '-x', label='Numba Single')
plt.plot(n,percent_faster[:,3], '-D', label='Numba Parallel')
plt.xlabel('Number of array elements')
plt.ylabel('Times slower than Numba Parallel (higer number is worse)')
plt.xscale('log')
plt.grid(True)
plt.legend()
plt.show()
plt.savefig('Machine2_per.png', dpi=600)
