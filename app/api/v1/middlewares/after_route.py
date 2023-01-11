import json
from typing import Callable
import time
import logging
from fastapi import Request, Response
from fastapi.routing import APIRoute
from urllib.parse import urlparse, parse_qsl
from app.api.v1.helpers import format_endpoint, generate_meta_url

log = logging.getLogger("uvicorn")


class AfterRoute(APIRoute):
    def alter_body(self, body, endpoint, params):
        data = json.loads(body)

        if isinstance(data["response"], list):
            data["results"] = [] if len(data["errors"]) > 0 else data["response"]
        else:
            data["result"] = {} if len(data["errors"]) > 0 else data["response"]
        del data["response"]

        if data["meta"]:
            data["_meta"] = generate_meta_url(endpoint, data["meta"], params)
        else:
            data["_meta"] = {}
        del data["meta"]
        data = json.dumps(data).encode()
        return data, str(len(data))

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)
            parse_result = urlparse(str(request.url))
            dict_params = parse_qsl(parse_result.query, keep_blank_values=True)

            endpoint = format_endpoint(request.base_url._url, request.url.path)
            response.body, response.headers["content-length"] = self.alter_body(
                response.body, endpoint, dict_params
            )

            return response

        return custom_route_handler
