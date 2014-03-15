export PROJECT_HOME=~/Projects/Python/intVideos/project
NBSTATS=$PROJECT_HOME/tools/nbstats.py
TOPICS=$PROJECT_HOME/tools/topics.py
SANITY=$PROJECT_HOME/tools/sanity.py
export CONTENT_HOME=~/Projects/Python/intermediate-notebooks

echo "Copying outline"
cd $PROJECT_HOME
cp outline.txt $CONTENT_HOME
echo "Creating statistics"
echo "   Content Analysis"
(cd $PROJECT_HOME/nbsource;
    $NBSTATS *.ipynb > $CONTENT_HOME/nbstats.txt)
echo "   Unstarted topics"
$TOPICS -u > $CONTENT_HOME/unstarted.txt
echo "   Orphaned notebooks"
$TOPICS -o > $CONTENT_HOME/orphaned.txt
echo "Generating and transferring notebooks"
rm notebooks/*.ipynb
$SANITY
tar cfh - ./notebooks/*.ipynb ./notebooks/nb | (cd $CONTENT_HOME; tar xf -)
echo "---------------------------"
(cd $CONTENT_HOME;
    git add *
    git commit -m "Nightly dump for `date '+%Y-%m-%d %H:%M'`"
)
