#!/usr/bin/env python
# -*- coding:utf-8 -*-

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
import time

class DateClass:
	def __init(self):
		print 'init'

	def GetDate(self,stock_code):
		'''
		hs300 = ts.get_hs300s()
		print 'hs300:',hs300
		hs300.to_csv('/Users/zj/company_code/stock_data_analysis/hs300.csv')
		'''
		#stock_code = '000776'
		print 'GetDate stock_code:',stock_code
		cons = ts.get_apis()
		#qfq 前复权
		df_cons = ts.bar(stock_code,conn=cons,adj='qfq',ma=[60,120,250])
		file_name = '/Users/zj/company_code/stock_data_analysis/data/' + stock_code +'_ma_qfq.csv'
		df_cons.to_csv(file_name)
		#不复权
		df_cons = ts.bar(stock_code,conn=cons,ma=[60,120,250])
		file_name = '/Users/zj/company_code/stock_data_analysis/data/' + stock_code +'_ma.csv'
		df_cons.to_csv(file_name)
		#后复权
		df_cons = ts.bar(stock_code,conn=cons,adj='hfq',ma=[60,120,250])
		file_name = '/Users/zj/company_code/stock_data_analysis/data/' + stock_code +'_ma_hfq.csv'
		df_cons.to_csv(file_name)

		#df = ts.get_k_data('000776',start='2009-01-01', end='')
		#df.to_csv('/Users/zj/company_code/stock_data_analysis/000776.csv',columns=['date','open','close','high','low','code'])

	def Exit(self):
		tmp = os.popen("ps -ef|grep -w get_code_data |awk '{print $2}'").readlines()
		for current in tmp:
			content = "kill -9 " + str(current)
			print 'content:',content
			current_tmp = os.popen(content)

	def GetPEPB(self):
		df = ts.get_stock_basics()
		pe = df.ix['000776']['pe']
		pb = df.ix['000776']['pb']
		#xxx= df.ix['000776']['20170508']
		print 'GetPEPB pe:',pe,' pb:',pb

	def GetAllMarkert(self):
		df = ts.get_index()
		print 'GetAllMarkert df:',df

	def ReadStockListFromFile(self,stock_list):
		file_object2 = open("/Users/zj/company_code/stock_data_analysis/gupiao_stock.txt",'r')
		try:
			lines = file_object2.readlines()
			#print "type(lines)=",type(lines)
			for line in lines:
				tmp_line = line.split(" ")
				stock_list[tmp_line[0].strip("\n")] = tmp_line[1].strip("\n")
		finally:
			file_object2.close()

if __name__ == '__main__':
	#get stocklist from file
	stock_list = {}
	DateClass().ReadStockListFromFile(stock_list)
	print 'stock_list:',stock_list
	#get stock data from remote server 
	for key in stock_list:
		#stock_code = '000776'
		print 'key:',key,' value:',stock_list[key]
		DateClass().GetDate(stock_list[key])
		time.sleep(10)
	#//DateClass().GetPEPB()
	#//DateClass().GetAllMarkert()
	#exit program
	DateClass().Exit()










