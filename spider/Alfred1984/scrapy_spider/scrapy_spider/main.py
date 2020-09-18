from scrapy import cmdline   #倒入此模块能够直接执行外部的命令
cmdline.execute("scrapy crawl crawl_comments".split())