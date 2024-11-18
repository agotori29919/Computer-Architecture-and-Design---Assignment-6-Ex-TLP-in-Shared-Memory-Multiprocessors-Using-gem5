import m5
from m5.objects import *
import threading
import numpy as np
import time
from queue import Queue

# DAXPY kernel: Y = a * X + Y using vectorized operations
def daxpy_worker(a, X, Y, task_queue):
    while True:
        start, end = task_queue.get()
        if start is None:
            break
        Y[start:end] = a * X[start:end] + Y[start:end]
        task_queue.task_done()

def multi_threaded_daxpy(a, X, Y, num_threads):
    task_queue = Queue()
    chunk_size = len(X) // (num_threads * 4)  # Smaller chunks for better load balancing

    # Enqueue tasks
    for i in range(0, len(X), chunk_size):
        start = i
        end = min(i + chunk_size, len(X))
        task_queue.put((start, end))

    # Start worker threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=daxpy_worker, args=(a, X, Y, task_queue))
        thread.start()
        threads.append(thread)

    # Wait for all tasks to be processed
    task_queue.join()

    # Stop workers
    for _ in threads:
        task_queue.put((None, None))
    for thread in threads:
        thread.join()

class MySystem(System):
    def __init__(self, num_cores, opLat, issueLat):
        super(MySystem, self).__init__()
        self.clk_domain = SrcClockDomain(clock='1GHz', voltage_domain=VoltageDomain())
        self.mem_mode = 'timing'
        self.mem_ranges = [AddrRange('512MB')]

        # Instantiate multiple CPU cores
        self.cpu = [MinorCPU(cpu_id=i) for i in range(num_cores)]

        # Assign the modified FU pool to each CPU
        for cpu in self.cpu:
            cpu.executeFuncUnits = MinorFUPool(funcUnits=[
                MinorFU(
                    opLat=opLat,
                    issueLat=issueLat,
                    opClasses=minorMakeOpClassSet([...]),
                    timings=[...],
                    description=f"FloatSimdFU opLat={opLat} issueLat={issueLat}"
                ),
                # Other functional units...
            ])

        # Create the memory bus
        self.membus = SystemXBar()

        # Connect the CPUs to the membus
        for cpu in self.cpu:
            cpu.icache_port = self.membus.cpu_side_ports
            cpu.dcache_port = self.membus.cpu_side_ports

        # Create a memory controller
        self.mem_ctrl = DDR3_1600_8x8(range=self.mem_ranges[0])
        self.mem_ctrl.port = self.membus.mem_side_ports

        # Connect the system port to the membus
        self.system_port = self.membus.cpu_side_ports

def run_simulation(num_cores, opLat, issueLat):
    # Initialize vectors with large size for significant computation
    vector_size = 10_000_000
    a = 2.5
    X = np.random.rand(vector_size).astype(np.float32)
    Y = np.random.rand(vector_size).astype(np.float32)

    # Start timing
    start_time = time.time()

    # Run the multi-threaded DAXPY kernel
    multi_threaded_daxpy(a, X, Y, num_cores)

    # End timing
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Simulation with opLat={opLat}, issueLat={issueLat}, num_cores={num_cores}")
    print(f"Execution Time: {execution_time:.4f} seconds")

    # Since we cannot simulate gem5 within this script, assume placeholder values
    total_cycles = execution_time * 1e9  # Assuming 1GHz clock
    floating_point_operations = vector_size * 2  # Each DAXPY operation involves a multiply and add
    throughput = floating_point_operations / total_cycles

    print(f"Total Cycles: {total_cycles:.0f}")
    print(f"Floating-point Operations: {floating_point_operations}")
    print(f"Throughput: {throughput:.4f} operations per cycle")
    print()

if __name__ == '__main__':
    num_cores = 4  # Set the number of CPU cores

    # Run simulations with different configurations of opLat and issueLat
    configurations = [
        (1, 6),  # Configuration A
        (2, 5),  # Configuration B
        (3, 4),  # Configuration C
        (2, 6),  # Configuration G (New)
        (4, 4),  # Configuration H (New)
        (6, 2),  # Configuration I (New)
    ]
    for opLat, issueLat in configurations:
        run_simulation(num_cores, opLat, issueLat)
