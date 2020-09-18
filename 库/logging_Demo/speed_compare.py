import time
import logging
logging.basicConfig(filename='test.log', level=logging.INFO)
logger = logging.getLogger('kenneth')

# a = time.time()
# num = 0
# while num < 10000:
#     num = num + 1
#     print(num)
# print('有"print"时的耗时：%f' % (time.time() - a))

b = time.time()
num = 0
while num < 1000000:
    num = num + 1
print('没有"print"时的耗时：%f' % (time.time() - b))
#
c = time.time()
num = 0
while num < 1000000:
    num = num + 1
logger.info('完成')
print('使用logger的耗时：%f' % (time.time() - c))