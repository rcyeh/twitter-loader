
cd $(dirname ${0})
mydir=$(/bin/pwd)

outdir=/mnt/NoBackup/twitter
if [ ! -d /mnt/NoBackup/twitter ]; then
  outdir=${HOME}/twitter
  mkdir -p ${outdir}
fi
prefix=*tweets_
s3bucket="s3://rcy-twitter/raw/aws/"
notify="arn:aws:sns:us-east-1:780170686194:rcyeh-sms"

i=0
# look for existing files and set index to first unused
echo "Looking for existing index high-water-mark ..."
for f in ${outdir}/${prefix}*; do
  j=$(echo ${f/${outdir}\/${prefix}/} | sed -e "s/\..*$//")
  if (( ${i} < ${j} )); then
    i=${j}
  fi
done

cd ${outdir}
while true; do
  prev_i=${i}
  i=$(( ${i} + 1 ))
  echo "Writing to ${outdir}/${prefix}${i}.json.gz"
  python ${mydir}/sample_stock_tweets.py ${i}
  aws s3 cp sample_tweets_${i}.json.gz ${s3bucket} --storage-class STANDARD_IA && touch uploaded_tweets_${i}.json.gz && rm -f sample_tweets_${i}.json.gz uploaded_tweets_${prev_i}.json.gz &
  if [ -f .shutdown ]; then
    break
  fi
  sleep 0.1
done
rm -f .shutdown
message="twitter-loader on $(hostname) shut down at $(date)"
aws sns publish --topic-arn "${notify}" --message "${message}" & 
echo ${message}
