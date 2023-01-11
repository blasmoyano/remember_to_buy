from math import ceil
from urllib.parse import urlencode
from urllib.parse import urljoin
from urllib.parse import urlparse


def generate_meta(page, per_page, total):
    return {
        "page": page,
        "per_page": per_page,
        "total_items": total,
        "total_pages": ceil(total / per_page),
        "next": page + 1,
        "previous": page if page == 0 else page + 1,
    }


def generate_meta_url(endpoint, meta, params):
    next_page = None if meta["page"] + 1 > meta["total_pages"] else meta["page"] + 1
    previous_page = None if meta["page"] - 1 == 0 else meta["page"] - 1

    params = dict(params)
    if params.get("page", False):
        del params["page"]

    if params.get("per_page", False):
        del params["per_page"]

    parameters = urlencode(params)

    if parameters:
        if next_page is None:
            meta["next"] = None
        else:
            meta[
                "next"
            ] = f"{endpoint}?{parameters}&page={next_page}&per_page={meta['per_page']}"
        if previous_page is None:
            meta["previous"] = None
        else:
            meta[
                "previous"
            ] = f"{endpoint}?{parameters}&page={previous_page}&per_page={meta['per_page']}"
    else:
        if next_page is None:
            meta["next"] = None
        else:
            meta["next"] = f"{endpoint}?page={next_page}&per_page={meta['per_page']}"

        if previous_page is None:
            meta["previous"] = None
        else:
            meta[
                "previous"
            ] = f"{endpoint}?page={previous_page}&per_page={meta['per_page']}"
    return meta


def format_endpoint(base, path):
    base = urlparse(base)
    base = base._replace(scheme="https").geturl()
    return urljoin(base, path)
