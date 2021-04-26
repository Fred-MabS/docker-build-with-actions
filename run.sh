SECRET=$1
echo RAW $SECRET
ROT=$(echo $SECRET | tr A-Za-z  B-ZAb-za)
echo ROT $ROT