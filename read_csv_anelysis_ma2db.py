#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import tushare as ts
import os
import csv
from pymongo import MongoClient
import time
import datetime
from string import *

def getEveryDay(begin_date,end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    while begin_date < end_date:
        ###date_str = begin_date.strftime("%Y-%m-%d")
        mid_date = begin_date + datetime.timedelta(days=1)
        ###tup = (str(begin_date),str(mid_date))
        ###date_list.append(tup)
        tmp_begin_date = str(begin_date).split(" ")
        date_list.append(str(tmp_begin_date[0]))
        begin_date = mid_date
    return date_list

def csv2mongdb(db,stock_code_c):
	#stock_code = '000776'
	#前复权
	#table_qfq = 'stockcode_'+ stock_code_c + '_qfq'
	my_set = db.table_qfq
	file_name = '/Users/zj/company_code/stock_data_analysis/data/' + stock_code_c +'_ma_qfq.csv'
	with open(file_name, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if row[1] == "code":
				print "code head is abandod:",stock_code_c
			else:
				result = my_set.insert({"datetime":row[0],"stock_code":row[1],"open":row[2],"close":row[3],"high":row[4],"low":row[5],"vol":row[6],"amount":row[7],"ma60":row[8],"ma120":row[9],"ma250":row[10]})
	#不复权
	#my_set = db.stockcode_000776
	#table = 'stockcode_'+ stock_code_c
	my_set = db.table_none_fq
	file_name = '/Users/zj/company_code/stock_data_analysis/data/' + stock_code_c +'_ma.csv'
	with open(file_name, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if row[1] == "code":
				print "code head is abandod:",stock_code_c
			else:
				result = my_set.insert({"datetime":row[0],"stock_code":row[1],"open":row[2],"close":row[3],"high":row[4],"low":row[5],"vol":row[6],"amount":row[7],"ma60":row[8],"ma120":row[9],"ma250":row[10]})
	#后复权
	#my_set = db.stockcode_000776_hfq
	#table_hfq = 'stockcode_'+ stock_code_c+ '_hfq'
	my_set = db.table_hfq
	file_name = '/Users/zj/company_code/stock_data_analysis/data/' + stock_code_c +'_ma_hfq.csv'
	with open(file_name, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			if row[1] == "code":
				print "code head is abandod:",stock_code_c
			else:
				result = my_set.insert({"datetime":row[0],"stock_code":row[1],"open":row[2],"close":row[3],"high":row[4],"low":row[5],"vol":row[6],"amount":row[7],"ma60":row[8],"ma120":row[9],"ma250":row[10]})

def ReadStockListFromFile(stock_list):
	file_object2 = open("/Users/zj/company_code/stock_data_analysis/gupiao_stock.txt",'r')
	try:
		lines = file_object2.readlines()
		#print "type(lines)=",type(lines)
		for line in lines:
			tmp_line = line.split(" ")
			stock_list[tmp_line[1].strip("\n")] = tmp_line[0].strip("\n")
			#stock_list[tmp_line[0].strip("\n")] = tmp_line[1].strip("\n")
	finally:
		file_object2.close()

def ma_algrithm_own(days,my_set,stock_code,stock_list):
	#results = my_set.find({"datetime":{'$gte':timestamp0,'$lt':timestamp1}})
	buy_cost = 0
	buy_count = 0
	sell_own = 0
	type1 = 0
	type2 = 0
	type3 = 0
	type4 = 0
	print 'ma_algrithm_own ----------------------enter----------------------'
	for day in days:
		results = my_set.find({"datetime":day,"stock_code":stock_code})
		for res in results:
			keys = res.keys()
			if "close" in keys and  "ma250" in keys:
				#print "ma_algrithm_own day",day," close:",res["close"]," ma250:",res["ma250"]
				if not res["ma250"].strip():
					print 'ma250 is empty'
					continue
				close = float(res["close"])
				ma250 = float(res["ma250"])
				if close <= ma250:
					ret=(ma250 - close )*100/close
					'''
					if ret >5 and ret<=15 :
					#if ret >5 and ret<=15 and type1  10:
						type1 = type1 + 1
						shou_count = 1
						buy_num=shou_count*100
						buy_cost = buy_cost - close*buy_num
						buy_count = buy_count + shou_count
						print 'stock_code:',stock_code," day",day," close:",res["close"]," ma250:",res["ma250"]
						print '============stock_name:',stock_list[stock_code],' stock_code:',stock_code," 买入1:buy_count:",buy_count," sell_own:",sell_own," 盈余:",(sell_own+buy_cost)," 持仓:",buy_count*100," 比率(close_ma250):",ret
					'''
					
					'''
					if ret >15 and ret <=30 :
					#if ret >15 and ret <=30 and type2 <= 10:
						type2 = type2 + 1
						shou_count = 1
						buy_num=shou_count*100
						buy_cost = buy_cost - close*buy_num
						buy_count = buy_count + shou_count
						print 'stock_code:',stock_code," day",day," close:",res["close"]," ma250:",res["ma250"]
						print '============stock_name:',stock_list[stock_code],' stock_code:',stock_code," 买入2:buy_count:",buy_count," sell_own:",sell_own," 盈余:",(sell_own+buy_cost)," 持仓:",buy_count*100," 比率(close_ma250):",ret
					'''
					
					if ret >30 and ret<=45 :
					#if ret >30 and ret<=45 and type3 <= 10:
						type3 = type3 + 1
						shou_count = 1
						buy_num=shou_count*100
						buy_cost = buy_cost - close*buy_num
						buy_count = buy_count + shou_count
						print 'stock_code:',stock_code," day",day," close:",res["close"]," ma250:",res["ma250"]
						print '============stock_name:',stock_list[stock_code],' stock_code:',stock_code," 买入3:buy_count:",buy_count," sell_own:",sell_own," 盈余:",(sell_own+buy_cost)," 持仓:",buy_count*100," 比率(close_ma250):",ret
					
					if ret > 45 :
					#if ret >60 and ret<=75 and type4 <= 10:
						type4 = type4 + 1
						shou_count =1
						buy_num=shou_count*100
						buy_cost = buy_cost - close*buy_num
						buy_count = buy_count + shou_count
						print 'stock_code:',stock_code," day",day," close:",res["close"]," ma250:",res["ma250"]
						print '============stock_name:',stock_list[stock_code],' stock_code:',stock_code," 买入4:buy_count:",buy_count," sell_own:",sell_own," 盈余:",(sell_own+buy_cost)," 持仓:",buy_count*100," 比率(close_ma250):",ret

					'''
					if ret >40 and ret<=50:
						buy_cost = buy_cost - close*400
						buy_count = buy_count + 4
					'''
				if close > ma250:
					ret=(close -ma250 )*100/ma250
					sell_own = buy_count*close*100
					#if ret > 10 and ret <= 30:
					#	print "*****buy_cost:",buy_cost," sell_own:",sell_own," 盈余:",(sell_own+buy_cost)
					if ret > 20:
						if (sell_own+buy_cost) > 0:
							print 'stock_code:',stock_code," day",day," close:",res["close"]," ma250:",res["ma250"]
							print 'stock_name:',stock_list[stock_code],' stock_code:',stock_code," 卖出#######buy_cost:",buy_cost," sell_own:",sell_own," 盈余:",(sell_own+buy_cost)," 持仓:",buy_count*100," 盈利率:",(sell_own+buy_cost)*100/-buy_cost," 高过M250比率:",ret

	print 'ma_algrithm_own ----------------------exit----------------------'


if __name__ == '__main__':
	print "---------------------------------main enter---------------------------"
	conn = MongoClient('127.0.0.1', 27017)
	db = conn.stockdata
	days = getEveryDay('2017-01-01','2017-11-20')

	stock_list = {}
	ReadStockListFromFile(stock_list)
	print 'stock_list:',stock_list

	'''
	count = 0
	for stock_code in stock_list:
		count = count +1
		#stock_code = stock_list[key]
		print 'index of count:',count,' key:',key,' stock_code:',stock_code
		csv2mongdb(db,stock_code)
	'''

	#'''
	qfq_count = 0
	for stock_code in stock_list:
		qfq_count = qfq_count +1
		#stock_code = stock_list[key]
		print 'qfq_count:',qfq_count,' stock_code:',stock_code
		my_set = db.table_qfq
		ma_algrithm_own(days,my_set,stock_code,stock_list)
	#'''
	'''
	my_set = db.table_qfq
	ma_algrithm_own(days,my_set,'603288')
	'''





