import logging
#设置log的目录名称和日志的级别, 根据level等级确定是否输出哪个级别，debug<info<warning<error<critical
logging.basicConfig(filename='test.log', level=logging.INFO)

#创建log的对象，
# logger = logging.getLogger()     #使用此方法默认对象是root
logger_name = 'test1'
logger = logging.getLogger(logger_name)

#详细信息，典型地调试问题时会感兴趣
logger.debug('debug message')
# 证明事情按预期工作
logger.info('debug message')
# 表明发生了一些意外，或者不久的将来会发生问题（如‘磁盘满了’）。软件还是在正常工作
logger.warning('debug message')
# 由于更严重的问题，软件已不能执行一些功能了
logger.error('debug message')
# 严重错误，表明软件已不能继续运行了
logger.critical('debug message')



