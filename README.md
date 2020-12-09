# building docker image
$ docker-compose build
# run MongoDB
$ docker-compose up mongodb
# activate interactive bash shell on the container
$ docker-compose run --rm crawler /bin/bash
# run crawler.py
$ python crawler.py --keyword "keyword"