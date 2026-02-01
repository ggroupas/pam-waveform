import inspect
import sys


def gray_recursive(M: int) -> list[str]:
    """
    Generate the Gray code of order M.

    Parameters
    ----------
    M : int
        Number of bits of the Gray code. The function returns 2**M
        Gray codewords, each of length M.

    Returns
    -------
    list of str
        A list containing the Gray codewords in reflected Gray code order.
    """
    if M == 0:
        return []
    if M == 1:
        return ["0", "1"]

    prev = gray_recursive(M - 1)

    first_half = ["0" + code for code in prev]
    second_half = ["1" + code for code in reversed(prev)]

    return first_half + second_half

def gray_iterative(M: int) -> list[str]:
    """
    Generate the Gray code of order M.

    Parameters
    ----------
    M : int
        Number of bits of the Gray code. The function returns 2**M
        Gray codewords, each of length M.

    Returns
    -------
    list of str
        A list containing the Gray codewords in reflected Gray code order.
    """
    if M == 0:
        return []

    result = ["0", "1"]  # Gray(1)
    for bits in range(2, M + 1):
        reflected = list(reversed(result))
        result = ["0" + code for code in result] + ["1" + code for code in reflected]
    return result

def test():
    """
    Run time and memory benchmarks for both Gray code implementations.

    Tests for code sizes: 4, 16, 256 (i.e., M = 2, 4, 8 bits)

    Measures:
    - Time: execution time in milliseconds
    - Heap Memory: memory allocated on heap (via tracemalloc)
    - Stack Depth: estimated stack frame overhead for recursive calls
    """
    import time
    import tracemalloc
    import math

    M_sizes = [4, 16, 256]

    print(f"""
{'='*105}
Gray Code Benchmarks
{'='*105}

{'Codes':<8} {'Bits':<6} {'--- Recursive ---':<36} {'--- Iterative ---':<36}
{'(2^M)':<8} {'(M)':<6} {'Time(ms)':<11} {'Heap(KB)':<11} {'Stack(KB)':<14} {'Time(ms)':<11} {'Heap(KB)':<11} {'Stack(KB)':<11}
{'-'*105}""")

    STACK_FRAME_SIZE = inspect.currentframe().__sizeof__()

    for num_codes in M_sizes:
        M = int(math.log2(num_codes))

        tracemalloc.start()
        start_time = time.perf_counter()
        gray_recursive(M)
        time_rec = (time.perf_counter() - start_time) * 1000
        _, peak_rec = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        stack_overhead_rec = M * STACK_FRAME_SIZE

        tracemalloc.start()
        start_time = time.perf_counter()
        gray_iterative(M)
        time_iter = (time.perf_counter() - start_time) * 1000
        _, peak_iter = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        stack_overhead_iter = STACK_FRAME_SIZE  # Iterative has no stack overhead (just 1 frame for the function call itself)

        print(f"{num_codes:<8} {M:<6} {time_rec:<11.3f} {peak_rec/1024:<11.2f} {stack_overhead_rec/1024:<14.2f} {time_iter:<11.3f} {peak_iter/1024:<11.2f} {stack_overhead_iter/1024:<11.2f}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test()
    else:
        print(f"""
    Gray code generation examples
    
    --- Recursive ---
    4:{gray_recursive(2)}
    G16:{gray_recursive(4)} 
    G256:{gray_recursive(8)}
    
    --- Iterative ---
    4:{gray_iterative(2)}
    G16:{gray_iterative(4)} 
    G256:{gray_iterative(8)}
    
    Run with --test for benchmarks
    """)