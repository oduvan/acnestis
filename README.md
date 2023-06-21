[![PyPI version fury.io](https://badge.fury.io/py/acnestis.svg)](https://pypi.python.org/pypi/acnestis/) 
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/acnestis.svg)](https://pypi.python.org/pypi/acnestis/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Acnestis - collect, aggregate and convert

![Acnestis](https://github.com/oduvan/acnestis/blob/master/title-600.png)

A very simple tool that allows you collect data from different sources, change it ia different ways

## Install

```bash
$ pip install acnestis
```

## You can do in declarative way

* convert data in the current folder
* aggregate data from different sources
* inheritence - when you collect data from different source - you can replace any file and those files will be used in the child repo

## Ok, this is confusing. Show me some example

first of all, you can find some examples in the [tests/data](https://github.com/oduvan/acnestis/tree/master/tests/data) folder 

*(source folders, or from-folders, may contain both yaml and py files, that doesn't mean both are required. We just make alternatives for testing and illustration)*


## Acnestis decloration

in order to declarate folder as acnestis folder you should do one of the following 

* create `.acnestis.yaml` file in that folder
* create `.acnestis.py` file in that folder. Py-file has an identical functionality, but some more power (of course)
* create both `.asnestis.yaml` and `.acnestis.py` - in that case yaml-file will be used as the main one, but can use declared global variables from the py-file
* declarate some of the sub-folders (even non-existed), in the current acnestis-decloration

In order to process acnestis folders - you should do

```bash
$ acnesting process from/folder to/folder
```

if no acnestis decloration in the `from/folder` it will just copy files to `to/folder`. if `from/folder` has at least one acnestis decloration - it will be used for processing that folder, the rest will be copied


### Simple convertion

*From: [tests/data/002_concat_poem](https://github.com/oduvan/acnestis/tree/master/tests/data/002_concat_poem/) to: [tests/data/002_concat_poem_result](https://github.com/oduvan/acnestis/tree/master/tests/data/002_concat_poem_result)*

this is a very simple example, where all files from folder poem.txt will be connected into a single file

* we declarate [poem.txt](https://github.com/oduvan/acnestis/tree/master/tests/data/002_concat_poem/poem.txt) folder as acnestis folder

Py version:

```python
from acnestis.processing import Processor
from acnestis.steps import concat_files

PROCESSOR = Processor([concat_files("poem.txt")], as_file="poem.txt")
```

YAML version:

```yaml
steps:
  - name: concat_files
    into_file: poem.txt
as_file: poem.txt
```

It has one single step `concat_files` with attribute `into_file: poem.txt` - so it simply concat all the files into one

Also processing has attribute `as_file` means the folder will be replaced with one file `poem.txt`

### Docker for more complex convertion

*From [tests/data/006_docker_svgo](https://github.com/oduvan/acnestis/tree/master/tests/data/006_docker_svgo) to: [tests/data/006_docker_svgo_result](https://github.com/oduvan/acnestis/tree/master/tests/data/006_docker_svgo_result)

you can build own convertion tools using docker

Py version:

```python
from acnestis.processing import Processor
from acnestis.steps import docker

PROCESSOR = Processor(
    [docker("acnestis_svgo", skip_pull=True)],
)
```

YAML version:

```yaml
steps:
  - name: docker
    image: acnestis_svgo
    skip_pull: true
```

one single step of using docker image `acnestis_svgo` for processing acnestis folder.

[Dockerfile of acnestis_svgo](https://github.com/oduvan/acnestis/tree/master/tests/docker_svgo/Dockerfile) is very simple:

```Dockerfile
# Base image
FROM node:20-alpine

# Install SVGO
RUN npm install -g svgo

# Execute the SVGO command when the container starts
ENTRYPOINT ["svgo", "-f", "/data_input", "-o", "/data_output"]
```

### you can use simple python-code for convertion

From [tests/data/004_code](https://github.com/oduvan/acnestis/tree/master/tests/data/004_code) to [tests/data/004_code_result](https://github.com/oduvan/acnestis/tree/master/tests/data/004_code_result)

## Now let's play with aggregation.

we want not only convert data, but first collect it from different sources

For the testing and examples we will use [oduvan/acnestis-test-repo](https://github.com/oduvan/acnestis-test-repo.git) github repository and its branches.

### simple use of git-repo

From: [data/007_git](https://github.com/oduvan/acnestis/tree/master/tests/data/007_git) to [data/007_git_result](https://github.com/oduvan/acnestis/tree/master/tests/data/007_git_result)

as any folders in the given repo are declarated as acnestis - we will see a simple copy files from the repo

Py version:

```python
from acnestis.processing import Processor
from acnestis.steps import git

PROCESSOR = Processor(
    [git("https://github.com/oduvan/acnestis-test-repo.git", branch="main")],
)
```

YAML version:

```yaml
steps:
  - name: git
    url: https://github.com/oduvan/acnestis-test-repo.git
    branch: main
```

### injection in the child 

From: [tests/data/008_git_processing](https://github.com/oduvan/acnestis/tree/master/tests/data/008_git_processing) to: [tests/data/008_git_processing_result](https://github.com/oduvan/acnestis/tree/master/tests/data/008_git_processing_result)

YAML version:

```yaml
steps:
  - name: git
    url: https://github.com/oduvan/acnestis-test-repo.git
```

is very simple, but the master branch of the repo contains an acnestis-folder, which means it will be processed after checkout into the current one.

During the checkout `poem.txt` folder will be created and all of the files in the folder will be connected

but in the current repo we created a folder poem.txt with file `3.txt` so that file become a part of processing process 

## More complex examples:

for more example check [tests/data](https://github.com/oduvan/acnestis/tree/master/tests/data) folder

* [009_git_subfolder](https://github.com/oduvan/acnestis/tree/master/tests/data/009_git_subfolder) - we don't need all of the files from the git repo, but only specific folder
* [010_subprocess_git](https://github.com/oduvan/acnestis/tree/master/tests/data/010_subprocess_git) - we declarate a specific acnestis folder for processing
* [011_sub_git_copy](https://github.com/oduvan/acnestis/tree/master/tests/data/011_sub_git_copy) - using of copy and rm steps
* [013_simple_aggregate](https://github.com/oduvan/acnestis/tree/master/tests/data/013_simple_aggregate) and [014_aggregate_two_poems](https://github.com/oduvan/acnestis/tree/master/tests/data/014_aggregate_two_poems) - more complex aggregation examples