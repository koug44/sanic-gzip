import gzip
import zlib

from functools import wraps
from sanic.response import StreamingHTTPResponse

DEFAULT_MIME_TYPES = frozenset(
    [
        "text/html",
        "text/css",
        "text/xml",
        "text/plain",
        "application/json",
        "application/javascript",
    ]
)


async def _gzip_compress(response, compress_level):
    gzip_content = gzip.compress(response.body, compress_level)
    response.body = gzip_content
    response.headers["Content-Encoding"] = "gzip"
    response.headers["Content-Length"] = len(response.body)
    return response


async def _zlib_compress(response, compress_level):
    zlib_content = zlib.compress(response.body, compress_level)
    response.body = zlib_content
    response.headers["Content-Encoding"] = "deflate"
    response.headers["Content-Length"] = len(response.body)
    return response


def compress(compress_level=6, compress_min_size=500):
    def decorator(f):
        @wraps(f)
        async def _compress_response(request, *args, **kwargs):

            accept_encoding = request.headers.get("Accept-Encoding", "").lower()

            if (
                not accept_encoding
                or "gzip" not in accept_encoding
                or "deflate" not in accept_encoding
            ):
                return await f(request, *args, **kwargs)

            response = await f(request, *args, **kwargs)

            if (
                type(response) is StreamingHTTPResponse
                or not 200 <= response.status < 300
            ):
                return response

            content_length = len(response.body)
            content_type = response.content_type

            if ";" in content_type:
                content_type = content_type.split(";")[0]

            if (
                content_type not in DEFAULT_MIME_TYPES
                or content_length < compress_min_size
            ):
                return response

            if "gzip" in accept_encoding:
                return await _gzip_compress(response, compress_level)

            if "deflate" in accept_encoding:
                return await _zlib_compress(response, compress_level)

            return response

        return _compress_response

    return decorator
