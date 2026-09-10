"""api-shop public API.

The v2 API is framework-neutral. Version 1.x names remain exported during the
compatibility window and are also available from :mod:`api_shop.legacy`.
"""

name = "api_shop"

from .version import __version__

from .contracts import (  # noqa: E402
    ApiError,
    Body,
    Cookie,
    File,
    Form,
    Header,
    Path,
    Query,
    RequestContext,
    ResponseContext,
)
from .dispatcher import Dispatcher  # noqa: E402
from .legacy import (  # noqa: E402
    Api,
    ApiDataClass,
    ApiResponseModelFields,
    ApiShop,
    SingleApiShop,
    get_api_result_json,
    get_api_result_response,
    get_single_apishop,
    return_response,
    single_apishop,
)
from .openapi import generate_openapi  # noqa: E402
from .registry import ApiRegistry  # noqa: E402

__all__ = [
    "ApiRegistry",
    "Dispatcher",
    "RequestContext",
    "ResponseContext",
    "ApiError",
    "Path",
    "Query",
    "Header",
    "Cookie",
    "Body",
    "Form",
    "File",
    "generate_openapi",
    "Api",
    "ApiDataClass",
    "ApiResponseModelFields",
    "ApiShop",
    "SingleApiShop",
    "get_api_result_json",
    "get_api_result_response",
    "get_single_apishop",
    "return_response",
    "single_apishop",
]
