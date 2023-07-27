# scheduler-server

[![Image Builds](https://img.shields.io/github/actions/workflow/status/simonsobs/scheduler-server/build.yaml?branch=main)](https://github.com/simonsobs/scheduler-server/actions/workflows/build.yaml?query=workflow%3A%22Publish+Images+to+Container+Registries%22)
[![Docker Hub](https://img.shields.io/badge/dockerhub-latest-blue)](https://hub.docker.com/r/simonsobs/scheduler-server)

## Related Packages

* [**scheduler**](https://github.com/simonsobs/scheduler) - The core scheduling
  library, a.k.a. `schedlib`.
* [**scheduler-server**](https://github.com/simonsobs/scheduler-server) - This
  package. The Flask API for fetching schedules.
* [**scheduler-web**](https://github.com/simonsobs/scheduler-web) - The web
  front end for the scheduler.

## Installation
First clone this repository, and then install it with
```bash
pip install -r requirements.txt
pip install -e .
```
## Launch
Launching it requires `gunicorn` to be available. If we are inside this directory, run
```bash
gunicorn --bind localhost:8010 scheduler_server.app:app
```

### Docker
Alternatively, you can launch the server in a docker container:
```bash
docker run --rm -p 8010:8010 scheduler-server
```

## Schedule API
The API is temporarily hosted here: https://scheduler-uobd.onrender.com

### Endpoint
`POST /api/v1/schedule/`

### Purpose
The Schedule API is used to generate a schedule of commands.

### Request
The API expects a JSON object in the request body with the following properties:

- `t0`: a string representing the start time in the format "YYYY-MM-DD HH:MM"
- `t1`: a string representing the end time in the format "YYYY-MM-DD HH:MM"
- `policy`: a json string representing the scheduling policy. It should contain a `"policy"` key which specify the name of the policy and a `"config"` key which contains a dictionary of configurations for this given policy. The provided configuration will overwrite the default configuration used. Current supported policy names: `"dummy"` and `"basic"`.  

### Response

The API returns a JSON object with the following properties:
- `status`: a string indicating the status of the request, either 'ok' or 'error'
- `commands`: a string representing the generated schedule of commands
- `message`: a string representing the message of the request

The API will return a HTTP status code of 200 OK on success and 400 Bad Request on error.

### Example

Request:
```
POST /api/v1/schedule/
{
"t0": "2022-01-01 12:00",
"t1": "2022-01-01 14:00",
"policy": {"policy": "dummy", "config": {}}
}
```

Successful Response:
```
{
"status": "ok",
"commands": "import time\ntime.sleep(1)\ntime.sleep(1)\ntime.sleep(1)\n",
"message": "Success"
}
```

Unsuccessful Response:
```
{
"status": "error",
"message": "Invalid input"
}
```

Test with Curl
```bash
curl -L -X POST -H "Content-Type: application/json" -d '{"t0": "2022-01-01 12:00", "t1": "2022-01-01 14:00", "policy": "{\"policy\": \"dummy\", \"config\": {}}"}' http://127.0.0.1:8010/api/v1/schedule
```
