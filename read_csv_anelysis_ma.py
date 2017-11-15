import sys
import tushare as ts
import os

if __name__ == '__main__':
	with open('/Users/zj/company_code/test/000776_ma.csv', 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
		line = ''.join(line).strip('\n')
		print 'line:',line
