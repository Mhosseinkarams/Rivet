#!/usr/bin/env python
import os
from ci_configs import *
from natsort import natsorted

def get_lines():

    writeLines = []

    writeLines.append(f"#!/usr/bin/env bash")
    writeLines.append(f"\n")
    jobNames = os.listdir(f"{CI_RUNNER_PATH}/yodas")
    for jobName in jobNames:
        jobPath = f"{CI_RUNNER_PATH}/yodas/{jobName}/"
        yodaFiles = natsorted(os.listdir(jobPath))
        os.system(f"mkdir -p {CI_DEPLOY_PATH}/plots/{jobName}")
        writeLines.append(f'rivet-mkhtml {" ".join(jobPath+f for f in yodaFiles)} -o {CI_DEPLOY_PATH}/plots/{jobName} --single --mc-errs' )
    writeLines.append(f"\n")

    return writeLines

def main():

    writeLines = get_lines()
    with open("deploy_validation.sh", "w") as wf:
        for line in writeLines:
            wf.write(line + "\n")

if __name__ == "__main__":
    main()
