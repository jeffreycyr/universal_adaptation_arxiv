import pysam
import pandas as pd

# Load your VCF file
vcf_path = "variants.vcf.gz"
vcf = pysam.VariantFile(vcf_path)

# Initialize lists
records = []

# Loop through variants
for rec in vcf.fetch():
    # Extract allele frequency if available
    af = rec.info.get("AF", [None])[0]
    # Fallback: estimate from genotype counts
    if af is None and "AC" in rec.info and "AN" in rec.info:
        af = rec.info["AC"][0] / rec.info["AN"]

    # Timepoint placeholder (replace with actual if known)
    time = rec.pos  # or use sample metadata if available

    records.append({
        "time": time,
        "mutation_count": 1,
        "allele_frequency": af,
        "V": None,  # We'll estimate this later
        "S": None,  # Placeholder for selection coefficient
        "C": None,  # Placeholder for constraint
        "P_star": None  # Placeholder for normalized fitness
    })

# Convert to DataFrame
df = pd.DataFrame(records)

# Aggregate by time (if multiple variants per timepoint)
df = df.groupby("time").agg({
    "mutation_count": "sum",
    "allele_frequency": "mean"
}).reset_index()

# Save to CSV
df.to_csv("adaptation_metrics.csv", index=False)
print("✅ Adaptation metrics saved to adaptation_metrics.csv")
