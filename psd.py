import numpy as np


def calculate_psd(T_s, M, f_max=5e9):
    """
    Calculate the Power Spectral Density of the PAM waveform.

    S_X(f) = E{a_k^2}/T_s * |P(f)|^2

    Parameters:
    -----------
    T_s : float
        Symbol duration
    M : int
        Number of amplitude levels
    f_max : float
        Maximum frequency for plotting (default: 5 GHz)

    Returns:
    --------
    f : ndarray
        Frequency vector
    S_X : ndarray
        Power spectral density
    """
    # Frequency vector
    f = np.linspace(-f_max, f_max, 10000)

    # Calculate E{a_k^2} for uniform symbol distribution
    # For M-PAM with A_m = β(2m - M + 1), where m ∈ [0, M-1]
    amplitudes = np.array([A_m(m) for m in range(M)])
    E_ak_squared = np.mean(amplitudes ** 2)

    # Fourier transform of triangular pulse p(t)
    # For symmetric triangular: P(f) = T_s * sinc^2(π*f*T_s)
    P_f = T_s * np.sinc(f * T_s) ** 2

    # Calculate PSD
    S_X = (E_ak_squared / T_s) * np.abs(P_f) ** 2

    print(f"""
--- PSD Calculation ---
E{{a_k^2}}: {E_ak_squared:.4f}
Symbol duration T_s: {T_s * 1e9:.2f} ns
Frequency range: {-f_max / 1e9:.1f} to {f_max / 1e9:.1f} GHz
""")

    return f, S_X


def plot_psd(f, S_X, T_s):
    """
    Plot the Power Spectral Density.
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))

    # Plot PSD in dB scale
    S_X_dB = 10 * np.log10(S_X + 1e-12)  # Add small value to avoid log(0)

    plt.plot(f / 1e9, S_X_dB, 'b-', linewidth=1.5)
    plt.xlabel('Frequency (GHz)', fontsize=12)
    plt.ylabel('Power Spectral Density (dB)', fontsize=12)
    plt.title(f'PSD of PAM Waveform - M={M}, T_s={T_s * 1e9:.2f} ns',
              fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Save plot
    plt.savefig('psd_plot.png', dpi=150)
    print(f"PSD plot saved to: psd_plot.png")
    plt.show()



def main(N, T_s, input_bits):
    """
    Generate and plot PAM waveform and PSD.
    """
    # ... existing code ...

    # Plot the waveform

    # Part 3: Calculate and plot PSD
    f, S_X = calculate_psd(T_s, M)
    plot_psd(f, S_X, T_s)
