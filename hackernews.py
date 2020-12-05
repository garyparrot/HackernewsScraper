import re
import os
import time
import sys
import threading
from website import Website
from hacker_news_client import HackerNewsClient, HackerNewsItem

class TaskContext:
    """Store global information for threads"""

    def __init__(self, max_task_id, output = sys.stdout):
        self.max_task_id = max_task_id
        self.current = max_task_id
        self.output = output

    def nextTaskId(self):
        if self.current <= 0:
            return None
        else:
            self.current -= 1
            return self.current

class Pipeline:
    """Helper class for process object with pipeline pattern"""

    def __init__(self):
        self.pipes = []

    def next(self, pipe):
        self.pipes.append(pipe)
        return self

    def __call__(self, item):
        for pipe in self.pipes:
            item = pipe(item)
        return item

def processing(context: TaskContext):
    """parsing worker"""

    def pipe_item_to_text(x: HackerNewsItem):
        text = ""
        if x.title: text += x.title + " "
        if x.text:  text += x.text + " "
        return text
    
    pipe_remove_non_ascii = lambda x: re.sub(r"[^a-zA-Z]",r" ", x)
    pipe_merge_spaces     = lambda x: re.sub(' +', ' ', x)
    pipe_to_lower         = lambda x: x.lower()
    pipe_newline          = lambda x: x + "\n"
    pipe_file_writer      = lambda x: x if context.output.write(x) else x

    pipeline = Pipeline() \
            .next(pipe_remove_non_ascii) \
            .next(pipe_merge_spaces) \
            .next(pipe_to_lower) \
            .next(pipe_newline) \
            .next(pipe_file_writer)

    while True:
        try:
            # Get new task
            itemId = context.nextTaskId()
            # Exit loop if no more task
            if not itemId: break
            # Request a item from HN
            item = HackerNewsClient.getItem(itemId)

            # If it is a story, parse the site
            if item.type == "story" and item.url:
                print("Process", itemId, item.type, " -", item.title)
                print("Find website:", item.url)
                site = Website(item.url)
                pipeline(site.result)
            elif item.type == "comment":
                print("Process", itemId, item.type, " -", item.text[:30])
                pipeline(pipe_item_to_text(item))

        except Exception as e:
            print(e)

def main():
    with open(os.environ.get("FILENAME", "WordFile"), "a+") as f:
        offset = int(os.environ.get('ITEM_OFFSET', HackerNewsClient.getMaxItem()))
        context = TaskContext(offset, output = f)
        processing(context)

if __name__ == "__main__":
    main()
