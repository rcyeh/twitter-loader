
cd $(dirname ${0})
mydir=$(/bin/pwd)

outdir=/mnt/NoBackup/twitter
if [ ! -d /mnt/NoBackup/twitter ]; then
  outdir=${HOME}/twitter
  mkdir -p ${outdir}
fi
prefix=*tweets_
s3bucket="s3://rcy-twitter/raw/aws/"

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
  echo "Writing to ${outdir}/${prefix}${i}.json.gz"
  python ${mydir}/sample_stock_tweets.py ${i}
  for p in sample; do
    aws s3 cp ${p}_tweets_${i}.json.gz ${s3bucket} --storage-class STANDARD_IA && rm -f ${p}_tweets_${i}.json.gz && touch uploaded_tweets_${i}.json.gz
  done &
  sleep 0.1
done
