SECRET=$1
echo RAW $SECRET
ROT=$(echo $SECRET | tr A-Za-z  B-ZAb-za)
echo ROT $ROT
MD5=$(echo $SECRET | md5 )
echo MD5 $MD5
if [ "$1" = "some secret value" ]
then
    echo "This is it"
else
    echo "This is NOT"
fi
