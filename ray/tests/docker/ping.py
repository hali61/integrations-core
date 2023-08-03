# Script used for docker healthcheck because curl is not installed (and I want to avoid building a custom image)

import sys
from urllib.request import urlopen, Request

with urlopen(Request(sys.argv[1])) as response:
    if response.status == 200:
        exit(0)
    else:
        exit(1)
