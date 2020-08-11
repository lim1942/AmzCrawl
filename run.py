from BSrank.get_item import *

target_list = sys.argv[1:].copy()
if target_list[0] != ROOT:
    target_list.insert(0, ROOT)
target = NODE_SEP.join(target_list)
print(target)
main(target)