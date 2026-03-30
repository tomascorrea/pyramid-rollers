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

## License

Mozilla Public License 2.0
