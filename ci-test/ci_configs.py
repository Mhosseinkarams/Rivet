import pwd
import os
import time
time_stamp = time.strftime("%Y_%m_%d", time.localtime())

CI_SHELL = pwd.getpwuid(os.getuid()).pw_shell
CI_TEST = os.getenv("CI_TEST")
CI_HOME = os.getenv("CI_HOME")
CI_PAG = os.getenv("CI_PAG")
CI_ANALYSIS = os.getenv("CI_ANALYSIS")
CI_BEAMENERGY = os.getenv("CI_BEAMENERGY")
CI_COMMIT_SHA = os.getenv("CI_COMMIT_SHORT_SHA")
CI_LABELS = os.getenv("CI_MERGE_REQUEST_LABELS")
CI_TITLE = os.getenv("CI_MERGE_REQUEST_TITLE")
CI_STAMP = os.getenv("CI_STAMP")
CI_DEPLOY_PATH = os.getenv("CI_DEPLOY_PATH")
CI_RUNNER_PATH = os.getenv("CI_RUNNER_PATH")
EOS_PATH = os.getenv("EOS_PATH")
EOS_YODA_PATH = os.getenv("EOS_YODA_PATH")
HEPMC_PATH = os.getenv("HEPMC_PATH")

