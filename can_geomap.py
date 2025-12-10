import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

# ========= CONFIG =========
EXCEL_FILE = "locations.xlsx"
SHAPEFILE = "ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp"

LAT_COL = "latitude"
LON_COL = "longitude"
CAT_COL = "category"
# ==========================

def main():
    # 1. Load Shapefile
    if not os.path.exists(SHAPEFILE):
        raise FileNotFoundError(f"Shapefile not found: {SHAPEFILE}")

    print("Loading Canada boundary...")
    world = gpd.read_file(SHAPEFILE)

    # The column is typically called ADMIN
    canada = world[world["ADMIN"] == "Canada"]

    # 2. Load

    print("Loading Excel locations...")
    df = pd.read_excel(EXCEL_FILE)

    # 3. Convert to GeoDataFrame
    gdf_points = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df[LON_COL], df[LAT_COL]),
        crs="EPSG:4326"
    )

    # 4. Reproject both datasets to Canada Albers
    canada = canada.to_crs(epsg=3347)
    gdf_points = gdf_points.to_crs(epsg=3347)

    # 5. Plot
    print("Creating map...")
    fig, ax = plt.subplots(figsize=(8, 8))

    canada.plot(ax=ax, color="white", edgecolor="black")

    gdf_points.plot(
        ax=ax,
        column=CAT_COL,
        legend=True,
        markersize=20,
        alpha=0.9,
    )
    
    # --- Label each point with its Excel ID ---
    for x, y, label in zip(gdf_points.geometry.x, gdf_points.geometry.y, gdf_points["id"]):
        ax.text(x, y, str(label), fontsize=6, ha="center", va="center")
    # -------------------------------------------


    ax.set_axis_off()
    plt.tight_layout()

    # 6. Save
    output_file = "canada_points.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")

    print(f"\n✔ Map successfully saved as {output_file}\n")
    plt.show()


if __name__ == "__main__":
    main()
