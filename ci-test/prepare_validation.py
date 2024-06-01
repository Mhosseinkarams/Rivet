#!/usr/bin/env python
import os, re
from ci_configs import *

def collect_pag():

    pag_header = "PAG::"

    # list of PAG directories
    pags = ["B2G", "BPH", "EXO", "FSQ", "GEN", "HIG", "HIN", "SMP", "SUS", "TOP"]

    # collect PAG from the given labels
    labels = CI_LABELS.split(",")
    this_pag = []
    for pag in pags:
        if f"{pag_header}{pag}" in labels:
            this_pag.append(pag)

    # label should be given with PAG
    if len(this_pag) == 0:
        raise ValueError(f"No label given with PAG name that are in {pags}")

    # label should not be given with more than one PAG
    if len(this_pag) > 1:
        raise ValueError(f"More than one label given for PAG {pag}, choose one")

    # return one and only PAG
    return this_pag[0]

def collect_analysis(pag):

    title = CI_TITLE

    # title should only have one () pair for InspireHEP ID parsing
    if (title.count("(") != 1) and (title.count(")") != 1) :
        raise ValueError(f"Number of parentheses, '(' and ')', should each be one in the PR title")

    this_analysis = re.findall('\((.*?)\)',title)[0]

    # Rivet cc file should exist
    if not os.path.exists(f"{CI_HOME}/{pag}/src/{this_analysis}.cc"):
        raise ValueError(f"Rivet cc file {CI_HOME}/{pag}/src/{this_analysis}.cc does not exist")
    # Rivet data files should exist
    if not os.path.exists(f"{CI_HOME}/{pag}/data/{this_analysis}.info"):
        raise ValueError(f"Rivet data file {CI_HOME}/{pag}/data/{this_analysis}.info does not exist")
    if not os.path.exists(f"{CI_HOME}/{pag}/data/{this_analysis}.plot"):
        raise ValueError(f"Rivet data file {CI_HOME}/{pag}/data/{this_analysis}.plot does not exist")
    if not os.path.exists(f"{CI_HOME}/{pag}/data/{this_analysis}.yoda"):
        raise ValueError(f"Rivet data file {CI_HOME}/{pag}/data/{this_analysis}.yoda does not exist")

    return this_analysis

def collect_beamenergy():

    beamenergy_header = "BeamE::"

    beamenergies = ["7TeV", "8TeV", "13TeV", "13p6TeV"]
    this_beamenergy = []
    # collect BEAM E from the given labels
    labels = CI_LABELS.split(",")

    for beamenergy in beamenergies:
        if f"{beamenergy_header}{beamenergy}" in labels:
            this_beamenergy.append(beamenergy)

    # label should be given with beamenergy
    if len(this_beamenergy) == 0:
        raise ValueError(f"No label given with beamenergy name that are in {beamenergies}")

    # label should not be given with more than one beamenergy
    if len(this_beamenergy) > 1:
        raise ValueError(f"More than one label given for beamenergy {beamenergy}, choose one")

    # return one and only beamenergy
    return this_beamenergy[0]

def main():

    # collect job arguments
    pag = collect_pag()
    analysis = collect_analysis(pag)
    beamenergy = collect_beamenergy()

    with open("setenv_validation.sh", "w") as wf:
        wf.write(f"#!/usr/bin/env bash\n")
        wf.write(f"export CI_PAG={pag}\n")
        wf.write(f"export CI_ANALYSIS={analysis}\n")
        wf.write(f"export CI_BEAMENERGY={beamenergy}\n")

if __name__ == "__main__":
    main()
