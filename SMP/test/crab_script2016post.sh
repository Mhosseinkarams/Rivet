#this is not mean to be run locally

echo Check if TTY
if [ "`tty`" != "not a tty" ]; then
  echo "YOU SHOULD NOT RUN THIS IN INTERACTIVE, IT DELETES YOUR LOCAL FILES"
else
echo "================== START OF CUSTOM CRAB SCRIPT========================="
cp -rv rivetSetup.sh ${CMSSW_BASE}/src/Rivet
echo "Preparing Rivet paths"
source ${CMSSW_BASE}/src/Rivet/rivetSetup.sh
echo "Run CMSSW"
cmsRun -j FrameworkJobReport.xml -p runRivetAnalyzer_VJJ_miniAOD2016post.py

echo "============= END OF CUSTOM CRAB SCRIPT ========================="
fi
