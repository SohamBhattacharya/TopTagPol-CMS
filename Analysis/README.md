# Submitting condor jobs
1. Create a config file like `configs/condor/job_config.yml` which contains:
	* The python file the job will run (e.g. `python/condor-compatible-worker.py`).
	* The script that will run that python file (e.g. `configs/condor/condor_script_template_general.sh`).
	* The condor submit file (e.g. `configs/condor/condor_config_template_general.submit`).
	* The samples to be run over.
	* The output directory and file names.
2. To submit the jobs, run:
`python python/run_condor_general.py --config configs/condor/job_config.yml --submit`
Omitting the option `--submit` will only create the condor directories and files and will NOT submit the jobs.
You can use that for debugging.

3. Check the failed jobs with:
`python python/findFailedCondorJobs.py -d <dir1> <dir2> ...`
where `<dir>` are the directories under the condor job directory.
Pass the flag `--submit` to resubmit the failed jobs.	