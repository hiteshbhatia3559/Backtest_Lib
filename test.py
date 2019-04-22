import datetime

base = datetime.datetime(2019,4,22,0,0,0)
date_list = [base - datetime.timedelta(minutes=x) for x in range(0, 10)]

print(date_list)
