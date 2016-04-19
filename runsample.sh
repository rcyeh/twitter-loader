
cd $(dirname ${0})
mydir=$(/bin/pwd)

outdir=/mnt/NoBackup/twitter
prefix=*tweets_
s3bucket="s3://rcy-twitter/raw/home/"

i=0
# look for existing files and set index to first unused
for f in ${outdir}/${prefix}*; do
  j=$(echo ${f/${outdir}\/${prefix}/} | sed -e "s/\..*$//")
  if (( ${i} < ${j} )); then
    i=${j}
  fi
done

cd ${outdir}
while true; do
  i=$(( ${i} + 1 ))
  echo "Writing to ${outdir}/${prefix}${i}.json"
  python ${mydir}/sample_stock_tweets.py ${i}
  for p in entity sample; do
    aws s3 cp ${p}_tweets_${i}.json.gz ${s3bucket} --storage-class REDUCED_REDUNDANCY
  done &
  sleep 30
done
