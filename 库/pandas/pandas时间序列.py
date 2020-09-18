
import pandas as pd
import numpy as np
import datetime

# 依托 NumPy 的 datetime64、timedelta64 等数据类型，pandas 可以处理各种时间序列数据，
# 还能调用 scikits.timeseries 等 Python 支持库的时间序列功能。？
# 解析时间格式字符串、np.datetime64、datetime.datetime 等多种时间序列数据。
dti = pd.to_datetime(['1/1/2018', np.datetime64('2018-01-01'), datetime.datetime(2018, 1, 1)])
print(dti)

#生成 DatetimeIndex、TimedeltaIndex、PeriodIndex 等定频日期与时间段序列。
dti = pd.date_range('2018-01-01', periods=3, freq='H')
print(dti)

# 处理、转换带时区的日期时间数据。
dti = dti.tz_localize('UTC')
print(dti)
dti.tz_convert('US/Pacific')
print(dti)

# 用绝对或相对时间差计算日期与时间。
friday = pd.Timestamp('2018-01-05')
print(friday.day_name())
# 添加 1 个日历日
saturday = friday + pd.Timedelta('1 day')
# 添加 1 个工作日，从星期五跳到星期一
monday = friday + pd.offsets.BDay()
print(monday)

# Pandas 提供了一组精悍、实用的工具集以完成上述操作。
# Pandas 支持 4 种常见时间概念：
# 日期时间（Datetime）：带时区的日期时间，类似于标准库的 datetime.datetime
# 时间差（Timedelta）：绝对时间周期，类似于标准库的 datetime.timedelta
# 时间段（Timespan）：在某一时点以指定频率定义的时间跨度
# 日期偏移（Dateoffset）：与日历运算对应的时间段，类似 dateutil 的 dateutil.relativedelta.relativedelta
#  一般情况下，时间序列主要是 Series 或 DataFrame 的时间型索引，可以用时间元素进行操控。
pd.Series(range(3), index=pd.date_range('2000', freq='D', periods=3))

pd.Series(pd.date_range('2000'), freq='D', periods=3)

