# building docker image
$ docker-compose build
# activate interactive bash shell on the container
$ docker-compose run --rm crawler /bin/bash
# run crawler.py
$ python crawler.py --keyword "keyword"