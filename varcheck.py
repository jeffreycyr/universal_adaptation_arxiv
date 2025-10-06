import pandas as pd
import gzip

vcf_path = "variants.vcf.gz"
records = []

with gzip.open(vcf_path, 'rt') as f:
    for line in f:
        if line.startswith("#"):
            continue  # Skip header
        parts = line.strip().split('\t')
        pos = int(parts[1])
        info = parts[7]

        # Extract allele frequency (AF) if present
        af = None
        for field in info.split(';'):
            if field.startswith("AF="):
                try:
                    af = float(field.split("=")[1].split(",")[0])
                except ValueError:
                    af = None

        records.append({
            "time": pos,  # Using position as a placeholder for time
            "mutation_count": 1,
            "allele_frequency": af
        })

# Convert to DataFrame
df = pd.DataFrame(records)

# Aggregate by time (if needed)
df = df.groupby("time").agg({
    "mutation_count": "sum",
    "allele_frequency": "mean"
}).reset_index()

# Save to CSV
df.to_csv("adaptation_metrics.csv", index=False)
print("✅ Saved adaptation_metrics.csv")
