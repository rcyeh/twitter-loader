
i=0
while true; do
  echo ${i}
  python ./sample_stock_tweets.py >> /mnt/NoBackup/twitter/CCtweets_${i}.json
  i=$[ $i + 1 ]
done
