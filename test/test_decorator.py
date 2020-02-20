"""
Created on Oct 11, 2018

@author: eric-spitler
"""
import random
from typing import List
import unittest

from sanic import Sanic
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView

from sanic_gzip import Compress

# Define body once so that response size comparisons are valid
BODY = ''.join(str(random.random()) for _ in range(100))


def handle(request):
    print(f'Processing request : {request}')
    print(f'Request headers : {request.headers}')
    return HTTPResponse(BODY, content_type='text/plain')


class DecoratorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = Sanic(name='sanic-gzip-test')
        cls.compressor = Compress(compress_min_size=1)

        @cls.app.route(uri='/function')
        @cls.compressor.compress()
        async def get(request):
            return handle(request)

        class View(HTTPMethodView):

            @cls.compressor.compress()
            async def get(self, request):
                return handle(request)

        cls.app.add_route(handler=View.as_view(), uri='/view')

    def test_function_decoration(self):
        uncompressed_bytes = self._call_and_validate('/function', ['none'], False)

        compressed_bytes = self._call_and_validate('/function', ['gzip'], True)
        self.assertLess(compressed_bytes, uncompressed_bytes)

        # FIXME: deflate compression causes an error
        #   zlib.error: Error -3 while decompressing data: invalid stored block lengths
        # compressed_bytes = self._call_and_validate('/function', ['deflate'], True)
        # self.assertLess(compressed_bytes, uncompressed_bytes)

        compressed_bytes = self._call_and_validate('/function', ['gzip', 'deflate'], True)
        self.assertLess(compressed_bytes, uncompressed_bytes)

    def test_class_method_decoration(self):
        uncompressed_bytes = self._call_and_validate('/view', ['none'], False)

        compressed_bytes = self._call_and_validate('/view', ['gzip'], True)
        self.assertLess(compressed_bytes, uncompressed_bytes)

        # FIXME: deflate compression causes an error
        #   zlib.error: Error -3 while decompressing data: invalid stored block lengths
        # compressed_bytes = self._call_and_validate('/view', ['deflate'], True)
        # self.assertLess(compressed_bytes, uncompressed_bytes)

        compressed_bytes = self._call_and_validate('/view', ['gzip', 'deflate'], True)
        self.assertLess(compressed_bytes, uncompressed_bytes)

    def _call_and_validate(self, uri: str, encodings: List[str], is_compressed: bool) -> int:
        headers = {
            'Accept-Encoding': ', '.join(encodings)
        }
        print()
        print('-' * 120)
        print(f'Requesting {uri} with headers : {headers}')
        response = self.app.test_client.get(uri, headers=headers, gather_request=False)
        print(f'Response : {response}')
        print(f'Response body : {response.body}')
        print(f'Response headers : {response.headers}')
        self.assertEqual(response.status, 200)
        if is_compressed:
            self.assertIn('Content-Encoding', response.headers)
            self.assertIn(response.headers['Content-Encoding'], encodings)
        else:
            self.assertNotIn('Content-Encoding', response.headers)
        return int(response.headers['Content-Length'])
