import copy
import datetime
import ipaddress
import random

def main():
	#making log file 
	log_maker('log_test7.txt')
	#subject1()
	#subject(N), N:threshold to regard as server failure
	#subject2(2)
	#subject3(N, m, t), m:number of average calculation, t:threshold of ping to regard as server failure
	#subject3(3, 5, 90)
	#subject4(3,5,90)

def subject1():
	with open("log_test1.txt", 'r', encoding="utf-8") as f:
		data_list_import = f.readlines()
	f.close();

	data_list=copy.deepcopy(data_list_import)

	LOG_TIME = 0
	SERVER_ADDR = 1
	PING_RESULT = 2

	log_table = list()
	for data in data_list:
		log_split_str = data.split(',')
		log_table.append(log_split_str)

	i = 0
	failure_count = 0
	while i < len(log_table):
		if log_table[i][PING_RESULT] != '-\n':
			i = i + 1
			continue;

		j = i + 1
		while j < len(log_table):
			if log_table[i][SERVER_ADDR] == log_table[j][SERVER_ADDR]:
				if log_table[j][PING_RESULT] == '-\n':
					del(log_table[j])
					j = j + 1
				else:
					start = datetime.datetime.strptime(log_table[i][LOG_TIME],'%Y%m%d%H%M%S')
					end = datetime.datetime.strptime(log_table[j][LOG_TIME],'%Y%m%d%H%M%S')

					failure_time = end - start
					msg = 'server:' + log_table[i][SERVER_ADDR] + '\tfailure_time:'
					print(msg, end='')
					print(failure_time, end='')
					print('\t(', end='')
					print(start, end='')
					print('<--->', end='')
					print(end, end='')
					print(')')
					failure_count = failure_count + 1
					break;

			j = j + 1

		if j == len(log_table):
			start = datetime.datetime.strptime(log_table[i][LOG_TIME],'%Y%m%d%H%M%S')
			msg = 'server:' + log_table[i][SERVER_ADDR] + '\tfailure_time:'
			print(msg, end='')
			print('--:--:--', end='')
			print('\t(', end='')
			print(start, end='')
			print('<--->ongoing)',)
		i = i + 1
	print('failure count:' + str(failure_count))


def subject2(N):
	with open("log_test2.txt", 'r', encoding="utf-8") as f:
		data_list_import = f.readlines()
	f.close();

	print('N=' + str(N))

	data_list=copy.deepcopy(data_list_import)

	LOG_TIME = 0
	SERVER_ADDR = 1
	PING_RESULT = 2

	log_table = list()
	for data in data_list:
		log_split_str = data.split(',')
		log_table.append(log_split_str)

	i = 0
	failure_count = 0
	while i < len(log_table):
		if log_table[i][PING_RESULT] != '-\n':
			i = i + 1
			continue;

		j = i + 1
		time_no_ping = 1
		while j < len(log_table):
			if log_table[i][SERVER_ADDR] == log_table[j][SERVER_ADDR]:
				if log_table[j][PING_RESULT] == '-\n':
					del(log_table[j])
					j = j + 1
					time_no_ping = time_no_ping + 1
				else:
					if time_no_ping >= N:
						start = datetime.datetime.strptime(log_table[i][LOG_TIME],'%Y%m%d%H%M%S')
						end = datetime.datetime.strptime(log_table[j][LOG_TIME],'%Y%m%d%H%M%S')

						failure_time = end - start
						msg = 'server:' + log_table[i][SERVER_ADDR] + '\tfailure_time:'
						print(msg, end='')
						print(failure_time, end='')
						print('\t(', end='')
						print(start, end='')
						print('<--->', end='')
						print(end, end='')
						print(')')
						failure_count = failure_count + 1
					break;

			j = j + 1

		if j == len(log_table):
			start = datetime.datetime.strptime(log_table[i][LOG_TIME],'%Y%m%d%H%M%S')
			msg = 'server:' + log_table[i][SERVER_ADDR] + 'failure_time:'
			print(msg, end='')
			print('--:--:--', end='')
			print('\t(', end='')
			print(start, end='')
			print('<--->ongoing)',)
		i = i + 1
	
	print('failure count:' + str(failure_count))


def subject3(N,m,t):
	with open("log_test3.txt", 'r', encoding="utf-8") as f:
		data_list_import = f.readlines()
	f.close();

	print('m=' + str(m))
	print('t=' + str(t) + '[ms]')

	data_list=copy.deepcopy(data_list_import)
	#reference number to data_list components
	LOG_TIME = 0
	SERVER_ADDR = 1
	PING_RESULT = 2

	#list to store date, server address, and ping 
	log_table = list()
	for data in data_list:
		log_split_str = data.split(',')
		log_table.append(log_split_str)

	print('HIGH LOAD')
	print('server_adress\thigh load period\t\t\t\tping_average')
	print('-----------------------------------------------------------------------------')
	for i in range(0, len(log_table)-m):
		#set server to calculate average
		no_ping_flag = False
		server_type = log_table[i][SERVER_ADDR]
		if log_table[i][PING_RESULT] !='-\n':
			ping_sum = int(log_table[i][PING_RESULT])
		else:
			ping_sum = t*1.5
			no_ping_flag = True
		ping_sum_count = 1

		for j in range(i+1, len(log_table)):
			#add ping value
			if server_type == log_table[j][SERVER_ADDR]:
				if log_table[i][PING_RESULT] !='-\n':
					ping_sum = ping_sum + int(log_table[i][PING_RESULT])
				else:
					ping_sum = ping_sum + t*1.5
					no_ping_flag = True
				ping_sum_count = ping_sum_count + 1
			
			#show average ping when average ping is larger than 't'
			if ping_sum_count >= m:
				ping_avg = ping_sum / m
				if ping_avg > t:
					msg = log_table[i][SERVER_ADDR] + '\t'
					start_date = datetime.datetime.strptime(log_table[i][LOG_TIME],'%Y%m%d%H%M%S')
					start_date_msg = start_date.strftime('%Y/%m/%d/%H:%M:%S')
					end_date = datetime.datetime.strptime(log_table[j][LOG_TIME],'%Y%m%d%H%M%S')
					end_date_msg = end_date.strftime('%Y/%m/%d/%H:%M:%S')

					msg = msg + start_date_msg + '<-->' + end_date_msg + '\t' + str(round(ping_avg)) + 'ms'
					print(msg, end='')
					if no_ping_flag == True:
						print('*')
					else:
						print('\n',end='')
				break

	i = 0
	failure_count = 0
	print('\nSERVER FAILURE')
	print('server adress\tfailure period\t\t\t\t\tfailure time[hour:min:sec]')
	print('-----------------------------------------------------------------------------')
	while i < len(log_table):
		if log_table[i][PING_RESULT] != '-\n':
			i = i + 1
			continue;

		j = i + 1
		time_no_ping = 1
		while j < len(log_table):
			#find server failure period
			if log_table[i][SERVER_ADDR] == log_table[j][SERVER_ADDR]:
				if log_table[j][PING_RESULT] == '-\n':
					del(log_table[j])
					j = j + 1
					time_no_ping = time_no_ping + 1
				else:
					if time_no_ping >= N:
						start_date = datetime.datetime.strptime(log_table[i][LOG_TIME],'%Y%m%d%H%M%S')
						end_date = datetime.datetime.strptime(log_table[j][LOG_TIME],'%Y%m%d%H%M%S')

						failure_time = end_date - start_date
						msg = log_table[i][SERVER_ADDR] + '\t'
						start_date_msg = start_date.strftime('%Y/%m/%d/%H:%M:%S')
						end_date_msg = end_date.strftime('%Y/%m/%d/%H:%M:%S')
						msg = msg + start_date_msg + '<-->' + end_date_msg + '\t'
						print(msg, end='')
						print(failure_time)

						failure_count = failure_count + 1
					break;

			j = j + 1

		#show ongoing server failure
		if j == len(log_table):
			start = datetime.datetime.strptime(log_table[i][LOG_TIME],'%Y%m%d%H%M%S')
			msg = 'server:' + log_table[i][SERVER_ADDR] + '\tfailure_time:'
			print(msg, end='')
			print('--:--:--', end='')
			print('\t(', end='')
			print(start, end='')
			print('<--->ongoing)',)
		i = i + 1
	
	print('failure count:' + str(failure_count))


def subject4(N,m,t):
	#loading log data
	with open("log_test6.txt", 'r', encoding="utf-8") as f:
		data_list_import = f.readlines()
	f.close();

	print('m=' + str(m))
	print('t=' + str(t) + '[ms]')

	data_list=copy.deepcopy(data_list_import)
	#reference number to data_list components
	LOG_TIME = 0
	SERVER_ADDR = 1
	PING_RESULT = 2

	#list to store date, server address, and ping 
	log_table = list()
	subnet_log_list = list()
	for data in data_list:
		log_split_str = data.split(',')
		log_table.append(log_split_str)

	print('HIGH LOAD')
	print('server_adress\thigh load period\t\t\t\tping_average')
	print('-----------------------------------------------------------------------------')
	for i in range(0, len(log_table)-m):
		#set server to calculate average
		no_ping_flag = False
		server_type = log_table[i][SERVER_ADDR]
		if log_table[i][PING_RESULT] !='-\n':
			ping_sum = int(log_table[i][PING_RESULT])
		else:
			ping_sum = t*1.5
			no_ping_flag = True
		ping_sum_count = 1

		for j in range(i+1, len(log_table)):
			#add ping value
			if server_type == log_table[j][SERVER_ADDR]:
				if log_table[i][PING_RESULT] !='-\n':
					ping_sum = ping_sum + int(log_table[i][PING_RESULT])
				else:
					ping_sum = ping_sum + t*1.5
					no_ping_flag = True
				ping_sum_count = ping_sum_count + 1
			
			#show average ping when average ping is larger than 't'
			if ping_sum_count >= m:
				ping_avg = ping_sum / m
				if ping_avg > t:
					msg = log_table[i][SERVER_ADDR] + '\t'
					start_date = datetime.datetime.strptime(log_table[i][LOG_TIME],'%Y%m%d%H%M%S')
					start_date_msg = start_date.strftime('%Y/%m/%d/%H:%M:%S')
					end_date = datetime.datetime.strptime(log_table[j][LOG_TIME],'%Y%m%d%H%M%S')
					end_date_msg = end_date.strftime('%Y/%m/%d/%H:%M:%S')

					msg = msg + start_date_msg + '<-->' + end_date_msg + '\t' + str(round(ping_avg)) + 'ms'
					print(msg, end='')
					if no_ping_flag == True:
						print('*')
					else:
						print('\n',end='')
				break


	i = 0
	failure_count = 0
	print('\nSERVER/SWITCH  FAILURE')
	print('server adress\tfailure period\t\t\t\t\tfailure time[hour:min:sec]')
	print('-----------------------------------------------------------------------------')
	while i < len(log_table):
		if log_table[i][PING_RESULT] != '-\n':
			i = i + 1
			continue;

		j = i + 1
		time_no_ping = 1
		while j < len(log_table):
			#find server failure period
			if log_table[i][SERVER_ADDR] == log_table[j][SERVER_ADDR]:
				if log_table[j][PING_RESULT] == '-\n':
					k = j+1
					while k < len(log_table):
						if log_table[k][PING_RESULT] == '-\n':
							


					del(log_table[j])
					j = j + 1
					time_no_ping = time_no_ping + 1
				else:
					if time_no_ping >= N:
						start_date = datetime.datetime.strptime(log_table[i][LOG_TIME],'%Y%m%d%H%M%S')
						end_date = datetime.datetime.strptime(log_table[j][LOG_TIME],'%Y%m%d%H%M%S')

						failure_time = end_date - start_date
						msg = log_table[i][SERVER_ADDR] + '\t'
						start_date_msg = start_date.strftime('%Y/%m/%d/%H:%M:%S')
						end_date_msg = end_date.strftime('%Y/%m/%d/%H:%M:%S')
						msg = msg + start_date_msg + '<-->' + end_date_msg + '\t'
						print(msg, end='')
						print(failure_time)

						failure_count = failure_count + 1
					break;

			j = j + 1

		#show ongoing server failure
		if j == len(log_table):
			start = datetime.datetime.strptime(log_table[i][LOG_TIME],'%Y%m%d%H%M%S')
			msg = 'server:' + log_table[i][SERVER_ADDR] + '\tfailure_time:'
			print(msg, end='')
			print('--:--:--', end='')
			print('\t(', end='')
			print(start, end='')
			print('<--->ongoing)',)
		i = i + 1
	
	print('failure count:' + str(failure_count))

#function to generate log file automatically
def log_maker(output_file_name):
	#you can add server address in the server_ipv4_list
	server_ipv4_list = [
					'10.20.30.1/16',
					'10.20.30.2/16',
					'192.168.1.1/24',
					'192.168.1.2/24',
					'192.168.1.3/24',
					'192.168.1.4/24',
					'10.25.20.1/16',
					'10.25.20.2/16'
	]
	#ping will generate random 1 from PING_MAX
	PING_MAX = 100;

	#logging will start at log_start_time
	log_start_time = datetime.datetime(2020, 10, 19, 13, 31, 30)
	#interval of ping test
	log_interval = datetime.timedelta(seconds=30)
	#interval of ping request during the ping test
	ping_interval = datetime.timedelta(seconds=0)
	#number of ping test
	log_period_count = 30

	#open file with overwrite mode
	with open(output_file_name, 'w', encoding='utf-8') as fp:
		log_time = log_start_time;
		#generate log
		for i in range(log_period_count):
			for j in range(len(server_ipv4_list)):
				ping_interval = datetime.timedelta(seconds=j)
				#ping_interval = datetime.timedelta(seconds=0)
				log_ping_time = log_time + ping_interval
				log_msg = log_ping_time.strftime('%Y%m%d%H%M%S')
				log_msg = log_msg + ',' + server_ipv4_list[j] + ',' + str(random.randint(0,PING_MAX)) + '\n'
				#show log on the cmd
				print(log_msg,end='')
				#writing log to File
				fp.write(log_msg)

			log_time = log_time + log_interval
	fp.close()

	print('Log was generated successfully.')

main()
