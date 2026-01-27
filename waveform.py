import sys

import numpy as np
import matplotlib as plt
import scipy as sp
from graycode import gray_recursive


def A_m(m: int):
    """Calculate amplitude for symbol m using A_m = β(2m - M + 1) with β=1"""
    return 2*m-M+1

def P_t(t, T_s):
    """
    Triangular pulse with duration T_s and max amplitude 1.
    p(t) = 1 - |t|/T_s  for |t| <= T_s
    p(t) = 0            otherwise
    """
    return np.where(np.abs(t) <= T_s, 1 - np.abs(t) / T_s, 0)

def X_t(amplitudes, N, T_s):
    """
    Generate PAM waveform x(t) = Σ a_k * p(t - kT_s)

    Parameters:
    -----------
    amplitudes : list[int]
        Amplitude values for each symbol (a_k)
    N : int
        Number of samples per symbol duration T_s
    T_s : float

        Symbol duration

    Returns:
    --------
    t : ndarray
        Time vector
    x : ndarray
        Waveform x(t)
    """
    num_symbols = len(amplitudes)

    # Total time span: each pulse extends ±T_s, so add extra space
    total_duration = (num_symbols + 1) * T_s

    # Create time vector with N samples per T_s
    total_samples = int(N * total_duration / T_s)
    t = np.linspace(0, total_duration, total_samples)

    # Initialize waveform
    x = np.zeros_like(t)

    # Generate waveform as sum of shifted pulses: x(t) = Σ a_k * p(t - kT_s)
    for k, a_k in enumerate(amplitudes):
        x += a_k * P_t(t - k * T_s, T_s)

    print(f"""
--- Waveform Generation ---
Number of symbols: {num_symbols}
Samples per symbol (N): {N}
Symbol duration (T_s): {T_s}
Total duration: {total_duration:.4f}
Total samples: {total_samples}
Bit rate: {int(np.log2(M)) / T_s:.2f} bit/s"""
    )

    return t, x

def plot_waveform(t, x, amplitudes, T_s):
    """
    Plot the PAM waveform with symbol positions marked.
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(14, 6))

    # Plot waveform
    plt.plot(t, x, 'b-', linewidth=1.5, label='x(t)')

    # Mark symbol positions
    for k, a_k in enumerate(amplitudes):
        t_k = k * T_s
        plt.axvline(t_k, color='gray', linestyle='--', alpha=0.3)
        plt.plot(t_k, a_k, 'ro', markersize=8, label=f'Symbol {k}' if k == 0 else '')

    plt.xlabel('Time (t)', fontsize=12)
    plt.ylabel('Amplitude', fontsize=12)
    plt.title(f'PAM Waveform x(t) - M={M}, T_s={T_s}', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    # Save plot
    plt.savefig('waveform_plot.png', dpi=150)
    print(f"\nPlot saved to: waveform_plot.png")
    plt.show()

    return plt

def bits_to_symbols(bits: str, M: int) -> list[int]:
    # 1. create groups
    bits_per_symbol = int(np.log2(M))
    number_of_groups = len(bits) // bits_per_symbol
    bit_groups = [bits[i*bits_per_symbol:(i+1)*bits_per_symbol] for i in range(number_of_groups)]
    print(f"""
Bits per symbol: {bits_per_symbol}
Number of symbols: {number_of_groups}
Bit groups: {bit_groups}"""
    )

    # 2. gray code words
    gray_code_words = gray_recursive(bits_per_symbol)

    # 3. map each bit group to symbol index m (find position in Gray code table)
    symbols = [gray_code_words.index(bit_group) for bit_group in bit_groups]

    # 4. convert symbols to amplitudes
    amplitudes = [A_m(m) for m in symbols]

    print(f"""
Symbols (m): {symbols}
Amplitudes (A_m): {amplitudes}"""
    )

    return amplitudes


p = 8 # last academic ID digit
M = 2**(p+3) if p <= 5 else 2**(p-2) # amplitude points of waveform
input_bits = '110101100011100010010011'

# Calculate T_s from bit rate constraint: bit_rate = 1 Gbit/s
# Bit rate = (bits per symbol) / T_s
# Therefore: T_s = (bits per symbol) / bit_rate
bit_rate = 1e9  # 1 Gbit/s = 1e9 bit/s
bits_per_symbol = int(np.log2(M))
T_s = bits_per_symbol / bit_rate  # Symbol duration in seconds

# Default number of samples per symbol
N = 100

# Parse command line arguments if provided (can override defaults)
# Filter out IDE-specific arguments (like --mode=client)
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        N = int(sys.argv[1])
    if len(sys.argv) >= 3:
        T_s = float(sys.argv[2])  # Override calculated T_s if provided
    if len(sys.argv) >= 4:
        input_bits = str(sys.argv[3])

print(f"""
p = {p}
M = {M}
Bits per symbol: {bits_per_symbol}
Bit rate: {bit_rate/1e9:.1f} Gbit/s
Symbol duration T_s: {T_s*1e9:.2f} ns
Amplitude range: {A_m(0)} to {A_m(M - 1)}
Input bits: {input_bits}"""
)

amplitudes = bits_to_symbols(input_bits, M)

# Generate the waveform
t, x = X_t(amplitudes, N, T_s)

# Plot the waveform
plot_waveform(t, x, amplitudes, T_s)

