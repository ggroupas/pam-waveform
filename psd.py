import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
import os
from waveform import DEFAULT_T_s, M

T_s: float = DEFAULT_T_s
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
    return (T_s / 2) * np.sinc(f * T_s / 2) ** 2

def P_fft(T_s: float, num_samples: int = 10000) -> tuple[NDArray[np.floating], NDArray[np.complexfloating]]:
    """
    Spectrum of triangular pulse using FFT.

    Parameters
    ----------
    T_s : symbol duration in seconds
    num_samples : FFT points (higher = finer frequency grid)

    Returns
    -------
    (frequencies, complex spectrum)
    """
    t_max = T_s * 5
    dt = t_max / num_samples
    t = np.linspace(-t_max / 2, t_max / 2, num_samples, endpoint=False)
    p_t = np.where(np.abs(t) <= T_s / 2, 1 - 2 * np.abs(t) / T_s, 0)
    P_f = dt * np.fft.fftshift(np.fft.fft(np.fft.fftshift(p_t)))
    f = np.fft.fftshift(np.fft.fftfreq(num_samples, dt))
    return f, P_f

def spectrum_fft(t: NDArray[np.floating], x: NDArray[np.floating]) -> NDArray[np.complexfloating]:
    """
    Parameters
    ----------
    t : time array
    x : signal values

    Returns
    -------
    Complex spectrum (fftshifted)
    """
    dt = t[1] - t[0]
    return dt * np.fft.fftshift(np.fft.fft(np.fft.fftshift(x)))


def power_spectral_density(t: NDArray[np.floating], x: NDArray[np.floating]) -> NDArray[np.floating]:
    """
    Parameters
    ----------
    t : time array
    x : signal values

    Returns
    -------
    Power spectral density
    """
    T = np.max(t) - np.min(t)
    return 1.0 / T * np.abs(spectrum_fft(t, x)) ** 2.0

def energy(t: NDArray[np.floating], x: NDArray[np.floating]) -> float:
    """
    Signal energy: ∫|x(t)|² dt

    Parameters
    ----------
    t : time array
    x : signal values

    Returns
    -------
    Energy
    """
    return np.trapezoid(np.abs(x) ** 2.0, t)


if __name__ == "__main__":
    bits_per_symbol = int(np.log2(M))
    E_a2 = (M**2 - 1) / 3

    print(f"M={M}, T_s={T_s:.2e}s, Bit rate={bits_per_symbol/T_s/1e9:.2f} Gbit/s, E{{a_k²}}={E_a2:.2f}")

    # Compute spectra
    f_fft, P_f_fft = P_fft(T_s)
    P_f = P(f_fft, T_s)
    S_X = (E_a2 / T_s) * np.abs(P_f) ** 2

    # ===== FIGURE 1: Pulse Spectrum P(f) - 3 subplots =====
    fig1, axes1 = plt.subplots(1, 3, figsize=(15, 4))

    for ax, data, title, color in zip(
        axes1[:2],
        [P_f, P_f_fft],
        ['P(f)', 'P(f) FFT'],
        ['b-', 'r-']
    ):
        ax.plot(f_fft/1e9, np.abs(data), color, linewidth=2)
        ax.set(xlabel='Frequency (GHz)', ylabel='|P(f)|', title=title, xlim=[-5, 5])
        ax.grid(True)

    axes1[2].plot(f_fft / 1e9, np.abs(P_f), 'b-', label='Simple', linewidth=2)
    axes1[2].plot(f_fft/1e9, np.abs(P_f_fft), 'r--', label='FFT', linewidth=1.5)
    axes1[2].set(xlabel='Frequency (GHz)', ylabel='|P(f)|', title='Comparison', xlim=[-5, 5])
    axes1[2].legend()
    axes1[2].grid(True)

    fig1.suptitle('Triangular Pulse Spectrum P(f)', fontsize=14)
    plt.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(f'{OUTPUT_DIR}/pulse_spectrum_comparison.png', dpi=150)

    # ===== FIGURE 2: Power Spectral Density S_X(f) =====
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(f_fft/1e9, S_X, 'b-', linewidth=2, label=r'$S_X(f) = \frac{E\{a_k^2\}}{T_s}|P(f)|^2$')
    ax2.set(xlabel='Frequency (GHz)', ylabel=r'$S_X(f)$ (W/Hz)',
            title=f'Power Spectral Density (M={M})', xlim=[-5, 5])
    ax2.legend()
    ax2.grid(True)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/psd_plot.png', dpi=150)

    plt.show()