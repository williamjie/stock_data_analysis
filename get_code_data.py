'''
import sys
import tushare as ts


#print "333:",ts.get_k_data('000776', ktype='W', autype='hfq')
cons = ts.get_apis()
#df = ts.bar('000776',conn=cons,ma=[60,120,250])
#df.head(5)
#print 'df:',df

print "xxxxx year:",ts.bar('000776',conn=cons,freq='Y')
sys.exit()
'''
import sys
import tushare as ts
import os

class DateClass:
	def __init(self):
		print 'init'
	
	def GetDate(self):
		cons = ts.get_apis()
		df_cons = ts.bar('000776',conn=cons,ma=[60,120,250])
		df_cons.to_csv('/Users/zj/company_code/test/000776_ma.csv')

		df = ts.get_k_data('000776',start='2009-01-01', end='')
		df.to_csv('/Users/zj/company_code/test/000776.csv',columns=['date','open','close','high','low','code'])

	def Exit(self):
		tmp = os.popen("ps -ef|grep -w get_code_data |awk '{print $2}'").readlines()
		for current in tmp:
			content = "kill -9 " + str(current)
			print 'content:',content
			current_tmp = os.popen(content)

if __name__ == '__main__':
	DateClass().GetDate()
	DateClass().Exit()










