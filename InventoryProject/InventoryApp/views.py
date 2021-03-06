# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from InventoryApp.models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.db import connection
from passlib.hash import sha256_crypt
import collections
import json
import logging
from django.db.models import *

from datetime import datetime
import datetime as dt1
import time
import sys
#########################################################################################################################################
def login(request):
	if(request.method == "POST"):
		logging.debug("adduser:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "login_inventory....."
		try:
			body_unicode = request.body.decode('utf-8')
			logindata = json.loads(body_unicode)
			print request.body
			#return data1
		except Exception, e:
			err_desc = 'login:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("login:"+ output)
			return HttpResponse(err_desc)	
			#return "value error"
			
		if(not logindata):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("adduser_status:"+ output)
			return HttpResponse(output)
			
		if((logindata.get('username') is None) or ((logindata.get('username') is not None) and (len(logindata['username']) <=0))):
			output_str += ",username is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("username:"+ output)
			return HttpResponse(output)
			
		else:
			username = logindata['username']
			
		if((logindata.get('password') is None) or ((logindata.get('password') is not None) and (len(logindata['password']) <=0))):
			output_str += ",passsword is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("login_status:"+ output)
			return HttpResponse(output)
			
		else:
			passcode = logindata['password']
			
		login_history = True
		
		login_history_get = jts_employees.objects.filter(userName=username)
		if(len(login_history_get) == 0): #just update the ChangeDate         
			login_history= False
			#print("matching")
			output = '{"error_code":"2", "error_desc": "Invalid username"}'
			logging.debug("login_status:"+ output)
			return HttpResponse(output)
			
		cursor = connection.cursor()
		cursor.execute ("select password from jts_employees where fullName = '%s'" %(username))
		rows = cursor.fetchall()
		if(len(rows)>0):
			for row in rows:
				password = row[0]
				verification = sha256_crypt.verify(passcode,password)
				if (verification == True):
					output = '{"error_code":"1", "error_desc": "login Successfull"}'
					logging.debug("login_status:"+ output)
					return HttpResponse(output)
				else:
					output = '{"error_code":"2", "error_desc": "Invalid password"}'
					logging.debug("login_status:"+ output)
					return HttpResponse(output)
					
	else:
		logging.debug("login_status: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("login_status:"+ output)
		return HttpResponse(output)

			
#######################################################################################################################################
def add_employee(request):
	if(request.method == "POST"):
		logging.debug("adduser:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "Inserting data into employees.."
		try:
			adduserdata = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("adduser_status:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not adduserdata):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("adduser_status:"+ output)
			return HttpResponse(output)
			
		if((adduserdata.get('fullname') is None) or ((adduserdata.get('fullname') is not None) and (len(adduserdata['fullname']) <=0))):
			output_str += ",fullname is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("fullname:"+ output)
			return HttpResponse(output)
			
		else:
			fullname = adduserdata['fullname']
			
		'''if((adduserdata.get('lastname') is None) or ((adduserdata.get('lastname') is not None) and (len(adduserdata['lastname']) <=0))):
			output_str += ",lastname is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("lastname:"+ output)
			return HttpResponse(output)
			
		else:
			lastname = adduserdata['lastname']'''
				
		if((adduserdata.get('username') is None) or ((adduserdata.get('username') is not None) and (len(adduserdata['username']) <=0))):
			output_str += ",username is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("username:"+ output)
			return HttpResponse(output)
			
		else:
			username = adduserdata['username']
			
		if((adduserdata.get('emailid') is None) or ((adduserdata.get('emailid') is not None) and (len(adduserdata['emailid']) <=0))):
			output_str += ",emailid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("emailid:"+ output)
			return HttpResponse(output)
			
		else:
			emailid = adduserdata['emailid']
			
		if((adduserdata.get('password') is None) or ((adduserdata.get('password') is not None) and (len(adduserdata['password']) <=0))):
			output_str += ",password is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("password:"+ output)
			return HttpResponse(output)
			
		else:
			password = sha256_crypt.hash(adduserdata['password'])
		
		if((adduserdata.get('gender') is None) or ((adduserdata.get('gender') is not None) and (len(adduserdata['gender']) <=0))):
			output_str += ",gender is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("gender:"+ output)
			return HttpResponse(output)
			
		else:
			gender = adduserdata['gender']
			
		if((adduserdata.get('bloodgroup') is None) or ((adduserdata.get('bloodgroup') is not None) and (len(adduserdata['bloodgroup']) <=0))):
			output_str += ",bloodgroup is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("bloodgroup:"+ output)
			return HttpResponse(output)
			
		else:
			bloodgroup = adduserdata['bloodgroup']
			
		if((adduserdata.get('dateofbirth') is None) or ((adduserdata.get('dateofbirth') is not None) and (len(adduserdata['dateofbirth']) <=0))):
			output_str += ",dateofbirth is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("dateofbirth:"+ output)
			return HttpResponse(output)
			
		else:
			dateofbirth = adduserdata['dateofbirth']
			
		if((adduserdata.get('dateofjoining') is None) or ((adduserdata.get('dateofjoining') is not None) and (len(adduserdata['dateofjoining']) <=0))):
			output_str += ",dateofjoining is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("dateofjoining:"+ output)
			return HttpResponse(output)
			
		else:
			dateofjoining = adduserdata['dateofjoining']
			
		if((adduserdata.get('department') is None) or ((adduserdata.get('department') is not None) and (len(adduserdata['department']) <=0))):
			output_str += ",department is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("department:"+ output)
			return HttpResponse(output)
			
		else:
			department = adduserdata['department']
			
		if((adduserdata.get('address') is None) or ((adduserdata.get('address') is not None) and (len(adduserdata['address']) <=0))):
			output_str += ",address is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("address:"+ output)
			return HttpResponse(output)
			
		else:
			address = adduserdata['address']
			
		if(adduserdata.get('reportinghead') is None):
			output_str += ",reportinghead is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("reportinghead:"+ output)
			return HttpResponse(output)
			
		else:
			reportinghead = adduserdata['reportinghead']
			
		if(adduserdata.get('reportinghr') is None):
			output_str += ",reportinghr is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("reportinghr:"+ output)
			return HttpResponse(output)
			
		else:
			reportinghr = adduserdata['reportinghr']
			
		if((adduserdata.get('worklocation') is None) or ((adduserdata.get('worklocation') is not None) and (len(adduserdata['worklocation']) <=0))):
			output_str += ",worklocation is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("worklocation:"+ output)
			return HttpResponse(output)
			
		else:
			worklocation = adduserdata['worklocation']
			
		'''if((adduserdata.get('statusid') is None) or ((adduserdata.get('statusid') is not None) and (len(adduserdata['statusid']) <=0))):
			output_str += ",statusid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("statusid:"+ output)
			return HttpResponse(output)
			
		else:
			statusid = adduserdata['statusid']'''
			
			#checks db	
		user_history = True
		
		user_history_get = jts_employees.objects.filter(userName=username)
		if(len(user_history_get) > 0): #just update the ChangeDate         
			user_history = False
			#print("matching")
			output = '{"error_code":"4", "error_desc": "user already exists please login"}'
			logging.debug("add_user:"+ output)
			return HttpResponse(output)

		try:
			user_input = jts_employees(fullName = fullname,userName = username,emailId = emailid,Password = password,gender = gender,bloodGroup = bloodgroup,dateOfBirth = dateofbirth,dateOfJoining = dateofjoining,departmentId = department,Address = address,managerId_id = reportinghead,reportingHr_id = reportinghr,workLocation_id = worklocation)
			user_input.save()
			output = '{"error_code":"1", "error_desc": "record added"}' 
			logging.debug("add_user:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'adduser:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("adduser:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to add user"}' 
			logging.debug("add_user:"+ output)
			return HttpResponse(err_desc)
	else:
		logging.debug("adduser: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("add_user:"+ output)
		return HttpResponse(output)

##########################################################################################################################################
def update_employee(request):
	if(request.method == "POST"):
		logging.debug("update_user:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "updating user.."
		try:
			updateuserdata = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("update_user:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not updateuserdata):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("update_user:"+ output)
			return HttpResponse(output)
			
		if((updateuserdata.get('id') is None) or ((updateuserdata.get('id') is not None) and (len(updateuserdata['id']) <=0))):
			output_str += ",userid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("userid:"+ output)
			return HttpResponse(output)
		
		else:
			userid = updateuserdata['id']
				
		if((updateuserdata.get('fullname') is None) or ((updateuserdata.get('fullname') is not None) and (len(updateuserdata['fullname']) <=0))):
			output_str += ",fullname is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("fullname:"+ output)
			return HttpResponse(output)
			
		else:
			fullname = updateuserdata['fullname']
				
		if((updateuserdata.get('username') is None) or ((updateuserdata.get('username') is not None) and (len(updateuserdata['username']) <=0))):
			output_str += ",username is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("username:"+ output)
			return HttpResponse(output)
			
		else:
			username = updateuserdata['username']
			
		if((updateuserdata.get('emailid') is None) or ((updateuserdata.get('emailid') is not None) and (len(updateuserdata['emailid']) <=0))):
			output_str += ",emailid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("emailid:"+ output)
			return HttpResponse(output)
			
		else:
			emailid = updateuserdata['emailid']
		
		if((updateuserdata.get('gender') is None) or ((updateuserdata.get('gender') is not None) and (len(updateuserdata['gender']) <=0))):
			output_str += ",gender is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("gender:"+ output)
			return HttpResponse(output)
			
		else:
			gender = updateuserdata['gender']
			
		if((updateuserdata.get('bloodgroup') is None) or ((updateuserdata.get('bloodgroup') is not None) and (len(updateuserdata['bloodgroup']) <=0))):
			output_str += ",bloodgroup is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("bloodgroup:"+ output)
			return HttpResponse(output)
			
		else:
			bloodgroup = updateuserdata['bloodgroup']
			
		if((updateuserdata.get('dateofbirth') is None) or ((updateuserdata.get('dateofbirth') is not None) and (len(updateuserdata['dateofbirth']) <=0))):
			output_str += ",dateofbirth is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("dateofbirth:"+ output)
			return HttpResponse(output)
			
		else:
			dateofbirth = updateuserdata['dateofbirth']
			
		if((updateuserdata.get('dateofjoining') is None) or ((updateuserdata.get('dateofjoining') is not None) and (len(updateuserdata['dateofjoining']) <=0))):
			output_str += ",dateofjoining is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("dateofjoining:"+ output)
			return HttpResponse(output)
			
		else:
			dateofjoining = updateuserdata['dateofjoining']
			
		'''if(updateuserdata.get('dateofexit') is None):
			output_str += ",dateofexit is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("dateofexit:"+ output)
			return HttpResponse(output)
			
		else:
			dateofexit = updateuserdata['dateofexit']'''
			
		if((updateuserdata.get('department') is None) or ((updateuserdata.get('department') is not None) and (len(updateuserdata['department']) <=0))):
			output_str += ",department is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("department:"+ output)
			return HttpResponse(output)
			
		else:
			department = updateuserdata['department']
			
		if((updateuserdata.get('reportinghead') is None) or ((updateuserdata.get('reportinghead') is not None) and (len(updateuserdata['reportinghead']) <=0))):
			output_str += ",reportinghead is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("reportinghead:"+ output)
			return HttpResponse(output)
			
		else:
			reportinghead = updateuserdata['reportinghead']
			
		if((updateuserdata.get('reportinghr') is None) or ((updateuserdata.get('reportinghr') is not None) and (len(updateuserdata['reportinghr']) <=0))):
			output_str += ",reportinghr is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("reportinghr:"+ output)
			return HttpResponse(output)
			
		else:
			reportinghr = updateuserdata['reportinghr']
			
		if((updateuserdata.get('address') is None) or ((updateuserdata.get('address') is not None) and (len(updateuserdata['address']) <=0))):
			output_str += ",address is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("address:"+ output)
			return HttpResponse(output)
			
		else:
			address = updateuserdata['address']
			
		if((updateuserdata.get('worklocation') is None) or ((updateuserdata.get('worklocation') is not None) and (len(updateuserdata['worklocation']) <=0))):
			output_str += ",worklocation is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("worklocation:"+ output)
			return HttpResponse(output)
			
		else:
			worklocation = updateuserdata['worklocation']

		try:
			user_input = jts_employees.objects.filter(id = userid).update(fullName = fullname,userName = username,emailId = emailid,gender = gender,bloodGroup = bloodgroup,dateOfBirth = dateofbirth,dateOfJoining = dateofjoining,departmentId = department,Address = address,managerId_id = reportinghead,reportingHr_id = reportinghr,workLocation_id = worklocation)
			output = '{"error_code":"1", "error_desc": "record updated"}' 
			logging.debug("update_user:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'update_user:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("update_user:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to update the record/ID doesnot exists"}' 
			logging.debug("update_user:"+ output)
			return HttpResponse(err_desc)
	else:
		logging.debug("update_user: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("update_user:"+ output)
		return HttpResponse(output)
		
################################################################################################################################
def get_employee(request):
	cursor = connection.cursor()
	cursor.execute("select e.id,e.fullName as fullname,e.userName,e.emailId,e.gender,e.bloodGroup,e.dateOfBirth,e.dateOfJoining,e.dateOfExit,e.Address,m.fullName as manager,h.fullName as hrname,e.departmentId,d.departmentName,e.workLocation_id,w.location from jts_employees e LEFT JOIN jts_employees m ON e.managerId_id = m.id LEFT JOIN jts_employees h ON e.reportingHr_id = h.id JOIN jts_departments d ON e.departmentId = d.id JOIN emp_location w ON e.worklocation_id = w.id ORDER BY e.id")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['fullname'] = row[1]
		d['username'] = row[2]
		d['emailid'] = row[3]
		d['gender'] = row[4]
		d['bloodgroup'] = row[5]
		d['dateofbirth'] = row[6]
		d['dateofjoining'] = row[7]
		d['dateofexit'] = row[8]
		d['address'] = row[9]
		d['reportinghead'] = row[10]
		d['reportinghr'] = row[11]
		d['department'] = row[13]
		d['worklocation'] = row[15]
		objects_list.append(d)
	json_output='{"user_details":'	
	json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
	json_output+='}'
	logging.debug("get_user:")
	return HttpResponse(json_output)
	
################################################################################################################################
def search_employee(request):
	if(request.method == "POST"):
		logging.debug("search_employees:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "searching employees.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("search_employees:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("search_employees:"+ output)
			return HttpResponse(output)
			
		if((data1.get('employeename') is None) or ((data1.get('employeename') is not None) and (len(data1['employeename']) <=0))):
			output_str += ",searchvalue is required"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("search_employees:"+ output)
			return HttpResponse(output)
		
		else:
			employeename = data1['employeename']
			
		try:
			cursor = connection.cursor()
			cursor.execute("set @employee = '%s'" %(employeename))
			cursor.execute("set @employee = CONCAT('%',@employee,'%')")
			cursor.execute("select e.id,e.fullName as fullname,e.userName,e.emailId,e.password,e.gender,e.bloodGroup,e.dateOfBirth,e.dateOfJoining,e.dateOfExit,e.Address,m.fullName as manager,h.fullName as hrname,e.departmentId,d.departmentName,e.jobRole_id,j.jobRole,e.workLocation_id,w.location from jts_employees e LEFT JOIN jts_employees m ON e.managerId_id = m.id LEFT JOIN jts_employees h ON e.reportingHr_id = h.id JOIN jts_departments d ON e.departmentId = d.id JOIN emp_jobrole j ON e.jobRole_id = j.id JOIN emp_location w ON e.worklocation_id = w.id and e.fullName LIKE @employee")
			rows = cursor.fetchall()
			objects_list = []
			for row in rows:
				d = collections.OrderedDict()
				d['id']=row[0]
				d['fullname'] = row[1]
				d['username'] = row[2]
				d['emailid'] = row[3]
				d['password'] = row[4]
				d['gender'] = row[5]
				d['bloodgroup'] = row[6]
				d['dateofbirth'] = row[7]
				d['dateofjoining'] = row[8]
				d['dateofexit'] = row[9]
				d['address'] = row[10]
				d['reportinghead'] = row[11]
				d['reportinghr'] = row[12]
				d['department'] = row[14]
				d['jobrole'] = row[16]
				d['worklocation'] = row[18]
				objects_list.append(d)
			json_output='{"user_details":'	
			json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
			json_output+='}'
			logging.debug("get_user:")
			return HttpResponse(json_output)
		except Exception, e:
			err_desc = 'search_employees:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("search_employees:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Invalid keyword/product"}' 
			logging.debug("search_employees:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("search_employees: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("search_employees:"+ output)
		return HttpResponse(output)
	
	
#################################################################################################################################
def get_hr(request):
	cursor = connection.cursor()
	cursor.execute("select r.jobRole_id,j.jobRole,r.userId_id,e.userName from user_roles r JOIN emp_jobrole j ON r.jobRole_id = j.id JOIN jts_employees e ON r.userId_id = e.id where j.jobRole = 'hr'")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['employeeid']=row[2]
		d['hrname']=row[3]
		d['role'] = row[1]
		objects_list.append(d)
	json_output='{"hr_details":'	
	json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
	json_output+='}'
	logging.debug("hr_details:")
	return HttpResponse(json_output)
#################################################################################################################################
def get_user(request):
	if(request.method == "POST"):
		logging.debug("search_employees:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "getting user.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("get_user:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("get_user:"+ output)
			return HttpResponse(output)
			
		if((data1.get('username') is None) or ((data1.get('username') is not None) and (len(data1['username']) <=0))):
			output_str += ",username is required"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("username:"+ output)
			return HttpResponse(output)
		
		else:
			username = data1['username']
		
		try:
			cursor = connection.cursor()
			cursor.execute("select jts_employees.id,jts_employees.userName,user_menus.menuName from jts_employees,user_roles,emp_jobrole,user_menus WHERE jts_employees.userName = '%s' and user_roles.userId_id = jts_employees.id and user_roles.jobRole_id = emp_jobrole.id and user_menus.jobRole_id = emp_jobrole.id group by user_menus.menuName" %(username))
			rows = cursor.fetchall()
			objects_list = []
			for row in rows:
				d = collections.OrderedDict()
				d['employeeid']=row[0]
				d['username'] = row[1]
				d['usermenus'] = row[2]
				objects_list.append(d)
			json_output='{"user_details":'	
			json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
			json_output+='}'
			logging.debug("user_details:")
			return HttpResponse(json_output)
		
		except Exception, e:
			err_desc = 'get_user:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("get_user:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Invalid username"}' 
			logging.debug("get_user:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("get_user: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("get_user:"+ output)
		return HttpResponse(output)
	
###############################################################################################################################
def forget_password(request):
	if(request.method == "POST"):
		logging.debug("search_employees:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "updating new password...."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("forget_password:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("forget_password:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",userid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("userid:"+ output)
			return HttpResponse(output)
		
		else:
			userid = data1['id']

		if((data1.get('username') is None) or ((data1.get('username') is not None) and (len(data1['username']) <=0))):
			output_str += ",username is required"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("username:"+ output)
			return HttpResponse(output)
		
		else:
			username = data1['username']
		
		if((data1.get('newpassword') is None) or ((data1.get('newpassword') is not None) and (len(data1['newpassword']) <=0))):
			output_str += ",newpassword is required"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("forget_password:"+ output)
			return HttpResponse(output)
		
		else:
			newpassword = data1['newpassword']
			
		if((data1.get('confirmpassword') is None) or ((data1.get('confirmpassword') is not None) and (len(data1['confirmpassword']) <=0))):
			output_str += ",confirmpassword is required"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("forget_password:"+ output)
			return HttpResponse(output)
		
		else:
			confirmpassword = data1['confirmpassword']
			
			
		if(newpassword == confirmpassword):
			passcode = sha256_crypt.hash(newpassword)
			try:
				user_input = jts_employees.objects.filter(id = userid).update(userName = username,Password = passcode)
				output = '{"error_code":"1", "error_desc": "password updated"}' 
				logging.debug("update_user:"+ output)
				return HttpResponse(output)
			
			except Exception, e:
				err_desc = 'forget_password:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
				logging.debug("forget_password:"+ err_desc)
				output = '{"error_code":"2", "error_desc": "Failed to update the password"}' 
				logging.debug("forget_password:"+ output)
				return HttpResponse(err_desc)
			
		else:
			output = '{"error_code":"3", "error_desc": "passwords dosent match"}'
			return HttpResponse(output)
			
		
	else:
		logging.debug("forget_employees: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("forget_employees:"+ output)
		return HttpResponse(output)
		
###############################################################################################################################
def add_userrole(request):
	if(request.method == "POST"):
		logging.debug("add_userrole:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "Inserting data into userroles.."
		try:
			adduserdata = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_userrole:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not adduserdata):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_userrole:"+ output)
			return HttpResponse(output)
			
		if((adduserdata.get('userid') is None) or ((adduserdata.get('userid') is not None) and (len(adduserdata['userid']) <=0))):
			output_str += ",userid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("userid:"+ output)
			return HttpResponse(output)
			
		else:
			userid = adduserdata['userid']
			
		if((adduserdata.get('jobrole') is None) or ((adduserdata.get('jobrole') is not None) and (len(adduserdata['jobrole']) <=0))):
			output_str += ",jobrole is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("jobrole:"+ output)
			return HttpResponse(output)
			
		else:
			jobrole = adduserdata['jobrole']
			
		'''history_userrole = True
		
		user_history_get = user_roles.objects.filter(jobRole_id = jobrole,userId_id = userid)
		if(len(user_history_get) > 0): #just update the ChangeDate         
			user_history = False
			#print("matching")
			output = '{"error_code":"4", "error_desc": "user already exists please login"}'
			logging.debug("add_user:"+ output)
			return HttpResponse(output)'''
		
		
		try:
			user_input = user_roles(jobRole_id = jobrole,userId_id = userid)
			user_input.save()
			output = '{"error_code":"1", "error_desc": "record added"}' 
			logging.debug("add_userrole:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'add_userrole:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("add_userrole:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to add userroles"}' 
			logging.debug("add_userrole:"+ output)
			return HttpResponse(err_desc)
	else:
		logging.debug("add_userrole: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("add_userrole:"+ output)
		return HttpResponse(output)	
		
###############################################################################################################################
def update_userrole(request):
	if(request.method == "POST"):
		data = request.body
		print data
		for rows in data:
			name = rows.data["name"]
			print name
			
		
	

################################################################################################################################
def get_departments(request):
	cursor = connection.cursor()
	cursor.execute("select d.*,e.fullName from jts_departments d,jts_employees e where d.departmentHead_id = e.id")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['departmentname'] = row[1]
		d['departmenthead'] = row[3]
		objects_list.append(d)
	json_output='{"department_details":'	
	json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
	json_output+='}'
	logging.debug("get_departments:")
	return HttpResponse(json_output)
	
################################################################################################################################
def get_emplocation(request):
	cursor = connection.cursor()
	cursor.execute("select * from emp_location")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['location'] = row[1]
		objects_list.append(d)
	json_output='{"emp_location_details":'	
	json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
	json_output+='}'
	logging.debug("get_emplocation:")
	return HttpResponse(json_output)
	
################################################################################################################################
def get_empjobrole(request):
	cursor = connection.cursor()
	cursor.execute("select * from emp_jobrole")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['jobrole'] = row[1]
		objects_list.append(d)
	json_output='{"emp_jobrole_details":'	
	json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
	json_output+='}'
	logging.debug("get_empjobrole:")
	return HttpResponse(json_output)
#################################################################################################################################
def add_familydetails(request):
	if(request.method == "POST"):
		logging.debug("adduser:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "Inserting data into employee family table.."
		try:
			adduserdata = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_family_details:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not adduserdata):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_family_details:"+ output)
			return HttpResponse(output)
			
		if((adduserdata.get('employeeid') is None) or ((adduserdata.get('employeeid') is not None) and (len(adduserdata['employeeid']) <=0))):
			output_str += ",employeeid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("employeeid:"+ output)
			return HttpResponse(output)
			
		else:
			employeeid = adduserdata['employeeid']
			
		if((adduserdata.get('name') is None) or ((adduserdata.get('name') is not None) and (len(adduserdata['name']) <=0))):
			output_str += ",name is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("name:"+ output)
			return HttpResponse(output)
			
		else:
			name = adduserdata['name']
			
		if((adduserdata.get('gender') is None) or ((adduserdata.get('gender') is not None) and (len(adduserdata['gender']) <=0))):
			output_str += ",gender is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("gender:"+ output)
			return HttpResponse(output)
			
		else:
			gender = adduserdata['gender']
			
		if((adduserdata.get('dateofbirth') is None) or ((adduserdata.get('dateofbirth') is not None) and (len(adduserdata['dateofbirth']) <=0))):
			output_str += ",dateofbirth is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("dateofbirth:"+ output)
			return HttpResponse(output)
			
		else:
			dateofbirth = adduserdata['dateofbirth']
			
		if((adduserdata.get('relationship') is None) or ((adduserdata.get('relationship') is not None) and (len(adduserdata['relationship']) <=0))):
			output_str += ",relationship is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("relationship:"+ output)
			return HttpResponse(output)
			
		else:
			relationship = adduserdata['relationship']
			
					#checks db	
		user_history = True
		cursor = connection.cursor()
		cursor.execute("select employeeId_id,Name,Relationship from family_details where employeeId_id = '%s' and Name = '%s' and Relationship = '%s'" %(employeeid,name,relationship))
		user_history_get = cursor.fetchall()
		if(len(user_history_get) > 0): #just update the ChangeDate         
			is_history_rec_needed = False
			#print("matching")
			output = '{"error_code":"4", "error_desc": "family details of this employee already exists"}'
			logging.debug("add_user:"+ output)
			return HttpResponse(output)
			
		try:
			user_input = family_details(Name = name,gender = gender,DateOfBirth = dateofbirth,Relationship = relationship,employeeId_id = employeeid)
			user_input.save()
			output = '{"error_code":"1", "error_desc": "record added"}' 
			logging.debug("add_family_details:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'add_family_details:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("add_fmaily_details:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed add family member"}' 
			logging.debug("add_family_details:"+ output)
			return HttpResponse(err_desc)
	else:
		logging.debug("add_family_details: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("add_family_details:"+ output)
		return HttpResponse(output)
		
################################################################################################################################
def update_familydetails(request):
	if(request.method == "POST"):
		logging.debug("adduser:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "updating employee family table.."
		try:
			adduserdata = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("update_family_details:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not adduserdata):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_family_details:"+ output)
			return HttpResponse(output)
			
		if((adduserdata.get('id') is None) or ((adduserdata.get('id') is not None) and (len(adduserdata['id']) <=0))):
			output_str += ",id is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("id:"+ output)
			return HttpResponse(output)
			
		else:
			memberid = adduserdata['id']
			
		if((adduserdata.get('employeeid') is None) or ((adduserdata.get('employeeid') is not None) and (len(adduserdata['employeeid']) <=0))):
			output_str += ",employeeid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("employeeid:"+ output)
			return HttpResponse(output)
			
		else:
			employeeid = adduserdata['employeeid']
			
		if((adduserdata.get('name') is None) or ((adduserdata.get('name') is not None) and (len(adduserdata['name']) <=0))):
			output_str += ",name is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("name:"+ output)
			return HttpResponse(output)
			
		else:
			name = adduserdata['name']
			
		if((adduserdata.get('gender') is None) or ((adduserdata.get('gender') is not None) and (len(adduserdata['gender']) <=0))):
			output_str += ",gender is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("gender:"+ output)
			return HttpResponse(output)
			
		else:
			gender = adduserdata['gender']
			
		if((adduserdata.get('dateofbirth') is None) or ((adduserdata.get('dateofbirth') is not None) and (len(adduserdata['dateofbirth']) <=0))):
			output_str += ",dateofbirth is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("dateofbirth:"+ output)
			return HttpResponse(output)
			
		else:
			dateofbirth = adduserdata['dateofbirth']
			
		if((adduserdata.get('relationship') is None) or ((adduserdata.get('relationship') is not None) and (len(adduserdata['relationship']) <=0))):
			output_str += ",relationship is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("relationship:"+ output)
			return HttpResponse(output)
			
		else:
			relationship = adduserdata['relationship']
			
		try:
			user_input = family_details.objects.filter(id = memberid).update(Name = name,gender = gender,DateOfBirth = dateofbirth,Relationship = relationship,employeeId_id = employeeid)
			output = '{"error_code":"1", "error_desc": "record updated"}' 
			logging.debug("update_family_details:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'update_family_details:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("update_family_details:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to update the record/ID doesnot exists"}' 
			logging.debug("update_family_details:"+ output)
			return HttpResponse(err_desc)
	else:
		logging.debug("update_family_details: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("update_family_details:"+ output)
		return HttpResponse(output)
			
####################################################################################################################################
def get_familydetails(request):
	cursor = connection.cursor()
	cursor.execute("select f.*,e.fullname as employeename from family_details f JOIN jts_employees e where f.employeeId_id = e.id")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['employeeid'] = row[5]
		d['employeename'] = row[6]
		d['family_member_name'] = row[1]
		d['gender'] = row[2]
		d['dateofbirth'] = row[3]
		d['relationship'] = row[4]
		objects_list.append(d)
	json_output='{"employee_family_details":'	
	json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
	json_output+='}'
	logging.debug("get_familydetails:")
	return HttpResponse(json_output)
		
##########################################################################################################################################################################
def add_warehouse(request):
	if(request.method == "POST"):
		logging.debug("warehouse_add:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "Inserting data into warehouse.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("warehouse_add:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("location_add:"+ output)
			return HttpResponse(output)
				
		if((data1.get('warehousename') is None) or ((data1.get('warehousename') is not None) and (len(data1['warehousename']) <=0))):
			output_str += ",warehousename is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("warehousename:"+ output)
			return HttpResponse(output)
			
		else:
			warehousename = data1['warehousename']
			
		if((data1.get('locationid') is None) or ((data1.get('locationid') is not None) and (len(data1['locationid']) <=0))):
			output_str += ",locationid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("locationid:"+ output)
			return HttpResponse(output)
			
		else:
			locationid = data1['locationid']
			
		if((data1.get('statusid') is None) or ((data1.get('statusid') is not None) and (len(data1['statusid']) <=0))):
			output_str += ",statusid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("statusid:"+ output)
			return HttpResponse(output)
			
		else:
			statusid = data1['statusid']
		#checks db	
		is_history_rec_needed = True
		cursor = connection.cursor()
		cursor.execute("select warehouseName,locationId_id from inv_warehouse where warehouseName = '%s' and locationId_id = '%s'" %(warehousename,locationid))
		warehouse_status_get = cursor.fetchall()
		#warehouse_status_get = ((inv_warehouse.objects.filter(warehouseName=warehousename)) and (inv_warehouse.objects.filter(locationId_id = locationid))) 
		if(len(warehouse_status_get) > 0): #just update the ChangeDate         
			is_history_rec_needed = False
			#print("matching")
			output = '{"error_code":"4", "error_desc": "Your warehouse already exists."}'
			logging.debug("warehouse_add:"+ output)
			return HttpResponse(output)

		try:
			warehouse_rec = inv_warehouse(warehouseName = warehousename,locationId_id = locationid,statusId_id = statusid)
			warehouse_rec.save()
			output = '{"error_code":"1", "error_desc": "record added"}' 
			logging.debug("warehouse_add:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'warehouse_add:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("warehouse_add:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to add record"}' 
			logging.debug("warehouse_add:"+ output)
			return HttpResponse(err_desc)
	else:
		logging.debug("warehouse_add: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("warehouse_add:"+ output)
		return HttpResponse(output)
			

####################################################################################################################################
def get_warehouse(request):
	'''try:
		json_data ='{"warehouse_details":'
		json_data+=json.dumps([dict(item) for item in inv_warehouse.objects.all().values('id', 'warehouseName','locationId_id','statusId_id')])
		json_data+='}'
		return HttpResponse(json_data)
			
	except ValueError as e:
		return HttpResponse(e)'''
		
	cursor = connection.cursor()
	cursor.execute("select w.id,w.warehouseName,w.locationId_id,w.statusId_id,l.locationName,s.statusName from inv_warehouse as w JOIN inv_location as l,inv_status as s WHERE w.locationId_id = l.id and w.statusId_id = s.id")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['warehousename'] = row[1]
		d['locationname'] = row[4]
		d['statusname'] = row[5]
		objects_list.append(d)
	json_output='{"warehouse_details":'	
	json_output+= json.dumps(objects_list,indent = 3)
	json_output+='}'
	logging.debug("get_warehouse:")
	return HttpResponse(json_output)
#################################################################################################################################
def active_warehouse(request):
	cursor = connection.cursor()
	cursor.execute("select w.id,w.warehouseName,w.locationId_id,w.statusId_id,l.locationName,s.statusName from inv_warehouse as w JOIN inv_location as l,inv_status as s WHERE w.locationId_id = l.id and w.statusId_id = s.id and w.statusId_id = 1")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['warehousename'] = row[1]
		d['locationname'] = row[4]
		d['statusname'] = row[5]
		objects_list.append(d)
	json_output='{"active_warehouse_details":'	
	json_output+= json.dumps(objects_list,indent = 3)
	json_output+='}'
	logging.debug("active_warehouse:")
	return HttpResponse(json_output)

###################################################################################################################################
def del_warehouse(request):
	if(request.method == "POST"):
		logging.debug("del_warehouse:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "deleting warehouse.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("del_warehouse:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("del_warehouse:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",warehouseid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("warehouseid:"+ output)
			return HttpResponse(output)
		
		else:
			warehouseid = data1['id']
			
			
		warehouse_data_delete = True
		
		del_data_get = inv_warehouse.objects.filter(id=warehouseid)
		if(len(del_data_get) > 0):
			del_data_get.delete()
			warehouse_data_delete = False
			#printing response
			output = '{"error_code":"0", "error_desc": "Your warehouse is deleted"}'
			logging.debug("del_warehouse:"+ output)
			return HttpResponse(output)
			
		else:
			output = '{"error_code":"2", "error_desc": "warehouse doesnot exists please insert the warehouse"}'
			logging.debug("del_warehouse:"+ output)
			return HttpResponse(output)
		

	else:
		logging.debug("del_warehouse: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("del_warehouse:"+ output)
		return HttpResponse(output)

#######################################################################################################################################
def update_warehouse(request):
	if(request.method == "POST"):
		logging.debug("update_warehouse:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "updating warehouse.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("warehousestatus:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("warehousestatus:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",warehouseid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("warehouseid:"+ output)
			return HttpResponse(output)
		
		else:
			warehouseid = data1['id']
				
		if((data1.get('warehousename') is None) or ((data1.get('warehousename') is not None) and (len(data1['warehousename']) <=0))):
			output_str += ",warehousename is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("warehousename:"+ output)
			return HttpResponse(output)
			
		else:
			warehousename = data1['warehousename']
			
		if((data1.get('locationid') is None) or ((data1.get('locationid') is not None) and (len(data1['locationid']) <=0))):
			output_str += ",locationid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("locationid:"+ output)
			return HttpResponse(output)
			
		else:
			locationid = data1['locationid']
			
		if((data1.get('statusid') is None) or ((data1.get('statusid') is not None) and (len(data1['statusid']) <=0))):
			output_str += ",statusid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("statusid:"+ output)
			return HttpResponse(output)
			
		else:
			statusid = data1['statusid']

		try:
			warehouse_rec = inv_warehouse.objects.filter(id = warehouseid).update(warehouseName = warehousename,locationId_id = locationid,statusId_id = statusid)
			output = '{"error_code":"1", "error_desc": "record updated"}' 
			logging.debug("add_warehouse:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'update_warehouse:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("update_warehouse:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to update the record/ID doesnot exists"}' 
			logging.debug("update_warehouse:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("update_warehouse: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("update_warehouse:"+ output)
		return HttpResponse(output)
########################################################################################################################################
def add_location(request):
	if(request.method == "POST"):
		logging.debug("location_add:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "Inserting data into location.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("location_add:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("location_add:"+ output)
			return HttpResponse(output)
				
		if((data1.get('locationname') is None) or ((data1.get('locationname') is not None) and (len(data1['locationname']) <=0))):
			output_str += ",locationname is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("locationname:"+ output)
			return HttpResponse(output)
			
		else:
			locationname = data1['locationname']
			
		if((data1.get('locationaddress') is None) or ((data1.get('locationaddress') is not None) and (len(data1['locationaddress']) <=0))):
			output_str += ",locationaddress is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("locationaddress:"+ output)
			return HttpResponse(output)
			
		else:
			locationaddress = data1['locationaddress']
			
		if((data1.get('statusid') is None) or ((data1.get('statusid') is not None) and (len(data1['statusid']) <=0))):
			output_str += ",statusid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("statusid:"+ output)
			return HttpResponse(output)
			
		else:
			statusid = data1['statusid']
		#checks db	
		is_history_rec_needed = True
		
		location_status_get = inv_location.objects.filter(locationName=locationname)
		if(len(location_status_get) > 0): #just update the ChangeDate         
			is_history_rec_needed = False
			#print("matching")
			output = '{"error_code":"4", "error_desc": "Your location already exists."}'
			logging.debug("location_add:"+ output)
			return HttpResponse(output)

		try:
			location_rec = inv_location(locationName = locationname,locationAddress = locationaddress,statusId_id = statusid)
			location_rec.save()
			output = '{"error_code":"1", "error_desc": "record added"}' 
			logging.debug("location_add:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'location:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("location:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to add record"}' 
			logging.debug("location_add:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("location_add: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("location_add:"+ output)
		return HttpResponse(output)

#########################################################################################################################################
def get_location(request):	
	cursor = connection.cursor()
	cursor.execute("select l.id,l.locationName,l.locationAddress,s.statusName from inv_location l,inv_status s where l.statusId_id = s.id")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['locationname'] = row[1]
		d['locationaddress'] = row[2]
		d['status'] = row[3]
		objects_list.append(d)
	j='{"location_details":'	
	j+= json.dumps(objects_list,indent = 3)
	j+='}'
	logging.debug("get_location:")
	return HttpResponse(j)
	
###############################################################################################################################
def active_location(request):
	cursor = connection.cursor()
	cursor.execute("select l.id,l.locationName,l.locationAddress,s.statusName from inv_location l,inv_status s where l.statusId_id = s.id and l.statusId_id = 1")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['locationname'] = row[1]
		d['locationaddress'] = row[2]
		d['status'] = row[3]
		objects_list.append(d)
	j='{"active_location_details":'	
	j+= json.dumps(objects_list,indent = 3)
	j+='}'
	logging.debug("active_location:")
	return HttpResponse(j)
	
#########################################################################################################################################
def del_location(request):
	if(request.method == "POST"):
		logging.debug("del_location:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "deleting location.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("del_location:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("del_location:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",locationid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("locationid:"+ output)
			return HttpResponse(output)
		
		else:
			locationid = data1['id']
			
			
		location_data_delete = True
		
		del_data_get = inv_location.objects.filter(id=locationid)
		if(len(del_data_get) > 0):
			del_data_get.delete()
			location_data_delete = False
			#printing response
			output = '{"error_code":"0", "error_desc": "Your location is deleted"}'
			logging.debug("del_location:"+ output)
			return HttpResponse(output)
			
		else:
			output = '{"error_code":"2", "error_desc": "location doesnot exists please insert the location"}'
			logging.debug("del_location:"+ output)
			return HttpResponse(output)
		

	else:
		logging.debug("location_delete: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("del_location:"+ output)
		return HttpResponse(output)
		
##########################################################################################################################################
def update_location(request):
	if(request.method == "POST"):
		logging.debug("update_location:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "updating location.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("update_location:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("update_location:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",locationid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("locationid:"+ output)
			return HttpResponse(output)
		
		else:
			locationid = data1['id']
				
		if((data1.get('locationname') is None) or ((data1.get('locationname') is not None) and (len(data1['locationname']) <=0))):
			output_str += ",locationname is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("locationname:"+ output)
			return HttpResponse(output)
			
		else:
			locationname = data1['locationname']
			
		if((data1.get('locationaddress') is None) or ((data1.get('locationaddress') is not None) and (len(data1['locationaddress']) <=0))):
			output_str += ",locationaddress is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("locationaddress:"+ output)
			return HttpResponse(output)
			
		else:
			locationaddress = data1['locationaddress']
			
		if((data1.get('statusid') is None) or ((data1.get('statusid') is not None) and (len(data1['statusid']) <=0))):
			output_str += ",statusid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("statusid:"+ output)
			return HttpResponse(output)
			
		else:
			statusid = data1['statusid']

		try:
			location_rec = inv_location.objects.filter(id = locationid).update(locationName = locationname,locationAddress = locationaddress,statusId_id = statusid)
			output = '{"error_code":"1", "error_desc": "record updated"}' 
			logging.debug("update_location:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'update_location:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("update_location:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to update the record/Id doesnot exists"}' 
			logging.debug("update_location:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("update_location: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("update_location:"+ output)
		return HttpResponse(output)

###########################################################################################################################################
def add_status(request):
	if(request.method == "POST"):
		logging.debug("add_status:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "Inserting data into status.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_status:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_status:"+ output)
			return HttpResponse(output)
				
		if((data1.get('statusname') is None) or ((data1.get('statusname') is not None) and (len(data1['statusname']) <=0))):
			output_str += ",statusname is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("statusname:"+ output)
			return HttpResponse(output)
			
		else:
			statusname = data1['statusname']
			
		status_rec = True
		
		status_rec_get = inv_status.objects.filter(statusName=statusname)
		if(len(status_rec_get) > 0): #just update the ChangeDate         
			status_rec = False
			#print("matching")
			output = '{"error_code":"2", "error_desc": "Status already exists"}'
			logging.debug("add_status:"+ output)
			return HttpResponse(output)
			
		try:
			status_rec = inv_status(statusName = statusname)
			status_rec.save()
			output = '{"error_code":"1", "error_desc": "record added"}' 
			logging.debug("add_status:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'addstatus:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("status:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to add record"}' 
			logging.debug("add_status:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("add_status: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("add_status:"+ output)
		return HttpResponse(output)
			

#######################################################################################################################################
def get_status(request):
	cursor = connection.cursor()
	cursor.execute("select * from inv_status")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['statusname'] = row[1]
		objects_list.append(d)
	json_output='{"status_details":'	
	json_output+= json.dumps(objects_list,indent = 3)
	json_output+='}'
	return HttpResponse(json_output)

#######################################################################################################################################
def update_status(request):
	if(request.method == "POST"):
		logging.debug("update_status:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "updating status.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("update_status:"+ output)
			return HttpResponse(output)
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("update_status:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",statusid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("statusid:"+ output)
			return HttpResponse(output)
		
		else:
			statusid = data1['id']
				
		if((data1.get('statusname') is None) or ((data1.get('statusname') is not None) and (len(data1['statusname']) <=0))):
			output_str += ",statusname is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("statusname:"+ output)
			return HttpResponse(output)
			
		else:
			statusname = data1['statusname']
			
		try:
			warehouse_rec = inv_status.objects.filter(id = statusid).update(statusName = statusname)
			output = '{"error_code":"1", "error_desc": "record updated"}' 
			logging.debug("update_status:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'update_status:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("update_status:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to update the record/ID doesnot exists"}' 
			logging.debug("update_status:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("update_status: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("update_status:"+ output)
		return HttpResponse(output)
#################################################################################################################################
def add_product(request):
	if(request.method == "POST"):
		logging.debug("add_product:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "Inserting data into products.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_product:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_product:"+ output)
			return HttpResponse(output)
			
		if((data1.get('productno') is None) or ((data1.get('productno') is not None) and (len(data1['productno']) <=0))):
			output_str += ",productno is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productno:"+ output)
			return HttpResponse(output)
			
		else:
			productno = data1['productno']
				
		if((data1.get('productname') is None) or ((data1.get('productname') is not None) and (len(data1['productname']) <=0))):
			output_str += ",productname is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productname:"+ output)
			return HttpResponse(output)
			
		else:
			productname = data1['productname']
			
		if((data1.get('productdescription') is None) or ((data1.get('productdescription') is not None) and (len(data1['productdescription']) <=0))):
			output_str += ",productdescription is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productdescription:"+ output)
			return HttpResponse(output)
			
		else:
			productdescription = data1['productdescription']
			
		if((data1.get('productmodel') is None) or ((data1.get('productmodel') is not None) and (len(data1['productmodel']) <=0))):
			output_str += ",productmodel is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productmodel:"+ output)
			return HttpResponse(output)
			
		else:
			productmodel = data1['productmodel']
			
		if((data1.get('productcompany') is None) or ((data1.get('productcompany') is not None) and (len(data1['productcompany']) <=0))):
			output_str += ",productcompany is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productcompany:"+ output)
			return HttpResponse(output)
			
		else:
			productcompany = data1['productcompany']
			
		if(data1.get('productpackage') is None):
			output_str += ",productpackage is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productpackage:"+ output)
			return HttpResponse(output)
			
		else:
			productpackage = data1['productpackage']
			
		if((data1.get('productpurchasable') is None) or ((data1.get('productpurchasable') is not None) and (len(data1['productpurchasable']) <=0))):
			output_str += ",productpurchasable is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productpurchasable:"+ output)
			return HttpResponse(output)
			
		else:
			productpurchasable = data1['productpurchasable']
			
		if(data1.get('productpurchaselistprice') is None):
			output_str += ",productpurchaselistprice is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productpurchaselistprice:"+ output)
			return HttpResponse(output)
			
		else:
			productpurchaselistprice = data1['productpurchaselistprice']
			
		if(data1.get('productpricetolerancepercent') is None):
			output_str += ",productpricetolerancepercent is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productpricetolerancepercent:"+ output)
			return HttpResponse(output)
			
		else:
			productpricetolerancepercent = data1['productpricetolerancepercent']
			
		if((data1.get('productsellable') is None) or ((data1.get('productsellable') is not None) and (len(data1['productsellable']) <=0))):
			output_str += ",productsellable is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productsellable:"+ output)
			return HttpResponse(output)
			
		else:
			productsellable = data1['productsellable']
			
		if((data1.get('productserialcontrolled') is None) or ((data1.get('productserialcontrolled') is not None) and (len(data1['productserialcontrolled']) <=0))):
			output_str += ",productserialcontrolled is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productserialcontrolled:"+ output)
			return HttpResponse(output)
			
		else:
			productserialcontrolled = data1['productserialcontrolled']
			
		if((data1.get('productbatchtracked') is None) or ((data1.get('productbatchtracked') is not None) and (len(data1['productbatchtracked']) <=0))):
			output_str += ",productbatchtracked is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productbatchtracked:"+ output)
			return HttpResponse(output)
			
		else:
			productbatchtracked = data1['productbatchtracked']
			
		
		if((data1.get('standardcost') is None) or ((data1.get('standardcost') is not None) and (len(data1['standardcost']) <=0))):
			output_str += ",standardcost is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("standardcost:"+ output)
			return HttpResponse(output)
			
		else:
			standardcost = data1['standardcost']
			
		if((data1.get('reorderlevel') is None) or ((data1.get('reorderlevel') is not None) and (len(data1['reorderlevel']) <=0))):
			output_str += ",reorderlevel is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("reorderlevel:"+ output)
			return HttpResponse(output)
			
		else:
			reorderlevel = data1['reorderlevel']
			
		if((data1.get('reorderquantity') is None) or ((data1.get('reorderquantity') is not None) and (len(data1['reorderquantity']) <=0))):
			output_str += ",reorderquantity is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("reorderquantity:"+ output)
			return HttpResponse(output)
			
		else:
			reorderquantity = data1['reorderquantity']
			
		if((data1.get('producttype') is None) or ((data1.get('producttype') is not None) and (len(data1['producttype']) <=0))):
			output_str += ",producttype is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("producttype:"+ output)
			return HttpResponse(output)
			
		else:
			producttype = data1['producttype']
			
		if((data1.get('productuom') is None) or ((data1.get('productuom') is not None) and (len(data1['productuom']) <=0))):
			output_str += ",productuom is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productuom:"+ output)
			return HttpResponse(output)
			
		else:
			productuom = data1['productuom']
					
		if((data1.get('statusid') is None) or ((data1.get('statusid') is not None) and (len(data1['statusid']) <=0))):
			output_str += ",statusid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("statusid:"+ output)
			return HttpResponse(output)
			
		else:
			statusid = data1['statusid']
		#checks db	
		'''is_history_rec_needed = True
		
		warehouse_status_get = inv_products.objects.filter(warehouseName=warehousename)
		if(len(warehouse_status_get) > 0): #just update the ChangeDate         
			is_history_rec_needed = False
			#print("matching")
			output = '{"error_code":"4", "error_desc": "Response= Your warehouse already exists."}'
			logging.debug("add_product:"+ output)
			return HttpResponse(output)'''

		try:
			products_rec = inv_products(productNo = productno,productName = productname,productDescription = productdescription,productModel = productmodel,productCompany = productcompany,productPackage = productpackage,productPurchasable = productpurchasable,productPurchaseListPrice = productpurchaselistprice,productPriceTolerancePercent = productpricetolerancepercent,productSellable = productsellable,productSerialControlled = productserialcontrolled,productBatchTracked = productbatchtracked,standardCost = standardcost,reorderLevel = reorderlevel,reorderQty = reorderquantity,productType_id = producttype,productUOM_id = productuom,statusId_id = statusid)
			products_rec.save()
			output = '{"error_code":"1", "error_desc": "Record added"}' 
			logging.debug("add_product:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'add_product:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("warehouse_add:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to add record"}' 
			logging.debug("add_product:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("add_product: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("add_product:"+ output)
		return HttpResponse(output)

###########################################################################################################################################
def add_production(request):
	if(request.method == "POST"):
		logging.debug("add_jtsproduct:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "Inserting data into production table.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_jtsproduct:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_jtsproduct:"+ output)
			return HttpResponse(output)
				
		if((data1.get('productname') is None) or ((data1.get('productname') is not None) and (len(data1['productname']) <=0))):
			output_str += ",productname is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productname:"+ output)
			return HttpResponse(output)
			
		else:
			productname = data1['productname']
			
		if((data1.get('jtsproductid') is None) or ((data1.get('jtsproductid') is not None) and (len(data1['jtsproductid']) <=0))):
			output_str += ",jtsproductid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("jtsproductid:"+ output)
			return HttpResponse(output)
			
		else:
			jtsproductid = data1['jtsproductid']
			
		if((data1.get('basequantity') is None) or ((data1.get('basequantity') is not None) and (len(data1['basequantity']) <=0))):
			output_str += ",basequantity is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("basequantity:"+ output)
			return HttpResponse(output)
			
		else:
			basequantity = data1['basequantity']


		try:
			products_rec = inv_products(baseQuantity = basequantity,jts_products_id = jtsproductid,productId_id = productname)
			products_rec.save()
			output = '{"error_code":"1", "error_desc": "Record added"}' 
			logging.debug("add_jtsproduct:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'add_jtsproduct:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("warehouse_add:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to add record"}' 
			logging.debug("add_jtsproduct:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("add_jtsproduct: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("add_jtsproduct	:"+ output)
		return HttpResponse(output)
		
################################################################################################################################
def update_product(request):
	if(request.method == "POST"):
		logging.debug("add_product:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "updating data of products.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_product:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_product:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",productid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productid:"+ output)
			return HttpResponse(output)
		
		else:
			productid = data1['id']
			
		if((data1.get('productno') is None) or ((data1.get('productno') is not None) and (len(data1['productno']) <=0))):
			output_str += ",productno is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productno:"+ output)
			return HttpResponse(output)
			
		else:
			productno = data1['productno']
			
		if((data1.get('productname') is None) or ((data1.get('productname') is not None) and (len(data1['productname']) <=0))):
			output_str += ",productname is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productname:"+ output)
			return HttpResponse(output)
			
		else:
			productname = data1['productname']
			
		if((data1.get('productdescription') is None) or ((data1.get('productdescription') is not None) and (len(data1['productdescription']) <=0))):
			output_str += ",productdescription is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productdescription:"+ output)
			return HttpResponse(output)
			
		else:
			productdescription = data1['productdescription']
			
		if((data1.get('productmodel') is None) or ((data1.get('productmodel') is not None) and (len(data1['productmodel']) <=0))):
			output_str += ",productmodel is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productmodel:"+ output)
			return HttpResponse(output)
			
		else:
			productmodel = data1['productmodel']
			
		if((data1.get('productcompany') is None) or ((data1.get('productcompany') is not None) and (len(data1['productcompany']) <=0))):
			output_str += ",productcompany is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productcompany:"+ output)
			return HttpResponse(output)
			
		else:
			productcompany = data1['productcompany']
			
		if(data1.get('productpackage') is None):
			output_str += ",productpackage is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productpackage:"+ output)
			return HttpResponse(output)
			
		else:
			productpackage = data1['productpackage']
			
		if((data1.get('productpurchasable') is None) or ((data1.get('productpurchasable') is not None) and (len(data1['productpurchasable']) <=0))):
			output_str += ",productpurchasable is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productpurchasable:"+ output)
			return HttpResponse(output)
			
		else:
			productpurchasable = data1['productpurchasable']
			
		if((data1.get('productpurchaselistprice') is None) or ((data1.get('productpurchaselistprice') is not None) and (len(data1['productpurchaselistprice']) <=0))):
			output_str += ",productpurchaselistprice is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productpurchaselistprice:"+ output)
			return HttpResponse(output)
			
		else:
			productpurchaselistprice = data1['productpurchaselistprice']
			
		if((data1.get('productpricetolerancepercent') is None) or ((data1.get('productpricetolerancepercent') is not None) and (len(data1['productpricetolerancepercent']) <=0))):
			output_str += ",productpricetolerancepercent is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productpricetolerancepercent:"+ output)
			return HttpResponse(output)
			
		else:
			productpricetolerancepercent = data1['productpricetolerancepercent']
			
		if((data1.get('productsellable') is None) or ((data1.get('productsellable') is not None) and (len(data1['productsellable']) <=0))):
			output_str += ",productsellable is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productsellable:"+ output)
			return HttpResponse(output)
			
		else:
			productsellable = data1['productsellable']
			
		if((data1.get('productserialcontrolled') is None) or ((data1.get('productserialcontrolled') is not None) and (len(data1['productserialcontrolled']) <=0))):
			output_str += ",productserialcontrolled is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productserialcontrolled:"+ output)
			return HttpResponse(output)
			
		else:
			productserialcontrolled = data1['productserialcontrolled']
			
		if((data1.get('productbatchtracked') is None) or ((data1.get('productbatchtracked') is not None) and (len(data1['productbatchtracked']) <=0))):
			output_str += ",productbatchtracked is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productbatchtracked:"+ output)
			return HttpResponse(output)
			
		else:
			productbatchtracked = data1['productbatchtracked']
			
		
		if((data1.get('standardcost') is None) or ((data1.get('standardcost') is not None) and (len(data1['standardcost']) <=0))):
			output_str += ",standardcost is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("standardcost:"+ output)
			return HttpResponse(output)
			
		else:
			standardcost = data1['standardcost']
			
		if((data1.get('reorderlevel') is None) or ((data1.get('reorderlevel') is not None) and (len(data1['reorderlevel']) <=0))):
			output_str += ",reorderlevel is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("reorderlevel:"+ output)
			return HttpResponse(output)
			
		else:
			reorderlevel = data1['reorderlevel']
			
		if((data1.get('reorderquantity') is None) or ((data1.get('reorderquantity') is not None) and (len(data1['reorderquantity']) <=0))):
			output_str += ",reorderquantity is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("reorderquantity:"+ output)
			return HttpResponse(output)
			
		else:
			reorderquantity = data1['reorderquantity']
			
		if((data1.get('producttype') is None) or ((data1.get('producttype') is not None) and (len(data1['producttype']) <=0))):
			output_str += ",producttype is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("producttype:"+ output)
			return HttpResponse(output)
			
		else:
			producttype = data1['producttype']
			
		if((data1.get('productuom') is None) or ((data1.get('productuom') is not None) and (len(data1['productuom']) <=0))):
			output_str += ",productuom is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productuom:"+ output)
			return HttpResponse(output)
			
		else:
			productuom = data1['productuom']
					
		if((data1.get('statusid') is None) or ((data1.get('statusid') is not None) and (len(data1['statusid']) <=0))):
			output_str += ",statusid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("statusid:"+ output)
			return HttpResponse(output)
			
		else:
			statusid = data1['statusid']
				
		
		try:
			products_rec = inv_products.objects.filter(id=productid).update(productNo = productno,productName = productname,productDescription = productdescription,productModel = productmodel,productCompany = productcompany,productPackage = productpackage,productPurchasable = productpurchasable,productPurchaseListPrice = productpurchaselistprice,productPriceTolerancePercent = productpricetolerancepercent,productSellable = productsellable,productSerialControlled = productserialcontrolled,productBatchTracked = productbatchtracked,standardCost = standardcost,reorderLevel = reorderlevel,reorderQty = reorderquantity,productType_id = producttype,productUOM_id = productuom,statusId_id = statusid)
			output = '{"error_code":"1", "error_desc": "record updated"}' 
			logging.debug("update_product:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'update_product:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("update_product:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to update the record/ID doesnot exists"}' 
			logging.debug("update_product:"+ output)
			return HttpResponse(err_desc)
	else:
		logging.debug("update_product: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("update_product:"+ output)
		return HttpResponse(output)
###############################################################################################################################
def get_product(request):
	cursor = connection.cursor()
	cursor.execute("select p.id,p.productNo,p.productName,p.productDescription,p.productModel,p.productCompany,p.productPackage,p.productPurchasable,p.productPurchaseListPrice,p.productPriceTolerancePercent,p.productSellable,p.productSerialControlled,p.productBatchTracked,p.standardCost,p.reorderLevel,p.reorderQty,t.materialType,u.measurementName,s.statusName,c.materialCategory from inv_products p JOIN inv_materialType t ON p.productType_id = t.id JOIN inv_UnitOfMeasure u ON p.productUOM_id = u.id JOIN inv_status s ON p.statusId_id = s.id JOIN inv_materialCategory c ON p.productCategory_id = c.id")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['productno'] = row[1]
		d['productname'] = row[2]
		d['productdescription'] = row[3]
		d['productmodel'] = row[4]
		d['productcompany'] = row[5]
		d['productpackage'] = row[6]
		d['productpurchasable'] = row[7]
		d['productpurchaselistprice'] = row[8]
		d['productPriceTolerancePercent'] = row[9]
		d['productsellable'] = row[10]
		d['productserialcontrolled'] = row[11]
		d['productbatchtracked'] = row[12]
		d['standardcost'] = row[13]
		d['reorderlevel'] = row[14]
		d['reorderqty'] = row[15]
		d['producttype'] = row[16]
		d['productuom'] = row[17]
		d['productcategory'] = row[19]
		d['status'] = row[18]
		objects_list.append(d)
	json_output='{"product_details":'	
	json_output+= json.dumps(objects_list,indent = 3)
	json_output+='}'
	return HttpResponse(json_output)

################################################################################################################################
def add_productquantity(request):
	if(request.method == "POST"):
		logging.debug("add_product_quantity:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "Inserting quantity.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_product_quantity:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_product_quantity:"+ output)
			return HttpResponse(output)
				
		if((data1.get('quantity') is None) or ((data1.get('quantity') is not None) and (len(data1['quantity']) <=0))):
			output_str += ",quantity is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("quantity:"+ output)
			return HttpResponse(output)
			
		else:
			quantity = data1['quantity']
			
		if((data1.get('productid') is None) or ((data1.get('productid') is not None) and (len(data1['productid']) <=0))):
			output_str += ",product is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productid:"+ output)
			return HttpResponse(output)
			
		else:
			productid = data1['productid']
			
		if((data1.get('positionid') is None) or ((data1.get('positionid') is not None) and (len(data1['positionid']) <=0))):
			output_str += ",position is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productid:"+ output)
			return HttpResponse(output)
			
		else:
			positionid = data1['positionid']
			
		if((data1.get('warehouseid') is None)):
			output_str += ",warehouse is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("warehouseid:"+ output)
			return HttpResponse(output)
			
		else:
			warehouseid = data1['warehouseid']
			
		if((data1.get('locationid') is None)):
			output_str += ",location is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("locationid:"+ output)
			return HttpResponse(output)
			
		else:
			locationid = data1['locationid']
			
			
		try:
			quantity_rec = inv_quantity(quantity = quantity,locationId_id = locationid,positionId_id = positionid,productId_id = productid,warehouseId_id = warehouseid)
			quantity_rec.save()
			output = '{"error_code":"1", "error_desc": "quantity updated"}' 
			logging.debug("add_status:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'add_product_quantity:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("add_product_quantity:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to add record"}' 
			logging.debug("add_product_quantity:"+ output)
			return HttpResponse(err_desc)
	else:
		logging.debug("add_product_quantity: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("add_product_quantity:"+ output)
		return HttpResponse(output)
		
##################################################################################################################################
def update_productquantity(request):
	if(request.method == "POST"):
		logging.debug("update_product_quantity:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "updating quantity.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("update_product_quantity:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_product:"+ output)
			return HttpResponse(output)
			
		if((data1.get('quantityid') is None) or ((data1.get('quantityid') is not None) and (len(data1['quantityid']) <=0))):
			output_str += ",quantityid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("quantityid:"+ output)
			return HttpResponse(output)
		
		else:
			quantityid = data1['quantityid']
			
		if((data1.get('quantity') is None) or ((data1.get('quantity') is not None) and (len(data1['quantity']) <=0))):
			output_str += ",quantity is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("quantity:"+ output)
			return HttpResponse(output)
			
		else:
			quantity = data1['quantity']
			
		if((data1.get('positionid') is None) or ((data1.get('positionid') is not None) and (len(data1['positionid']) <=0))):
			output_str += ",positionid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("positionid:"+ output)
			return HttpResponse(output)
			
		else:
			positionid = data1['positionid']
			
		if((data1.get('productid') is None) or ((data1.get('productid') is not None) and (len(data1['productid']) <=0))):
			output_str += ",productid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productid:"+ output)
			return HttpResponse(output)
			
		else:
			productid = data1['productid']
			
		if((data1.get('locationid') is None) or ((data1.get('locationid') is not None) and (len(data1['locationid']) <=0))):
			output_str += ",locationid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("locationid:"+ output)
			return HttpResponse(output)
			
		else:
			locationid = data1['locationid']
			
		if((data1.get('warehouseid') is None) or ((data1.get('warehouseid') is not None) and (len(data1['warehouseid']) <=0))):
			output_str += ",warehouseid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("warehouseid:"+ output)
			return HttpResponse(output)
			
		else:
			warehouseid = data1['warehouseid']

		try:
			products_rec = inv_quantity.objects.filter(quantityId=quantityid).update(quantity = quantity,locationId_id = locationid,positionId_id = positionid,productId_id = productid,warehouseId_id = warehouseid)
			output = '{"error_code":"1", "error_desc": "record updated"}' 
			logging.debug("update_product_quantity:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'update_product_quantity:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("update_product_quantity:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to update the record/ID doesnot exists"}' 
			logging.debug("update_product_quantity:"+ output)
			return HttpResponse(err_desc)
	else:
		logging.debug("update_product_quantity: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("update_product_quantity:"+ output)
		return HttpResponse(output)
#################################################################################################################################
def get_productquantity(request):
	cursor = connection.cursor()
	cursor.execute("select q.*,p.productName,po.position from inv_quantity q JOIN inv_products p ON q.productId_id = p.id JOIN inv_position po ON q.positionId_id = po.id")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['quantityid']=row[0]
		d['productname'] = row[6]
		d['quantity'] = row[1]
		d['position'] = row[7]
		d['locationid'] = row[2]
		d['warehouseid'] = row[5]
		objects_list.append(d)
	json_output='{"product_quantity_details":'	
	json_output+= json.dumps(objects_list,indent = 3)
	json_output+='}'
	return HttpResponse(json_output)
#############################################################################################################################################
def get_productcategory(request):
	if(request.method == "POST"):
		logging.debug("search_product_on_category:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "Listing products.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("search_product_on_category:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("search_product_on_category:"+ output)
			return HttpResponse(output)
			
		if((data1.get('productcategory') is None) or ((data1.get('productcategory') is not None) and (len(data1['productcategory']) <=0))):
			output_str += ",category is required"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("category_value:"+ output)
			return HttpResponse(output)
		
		else:
			productcategory = data1['productcategory']

		try:
			cursor = connection.cursor()
			cursor.execute("select p.id,p.productName,p.productDescription,p.productModel,p.productCompany,p.productPackage,t.materialType,u.measurementName,s.statusName,c.materialCategory from inv_products p JOIN inv_materialType t ON p.productType_id = t.id JOIN inv_UnitOfMeasure u ON p.productUOM_id = u.id JOIN inv_status s ON p.statusId_id = s.id JOIN inv_materialCategory c ON p.productCategory_id = c.id where p.productCategory_id = '%s'"%(productcategory))
			rows = cursor.fetchall()
			objects_list = []
			for row in rows:
				d = collections.OrderedDict()
				d['id']=row[0]
				d['productname'] = row[1]
				d['productdescription'] = row[2]
				d['productmodel'] = row[3]
				d['productcompany'] = row[4]
				d['productpackage'] = row[5]
				d['producttype'] = row[6]
				d['productuom'] = row[7]
				d['productcategory'] = row[9]
				d['status'] = row[8]
				objects_list.append(d)
			json_output='{"product_category_details":'	
			json_output+= json.dumps(objects_list,indent = 3)
			json_output+='}'
			return HttpResponse(json_output)
		except Exception, e:
			err_desc = 'search_product_on_category:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("search_product_on_category:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Invalid keyword/product"}' 
			logging.debug("search_product_on_category:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("search_product_on_category: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("search_product_on_category:"+ output)
		return HttpResponse(output)


#############################################################################################################################################
def active_product(request):
	cursor = connection.cursor()
	cursor.execute("select p.id,p.productName,p.productDescription,p.productModel,p.productCompany,p.productPackage,p.productPurchasable,p.productPurchaseListPrice,p.productPriceTolerancePercent,p.productSellable,p.productSerialControlled,p.productBatchTracked,p.standardCost,p.reorderLevel,p.reorderQty,t.materialType,u.measurementName,s.statusName,c.materialCategory from inv_products p JOIN inv_materialType t ON p.productType_id = t.id JOIN inv_UnitOfMeasure u ON p.productUOM_id = u.id JOIN inv_status s ON p.statusId_id = s.id JOIN inv_materialCategory c ON p.productCategory_id = c.id")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['productname'] = row[1]
		d['productdescription'] = row[2]
		d['productmodel'] = row[3]
		d['productcompany'] = row[4]
		d['productpackage'] = row[5]
		d['producttype'] = row[15]
		d['status'] = row[17]
		objects_list.append(d)
	json_output='{"active_product_details":'	
	json_output+= json.dumps(objects_list,indent = 3)
	json_output+='}'
	return HttpResponse(json_output)
	
#############################################################################################################################
def search_product(request):
	if(request.method == "POST"):
		logging.debug("search_product:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "searching product.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("search_product:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("search_product:"+ output)
			return HttpResponse(output)
			
		if((data1.get('search') is None) or ((data1.get('search') is not None) and (len(data1['search']) <=0))):
			output_str += ",search value is required"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("search_value:"+ output)
			return HttpResponse(output)
		
		else:
			search = data1['search']
			
		try:
			cursor = connection.cursor()
			cursor.execute("set @search = '%s'" %(search))
			cursor.execute("set @search = CONCAT('%',@search,'%')")
			cursor.execute("select p.id,p.productName,p.productDescription,p.productModel,p.productCompany,p.productPackage,p.productPurchasable,p.productPurchaseListPrice,p.productPriceTolerancePercent,p.productSellable,p.productSerialControlled,p.productBatchTracked,p.standardCost,p.reorderLevel,p.reorderQty,t.materialType,u.measurementName,s.statusName,c.materialCategory from inv_products p JOIN inv_materialType t ON p.productType_id = t.id JOIN inv_UnitOfMeasure u ON p.productUOM_id = u.id JOIN inv_status s ON p.statusId_id = s.id JOIN inv_materialCategory c ON p.productCategory_id = c.id and productName LIKE @search")
			rows = cursor.fetchall()
			objects_list = []
			for row in rows:
				d = collections.OrderedDict()
				d['id']=row[0]
				d['productname'] = row[1]
				d['productdescription'] = row[2]
				d['productmodel'] = row[3]
				d['productcompany'] = row[4]
				d['productpackage'] = row[5]
				d['productpurchasable'] = row[6]
				d['productpurchaselistprice'] = row[7]
				d['productPriceTolerancePercent'] = row[8]
				d['productsellable'] = row[9]
				d['productserialcontrolled'] = row[10]
				d['productbatchtracked'] = row[11]
				d['standardcost'] = row[12]
				d['reorderlevel'] = row[13]
				d['reorderqty'] = row[14]
				d['producttype'] = row[15]
				d['productuom'] = row[16]
				d['productcategory'] = row[18]
				d['status'] = row[17]
				objects_list.append(d)
			json_output='{"product_details":'	
			json_output+= json.dumps(objects_list,indent = 3)
			json_output+='}'
			return HttpResponse(json_output)
		except Exception, e:
			err_desc = 'search_product:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("search_product:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Invalid keyword/product"}' 
			logging.debug("search_product:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("search_product: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("search_product:"+ output)
		return HttpResponse(output)
		
################################################################################################################################
def del_product(request):
	if(request.method == "POST"):
		logging.debug("del_product:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "deleting product.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("del_product:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("del_product:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",productid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productid:"+ output)
			return HttpResponse(output)
		
		else:
			productid = data1['id']
			
			
		product_data_delete = True
		
		del_data_get = inv_products.objects.filter(id=productid)
		if(len(del_data_get) > 0):
			del_data_get.delete()
			product_data_delete = False
			#printing response
			output = '{"error_code":"0", "error_desc": "Your product is deleted"}'
			logging.debug("del_product:"+ output)
			return HttpResponse(output)
			
		else:
			output = '{"error_code":"2", "error_desc": "product doesnot exists please insert product"}'
			logging.debug("del_product:"+ output)
			return HttpResponse(output)
		

	else:
		logging.debug("del_product: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("del_product:"+ output)
		return HttpResponse(output)
		
###############################################################################################################################
def get_category(request):
	cursor = connection.cursor()
	cursor.execute("select * from inv_materialCategory")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['category'] = row[1]
		objects_list.append(d)
	json_output='{"get_category":'	
	json_output+= json.dumps(objects_list,indent = 3)
	json_output+='}'
	return HttpResponse(json_output)
###############################################################################################################################
def add_position(request):
	if(request.method == "POST"):
		logging.debug("position_add:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "Inserting data into position database.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("position_add:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("position_add:"+ output)
			return HttpResponse(output)
				
		if((data1.get('position') is None) or ((data1.get('position') is not None) and (len(data1['position']) <=0))):
			output_str += ",position is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("position:"+ output)
			return HttpResponse(output)
			
		else:
			position = data1['position']
			
		if((data1.get('warehouseid') is None) or ((data1.get('warehouseid') is not None) and (len(data1['warehouseid']) <=0))):
			output_str += ",warehouseid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("warehouseid:"+ output)
			return HttpResponse(output)
			
		else:
			warehouseid = data1['warehouseid']
			
		if((data1.get('statusid') is None) or ((data1.get('statusid') is not None) and (len(data1['statusid']) <=0))):
			output_str += ",statusid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("statusid:"+ output)
			return HttpResponse(output)
			
		else:
			statusid = data1['statusid']
		#checks db	
		is_history_rec_needed = True
		
		position_status_get = inv_position.objects.filter(Position = position)
		if(len(position_status_get) > 0): #just update the ChangeDate         
			is_history_rec_needed = False
			#print("matching")
			output = '{"error_code":"4", "error_desc": "Your position already exists."}'
			logging.debug("location_add:"+ output)
			return HttpResponse(output)

		try:
			position_rec = inv_position(Position = position,warehouseId_id = warehouseid,statusId_id = statusid)
			position_rec.save()
			output = '{"error_code":"1", "error_desc": "Record added"}' 
			logging.debug("position_add:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'position_add:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("position_add:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to add record"}' 
			logging.debug("position_add:"+ output)
			return HttpResponse(err_desc)
	else:
		logging.debug("position_add: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("position_add:"+ output)
		return HttpResponse(output)
		
################################################################################################################################
def update_position(request):
	if(request.method == "POST"):
		logging.debug("update_position:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "updating position.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("update_position:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("update_position:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",positionid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("positionid:"+ output)
			return HttpResponse(output)
		
		else:
			positionid = data1['id']
				
		if((data1.get('position') is None) or ((data1.get('position') is not None) and (len(data1['position']) <=0))):
			output_str += ",position is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("position:"+ output)
			return HttpResponse(output)
			
		else:
			position = data1['position']
			
		if((data1.get('warehouseid') is None) or ((data1.get('warehouseid') is not None) and (len(data1['warehouseid']) <=0))):
			output_str += ",warehouseid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("warehouseid:"+ output)
			return HttpResponse(output)
			
		else:
			warehouseid = data1['warehouseid']
			
		if((data1.get('statusid') is None) or ((data1.get('statusid') is not None) and (len(data1['statusid']) <=0))):
			output_str += ",statusid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("statusid:"+ output)
			return HttpResponse(output)
			
		else:
			statusid = data1['statusid']

		try:
			position_rec = inv_position.objects.filter(id = positionid).update(Position = position,warehouseId_id = warehouseid,statusId_id = statusid)
			output = '{"error_code":"1", "error_desc": "record updated"}' 
			logging.debug("update_position:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'update_position:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("update_position:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to update the record/Id doesnot exists"}' 
			logging.debug("update_position:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("update_position: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("update_position:"+ output)
		return HttpResponse(output)
#################################################################################################################################
def get_position(request):
	cursor = connection.cursor()
	cursor.execute("select p.* ,w.warehouseName,s.statusName from inv_position as p JOIN inv_warehouse as w,inv_status as s where p.warehouseId_id = w.id and p.statusId_id = s.id")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['position'] = row[1]
		d['warehousename'] = row[4]
		d['statusname'] = row[5]
		objects_list.append(d)
	json_output='{"position_details":'	
	json_output+= json.dumps(objects_list,indent = 3)
	json_output+='}'
	logging.debug("get_position:")
	return HttpResponse(json_output)
	
#################################################################################################################################
def active_position(request):
	cursor = connection.cursor()
	cursor.execute("select p.* ,w.warehouseName,s.statusName from inv_position as p JOIN inv_warehouse as w,inv_status as s where p.warehouseId_id = w.id and p.statusId_id = s.id and p.statusId_id = 1")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['position'] = row[1]
		d['warehousename'] = row[4]
		d['statusname'] = row[5]
		objects_list.append(d)
	json_output='{"active_position_details":'	
	json_output+= json.dumps(objects_list,indent = 3)
	json_output+='}'
	logging.debug("get_position:")
	return HttpResponse(json_output)
	
###############################################################################################################################
def del_position(request):
	if(request.method == "POST"):
		logging.debug("del_position:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "deleting position.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("del_position:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("del_position:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",positionid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("positionid:"+ output)
			return HttpResponse(output)
		
		else:
			positionid = data1['id']
			
			
		position_data_delete = True
		
		del_data_get = inv_position.objects.filter(id=positionid)
		if(len(del_data_get) > 0):
			del_data_get.delete()
			position_data_delete = False
			#printing response
			output = '{"error_code":"0", "error_desc": "Your position is deleted"}'
			logging.debug("del_warehouse:"+ output)
			return HttpResponse(output)
			
		else:
			output = '{"error_code":"2", "error_desc": "position doesnot exists please insert the position"}'
			logging.debug("del_position:"+ output)
			return HttpResponse(output)
		

	else:
		logging.debug("del_position: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("del_position:"+ output)
		return HttpResponse(output)
		
###############################################################################################################################
def get_materialtype(request):
	cursor = connection.cursor()
	cursor.execute("select * from inv_materialType")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['materialtype'] = row[1]
		objects_list.append(d)
	json_output='{"materialtype_details":'	
	json_output+= json.dumps(objects_list,indent = 3)
	json_output+='}'
	return HttpResponse(json_output)
#############################################################################################################################
def get_uom(request):
	cursor = connection.cursor()
	cursor.execute("select * from inv_UnitOfMeasure")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['id']=row[0]
		d['measurementname'] = row[1]
		objects_list.append(d)
	json_output='{"uom_details":'	
	json_output+= json.dumps(objects_list,indent = 3)
	json_output+='}'
	return HttpResponse(json_output)
	
#############################################################################################################################
def add_requisition(request):
	if(request.method == "POST"):
		logging.debug("add_requisition:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "adding requisition.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_requisition:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_requisition:"+ output)
			return HttpResponse(output)
			
		if((data1.get('userid') is None) or ((data1.get('userid') is not None) and (len(data1['userid']) <=0))):
			output_str += ",userid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("userid:"+ output)
			return HttpResponse(output)
		
		else:
			userid = data1['userid']
			
		if((data1.get('duedate') is None) or ((data1.get('duedate') is not None) and (len(data1['duedate']) <=0))):
			output_str += ",duedate is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("duedate:"+ output)
			return HttpResponse(output)
		
		else:
			dueDate = data1['duedate']	
			
		try:
			requisition_rec = requisition(duedate = dueDate,userID_id = userid)
			requisition_rec.save()
			output = '{"error_code":"1", "error_desc": "Requisiton added"}' 
			logging.debug("add_requisition:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'add_requisition:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("add_requisition:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to add Requisition"}' 
			logging.debug("add_requisition:"+ output)
			return HttpResponse(err_desc)
	else:
		logging.debug("add_requisition: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("add_requisition:"+ output)
		return HttpResponse(output)
		
################################################################################################################################
def del_requisition(request):
	if(request.method == "POST"):
		logging.debug("del_requisition:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "deleting requisition.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("del_requisition:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("del_requisition:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",requisition is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("requisitionid:"+ output)
			return HttpResponse(output)
		
		else:
			requisitionid = data1['requisitionid']
			
			
		requisition_data_delete = True
		
		del_data_get = requisition.objects.filter(id=requisitionid)
		if(len(del_data_get) > 0):
			del_data_get.delete()
			requisition_data_delete = False
			#printing response
			output = '{"error_code":"0", "error_desc": "Your requisition is deleted"}'
			logging.debug("del_requisition:"+ output)
			return HttpResponse(output)
			
		else:
			output = '{"error_code":"2", "error_desc": "requisition doesnot exists please Make a requisition"}'
			logging.debug("del_requisition:"+ output)
			return HttpResponse(output)
		

	else:
		logging.debug("del_requisition: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("del_requisition:"+ output)
		return HttpResponse(output)
################################################################################################################################
def get_requisition(request):
	if(request.method == "POST"):
		logging.debug("requsition_details:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "getting requisitions.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("requsition_details:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("requsition_details:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",requisitionid is required"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("requsition_details:"+ output)
			return HttpResponse(output)
		
		else:
			requisitionid = data1['id']
			
		try:
			cursor = connection.cursor()
			cursor.execute("select r.*,e.userName,c.materialCategory,s.statusName from requisition r JOIN jts_employees e ON r.userId_id = e.id JOIN inv_materialCategory c ON r.productCategory_id = c.id JOIN inv_status s ON r.statusId_id = s.id where userId_id = '%s' order by r.requisitionDate desc" %(requisitionid))
			rows = cursor.fetchall()
			objects_list = []
			for row in rows:
				d = collections.OrderedDict()
				d['id']=row[0]
				d['username']=row[6]
				d['requisitiondate'] = row[1]
				d['duedate'] = row[2]
				d['materialcategory'] = row[7]
				d['status'] = row[8]
				objects_list.append(d)
			json_output='{"requisition":'	
			json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
			json_output+='}'
			logging.debug("requisition:")
			return HttpResponse(json_output)
		except Exception, e:
			err_desc = 'requsition_details:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("requsition_details:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Invalid id"}' 
			logging.debug("requsition_details:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("requsition_details: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("requsition_details:"+ output)
		return HttpResponse(output)
		
#################################################################################################################################
def get_newrequisition(request):
	if(request.method == "POST"):
		logging.debug("new_requsition:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "getting requisition.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("new_requsition:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("new_requsition:"+ output)
			return HttpResponse(output)
			
		if((data1.get('userid') is None) or ((data1.get('userid') is not None) and (len(data1['userid']) <=0))):
			output_str += ",userid is required"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("requsition_details:"+ output)
			return HttpResponse(output)
		
		else:
			userid = data1['userid']
			
		try:
			cursor = connection.cursor()
			cursor.execute("select id,requisitionDate,duedate,userID_id from requisition where userID_id = '%s' order by id desc limit 1" %(userid))
			rows = cursor.fetchall()
			objects_list = []
			for row in rows:
				d = collections.OrderedDict()
				d['requisitionid']=row[0]
				d['userid']=row[3]
				d['requisitiondate'] = row[1]
				d['duedate'] = row[2]
				objects_list.append(d)
			json_output='{"new_requisition":'	
			json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
			json_output+='}'
			logging.debug("new_requsition:")
			return HttpResponse(json_output)
		except Exception, e:
			err_desc = 'new_requsition:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("new_requsition:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Invalid userid"}' 
			logging.debug("new_requsition:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("new_requsition: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("new_requsition:"+ output)
		return HttpResponse(output)
	
################################################################################################################################
def add_requisitiondetails(request):
	if(request.method == "POST"):
		logging.debug("add_requisition_details:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "adding requisition details.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_requisition_details:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_requisition_details:"+ output)
			return HttpResponse(output)
			
		if((data1.get('quantity') is None) or ((data1.get('quantity') is not None) and (len(data1['quantity']) <=0))):
			output_str += ",quantity is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("quantity_requisition:"+ output)
			return HttpResponse(output)
		
		else:
			quantity = data1['quantity']
			
		if((data1.get('productid') is None) or ((data1.get('productid') is not None) and (len(data1['productid']) <=0))):
			output_str += ",productid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("productid_requisition:"+ output)
			return HttpResponse(output)
		
		else:
			productid = data1['productid']
			
		if((data1.get('requisitionid') is None) or ((data1.get('requisitionid') is not None) and (len(data1['requisitionid']) <=0))):
			output_str += ",requisitionid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("requisitionid:"+ output)
			return HttpResponse(output)
		
		else:
			requisitionid = data1['requisitionid']
			
		qty = []
		product = []
		requisition = []
		sqty = str(quantity)[1:-1]
		sproduct = str(productid)[1:-1]
		srequisitionid = str(requisitionid)[1:-1]
		
		for quant in sqty.split(","):
			qty.append(quant)
		print qty
			
		for prod in sproduct.split(","):
			product.append(prod)
		print product
		
		for req in srequisitionid.split(","):
			requisition.append(req)
		print requisition
		
		for rec in qty:
			index1=qty.index(rec)
			quantity1 = rec
			product1 = product[index1]
			requisition1 = requisition[index1]
			cursor = connection.cursor()
			print quantity1
			print product1
			print requisition1
			cursor.execute("insert into requisition_details(quantityrequested,productId_id,requisitionId_id) values('%s','%s','%s')" %(quantity1,product1,requisition1))
			cursor.commit()
		return HttpResponse("values inserted")
		'''try:
			requisition_details_rec = requisition_details(quantityRequested = quantity,productId_id = productid,requisitionId_id = requisitionid)
			requisition_details_rec.save()
			output = '{"error_code":"1", "error_desc": "Requisiton details added"}' 
			logging.debug("add_requisition_details:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'add_requisition_details:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("add_requisition_details:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to add Requisition"}' 
			logging.debug("add_requisition_details:"+ output)
			return HttpResponse(err_desc)'''
	else:
		logging.debug("add_requisition_details: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("add_requisition_details:"+ output)
		return HttpResponse(output)
		
###############################################################################################################################
def get_requisitiondetails(request):
	if(request.method == "POST"):
		logging.debug("requsition_details:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "getting requisitiondetials.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("requsition_details:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("requsition_details:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",requisitionid is required"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("requsition_details:"+ output)
			return HttpResponse(output)
		
		else:
			requisitionid = data1['id']
			
		try:
			cursor = connection.cursor()
			cursor.execute("select rd.* ,pr.productName,s.statusName from requisition_details rd JOIN inv_products pr ON rd.productId_id = pr.id JOIN inv_status s ON rd.statusId_id = s.id WHERE rd.requisitionId_id = '%s'" %(requisitionid))
			rows = cursor.fetchall()
			objects_list = []
			for row in rows:
				d = collections.OrderedDict()
				d['requisitionid'] = row[3]
				d['id']=row[0]
				d['productname'] = row[6]
				d['quantityrequested']=row[1]
				d['quantityissued'] = row[4]
				d['status'] = row[7]
				objects_list.append(d)
			json_output='{"requisition_details":'	
			json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
			json_output+='}'
			logging.debug("requisition_details:")
			return HttpResponse(json_output)
		except Exception, e:
			err_desc = 'requsition_details:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("requsition_details:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Invalid id"}' 
			logging.debug("requsition_details:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("requsition_details: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("requsition_details:"+ output)
		return HttpResponse(output)	
		
#############################################################################################################################################################
def get_storerequisition(request):
	cursor = connection.cursor()
	cursor.execute("select rd.productId_id,p.productName,rd.requisitionId_id,r.requisitionDate,r.duedate,r.statusId_id,s.statusName,r.userID_id,e.userName from requisition_details rd JOIN inv_products p ON rd.productId_id = p.id JOIN requisition r ON rd.requisitionId_id = r.id JOIN inv_status s ON r.statusId_id = s.id JOIN jts_employees e ON r.userID_id = e.id WHERE DATE(r.requisitionDate) <= CURDATE() order by r.requisitionDate desc")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['requisitionid']=row[2]
		d['productid'] = row[0]
		d['productname'] = row[1]
		d['userid'] = row[7]
		d['username']=row[8]
		d['requisitiondate'] = row[3]
		d['duedate'] = row[4]
		d['status'] = row[6]
		objects_list.append(d)
	json_output='{"store_requisition":'	
	json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
	json_output+='}'
	logging.debug("requisition:")
	return HttpResponse(json_output)

#################################################################################################################################
def get_todayrequisition(request):
	cursor = connection.cursor()
	cursor.execute("select rd.productId_id,p.productName,rd.requisitionId_id,r.requisitionDate,r.duedate,r.statusId_id,s.statusName,r.userID_id,e.userName from requisition_details rd JOIN inv_products p ON rd.productId_id = p.id JOIN requisition r ON rd.requisitionId_id = r.id JOIN inv_status s ON r.statusId_id = s.id JOIN jts_employees e ON r.userID_id = e.id WHERE DATE(r.requisitionDate) = CURDATE() order by r.requisitionDate desc")
	rows = cursor.fetchall()
	objects_list = []
	for row in rows:
		d = collections.OrderedDict()
		d['requisitionid']=row[2]
		d['productid'] = row[0]
		d['productname'] = row[1]
		d['userid'] = row[7]
		d['username']=row[8]
		d['requisitiondate'] = row[3]
		d['duedate'] = row[4]
		d['status'] = row[6]
		objects_list.append(d)
	json_output='{"today_requisition":'	
	json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
	json_output+='}'
	logging.debug("requisition:")
	return HttpResponse(json_output)

#############################################################################################################################################################
def get_storerequisitiondetails(request):
	if(request.method == "POST"):
		logging.debug("store_requisition_details:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "getting requisition details.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("store_requisition_details:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("store_requisition_details:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",requisitionid is required"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("store_requisition_details:"+ output)
			return HttpResponse(output)
		
		else:
			requisitionid = data1['id']
			
		try:
			cursor = connection.cursor()
			cursor.execute("select rd.id,rd.requisitionId_id,rd.productId_id,pr.productName,rd.quantityRequested,rd.quantityIssued,(rd.quantityRequested-rd.quantityIssued) as balance,rd.statusId_id,s.statusName from requisition_details rd JOIN inv_products pr ON rd.productId_id = pr.id JOIN inv_status s ON rd.statusId_id = s.id WHERE rd.requisitionId_id = %s" %(requisitionid))
			rows = cursor.fetchall()
			objects_list = []
			for row in rows:
				d = collections.OrderedDict()
				d['id']=row[0]
				d['requisitionid'] = row[1]
				d['productname'] = row[3]
				d['quantiyrequested'] = row[4]
				d['quantityissued'] = row[5]
				d['balance'] = row[6]
				d['status'] = row[8]
				objects_list.append(d)
			json_output='{"store_requisition_details":'	
			json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
			json_output+='}'
			logging.debug("store_requisition_details:")
			return HttpResponse(json_output)
		except Exception, e:
			err_desc = 'store_requisition_details:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("store_requisition_details:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Invalid id"}' 
			logging.debug("store_requisition_details:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("store_requisition_details: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("store_requisition_details:"+ output)
		return HttpResponse(output)
#############################################################################################################################################
def get_zerorequisitiondetails(request):
	if(request.method == "POST"):
		logging.debug("store_requisition_details_on_zero:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "getting requisition details.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("store_requisition_details:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("store_requisition_details_on_zero:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",requisitionid is required"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("store_requisition_details_on_zero:"+ output)
			return HttpResponse(output)
		
		else:
			requisitionid = data1['id']
			
		try:
			cursor = connection.cursor()
			cursor.execute("select rd.id,rd.requisitionId_id,rd.productId_id,pr.productName,rd.quantityRequested,rd.quantityIssued,(rd.quantityRequested-rd.quantityIssued) as balance,rd.statusId_id,s.statusName from requisition_details rd JOIN inv_products pr ON rd.productId_id = pr.id JOIN inv_status s ON rd.statusId_id = s.id WHERE rd.requisitionId_id = %s and (rd.quantityRequested-rd.quantityIssued) > 0" %(requisitionid))
			rows = cursor.fetchall()
			objects_list = []
			for row in rows:
				d = collections.OrderedDict()
				d['id']=row[0]
				d['requisitionid'] = row[1]
				d['productname'] = row[3]
				d['quantiyrequested'] = row[4]
				d['quantityissued'] = row[5]
				d['balance'] = row[6]
				d['status'] = row[8]
				objects_list.append(d)
			json_output='{"store_requisition_details_on_zero":'	
			json_output+= json.dumps(objects_list,indent = 3,sort_keys = True, default = str)
			json_output+='}'
			logging.debug("store_requisition_details_on_zero:")
			return HttpResponse(json_output)
		except Exception, e:
			err_desc = 'store_requisition_details_on_zero:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("store_requisition_details_on_zero:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Invalid id"}' 
			logging.debug("store_requisition_details_on_zero:"+ output)
			return HttpResponse(output)
	else:
		logging.debug("store_requisition_details_on_zero: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("store_requisition_details_on_zero:"+ output)
		return HttpResponse(output)
################################################################################################################################
def update_requisition(request):
	if(request.method == "POST"):
		logging.debug("add_requisition:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "updating requisition.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("update_requisition:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("update_requisition:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",requisitionid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("userid:"+ output)
			return HttpResponse(output)
		
		else:
			requisitionid = data1['id']
			
		if((data1.get('statusid') is None) or ((data1.get('statusid') is not None) and (len(data1['statusid']) <=0))):
			output_str += ",statusid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("statusid:"+ output)
			return HttpResponse(output)
		
		else:
			statusid = data1['statusid']

			
		try:
			requisition_rec = requisition.objects.filter(id = requisitionid).update(statusId_id = statusid)
			output = '{"error_code":"1", "error_desc": "Requisiton updated"}' 
			logging.debug("update_requisition:"+ output)
			return HttpResponse(output)
			
		except Exception, e:
			err_desc = 'update_requisition:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
			logging.debug("update_requisition:"+ err_desc)
			output = '{"error_code":"2", "error_desc": "Failed to update Requisition"}' 
			logging.debug("update_requisition:"+ output)
			return HttpResponse(err_desc)
	else:
		logging.debug("update_requisition: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("update_requisition:"+ output)
		return HttpResponse(output)
		
###############################################################################################################################
def update_requisitiondetails(request):
	if(request.method == "POST"):
		logging.debug("update_requisition_details:request is from ip: %s" %request.META.get('REMOTE_ADDE'))
		output_str = "updating requisition details.."
		try:
			data1 = json.loads((request.body).decode('utf-8'))
			print request.body
			#return data1
		except ValueError:
			output_str += ",invalid input, no proper JSON request "
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_requisition_details:"+ output)
			return HttpResponse(output)
			#return "value error"
			
		if(not data1):
			output_str += "all fields are necessary"
			output = '{"error_code":"2", "error_desc": "%s"}' %(output_str )
			logging.debug("add_requisition_details:"+ output)
			return HttpResponse(output)
			
		if((data1.get('id') is None) or ((data1.get('id') is not None) and (len(data1['id']) <=0))):
			output_str += ",requisition_details_id is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("requisition_details_id:"+ output)
			return HttpResponse(output)
		
		else:
			requisitiondetailsid = data1['id']
			
		if((data1.get('requisitionid') is None) or ((data1.get('requisitionid') is not None) and (len(data1['requisitionid']) <=0))):
			output_str += ",requisitionid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("requisitionid:"+ output)
			return HttpResponse(output)
		
		else:
			requisitionid = data1['requisitionid']
			
		if((data1.get('quantityissued') is None) or ((data1.get('quantityissued') is not None) and (len(data1['quantityissued']) <=0))):
			output_str += ",quantityissued is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("quantityissued:"+ output)
			return HttpResponse(output)
		
		else:
			quantityissued = data1['quantityissued']
			
		if((data1.get('statusid') is None) or ((data1.get('statusid') is not None) and (len(data1['statusid']) <=0))):
			output_str += ",statusid is mandatory"
			output = '{"error_code":"2", "error_desc": "%s"}' %output_str
			logging.debug("statusid:"+ output)
			return HttpResponse(output)
		
		else:
			statusid = data1['statusid']
		history_requisition = True
		getdata= requisition_details.objects.filter(id=requisitiondetailsid)
		if(len(getdata) > 0):
			for row1 in getdata:
				if((int(quantityissued) < int(row1.quantityIssued)) or (int(quantityissued) > int(row1.quantityRequested))):
					history_requisition = False
					output = '{"error_code":"2", "error_desc": "Issuing quantity should be >= previous Issued quantity (or) <= requested quantity"}' 
					logging.debug("statusid:"+ output)
					return HttpResponse(output)
				else:
					try:
						requisition_details_rec = requisition_details.objects.filter(id = requisitiondetailsid).update(quantityIssued = quantityissued,statusId_id = statusid)
						cursor = connection.cursor()
						cursor.execute("select requisitionId_id,statusId_id from requisition_details where requisitionId_id = '%s' AND (statusId_id = 6 OR statusId_id = 7)" %(requisitionid))
						rows = cursor.fetchall()
						if (len(rows) > 0):
							status = 7
						else:
							status = 8
						requisition_rec = requisition.objects.filter(id = requisitionid).update(statusId_id = status)
						output = '{"error_code":"1", "error_desc": "Requisiton details updated"}' 
						logging.debug("update_requisition_details:"+ output)
						return HttpResponse(output)
					except Exception, e:
						err_desc = 'update_requisition_details:exception details:[%s],[%s]' %((sys.exc_info()[0]), (sys.exc_info()[1]))
						logging.debug("update_requisition_details:"+ err_desc)
						output = '{"error_code":"2", "error_desc": "Failed to update requisition"}' 
						logging.debug("update_requisition_details:"+ output)
						return HttpResponse(err_desc)
					
	else:
		logging.debug("update_requisition_details: request is from the IP:%s" %request.META.get('REMOTE_ADDR'))
		output = '{"error_code":"2", "error_desc": "GET is not supported"}' 
		logging.debug("update_requisition_details:"+ output)
		return HttpResponse(output)
