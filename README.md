# Hackernews Scraper

Help scripts for scraping hackernews webiste based on the official [Hackernews API](https://github.com/HackerNews/API).

# Environment variable

- `FILENAME`: output file name
- `ITEM_OFFSET`: the offset of scraping first item id, note that the script scrap item in reverse older

# How to speed up the speed of scraping?

Just start multiple processes.

```console
env ITEM_OFFSET=25300000 python ./hackernews.py &
env ITEM_OFFSET=25200000 python ./hackernews.py &
env ITEM_OFFSET=25100000 python ./hackernews.py &
env ITEM_OFFSET=25000000 python ./hackernews.py &
env ITEM_OFFSET=24900000 python ./hackernews.py &
env ITEM_OFFSET=24800000 python ./hackernews.py &
```

NOTE THAT there is no synchronization between those process, processes can write data to output file in arbitrary order. This might cause some text get cut in the middle. If you care about this. don't use this script or make each process write different file.

```console
env FILENAME=part1 ITEM_OFFSET=25300000 python ./hackernews.py &
env FILENAME=part2 ITEM_OFFSET=25200000 python ./hackernews.py &
env FILENAME=part3 ITEM_OFFSET=25100000 python ./hackernews.py &
env FILENAME=part4 ITEM_OFFSET=25000000 python ./hackernews.py &
env FILENAME=part5 ITEM_OFFSET=24900000 python ./hackernews.py &
env FILENAME=part6 ITEM_OFFSET=24800000 python ./hackernews.py &
```
