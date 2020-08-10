import sys
import time
from BSrank.get_item import main

target = sys.argv[1]
while 1:
    try:
        main(target)
        break
    except Exception as e:
        print(e)
        time.sleep(60)
