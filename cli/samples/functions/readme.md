# Creating a Function

Read more about function details and requirements in the [Karbon Platform Services Admin Guide](https://portal.nutanix.com/page/documents/details?targetId=Karbon-Platform-Services-Admin-Guide:Karbon-Platform-Services-Admin-Guide).

A function lets you run code on data flowing through a [Data Pipeline](../datapipelines). This code could be as simple as basic text processing function or it could be advanced code implementing artificial intelligence algorithms, leveraging popular machine learning frameworks like Tensorflow. Supported languages include Python, Golang, and Node.js.

## Example Usage

Create a function with parameters and other attributes defined in a YAML file.

`user@host$ kps create -f echo-with-param.yaml`

## echo-with-param.yaml

This sample defines a function named `echo-param-fn` which accepts a parameter of type `string`.

The Python script `echo.py` executes in the Python run-time environment `python-env` running on the Karbon Platform Services edge and displays the string param onto stdout.


``` yaml
kind: function
name: echo-param-fn
project: Starter
description: this function accepts params
sourceCodePath: "echo.py"
language: python
environment: python-env
params:
  - name: param1
    type: string
```

| Field Name | Value or Subfield Name / Description | Value or Subfield Name / Description |
|----------------|----------------|----------------|
| kind | `function` | Specify the resource type  |
| name |     | Unique name for your function |
| project  |  | Specify an existing project by project name to associate with this resource |
| description |     | Describe your function |
| sourceCodePath |  | Specify the file system path for your function. This can be an absolute path or a path relative to location this echo-with-param.yaml file |
| language |  | Here, `python`. Code language. Other languages include: <br /> `golang` for Golang <br /> `node`  for Node.js|
| environment |  | Here, `python-env`. Run-time environment running on the Karbon Platform Services edge. Other run-times include: <br /> `tensorflow-python` for Tensorflow <br /> `node-env` for Node.js <br /> `golang` for Golang |
| params |  | Parameters to be passed into the function. These params can be different for different data pipelines. Please see how these are used in [data pipelines](../datapipelines) for more details |
|  | name | Here, `param1`. Name of the parameter defined in your Python script |
|  | type | A string that `echo.py` outputs or displays |


## object-detect.yaml

This sample defines a function named `object-detect-fn` which is associated with the Starter project. 

The Python script `detect.py` detects objects in a given graphic frame or JPG format file.
It executes in the Python run-time environment `tensorflow-python-env` running on the Karbon Platform Services edge.

``` yaml
kind: function
name: object-detect-fn
project: Starter
description: detects objects in a given frame/jpeg
sourceCodePath: "detect.py"
language: python
environment: tensorflow-python # use this if your function depends on tensorflow
```

| Field Name | Value or Subfield Name / Description | Value or Subfield Name / Description |
|----------------|----------------|----------------|
| kind | `function` | Specify the resource type  |
| name |     | Unique name for your function |
| project  |  | Specify an existing project by project name to associate with this resource |
| description |     | Describe your function |
| sourceCodePath |  | Specify the file system path for your function. This could be an absolute path or a path relative to location this object-detect.yaml file |
| language |  | Here, `python`. Code language |
| environment |  | Here, `tensorflow-python` for Tensorflow |
