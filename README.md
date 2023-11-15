# RASTA

Reproducibility of the Rasta experiment.

## Data

Some data are needed to reproduce the experiment (at the very least, the androzoo indexes we used to sample our dataset). Those data are too heavy to be stored in a git, so they need to be download from zenodo to the root of this repository:

```
curl https://zenodo.org/records/10137905/files/rasta_data_v1.0.tgz?download=1 | tar -xz
```

## Dependencies

To run the Rasta experiment, some tools are required:
- Docker (e.g. version 24.0.6), 
- Singularity (e.g version 3.11.1) 
- a modern version of Python (e.g. Python 3.10 or 3.11). 
- gzip
- sqlite3

One way to install those tools is to use Nixpkgs (`nix-shell -p docker singularity python310 python310Packages.numpy python310Packages.matplotlib sqlite3`), another way is to follow the instructions of the different tools (<https://docs.sylabs.io/guides/3.11/user-guide/>, <https://docs.docker.com/>).

They are also some python dependencies that need to be installed in a virtual env:

```
python3 -m venv venv
source venv/bin/activate
pip install rasta_data_manipulation/
pip install -r rasta_exp/requirements.txt
```

From now end, all commands are run from inside the venv.

## Dataset

The datasets we used (Drebin and Rasta, split in 10 balanced sets) are in `data/dataset`.

To reproduce the generation of the dataset, `latest.csv.gz` and `year_and_sdk.csv.gz` are required: `rasta-gen-dataset data/androzoo/latest.csv.gz data/androzoo/year_and_sdk.csv.gz -o data/dataset` (this will no generate the drebin dataset)

## Container Images

The containers are stored in `data/imgs`. They can be regenerated with

```
cd rasta_exp
./build_docker_images.sh ../data/imgs
cd ..
```

(The container images will be released with the final release)

The container and binary of Perfchecker is not provided as this tool is only available on demand.

## Experiment

The results of the experiment are stored in `data/results/archives/`. They can be extracted with:

```
mkdir -p data/results/reports/rasta
mkdir -p data/results/reports/drebin
for archive in $(ls data/results/archives/status_set*.tgz); do tar -xzf ${archive} --directory data/results/reports/rasta; done
tar -xzf data/results/archives/status_drebin.tgz --directory data/results/reports/drebin
```

They can also be regenerated by running the experiment.

To run the experiment local, first you must set the `settings.ini` file in `rasta_exp`. Replacing it by this is enough (don't forget to replace `<KEY>` by your AndroZoo key):

```
[AndroZoo]
apikey = <KEY>
base_url = https://androzoo.uni.lu
```

Then, you can run the experiment with:

```
./rasta_exp/run_exp_local.sh ./data/imgs ./data/dataset/drebin ./data/results/reports/drebin/status_drebin
for i in {0..9}; do
    ./rasta_exp/run_exp_local.sh ./data/imgs "./data/dataset/set${i}" "./data/results/reports/rasta/status_set${i}"
done;
```

(This takes a lot of times)

## Database

The reports are parsed into databases to help analyzing them. The database can be extracted from their dumps or generated from the reports and dataset.

To extract the dumps:

```
zcat data/results/drebin.sql.gz | sqlite3 data/results/drebin.db
zcat data/results/rasta.sql.gz | sqlite3 data/results/rasta.db
```

To generate the databases:

```
./rasta_data_manipulation/make_db.sh ./data
```

Generating the database require an androzoo API key and a lot of times because we download the apks to get there total dex size (the value indicated in latest.csv only take into account the size of `classes.dex` and not the sum of the size of all dex file when they are more than one).

## Database Usage


Most of the results used in the paper can be extracted with:

```
./rasta_data_manipulation/extract_result.sh ./data
```

They are 4 tables in the database, `apk`, `tool`, `exec` and `error`.

### Apk table

The data related to the apks of the dataset are in the `apk` table.

The entry of the `apk` table have the columns:

- `sha256`: The hash of the apk
- `first_seen_year`: The first year the apk has been seen
- `apk_size`: The total size of the apk
- `vt_detection`: The number of detections by Virus Total
- `min_sdk`: The min SDK indicated by the apk
- `max_sdk`: The max SDK indicated by the apk
- `target_sdk`: The target SDK indicated by the apk
- `apk_size_decile`: The decile of size apk the apk belong to
- `dex_date`: The date indicated in the dex file
- `pkg_name`: The name of the apk
- `vt_scan_date`: The year when the apk was provided to Virus Total
- `dex_size`: The total size of the dex files
- `added`: The year the apk was added to AndrooZoo
- `markets`: Where the apk was collected
- `dex_size_decile`: The decile of dex size the apk belong to
- `dex_size_decile_by_year`: The decile of dex size for the first_seen_year of the apk

### Tool table

The data related to the tools used by the experiment are in the `tool` table.

Its columns are:

- `tool_name`: The name of the tool
- `use_python`: If the tool uses python
- `use_java`: If the tool uses java
- `use_scala`: If the tool uses scala
- `use_ocaml`: If the tool uses ocaml
- `use_ruby`: If the tool uses ruby
- `use_prolog`: If the tool uses prolog
- `use_soot`: If the tool uses soot
- `use_androguard`: If the tool uses androguard
- `use_apktool`: If the tool uses apktool

### Exec table

The data related to the execution of an analysis are in the `exec` table.

- `sha256`: The hash of the tested apk
- `tool_name`: The name of the tested tool
- `tool_status`: The status of the analysis: FAILED, FINISHED, TIMEOUT, OTHER
- `time`: The duration of the analysis
- `exit_status`: The exit status code return by the execution
- `timeout`: If the execution timedout
- `max_rss_mem`: The memory used by the analysis

They are other values collected by `time` during the analysis:
- `avg_rss_mem`
- `page_size`
- `kernel_cpu_time`
- `user_cpu_time`
- `nb_major_page_fault`
- `nb_minor_page_fault`
- `nb_fs_input`
- `nb_fs_output`
- `nb_socket_msg_received`
- `nb_socket_msg_sent`
- `nb_signal_delivered`

### Error table

The error collected during the analysis are stored in the `error` table.
All columns are not used, depending on the `error_type`.

- `tool_name`: The name of the tool that raised the error
- `sha256`: The hash of the apk analyzed when the error was raised
- `error_type`: The type of error (Log4j, Java, Python, Xsb, Ocaml, Log4jSimpleMsg, Ruby)
- `error`: The name of the error
- `msg`: The message of the error
- `cause`: Rough estimation of the cause of the error
- `first_line`: The line number of the first line of the error in the log
- `last_line`: The line number of the last line of the error in the log
- `logfile_name`: The file in which the error was collected (usually stdout and stderr)
- `file`: The file of the ruby script that raised the error
- `line`: The line number of the instruction that raised the error
- `function`: The function that raised the error
- `level`: The level of the log (eg FATAL, CRITICAL)
- `origin`: The origin of the error (java class referred by log4j)
- `raised_info`: 'Raised at' information (for Ocaml errors)
- `called_info`: 'Called from' information (for Ocaml errors)

### Usage

The data can be explored using SQL queries. `tool_name` and `sha256` are the usual foreign keys used for joins.

#### Exemple:

This SQL query gives the average time taken by an analysis made by tool using soot, associated with the average size of bytecode of the applications analysed, grouped by deciles of this size on the whole dataset:

```
$ sqlite3 data/results/rasta.db
sqlite> SELECT AVG(dex_size), AVG(time) 
FROM exec 
    INNER JOIN apk ON exec.sha256=apk.sha256 
    INNER JOIN tool ON exec.tool_name=exec.tool_name 
WHERE tool.use_soot = TRUE AND exec.tool_status = 'FAILED' 
GROUP BY dex_size_decile
ORDER BY AVG(dex_size);
```

## Reusing a Specific Tool

The containers are not on docker hub yet, so they need to be built using `build_docker_images.sh`. The images are named `rasta-<tool-name>`, and the environment variables associated are in `rasta_exp/envs/<tool-name>_docker.env`.

To enter a container, run:

```
docker run --rm --env-file=rasta_exp/envs/mallodroid_docker.env -v /tmp/mnt:/mnt -it rasta-mallodroid bash
```

Here, `/tmp/mnt` is mounted to `/mnt` in the container. Put the `apk` to analyze in it. 

To run the analysis, run `/run.sh <apk>` where `<apk>` is the name of the apk in `/mnt`, without the `/mnt` prefix. The artifact of the analysis are stored in `/mnt`, including the `stdout`, `stderr` and result of the `time` command.

```
root@e3c39c14e382:/# ls /mnt
E29CCE76464767F97DAE039DBA0A0AAE798DF1763AD02C6B4A45DE81762C23DA.apk
root@e3c39c14e382:/# /run.sh E29CCE76464767F97DAE039DBA0A0AAE798DF1763AD02C6B4A45DE81762C23DA.apk
root@e3c39c14e382:/# ls /mnt/
E29CCE76464767F97DAE039DBA0A0AAE798DF1763AD02C6B4A45DE81762C23DA.apk  report  stderr  stdout
```