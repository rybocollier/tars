# tars 

## Requirements

```
docker
make
docker-compose
python3.7 + pip
ngrok
```

## Makefile commands

```
- build
  will build the tars docker container with `docker-compose`

- run
  runs tars inside docker

- stop
  stops docker-compose and removes volumes and images

- deps
  regenerates the requirements/.txt files from the requirements/.in files

```

## Updating Dependencies

Follow these steps if you wish to add/update/delete dependencies
from the requirements/.in files.

1. Run `make deps`
2. Run `make build` to build another tars docker image with the updated dependencies.

## Local Development

**Note:** The following instructions assumes that you have already added tars as an app to your 
          slack organization and provided the necessary permissions. 

1. Run `make run`. 
2. Ngrok will provide you an endpoint, copy that endpoint. See the example below.

```
$ make run
./scripts/run.sh
Starting ngrok in port 5000
tars is live at http://c9732b2e.ngrok.io/slack/events


Starting tars ... 
Starting tars ... done
Attaching to tars
tars    |  * Serving Flask app "tars" (lazy loading)
tars    |  * Environment: development
tars    |  * Debug mode: on
tars    |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
tars    |  * Restarting with stat
tars    |  * Debugger is active!
tars    |  * Debugger PIN: 100-210-009
```

3. Log into slack and go to events subscription for tars and add the URL to the Request URL field.
4. Slack will send a challenge request to tars, if it succeeds you can continue with local development.
5. If the challenge request fails, look at the log output from `docker-compose` to find out why the request failed.
