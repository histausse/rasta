# Directory structure
* docker
    Contains one directory per tool
    Each tool directory should have a RASTA_VERSION file that contains the subdir with the tested version
* tester
    A Python module to analyse the output of the tools, and detect errors
* envs
    One file per tool, used to setup the ENV variables in the containers.
    This env file MUST define a numerical TIMEOUT

# Installation

- Install docker

''''
apt install docker.io
''''

- Install singularity

''''
apt install singularity-ce
''''

# Scripts

## grunt-worker-launcher.sh

A script specifically designed to launch one instance on a cluster node. Typically, it would be passed to a batch command (on a cluster that is managed with slurm). This script is probably highly dependant on the cluster setup. There is little sense in manually launching this script.

## grunt-worker.py

Contains the bulk of the logic to:
    
- Obtain tasks (from a redis server). Here a task is a couple (APK, TOOL_NAME)
- check whether this task was already done
- create tmp dir
- Download the APK from AndroZoo
- run an analysis through a docker (`--docker`) or singularity (`--singularity`) container
- analyse the output of the analysis, and detect errors
- delete tmp dir
- save the results (into a couch database)
 
Also has a `--manual` mode, which is the simplest way to manually launch a task, in particular when coupled with the options to deactivate CouchDB (`--no-write-to-couch`) and Redis (`--no-mark-done`), and the option to not delete the tmp dir (`--keep-tmp-dir`).

## build_docker_images.sh

To batch create all Docker and Singularity images.

Parameter: the dir where the singularity files will be placed.

## launch-container.sh

- Called by grunt-worker.py.
- Can also be called manually to debug.

Parameters:

        1. Mode: Either DOCKER or SINGULARITY
        2. TOOL_NAME: for example, androguard or blueseal, etc
        3. CONTAINER_IMG: Either the name of the Docker image or the path to the sif file (without the trailing .sif)
        4. TMP_WORKDIR: a dir
        5. APK_FILENAME: the name of the APK file provided in TMP_WORKDIR (This script does NOT download apks)

# How to run

1. Choose the tool(s) you want to build the docker/singularity image by editing the file `./build_docker_images.sh on the line tools=. For example, to build didfail, change the line like below. By default, the script builds the docker/singularity image of all tools.

'''
tools="didfail"
'''


2. Create Docker and Singularity images (around 16 minutes on a modern laptop)
`./build_docker_images.sh path_you_want_the_sif_files_in` for example:

'''
bash build_docker_images.sh ~/singularity
'''

3.  Create a venv

'''
python3 -m venv rasta-venv
source rasta-venv/bin/activate
'''

4. Install necessary python package

'''
python3 -m pip install -r requirements.txt
'''

5. Launch one manual analysis

- 5.0: fill in the settings.ini file with your Androzoo api key:

'''
[AndroZoo]
apikey = your_api_key
'''

- 5.1: launch the singularity container on a given hash of Android application:

'''
./grunt-worker.py --base-dir /tmp/RASTA/  --no-mark-done --keep-tmp-dir --no-write-to-couch --manual --task didfail --sha APK_HASH --singularity --image-basedir SINGULARITY_IMAGE_DIRECTORY
'''

For example:

'''
./grunt-worker.py --base-dir /tmp/RASTA/  --no-mark-done --keep-tmp-dir --no-write-to-couch --manual --task didfail --sha 0003468487C29A71A5DA40F59E4F1F5DFF026126DD64BB58C572E30EE167C652 --singularity --image-basedir ~/singularity
'''
