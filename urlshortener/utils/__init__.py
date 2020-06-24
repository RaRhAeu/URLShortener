import io
from hashlib import sha256
from tempfile import SpooledTemporaryFile

import base62  # noqa
import segno


def generate_short_url(long_url=None, length=7):
    hs = sha256(long_url.encode('utf-8')).digest()
    short_url = base62.encodebytes(hs)[:length]
    return short_url


def generate_qr_code(hyperlink):
    qr = segno.make_qr(hyperlink)
    f = SpooledTemporaryFile()
    qr.save(f, kind="png", scale=10)
    f.seek(0)
    res_io = io.BytesIO(f.read())
    res_io.seek(0)
    return res_io
