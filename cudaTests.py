from numba import cuda
import numpy as np

@cuda.jit
def cudakernel0(array):
    thread_position = cuda.grid(1)
    array[thread_position] += 0.5

array = np.zeros(1024 * 1024, np.float32)
print('Initial array:', array)

print('Kernel launch: cudakernel1[1024, 1024](array)')
cudakernel0[1024, 1024](array)

print('Updated array:', array)

# Since it is a huge array, let's check that the result is correct:
print('The result is correct:', np.all(array == np.zeros(1024 * 1024, np.float32) + 0.5))