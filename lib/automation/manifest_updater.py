import os
from datetime import datetime

import yaml

from lib.tracking_decorator import TrackingDecorator


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


@TrackingDecorator.track_time
def update_manifest(manifest_path, data_path):
    # Load manifest
    with open(manifest_path, "r") as file:
        manifest = yaml.safe_load(file)

    updated = False
    csv_output_port = next(
        (output_port for output_port in manifest["output_ports"] if
         output_port["id"] == "hamburg-points-of-interest-csv"),
        None)

    # Iterate over files
    for subdir, dirs, files in sorted(os.walk(data_path)):
        subdir = subdir.replace(f"{data_path}/", "")
        for file in sorted([file for file in files if not file.endswith("-cache.csv")]):
            file_url = f"https://raw.githubusercontent.com/open-lifeworlds/open-lifeworlds-data-product-hamburg-points-of-interest-source-aligned/main/data/{subdir}/{file}"

            if csv_output_port["files"] is None:
                csv_output_port["files"] = []

            if csv_output_port is not None and file_url not in csv_output_port["files"]:
                csv_output_port["files"].append(file_url)
                print(f"✓ Update manifest by {subdir}/{file}")
                updated = True
            else:
                print(f"✓ Already in manifest {subdir}/{file}")

    if updated:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        csv_output_port["metadata"]["updated"] = timestamp
        print(f"✓ Update manifest timestamp")

    # Write manifest
    with open(manifest_path, "w") as file:
        yaml.dump(manifest, file, sort_keys=False, Dumper=IndentDumper, allow_unicode=True)
