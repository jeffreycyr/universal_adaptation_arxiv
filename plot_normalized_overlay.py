import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Logistic function
def logistic(B, K, r, B0):
    return K / (1 + np.exp(-r * (B - B0)))

# Load datasets
microbial = pd.read_csv("adaptation_metrics_filled.csv")
ml = pd.read_csv("ml_adaptation_metrics.csv")

# Clean data
def clean_data(x, y):
    mask = np.isfinite(x) & np.isfinite(y)
    return x[mask], y[mask]

x_m, y_m = clean_data(microbial["B"].values, microbial["P_star"].values)
x_ml, y_ml = clean_data(ml["B"].values, ml["P_star"].values)

# Fit logistic to microbial
popt_m, _ = curve_fit(logistic, x_m, y_m, p0=[1, 0.01, np.median(x_m)], maxfev=10000)
y_m_fit = logistic(x_m, *popt_m)

# Fit logistic to ML
popt_ml, _ = curve_fit(logistic, x_ml, y_ml, p0=[1, 0.01, np.median(x_ml)], maxfev=10000)
y_ml_fit = logistic(x_ml, *popt_ml)

# -----------------------------
# Normalize both fits to [0,1]
# -----------------------------
y_m_norm = y_m_fit / np.max(y_m_fit)
y_ml_norm = y_ml_fit / np.max(y_ml_fit)

# -----------------------------
# Plot overlay
# -----------------------------
plt.figure(figsize=(8,6))
plt.plot(x_m, y_m_norm, label="Microbial (normalized)", color="blue")
plt.plot(x_ml, y_ml_norm, label="ML (normalized)", color="orange")
plt.xlabel("Adaptation Budget B")
plt.ylabel("Normalized Performance P* (scaled)")
plt.title("Universal Adaptation Law: Normalized Overlay")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Pstar_vs_B_overlay.png", dpi=300)
plt.show()
