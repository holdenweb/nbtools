export SCAM_PROJECT=~/Projects/Python/intVideos/project
#
# XXX program positions should really be independent of $SCAM_PROJECT
#
NBSTATS=$SCAM_PROJECT/tools/nbstats.py
TOPICS=$SCAM_PROJECT/tools/topics.py
MERGE=$SCAM_PROJECT/tools/merge.py
export CONTENT_HOME=~/Projects/Python/intermediate-notebooks

echo "Copying outline"
cd $SCAM_PROJECT
cp outline.txt $CONTENT_HOME
echo "Creating statistics"
echo "   Content Analysis"
(cd $SCAM_PROJECT/nbsource;
    $NBSTATS *.ipynb > $CONTENT_HOME/nbstats.txt)
echo "   Unstarted topics"
$TOPICS -u > $CONTENT_HOME/unstarted.txt
echo "   Orphaned notebooks"
$TOPICS -o > $CONTENT_HOME/orphaned.txt
echo "Generating and transferring notebooks"
rm notebooks/*.ipynb
$MERGE
tar cfh - ./notebooks/*.ipynb ./notebooks/nb | (cd $CONTENT_HOME; tar xf -)
echo "---------------------------"
(cd $CONTENT_HOME;
    git add *
    git commit -m "Nightly dump for `date '+%Y-%m-%d %H:%M'`"
)
