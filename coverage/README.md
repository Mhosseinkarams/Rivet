# Rivet CMS analysis coverage

Current coverage: https://cms-rivet.web.cern.ch/cms-rivet/rivet-coverage-cms.html

## Instructions for updating

For the `mk-coverage-html-cms` step there might be the need to install the HTML package (`pip install --user html`)

API token needed for including merge requests, get it here: https://gitlab.cern.ch/profile/personal_access_tokens

    get-json-inspire-cms
    get-rivethd-json *.ins.json
    wget -N --no-check-certificate https://gitlab.com/hepcedar/rivet/raw/main/doc/coverage/rivet-coverage-cms.rank
    mk-coverage-html-cms inspire-cms-*.rhd.json -r rivet-coverage-cms.rank -R --token <you personal token>
    cp rivet-coverage-cms.html /eos/project/c/cmsweb/www/generators/Rivet/