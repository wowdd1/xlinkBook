#!/usr/bin/bash


clash_profiles="/mnt/c/Users/123/.config/clash/profiles/"
clash_config="/mnt/c/Users/123/.config/clash/profiles/list.yml"
out_file="/mnt/c/Users/123/Desktop/url.txt"

rawurlencode() {
  local string="${1}"
  local strlen=${#string}
  local encoded=""
  local pos c o

  for (( pos=0 ; pos<strlen ; pos++ )); do
     c=${string:$pos:1}
     case "$c" in
        [-_.~a-zA-Z0-9] ) o="${c}" ;;
        * )               printf -v o '%%%02x' "'$c"
     esac
     encoded+="${o}"
  done
  echo "${encoded}"    # You can either set a return variable (FASTER)
  REPLY="${encoded}"   #+or echo the result (EASIER)... or both... :p
}

grep  "url: https" $clash_config  > $out_file
sed  "s/    url: //g" -i $out_file

echo "myclash.txt"

RESULT=$(curl -s --upload-file $out_file https://transfer.sh/myclash.txt)

echo $RESULT

message="https://dianbao.vercel.app/send/3ACE17E995891/$(rawurlencode $RESULT)"

curl -s $message

echo ""

clash_profile_zip="clash-profiles.zip"
zip -rq  $clash_profile_zip $clash_profiles


echo ""
echo $clash_profile_zip

RESULT=$(curl -s --upload-file $clash_profile_zip "https://transfer.sh/$clash_profile_zip")

echo $RESULT

message="https://dianbao.vercel.app/send/3ACE17E995891/$(rawurlencode $RESULT)"

#echo $message

curl -s $message

rm $clash_profile_zip



echo ""
echo ""
