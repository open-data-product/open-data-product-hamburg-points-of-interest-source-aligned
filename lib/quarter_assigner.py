import json
import os

import pandas as pd
from opendataproduct.tracking_decorator import TrackingDecorator
from shapely.geometry.point import Point
from shapely.geometry.polygon import Polygon


@TrackingDecorator.track_time
def assign_quarter(geojson_path, csv_path, data_path, clean=False, quiet=False):
    # Load geojson
    geojson = read_geojson_file(
        os.path.join(
            geojson_path,
            "hamburg-administrative-boundaries",
            "hamburg-quarters.geojson",
        )
    )

    # Iterate over files
    for subdir, dirs, files in sorted(os.walk(csv_path)):
        # Make data path
        os.makedirs(data_path, exist_ok=True)

        for file_name in [
            file_name
            for file_name in sorted(files)
            if file_name.endswith("-details.csv")
        ]:
            source_file_path = os.path.join(csv_path, subdir, file_name)
            quarter_cache_file_path = os.path.join(data_path, "quarter-cache.csv")

            assign_quarter_id(
                source_file_path,
                quarter_cache_file_path,
                geojson=geojson,
                clean=clean,
                quiet=quiet,
            )


def assign_quarter_id(source_file_path, quarter_cache_file_path, geojson, clean, quiet):
    dataframe = read_csv_file(source_file_path)

    if "quarter_id" not in dataframe.columns:
        # Read LOR area cache
        if os.path.exists(quarter_cache_file_path):
            quarter_cache = read_csv_file(quarter_cache_file_path)
            quarter_cache.set_index("latlon", inplace=True)
        else:
            quarter_cache = pd.DataFrame(columns=["latlon", "quarter_id"])
            quarter_cache.set_index("latlon", inplace=True)

        dataframe = dataframe.assign(
            quarter_id=lambda df: df.apply(
                lambda row: build_quarter_id(
                    row["lat"],
                    row["lon"],
                    geojson,
                    quarter_cache,
                    quarter_cache_file_path,
                ),
                axis=1,
            )
        )
        dataframe_errors = dataframe["quarter_id"].isnull().sum()

        # Write csv file
        dataframe.assign(
            quarter_id=lambda df: df["quarter_id"].astype(int).astype(str).str.zfill(8)
        )
        dataframe.to_csv(source_file_path, index=False)
        if not quiet:
            print(
                f"✓ Assign quarter IDs to {os.path.basename(source_file_path)} with {dataframe_errors} errors"
            )
    else:
        print(f"✓ Already assigned quarter IDs to {os.path.basename(source_file_path)}")


def build_quarter_id(lat, lon, geojson, quarter_cache, quarter_cache_file_path):
    quarter_cache_index = f"{lat}_{lon}"

    # Check if planning area is already in cache
    if quarter_cache_index in quarter_cache.index:
        return quarter_cache.loc[quarter_cache_index]["quarter_id"]
    else:
        point = Point(lon, lat)

        quarter_id = None

        for feature in geojson["features"]:
            id = feature["properties"]["id"]
            coordinates = feature["geometry"]["coordinates"]
            polygon = build_polygon(coordinates)
            if point.within(polygon):
                quarter_id = id

        # Store result in cache
        if quarter_id is not None:
            quarter_cache.loc[quarter_cache_index] = {"quarter_id": quarter_id}
            quarter_cache.assign(
                quarter_id=lambda df: df["quarter_id"]
                .astype(int)
                .astype(str)
                .str.zfill(8)
            )
            quarter_cache.to_csv(quarter_cache_file_path, index=True)
            return quarter_id
        else:
            return 0


def build_polygon(coordinates) -> Polygon:
    points = [tuple(point) for point in coordinates[0][0]]
    return Polygon(points)


def read_csv_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as csv_file:
            return pd.read_csv(csv_file, dtype={"quarter_id": "str"})
    else:
        return None


def read_geojson_file(file_path):
    with open(file=file_path, mode="r", encoding="utf-8") as geojson_file:
        return json.load(geojson_file, strict=False)
