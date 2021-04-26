SECRET=$1
echo RAW $SECRET
ROT=$(echo $SECRET | tr A-Za-z  B-ZAb-za)
echo ROT $ROT
if [ "$1" = "some secret value" ]
then
    echo "This is it"
else
    echo "This is NOT"
fi
