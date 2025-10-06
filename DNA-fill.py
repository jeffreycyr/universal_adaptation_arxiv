import pandas as pd
import numpy as np

# Load your adaptation metrics
df = pd.read_csv("adaptation_metrics.csv")

# -----------------------------
# Default placeholder parameters
# -----------------------------
Ne = 1e8       # effective population size
mu = 1e-9      # mutation rate per base per generation
fb = 0.05      # fraction beneficial
default_S = 0.02
default_C = 0.01   # never zero!
alpha, beta, gamma = 1, 1, 1

# -----------------------------
# Variation V
# -----------------------------
V = Ne * mu * fb
df["V"] = V

# Selection S
df["S"] = default_S

# Constraint C
df["C"] = default_C

# -----------------------------
# Normalized performance P*
# -----------------------------
if "allele_frequency" in df.columns and df["allele_frequency"].notna().any():
    denom = df["allele_frequency"].max() - df["allele_frequency"].min()
    if denom > 0:
        df["P_star"] = (df["allele_frequency"] - df["allele_frequency"].min()) / denom
    else:
        # fallback to mutation count
        denom = df["mutation_count"].max() - df["mutation_count"].min()
        if denom > 0:
            df["P_star"] = (df["mutation_count"] - df["mutation_count"].min()) / denom
        else:
            df["P_star"] = np.linspace(0.1, 0.9, len(df))  # synthetic progression
else:
    denom = df["mutation_count"].max() - df["mutation_count"].min()
    if denom > 0:
        df["P_star"] = (df["mutation_count"] - df["mutation_count"].min()) / denom
    else:
        df["P_star"] = np.linspace(0.1, 0.9, len(df))

# -----------------------------
# Adaptation budget B
# -----------------------------
df["B_raw"] = ((df["V"]**alpha) * (df["S"]**beta)) / (df["C"]**gamma) * df["time"]

# Rescale B into a manageable range
scale_factor = df["B_raw"].max() / 100.0 if df["B_raw"].max() > 0 else 1
df["B"] = df["B_raw"] / scale_factor

# -----------------------------
# Final cleanup
# -----------------------------
df = df.replace([np.inf, -np.inf], np.nan).fillna(0)

# Save to new CSV
df.to_csv("adaptation_metrics_filled.csv", index=False)
print("✅ Saved adaptation_metrics_filled.csv with safe P_star and rescaled B")
