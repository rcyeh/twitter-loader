
outdir=/mnt/NoBackup/twitter
prefix=CCtweets_

i=0
# look for existing files and set index to first unused
for f in ${outdir}/${prefix}*; do
  j=$(echo ${f/${outdir}\/${prefix}/} | sed -e "s/\..*$//")
  if (( ${i} < ${j} )); then
    i=${j}
  fi
done

while true; do
  i=$(( ${i} + 1 ))
  echo "Writing to ${outdir}/${prefix}${i}.json"
  python ./sample_stock_tweets.py 2>&1 > ${outdir}/${prefix}${i}.json | tee -a ${outdir}/${prefix}${i}.stderr
  sleep 30
done
