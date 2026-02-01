# PAM Communication System - Τηλεπικοινωνιακά Συστήματα

**Στοιχεία:**
- p = 8 (τελευταίο ψηφίο ΑΜ)
- M = 64 (επίπεδα πλάτους)
- Bits per symbol = 6
- Bit rate = 1 Gbit/s

**Κυματομορφή PAM:**
$$x(t) = \sum_k a_k \cdot p(t - kT_s)$$

**Πλάτος συμβόλου:**
$$A_m = \beta(2m - M + 1), \quad 0 \leq m \leq M-1, \quad \beta = 1$$

---

## Μέρος Α - Gray Code (i_graycode.py)

### Μεθοδολογία
Αναδρομική υλοποίηση του κώδικα Gray για την αντιστοίχιση bit groups σε σύμβολα.

```python
gray_recursive(n: int) -> list[str]
# n = αριθμός bits
# Επιστρέφει 2^n Gray code words
```

## Μέρος Β - PAM Waveform (ii_waveform.py)

### Τυπολόγιο
**Τριγωνικός παλμός (συμμετρικός):**
$$p(t) = \begin{cases} 1 - \frac{2|t|}{T_s} & |t| \leq \frac{T_s}{2} \\ 0 & \text{αλλιώς} \end{cases}$$

### Μεθοδολογία

1. **Μετατροπή bits σε σύμβολα**: Χρήση Gray code για αντιστοίχιση bit groups → symbol index m
2. **Υπολογισμός πλατών**: A_m = β(2m - M + 1) με β=1
3. **Τριγωνικός παλμός**: p(t) = 1 - |t|/T_s για |t| ≤ T_s
4. **Κυματομορφή PAM**: x(t) = Σ_k a_k·p(t - kT_s)


### Αποτελέσματα
![PAM Waveform](output/waveform_plot.png)

---

## Μέρος Γ - Power Spectral Density (iii_psd.py)

### Τυπολόγιο

**Φάσμα τριγωνικού παλμού( συμμετρικό, κέντρο στο Ts/2):**
$$P(f) = \frac{T_s}{2} \cdot \text{sinc}^2\left(\frac{f \cdot T_s}{2}\right)$$

**Φάσμα με FFT:**
$$P_{fft}(f) = \Delta t \cdot \text{fftshift}(\text{fft}(\text{fftshift}(p(t))))$$

**Μέση τετραγωνική τιμή πλάτους (M-PAM):**
$$E\{a_k^2\} = \frac{M^2 - 1}{3}$$

**Φασματική πυκνότητα ισχύος:**
$$S_X(f) = \frac{E\{a_k^2\}}{T_s} \cdot |P(f)|^2$$


### Μεθοδολογία

**1. Φάσμα παλμού P(f)**

Αναλυτικά:
```
P(f) = (T_s/2) · sinc²(f·T_s/2)
```

Αριθμητικά με FFT:
```python
P_fft = dt * fftshift(fft(fftshift(p_t)))
```

**2. Φασματική πυκνότητα ισχύος S_X(f)**

Από τη σχέση:
```
S_X(f) = E{a_k²}/T_s · |P(f)|²
```

Όπου E{a_k²} = (M² - 1)/3 = 1365 για M=64.

### Αποτελέσματα

**Σύγκριση φάσματος παλμού:**
![Pulse Spectrum Comparison](output/pulse_spectrum_comparison.png)

Η αναλυτική μέθοδος και η FFT δίνουν πρακτικά ταυτόσημα αποτελέσματα.

**Φασματική πυκνότητα ισχύος:**
![PSD Plot](output/psd_plot.png)

---

## Εκτέλεση

```bash
# Μέρος Α
python i_graycode.py

# Μέρος Β
python ii_waveform.py [N] [T_s] [input_bits]
python ii_waveform.py 100 6e-9 "110101100011100010010011"

# Μέρος Γ
python iii_psd.py [N] [T_s]
python iii_psd.py 100 6e-9
```

---

## Δομή Αρχείων

```
communication-systems/
├── 1_graycode.py      # Μέρος Α - Gray code
├── 2_waveform.py      # Μέρος Β - PAM waveform
├── 3_psd.py           # Μέρος Γ - PSD
├── output/            # Αποθήκευση γραφημάτων
│   ├── waveform_plot.png
│   ├── pulse_spectrum_comparison.png
│   └── psd_plot.png
└── README.md
```

---
