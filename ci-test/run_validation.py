#!/usr/bin/env python
import os, sys, json
from ci_configs import *

CI_JOBENTRY = sys.argv[1]

def collect_jobs():

    json_path = f"{HEPMC_PATH}/{CI_JOBENTRY}.json"

    if not os.path.exists(json_path):
        sys.exit(f"JSON file for HEPMC files does not exist : {json_path}")

    with open (json_path, "r") as rf:
        jobs = json.load(rf)

    return jobs

def get_lines(jobs):

    def writeJobLines(jobName, jobArg):

        tmpJobLines = []

        jobType = jobArg["type"]
        jobSamples = jobArg["samples"]

        tmpJobLines.append(f"echo '\e[31m==> Started processing jobName :: {jobName}\e[0m'")
        tmpJobLines.append(f"mkdir -p yodas/{jobName}")
        tmpJobLines.append(f"mkdir -p plots/{jobName}")
        tmpJobLines.append(f"\n")

        yodaFiles = []
        for jobSample in jobSamples:
            tmpJobLines.append(f"wget https://rivetval.web.cern.ch/rivetval/HEPMC/{jobSample}.hepmc.gz --quiet")
            tmpJobLines.append(f"echo '==> Running jobSample :: {jobSample}'")
            tmpJobLines.append(f"rivet -a {CI_ANALYSIS} -o yodas/{jobName}/{jobSample}.yoda {jobSample}.hepmc.gz --pwd")
            tmpJobLines.append(f"rm {jobSample}.hepmc.gz")
            yodaFiles.append(f"yodas/{jobName}/{jobSample}.yoda")

        tmpJobLines.append(f"\n")

        tmpPlotLines = []

        # stacked plots for special cases
        if jobType == "stack": 
            # ratio plots don't properly work for ratio plots
            tmpStackLine = f"yodastack -M ratio -o yodas/{jobName}/{jobName}_stacked.yoda"
            for yodaFile in yodaFiles:
                tmpStackLine += f" {yodaFile}"
            tmpPlotLines.append(tmpStackLine)

        tmpJobLines.extend(tmpPlotLines)

        tmpJobLines.append(f"echo '\e[31m==> Finished processing jobName :: {jobName}\e[0m'")
        tmpJobLines.append(f"\n")
        tmpJobLines.append(f"\n")

        return tmpJobLines

    writeLines = []

    writeLines.append(f"#!/usr/bin/env bash")
    writeLines.append(f"\n")
    writeLines.append(f"cd {CI_RUNNER_PATH}")

    for jobName in jobs:
        jobArg = jobs[jobName]
        jobLines = writeJobLines(jobName, jobArg)
        writeLines.extend(jobLines)

    writeLines.append(f"cp -r {CI_RUNNER_PATH}/yodas/* {CI_DEPLOY_PATH}/yodas/")

    return writeLines

def main():

    jobs = collect_jobs()
    writeLines = get_lines(jobs)
    with open("run_validation.sh", "w") as wf:
        for line in writeLines:
            wf.write(line + "\n")

if __name__ == "__main__":

    main()
