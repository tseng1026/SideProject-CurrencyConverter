import hmac
import urllib.parse
from calendar import timegm
from datetime import datetime
from hashlib import sha256

import requests


class XPayToken(requests.auth.AuthBase):
    def __init__(self, shared_secret: str):
        self.shared_secret = shared_secret

    def __call__(self, r):
        url = urllib.parse.urlparse(r.url)
        resource_path = self._get_resource_path(url.path[1:])
        query_string = "&".join(sorted(url.query.split("&")))
        body = r.body
        token = self._get_x_pay_token(
            self.shared_secret,
            resource_path,
            query_string,
            body,
        )
        r.headers["x-pay-token"] = token
        return r

    def _get_x_pay_token(
        self,
        shared_secret: str,
        resource_path: str,
        query_string: str,
        body: dict,
    ):
        if not body:
            body = ""
        timestamp = str(timegm(datetime.utcnow().timetuple()))
        hash_string = hmac.new(
            bytes(shared_secret, "utf-8"),
            bytes(timestamp + resource_path + query_string, "utf-8") + body,
            digestmod=sha256,
        ).hexdigest()
        return "xv2:" + timestamp + ":" + hash_string

    def _get_resource_path(self, path):
        return path[path.find("/") + 1 :]
