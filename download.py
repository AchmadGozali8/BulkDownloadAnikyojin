import requests
from progress.bar import Bar
import time
import shutil
import os

url = "https://www1.zippyshare.com/d/SvQ3kiK3/24843/%5bAnikyojin.net%5d%20KanoAstra%2002%20%28480p%29%20-%20samehadaku.mkv"

#star download
with requests.get(url, stream=True) as r:
    with open('test.mkv', 'wb') as f:
        shutil.copyfileobj(r.raw, f)
