# pyramid-rollers

Helpers to build & document Web Services with [Pyramid](https://trypyramid.com/).

Originally forked from [Cornice](https://github.com/Cornices/cornice).

## Installation

```bash
pip install pyramid-rollers
```

## Quick Start

```python
from pyramid.config import Configurator
from pyramid_rollers import Service

hello = Service(name="hello", path="/hello", description="Simplest service")

@hello.get()
def get_hello(request):
    return {"Hello": "World"}

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("pyramid_rollers")
    config.scan()
    return config.make_wsgi_app()
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management
and [nox](https://nox.thea.codes/) for running the test matrix.

```bash
uv sync --dev
```

Run the full test matrix (marshmallow 3 and marshmallow 4):

```bash
uv run nox
```

Run the linter:

```bash
uv run ruff check .
```

## License

Mozilla Public License 2.0
