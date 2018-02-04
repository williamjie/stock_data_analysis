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

	def GetDate(self,cons_info,stock_code,file_name_qfq,file_name,file_name_hfq,qfq_update_flag,flag_update,hfq_update_flag):
		'''
		hs300 = ts.get_hs300s()
		print 'hs300:',hs300
		hs300.to_csv('/Users/zj/company_code/stock_data_analysis/hs300.csv')
		'''
		#stock_code = '000776'
		print 'GetDate stock_code:',stock_code,' qfq_update_flag:',qfq_update_flag,' flag_update:',flag_update,' hfq_update_flag:',hfq_update_flag
		if qfq_update_flag:
			#qfq 前复权
			df_cons = ts.bar(stock_code,conn=cons_info,adj='qfq',ma=[60,120,250])
			#file_name_qfq = '/Users/zj/company_code/stock_data_analysis/data/' + stock_code +'_ma_qfq.csv'
			df_cons.to_csv(file_name_qfq)
		if flag_update:
			#不复权
			df_cons = ts.bar(stock_code,conn=cons_info,ma=[60,120,250])
			#file_name = '/Users/zj/company_code/stock_data_analysis/data/' + stock_code +'_ma.csv'
			df_cons.to_csv(file_name)
		if hfq_update_flag:
			#后复权
			df_cons = ts.bar(stock_code,conn=cons_info,adj='hfq',ma=[60,120,250])
			#file_name_hfq = '/Users/zj/company_code/stock_data_analysis/data/' + stock_code +'_ma_hfq.csv'
			df_cons.to_csv(file_name_hfq)

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
				stock_list[tmp_line[1].strip("\n")] = tmp_line[0].strip("\n")
		finally:
			file_object2.close()

	def TimeStampToTime(timestamp):
		timeStruct = time.localtime(timestamp)
		return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

	def get_FileModifyTime(self,filePath):
		#filePath = unicode(filePath,'utf8')
		t = os.path.getmtime(filePath)
		return t

if __name__ == '__main__':
	cons = ts.get_apis()
	count = 0
	for fn in os.listdir('/Users/zj/company_code/stock_data_analysis/data/'): #fn 表示的是文件名
	        count = count+1
	print 'file count:',count
	#get stocklist from file
	stock_list = {}
	DateClass().ReadStockListFromFile(stock_list)
	print 'stock_list:',stock_list
	#get stock data from remote server 
	stock_num = 0
	for stock_code in stock_list:
		#stock_code = '000776'
		#stock_code = stock_list[key]
		stock_num = stock_num +1
		print '--------enter-------index of stock:',stock_num,' stock_code:',stock_code
		file_name_qfq = '/Users/zj/company_code/stock_data_analysis/data/' + stock_code +'_ma_qfq.csv'
		file_name = '/Users/zj/company_code/stock_data_analysis/data/' + stock_code +'_ma.csv'
		file_name_hfq = '/Users/zj/company_code/stock_data_analysis/data/' + stock_code +'_ma_hfq.csv'

		last_time_file_qfq = DateClass().get_FileModifyTime(file_name_qfq)
		last_time_file = DateClass().get_FileModifyTime(file_name)
		last_time_file_hfq = DateClass().get_FileModifyTime(file_name_hfq)

		chazhi_value_qfq = time.time() - last_time_file_qfq
		chazhi_value = time.time() - last_time_file
		chazhi_value_hfq = time.time() - last_time_file_hfq
		day_second = 24*60*60
		print 'chazhi_value_qfq:',chazhi_value_qfq,' chazhi_value:',chazhi_value,' chazhi_value_hfq:',chazhi_value_hfq,' day seconds:',day_second

		qfq_update_flag = False
		flag_update = False
		hfq_update_flag = False
		if os.path.isfile(file_name_qfq) == False or chazhi_value_qfq > day_second:
			qfq_update_flag = True
		if os.path.isfile(file_name)== False or chazhi_value > day_second:
			flag_update = True
		if os.path.isfile(file_name_hfq)== False or chazhi_value_hfq > day_second:
			hfq_update_flag = True

		if qfq_update_flag==True and flag_update==True and file_name_hfq == True:
			print ' sleep some time'
			time.sleep(60)

		#print 'time:',time.gmtime(os.path.getmtime(file_name))
		DateClass().GetDate(cons,stock_code,file_name_qfq,file_name,file_name_hfq,qfq_update_flag,flag_update,hfq_update_flag)
		print '--------enter exit-------'
	#//DateClass().GetPEPB()
	#//DateClass().GetAllMarkert()
	#exit program
	DateClass().Exit()




