#!/usr/bin/python
'''
This python program read the rnc_information with VENDOR, Technology, GW_URI, RNC, RNC_NAME
Then it output a file displaying the size of all DGW call trace acccording to the script configuration 
'''
__author__ = 'Marat'

import os, sys, getopt
from datetime import datetime

RNC_DGW_mapping = ''
DGW_IP_Name_mapping = ''
DGW_IP_Name = {}
DGW_RNC_Name = {}
Pssh_file = ''
File_size = ''
Date= ''

total_parameter = len(sys.argv)
myopts, args = getopt.getopt(sys.argv[1:],'RDF:o:', ['RNC=','DGW_HOST=', 'File_pssh=', 'Output='])

########################################
# define telecom vendor
# 1: Ericsson
# 2: Huawei
# 9: ALU
########################################
Vendor_name = {'1':"Ericsson",'2':"Huawei",'9':"ALU"}

#print ("Vendor ID test: %s" % (Vendor_ID_to_name(1)) )

########################################
# o == option
# a == argument passed to the o
########################################

for o, a in myopts:
    if o in ("-R", "--RNC"):
        RNC_DGW_mapping=a
    elif o in ("-D", "--DGW_HOST"):
        DGW_IP_Name_mapping=a
    elif o in ("-F", "--File_pssh"):
        Pssh_file=a 
    elif o in ("-o", "--Output"):
        File_size=a
    else:
        print("Usage: %s -R RNC_information -D grep 'DGW' /etc/hosts -o output" % sys.argv[0])

#Display input and output file name passed as the args
#print ("Input file : %s %s %s and output file %s" % (RNC_DGW_mapping, DGW_IP_Name_mapping, Pssh_file, File_size))

#build 'DGW_IP':'DGW_NAME' dictionary
with open(DGW_IP_Name_mapping, 'r') as file:
    for line in file.readlines():
        DGW_info=line.split() 
        DGW_IP_Name[DGW_info[0]]=DGW_info[1]
file.closed

#build 'DGW_IP_RNC_ID':'DGW_NAME RNC_NAME' dictionary
with open(RNC_DGW_mapping, 'r') as file:
    for line in file.readlines()[2:]:
        RNC_info = line.split() #[0]:VENDOR_ID, [1]:Technology, [2]:GW_URI, [3]:RNC, [4]RNC_NAME
# debug        print("%10s %5s %15s %5s %15s" % (Vendor_name[RNC_info[0].strip()], RNC_info[1], RNC_info[2][13:-6],\
# debug                RNC_info[3], RNC_info[4]))
        DGW_IP = RNC_info[2][13:-6].strip()
        DGW_RNC = RNC_info[3].strip()
        DGW_KEY = DGW_IP + "_" + DGW_RNC
        DGW_RNC_Name[DGW_KEY] = [Vendor_name[RNC_info[0].strip()], RNC_info[1], DGW_IP_Name[DGW_IP], RNC_info[3], RNC_info[4]]
file.closed

#replace the IP and append with 
with open(Pssh_file, 'r') as file:
    for line in file.readlines():
        Size_info=line.split()
        #print Size_info
        if len(Size_info) > 2:
            if Size_info[2] == "[SUCCESS]":
                current_DGW_IP = Size_info[3] 
                #print current_DGW_IP
            elif Size_info[2] == "[FAILURE]":
                print "Skip, unknown error with: ", Size_info[3]
        elif len(Size_info) < 3:
            my_key = current_DGW_IP + "_" + Size_info[1].split('/')[-1]
            DGW_RNC_Name[my_key].append(Size_info[0]) #append size of the folder 
            #print DGW_RNC_Name[my_key] 
        else:
            print "unknown error"
file.closed

with open(File_size, 'w') as file:
    print "Start writing %s" % (File_size)
    file.write("Check done on %s\n" % (datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')))
    file.write("Vendor\t%8sTech\tDGW server\tRNC_Name\tRNC_ID\tSize%s\n" % (' ',' '))
    for my_key, info_list in DGW_RNC_Name.iteritems():
        if len(info_list) == 6:
            Vendor, Technology, DGW_server, RNC_ID, RNC_Name, Size = info_list
            file.write("%-8s\t%s\t%s\t%-10s\t%s\t%-s\n" % (Vendor, Technology, DGW_server, RNC_Name, RNC_ID, Size))
        elif len(info_list) < 6:
            file.write("No size information for %s %s\n" % (info_list[2], info_list[4]))
file.closed
