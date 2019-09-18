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
compress = Compress()

@app.get("/logs")
@compress.compress()
async def my_verbose_function(request):
```

The current version supports both gzip and deflate algorithms.

## Options

Config options are to be setted as init argument:

* Compression min. size
* Compression level
* MIME types impacted
* Number of threadused for compression
