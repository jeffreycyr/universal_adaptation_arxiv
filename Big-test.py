import pandas as pd
import matplotlib.pyplot as plt

# Load both datasets
microbial = pd.read_csv("adaptation_metrics_filled.csv")
ml = pd.read_csv("ml_adaptation_metrics.csv")

# -----------------------------
# Plot normalized performance P* vs time
# -----------------------------
plt.figure(figsize=(8,6))
plt.plot(microbial["time"], microbial["P_star"], label="Microbial Evolution", marker="o")
plt.plot(ml["time"], ml["P_star"], label="ML Training", marker="s")
plt.xlabel("Time (generations / epochs)")
plt.ylabel("Normalized Performance P*")
plt.title("Universal Adaptation Law: P* vs Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Pstar_vs_time.png", dpi=300)
plt.show()

# -----------------------------
# Plot P* vs Adaptation Budget B
# -----------------------------
plt.figure(figsize=(8,6))
plt.plot(microbial["B"], microbial["P_star"], label="Microbial Evolution", marker="o")
plt.plot(ml["B"], ml["P_star"], label="ML Training", marker="s")
plt.xlabel("Adaptation Budget B")
plt.ylabel("Normalized Performance P*")
plt.title("Universal Adaptation Law: P* vs B")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Pstar_vs_B.png", dpi=300)
plt.show()
