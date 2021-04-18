'''Density range: protected region [11.42~16.82], CBD[9.18~13.95]'''
#Data in metric units
# Number of section = 1186
# Number of junction = 621

import sys
#import pandas as pd
from AAPI import *
from PyANGKernel import *
import time
import datetime



# --------------------- inputs ----------------------

def AAPILoad():
	AKIPrintString("Hello, Sydney CBD! - Chloe")

	with open('Microsimulation_result_2.txt', 'a') as file:
		file.truncate(0)
	with open('Microsimulation_result_time_2.txt', 'a') as file:
		file.truncate(0)
	with open('Protected_region_Microsimulation_result.txt', 'a') as file:
		file.truncate(0)
	with open('Protected_region_Microsimulation_result_time.txt', 'a') as file:
		file.truncate(0)
	with open("300s_data.txt", "a") as file:
		file.truncate(0)
	with open('Protected_region_300s_data.txt', 'a') as file:
		file.truncate(0)
	with open('pi_controller_n.txt', 'a') as file:
		file.truncate(0)
	with open('pi_controller_u.txt', 'a') as file:
		file.truncate(0)
	with open('pi_controller_u_raw_data.txt', 'a') as file:
		file.truncate(0)


	return 0

def AAPIInit():

	idVeh = ANGConnGetObjectId( AKIConvertFromAsciiString( "car" ), False )
	carPosition = AKIVehGetVehTypeInternalPosition( idVeh )
	astring = "Car postion:" +str(carPosition)
	#AKIPrintString(astring)
	return 0




def AAPIManage(absolute_time, time, warmup, cycle):

	#Define targeted junctions
	'''CHANGE THIS INFO BELOW'''


	#Information
	#Targeted junction number
	junction_list = 7411,6419,7503,7496,6486,6462,6275,6546,6529,13217,6367,6672,6682,6634,6600,6615,6608,9841,6864,6918,6379,6519,7460,7467,7898,8856,6499,6299,7069,6270,8470,8459,8277,8132
	inflow_phase_id_list = [[1,5,10,14,19,31],[6,11,23,28,45],[1,15,24],[14,16,25,29,33],[1,6,24,27,48],[1,5,7,53],[1,5,7,30],[47,52],[29,34,36],[1,4,6,15,20],[1,5,8],[1],[4],[1,8],[1,4,17],[1,6,9,11,19,24],[1,4,10],[4,7,17],[1,20],[5,8,11,17],[13,16,23],[11,13],[10,12,26],[21],[12,15],[5,19],[1,10],[1,7,11,14],[1,4],[1],[1,8],[1,5,7,11],[1,4,7],[1,4]]
	initial_maximum_green = [[30,30,30,30,30,30],[30,30,30,30,30],[30,30,30],[30,30,30,30,30],[30,30,30,30,30],[30,30,30,30],[30,30,30,30],[30,30],[30,30,30],[30,30,30,30,30],[30,30,30],[30],[30],[30,30],[30,30,30],[30,30,30,30,30,30],[30,30,30],[30,30,30],[30,30],[30,30,30,30],[30,30,30],[30,30],[30,30,30],[30],[30,30],[30,30],[30,30],[30,30,30,30],[30,30],[30],[30,30],[30,30,30,30],[30,30,30],[30,30]]
		#Manually append inflow  and phase data in a list. MUST BE IN THE SAME ORDER


	'''DO NOT CHANGE THE CODES BELOW'''
	u_data = open('pi_controller_u.txt', 'r+')
	u_list_st = list(u_data)
	u_list = []
	for data in u_list_st:
		u_list.append(int(data))




	if len(u_list) > 0:

		u = float(u_list[len(u_list) - 1])
		new_green_list = []
		nested_green = []
		for initial_green in initial_maximum_green:

			for green_time in initial_green:
				new_green_time = (10 - 40) * u + 40
				nested_green.append(new_green_time)
			new_green_list.append(nested_green)
		'''
		if u == 1:
			print("Sydney CBD congestion reached threshold limit. Adjusting maxmimum green time of targeted junction will be minimised now")
		if u == 0:
			print("Sdyney CBD congestion is mitigated. The maxmimum green time of targeted junction will be maximised.")
		if (u > 0) and (u<1):
			print("The level of congestion = medium")
		'''
		i = 0
		ii = 0
		while i < len(junction_list):
			junction_number = junction_list[i]
			while ii < len(inflow_phase_id_list[i]):
				phase = inflow_phase_id_list[i][ii]
				new_green_time = new_green_list[i][ii]
				initial_green_time = initial_maximum_green[i][ii]
				if u == 1:
					ECISetActuatedParamsMaxGreen(0, junction_number, phase, 10)
					#print("Green time is minimised : 10s")
				elif u == 0:
					ECISetActuatedParamsMaxGreen(0, junction_number, phase, initial_green_time)
					#print("Green time is maximised: ", initial_green_time)
				else:
					ECISetActuatedParamsMaxGreen(0, junction_number, phase, new_green_time)
					#print("Green time is adjusted: ", new_green_time)
				ii += 1
			ii = 0
			i += 1
	
	return 0


def AAPIPostManage(absolute_time, time, warmup, cycle):

	a = AKIEstGetIntervalStatistics()
	b = AKIIsGatheringStatistics()
	total_length = AKIGetTotalLengthSystem()
	section_number = AKIInfNetNbSectionsANG()
	section_id = AKIInfNetGetSectionANGId(1)
	junction_number = AKIInfNetNbJunctions()
	system_length = AKIGetTotalLengthSystem()
	net_section =  AKIInfNetNbSectionsANG()
	flow = 0
	density = 0
	total_vehicle = 0
	total_lengths = 0 
	for i in range(net_section):
		section_id =  AKIInfNetGetSectionANGId(i)
		section_info = AKIInfNetGetSectionANGInf(section_id)
		total_lengths = total_lengths + section_info.length
		nb_vehicles = AKIVehStateGetNbVehiclesSection(section_id, True)
		total_vehicle = total_vehicle + nb_vehicles
		estad2 = AKIEstGetParcialStatisticsSection(section_id, 180, 0)
		if (estad2.report==0):
			astring = "\t\t section_id :" + str(section_id)
			astring = "\t\t Report : " + str(estad2.report)
			astring = "\t\t Flow : " + str(estad2.Flow)
			astring = "\t\t Density : " + str(estad2.Density)		
			flow = flow + round((float(estad2.Flow) * float(section_info.length / 1000)), 2)
			density = density + round((float(estad2.Density) * float(section_info.length / 1000)), 2)
	flow = round(flow / (total_lengths / 1000), 2) 
	density = round(density / (total_lengths / 1000), 2) 
	with open('300s_data.txt', 'r+') as file:
		file.truncate(0)
	if ((time- 21600) % 180 == 0) and time != 21600:
		f = open('Microsimulation_result_2.txt', 'a')
		f.write(str(flow) + " " + str(density) + "\n")

		t = open('Microsimulation_result_time_2.txt', 'a')
		t.write(str(flow) + " " + str(density) + " " + str(time) + "\n")
		with open('300s_data.txt', 'r+') as file:
				file.truncate(0)
		file = open('300s_data.txt', 'a')
		file.write(str(density))
	flow = 0
	density = 0
	total_vehicle = 0
	total_lengths = 0

	pr = open('Protected_region.txt', 'r')
	pr_list_st = list(pr)
	pr_list = []

	for data in pr_list_st:
		pr_list.append(int(data))
	for id in pr_list:
		section_info = AKIInfNetGetSectionANGInf(id)
		total_lengths = total_lengths + section_info.length
		nb_vehicles = AKIVehStateGetNbVehiclesSection(section_id, True)
		total_vehicle = total_vehicle + nb_vehicles
		estad2 = AKIEstGetParcialStatisticsSection(id, 180, 0)
		if (estad2.report==0):
			astring = "\t\t section_id :" + str(id)
			astring = "\t\t Report : " + str(estad2.report)
			astring = "\t\t Flow : " + str(estad2.Flow)
			astring = "\t\t Density : " + str(estad2.Density)			
			flow = flow + round((float(estad2.Flow) * float(section_info.length / 1000)), 2)
			density = density + round((float(estad2.Density) * float(section_info.length / 1000)), 2)
	flow = round(flow / (total_lengths / 1000), 2) 
	density = round(density / (total_lengths / 1000), 2) 
	with open('Protected_region_300s_data.txt', 'a') as file:
		file.truncate(0)
	if ((time- 21600) % 180 == 0) and time != 21600:
		ff = open('Protected_region_Microsimulation_result.txt', 'a')
		ff.write(str(flow) + " " + str(density) + "\n")
		tt = open('Protected_region_Microsimulation_result_time.txt', 'a')
		tt.write(str(flow) + " " + str(density) + " " + str(time) + "\n")
		N_present = density * total_lengths /1000
		pi_data_file = open('pi_controller_n.txt', 'a')
		pi_data_file.write(str(N_present)+ "\n")
		
		#Change the data below; K_P, K_I for perimeter control
		K_P =- 0.003
		K_I = -0.002


		#Do not touch the codes below
		N_hat = 20.53 * total_lengths /1000
		'''Check this set point range below'''
		#N_hat = range(1100,1300) 
		'''Check this set point range above'''

		N_present = density * total_lengths /1000
		if N_present < N_hat:
			print("Network is not congested")
			u_data = open('pi_controller_u.txt', 'r+')
			u_list_st = list(u_data)
			u_list = []
			for data in u_list_st:
				u_list.append(float(data))
			if len(u_list) == 0:
				u_list.append(0)
			u_past = u_list[len(u_list) - 1]
			n_data = open('pi_controller_n.txt', 'r+')
			n_list_st = list(n_data)
			n_list = []
			for data in n_list_st:
				n_list.append(float(data))
			if len(n_list)> 2:

				N_past = float(n_list[len(n_list) - 2])

				print("u_past", u_past)
				print("K_P", K_P)
				print("N_past", N_past)
				print("N_present", N_present)
				print("K_I", K_I)
				print("N_hat", N_hat)



				u = u_past + K_P * (N_past - N_present) + K_I * (N_hat - N_present)
				print("Calculated u : ", u)
				print("The  Kp error: ", N_present - N_past)
				print("The  Ki error: ", N_hat - N_present )
				u_file = open('pi_controller_u_raw_data.txt', 'a')
				u_file.write(str(u)+ "\n")


				if u > 1:
					u = 1
				if u < 0:
					u = 0
				pi_data_file = open('pi_controller_u.txt', 'a')
				pi_data_file.write(str(u)+ "\n")	



		if N_present > N_hat:
			print("Network is congested")
			u_data = open('pi_controller_u.txt', 'r+')
			u_list_st = list(u_data)
			u_list = []
			for data in u_list_st:
				u_list.append(float(data))
			if len(u_list) == 0:
				u_list.append(0)
			u_past = u_list[len(u_list) - 1]
			n_data = open('pi_controller_n.txt', 'r+')
			n_list_st = list(n_data)
			n_list = []
			for data in n_list_st:
				n_list.append(float(data))
			if len(n_list)> 2:

				N_past = float(n_list[len(n_list) - 2])

				print("u_past", u_past)
				print("K_P", K_P)
				print("N_past", N_past)
				print("N_present", N_present)
				print("K_I", K_I)
				print("N_hat", N_hat)



				u = u_past + K_P * (N_past - N_present) + K_I * (N_hat - N_present)
				print("Calculated u : ", u)
				print("The  Kp error: ", N_present - N_past)
				print("The  Ki error: ", N_hat - N_present )
				u_file = open('pi_controller_u_raw_data.txt', 'a')
				u_file.write(str(u)+ "\n")


				if u > 1:
					u = 1
				if u < 0:
					u = 0
				pi_data_file = open('pi_controller_u.txt', 'a')
				pi_data_file.write(str(u)+ "\n")
			



	return 0



def AAPIFinish():
	print("Bye, Sydney CBD! - Chloe")
	return 0

def AAPIUnLoad():
	return 0

def AAPIEnterVehicle(idveh,idsection):
	return 0

def AAPIExitVehicle(idveh,idsection):
	return 0




