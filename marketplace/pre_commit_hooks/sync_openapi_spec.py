import json
from pathlib import Path

from ..api import api


def main():
    openapi_spec_path = Path("openapi.json")
    spec_staged = openapi_spec_path.read_text()
    spec_desired = json.dumps(api.openapi(), indent=4) + "\n"

    if spec_staged != spec_desired:
        print(
            f"The OpenAPI specification file {openapi_spec_path} was not in sync "
            "with the marketplace.api specification."
        )
        openapi_spec_path.write_text(spec_desired)


if __name__ == "__main__":
    raise SystemExit(main())
