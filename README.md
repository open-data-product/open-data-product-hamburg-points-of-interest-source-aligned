[![Crawl content](https://github.com/open-data-product/open-data-product-hamburg-points-of-interest-source-aligned/actions/workflows/crawl-content.yaml/badge.svg)](https://github.com/open-data-product/open-data-product-hamburg-points-of-interest-source-aligned/actions/workflows/crawl-content.yaml)
[![Issues](https://img.shields.io/github/issues/open-data-product/open-data-product-hamburg-points-of-interest-source-aligned)](https://github.com/open-data-product/open-data-product-hamburg-points-of-interest-source-aligned/issues)

<br />
<p align="center">
  <a href="https://github.com/open-data-product/open-data-product-hamburg-points-of-interest">
    <img src="logo-with-text.png" alt="Logo" style="height: 80px; ">
  </a>

  <h1 align="center">Hamburg points of interest</h1>

  <p align="center">
    Data product providing Hamburg points-of-interest data
  </p>
</p>

## About The Project

See [data product canvas](docs/data-product-canvas.md) and [ODPS canvas](./docs/odps-canvas.md).

### Built With

* [Python](https://www.python.org/)
* [uv](https://docs.astral.sh/uv/)
* [ruff](https://docs.astral.sh/ruff/)

## Installation

Install uv, see https://github.com/astral-sh/uv?tab=readme-ov-file#installation.

```shell
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Usage

Run this command to generate and activate a virtual environment.

```shell
uv venv
source .venv/bin/activate
```

Run this command to install dependencies defined in `pyproject.toml`.

```shell
uv sync
```

Run this command to re-install the Open Data Product Python library (if necessary).

```shell
uv pip install --no-cache-dir git+https://github.com/open-data-product/open-data-product-python-lib.git
```

Run this command to start the main script.

```shell
uv run main.py
```

## Roadmap

See the [open issues](https://github.com/open-data-product/open-data-product-hamburg-points-of-interest/issues) for a
list of proposed features (and
known issues).

## License

Source data distributed under [Open Data Commons Open Database License ](https://opendatacommons.org/licenses/odbl/) (
ODbL) by the [OpenStreetMap Foundation](https://osmfoundation.org/) (OSMF).

Data product distributed under the [CC-BY 4.0 License](https://creativecommons.org/licenses/by/4.0/).
See [LICENSE.md](./LICENSE.md) for more information.

## Contact

opendataproduct@gmail.com
