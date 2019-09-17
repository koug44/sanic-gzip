# sanic-gzip
A Sanic plugin to manage compression as a decorator

## Installation

Install with `pip`:

`pip install sanic-gzip`

## Usage

Usage is as simple as a decorator before your function

```python
from sanic import Sanic
from sanic_gzip import compress

app = Sanic(__name__)

@app.get("/logs")
@compress()
async def my_verbose_function(request):
```

The current version supports both gzip and deflate algorithms.

## Options

You can specify the compression level (1-9) and the minimum size (in bytes) threshold for compressing responses.

```python
def compress(compress_level=6, compress_min_size=500):
```
