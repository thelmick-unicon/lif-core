# Example usage

## Build the project
Navigate to this folder (where the `pyproject.toml` file is)

1. Export the dependencies (when using uv workspaces and having no project-specific lock-file):
``` shell
uv export --no-emit-project --output-file requirements.txt
```

2. Build a wheel:
``` shell
uv build --out-dir ./dist
```

## Build a docker image from root

``` shell
./build-docker.sh
```

## Run the image

``` shell
docker run --rm --name lif_example_data_source_rest_api -p 8011:8011 \
    lif-example-data-source-rest-api
````

The OpenAPI specification of this FastAPI app can now be accessed at http://localhost:8011/docs#


## API Calls for Manual Testing

You can manually test the API endpoints using `curl` and an environment variable for your auth token. 

Assuming the environment variable `API_TOKEN` is set to `1234abcd`

### Retrieve users (note the optional filters, `age_gt`, `name_like`, etc)
```shell
curl -X GET http://localhost:8011/users/ \
  -H "x-key: 1234abcd"
```

### Retrieve user with id `1000`
```shell
curl -X GET http://localhost:8011/users/1000 \
  -H "x-key: 1234abcd"
```

### Retrieve students (note the optional filters, `age_gt`, `name_like`, etc)
```shell
curl -X GET http://localhost:8011/students/ \
  -H "x-key: 1234abcd"
```

### Retrieve teachers (note the optional filters, `age_gt`, `name_like`, etc)
```shell
curl -X GET http://localhost:8011/teachers/ \
  -H "x-key: 1234abcd"
```

### Retrieve courses for the user with id `1000`
```shell
curl -X GET http://localhost:8011/users/1000/courses \
  -H "x-key: 1234abcd"
```

### Retrieve course with arbitrary id `123` (the id is not checked, just needs to be an `int`) for the user with id `1000`
```shell
curl -X GET http://localhost:8011/users/1000/courses/123 \
  -H "x-key: 1234abcd"
```

### Retrieve OB3CLR2 data with arbitrary user id `456` (the id is not checked, just needs to be an `int`)
```shell
curl -X GET http://localhost:8011/ob3clr2/456 \
  -H "x-key: 1234abcd"
```

### Retrieve LIF1 data with arbitrary user id `456` (the id is not checked, just needs to be an `int`)
```shell
curl -X GET http://localhost:8011/lif1/456 \
  -H "x-key: 1234abcd"
```

### Retrieve Campus API data with arbitrary user id `456` (the id is not checked, just needs to be an `int`)
```shell
curl -X GET http://localhost:8011/campusapi/456 \
  -H "x-key: 1234abcd"
```
