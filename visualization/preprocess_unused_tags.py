import pandas as pd

updated_df = pd.read_csv("visualization/public/updated_dataset.csv")

exif_baseline_path = "visualization/public/exif_baseline.csv"
# gps_baseline_path = "visualization/public/gps_baseline.csv"
# interop_baseline_path = "visualization/public/interop_baseline.csv"

exif_baseline_df = pd.read_csv(exif_baseline_path)
# gps_baseline_df = pd.read_csv(gps_baseline_path)
# interop_baseline_df = pd.read_csv(interop_baseline_path)

used_tags = set(updated_df["tag_name"].unique())

exif_filtered = exif_baseline_df[exif_baseline_df["Tag Name"].isin(used_tags)]
# gps_filtered = gps_baseline_df[gps_baseline_df["Tag Name"].isin(used_tags)]
# interop_filtered = interop_baseline_df[interop_baseline_df["Tag Name"].isin(used_tags)]

exif_filtered.to_csv("visualization/public/exif_baseline_filtered.csv", index=False)
# gps_filtered.to_csv("visualization/public/gps_baseline_filtered.csv", index=False)
# interop_filtered.to_csv(
#     "visualization/public/interop_baseline_filtered.csv", index=False
# )
