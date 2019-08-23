# -*- coding: utf-8 -*-
try:
    import urllib.request as urllib2
    from urllib.error import URLError
    from http.client import HTTPException
except ImportError:
    import urllib2
    from urllib2 import URLError
    from http.client import HTTPException
import time


BLOCK_SIZE = 8192


def do_download(url, hook=None):
    """
    Downloads file and returns speed in mbps.
    """
    returnFormat = "{:06.3f}"
    http_handler = None
    try:
        http_handler = urllib2.urlopen(url)
    except URLError as e:
        if hook is not None:
            hook(None, "'{}': {}".format(url, e.reason))
        return returnFormat.format(0)
    except HTTPException as e:
        if hook is not None:
            hook(None, "'{}': {}".format(url, e))
            hook(100)
        return returnFormat.format(0)

    if http_handler:
        file_size = float(http_handler.headers["Content-Length"])
        start_time = time.time()
        status_downloaded = 0
        while True:
            buf = http_handler.read(BLOCK_SIZE)
            if not buf:
                break
            if hook is not None:
                status_downloaded += len(buf)
                progress = (float(status_downloaded) / file_size) * 100
                if progress >= 1:
                    hook(int(progress))
                    status_downloaded = ((float(progress) - int(progress)) / 100) * file_size
        speed = ((file_size * 8) / (1024 * 1024)) / (time.time() - start_time)
        http_handler.close()
    else:
        speed = 0

    return returnFormat.format(speed)
