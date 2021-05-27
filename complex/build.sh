P='--platform=linux/amd64'

# docker build $P -f builders/Dockerfile.base -t builder/base . 
# docker build $P -f builders/Dockerfile.tool1 -t builder/tool1 . 
# docker build $P -f builders/Dockerfile.tool2 -t builder/tool2 . 
# docker build $P -f runners/Dockerfile.runner -t runner/runner .

IMAGES='builder/base builder/tool1 builder/tool2 runner/runner'

TIMEQUERY='.Created'
TIMEQUERY='.Metadata.LastTagTime'

for I in $IMAGES
do
    F="${I//\//_}"
    # docker inspect -f "{{ ${TIMEQUERY} }}" $I | sed 's/[-T ]//g' | sed 's/://' | sed 's/:/./' | cut -c 1-15
    TS=$(docker inspect -f "{{ ${TIMEQUERY} }}" $I | sed 's/[-T ]//g' | sed 's/://' | sed 's/:/./' | cut -c 1-15)
    echo $TS
    touch -m -t $TS dummy/$F
done

D='2021-05-17T15:36:40.082275013Z'