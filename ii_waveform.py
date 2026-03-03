import sys
import os

import numpy as np
import matplotlib.pyplot as plt
from i_graycode import gray_recursive

OUTPUT_DIR = "output"


def A_m(m: int):
    """Calculate amplitude for symbol m using A_m = β(2m - M + 1) with β=1"""
    return 2*m-M+1

def p_t(t, T_s):
    """
    Triangular pulse from 0 to T_s (one-sided).
    p(t) = 1 - t/T_s  for 0 <= t <= T_s
    p(t) = 0          otherwise
    """
    return np.where(np.abs(t) <= T_s, 1 - np.abs(t) / T_s, 0)

def X_t(amplitudes, T_s):
    """
    Generate PAM waveform x(t) = Σ_k (a_k * p(t - kT_s))

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

    # Generate waveform as sum of shifted pulses
    for k, a_k in enumerate(amplitudes):
        x += a_k * p_t(t - k * T_s, T_s)

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

    plt.figure(figsize=(14, 6))

    plt.plot(t, x, 'b-', linewidth=1.5, label='x(t)')

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

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(f'{OUTPUT_DIR}/waveform_plot.png', dpi=150)
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

# Default configuration
p = 8  # last academic ID digit
M = 2**(p+3) if p <= 5 else 2**(p-2)  # amplitude points of waveform

# Default parameters (single source of truth)
DEFAULT_N = 100
DEFAULT_INPUT_BITS = '110101100011100010010011'
DEFAULT_T_s = int(np.log2(M)) / 1e9  # Symbol duration for 1 Gbit/s


def main(N, T_s, input_bits):
    """
    Generate and plot PAM waveform.

    Parameters:
    -----------
    N : int
        Number of samples per symbol duration
        (default: 100)
    T_s : float or None
        Symbol duration in seconds. If None, calculated for 1 Gbit/s
        (default: None)
    input_bits : str
        Binary string to encode
        (default: '110101100011100010010011')
    """
    print(f"""
p = {p}
M = {M}
Bit rate: {int(np.log2(M)) / T_s / 1e9:.2f} Gbit/s
Bits per symbol: {int(np.log2(M))}
Symbol duration T_s: {T_s*1e9:.2f} ns
Amplitude range: {A_m(0)} to {A_m(M - 1)}
Input bits: {input_bits}"""
    )

    # Convert bits to symbols and amplitudes
    amplitudes = bits_to_symbols(input_bits, M)

    # Generate the waveform
    t, x = X_t(amplitudes, T_s)

    # Plot the waveform
    plot_waveform(t, x, amplitudes, T_s)

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) >= 2 else DEFAULT_N
    T_s = float(sys.argv[2]) if len(sys.argv) >= 3 else DEFAULT_T_s
    input_bits = sys.argv[3] if len(sys.argv) >= 4 else DEFAULT_INPUT_BITS

    main(N, T_s, input_bits)
