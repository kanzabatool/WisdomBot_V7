import json
import time

print('starting to read')
start_time = time.time()
my_dict = json.load(open('full_conceptnet_dict'))
print('DONE')
print("--- %s seconds ---" % (time.time() - start_time))

exit()
