
cd $(dirname ${0})
mydir=$(/bin/pwd)

outdir=/mnt/NoBackup/twitter
if [ ! -d /mnt/NoBackup/twitter ]; then
  outdir=${HOME}/twitter
  mkdir -p ${outdir}
fi
prefix=*tweets_

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
  sleep 30
done
