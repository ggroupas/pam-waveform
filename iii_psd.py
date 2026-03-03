import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
import os
import sys
from ii_waveform import DEFAULT_T_s, M, DEFAULT_N

OUTPUT_DIR = "output"


def P(f: NDArray[np.floating] | float, T_s: float) -> NDArray[np.floating] | float:
    """
    Spectrum of triangular pulse.
    P(f) = (T_s/2) * sinc²(f*T_s/2)

    Parameters
    ----------
    f : frequency in Hz
    T_s : symbol duration in seconds

    Returns
    -------
    Spectrum values (real, non-negative)
    """
    return (T_s / 2) * (np.sinc(f * T_s / 2) ** 2)


def P_fft(t: NDArray[np.floating], x: NDArray[np.floating]) -> NDArray[np.complexfloating]:
    """
    Parameters
    ----------
    t : time array
    x : signal values

    Returns
    -------
    Complex spectrum
    """
    dt = t[1] - t[0]
    return dt * np.fft.fftshift(np.fft.fft(np.fft.fftshift(x)))


def main():
    E_a2 = (M ** 2 - 1) / 3
    bits_per_symbol = int(np.log2(M))
    N_total = N * bits_per_symbol

    print(f"M={M}, T_s={T_s:.2e}s, Bit rate={bits_per_symbol / T_s / 1e9:.2f} Gbit/s, E{{a_k²}}={E_a2:.2f}")

    dt = T_s / N_total
    t = np.linspace(-T_s / 2, T_s / 2, N_total, endpoint=False)
    p_t = np.where(np.abs(t) <= T_s / 2, 1 - 2 * np.abs(t) / T_s, 0)
    f = np.fft.fftshift(np.fft.fftfreq(N_total, dt))

    P_f_fft = P_fft(t, p_t)
    P_f = P(f, T_s)
    S_X = (E_a2 / T_s) * np.abs(P_f_fft) ** 2

    # ===== FIGURE 1: Pulse Spectrum P(f) - 3 subplots =====
    fig1, axes1 = plt.subplots(1, 3, figsize=(15, 4))

    for ax, data, title, color in zip(
            axes1[:2],
            [P_f, P_f_fft],
            ['P(f)', 'P(f) FFT'],
            ['b-', 'r-']
    ):
        ax.plot(f / 1e9, np.abs(data), color, linewidth=2)
        ax.set(xlabel='Frequency (GHz)', ylabel='|P(f)|', title=title, xlim=[-5, 5])
        ax.grid(True)

    axes1[2].plot(f / 1e9, np.abs(P_f), 'b-', label='Simple', linewidth=2)
    axes1[2].plot(f / 1e9, np.abs(P_f_fft), 'r--', label='FFT', linewidth=1.5)
    axes1[2].set(xlabel='Frequency (GHz)', ylabel='|P(f)|', title='Comparison', xlim=[-5, 5])
    axes1[2].legend()
    axes1[2].grid(True)

    fig1.suptitle('Triangular Pulse Spectrum P(f)', fontsize=14)
    plt.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(f'{OUTPUT_DIR}/pulse_spectrum_comparison.png', dpi=150)

    # ===== FIGURE 2: Power Spectral Density S_X(f) =====
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(f / 1e9, S_X, 'b-', linewidth=2, label=r'$S_X(f) = \frac{E\{a_k^2\}}{T_s}|P(f)|^2$')
    ax2.set(xlabel='Frequency (GHz)', ylabel=r'$S_X(f)$ (W/Hz)',
            title=f'Power Spectral Density (M={M})', xlim=[-5, 5])
    ax2.legend()
    ax2.grid(True)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/psd_plot.png', dpi=150)

    plt.show()


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) >= 2 else DEFAULT_N
    T_s = float(sys.argv[2]) if len(sys.argv) >= 3 else DEFAULT_T_s

    main()