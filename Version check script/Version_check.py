#!/usr/bin/python
'''
This python program extract the version information of CovMo modules
Current output in wiki format
'''
__author__ = 'Marat'

import os, sys, subprocess
from datetime import datetime

#For each module, define a function(version-related string) -> the parsed string

############################################################
#TODO
#1. [done] collect the sample (DB version, Nationwide, project.config, nt_parser)
#2. [done] finish the string parser
#3. Finish Nationwide, nt_parser, project config
############################################################
#Testing file configuration
#test_path = "/Users/Marat/temp/Version_check/"
#CovMo_war = test_path + "CovMo_war" #testing
#Data_Processing = test_path + "DataProcessing" #testing
#NT_parser = test_path + "nt_parser"
#Parser_path = test_path + "parser/"

#Live file configuration
CovMo_war="/home/covmo/software/tomcat/webapps/CovMo/WEB-INF/classes/customer.properties"
Data_Processing="/home/covmo/software/tomcat/webapps/data_processing/WEB-INF/classes/default.properties"
NT_parser = "/opt/covmo/parser/nt/version.py"
Parser_path = "/opt/covmo/parser/"

#5 types of version check

####################################################################################
#1. webpage (CovMo, data-processing)
####################################################################################

def Web_page_version(module, module_version_path):
    version_info={}
#CovMo.war
    if module == "CovMo_war":
        #print "CovMo.war file path:", CovMo_war
        with open(module_version_path, 'r') as file:
            for line in file.readlines():
                line = line.strip()
                if "product.version" in line:
                    version = line.split('=')[1]
                if "product.buildDate" in line:
                    buildDate = line.split('=')[1]
                if "project.build_number" in line:
                    build_number = line.split('=')[1]
        file.closed
        version_info[module] = "Version:" + version + " Build Date:" + buildDate + " Build number:" + build_number
        print "| %s | %s |" % (module, version_info[module])
        
#Data Processing
    elif module == "Data_Processing":
        with open(module_version_path, 'r') as file:
            for line in file.readlines():
                line = line.strip()
                if "product.version" in line:
                    version = line.split('=')[1]
                if "product.buildDate" in line:
                    buildDate = line.split('=')[1]
                if "product.buildRevision" in line:
                    buildRevision = line.split('=')[1]
        file.closed
        version_info[module] = "Version:" + version + " Build Date:" + buildDate + " Build revision:" + buildRevision
        print "| %s | %s |" % (module, version_info[module])
    else:
        print "The module name may be incorrect, please have a check"

#Function testing
#Web_page_version("CovMo_war",CovMo_war)
#Web_page_version("Data_Processing",Data_Processing)

####################################################################################
#2. Program
####################################################################################

#GTGW
#gtgw version
def program_version(program):
    version_info={}
    if program == "GTGW":
        proc_output = subprocess.Popen(['gtgw','version'],stdout=subprocess.PIPE)
        gtgw_version = proc_output.stdout.readlines()
        #print gtgw_version
        version = gtgw_version[1].split(',')[1].replace('"',"")
        version_info[program] = version
        print "| " + program + " | " + version_info[program] + " |"

def output_position_version(Tech, position_path ):
    Position_program = "GTPositioning_Linux_Release"
    position_path = position_path + "positioning/"
    #print position_path

#LTE Position
#/opt/covmo/parser/positioning/GTPositioning_Linux_Release_LTE -v
    if Tech == "LTE":
        Position_program = position_path + Position_program + "_LTE"
        #print Position_program
        return subprocess.Popen([Position_program,'-v'],stdout=subprocess.PIPE )
#UMTS Position
#/opt/covmo/parser/positioning/GTPositioning_Linux_Release -v
    if Tech == "UMTS":
        Position_program = position_path + Position_program 
        return subprocess.Popen([Position_program,'-v'],stdout=subprocess.PIPE )

def position_version(Tech, parser_path ):
    version_info={}
    if Tech == "LTE":
        Position_name = "Position_" + Tech
        proc_output = output_position_version(Tech, parser_path)
        version_output = proc_output.stdout.readlines()
        version_output = map(str.strip, version_output[1:7])
        version_info[Position_name] = " ".join(version_output)
        print "| " + Position_name + " | " + version_info[Position_name] + " |"
    if Tech == "UMTS":
        Position_name = "Position_" + Tech
        proc_output = output_position_version(Tech, parser_path)
        version_output = proc_output.stdout.readlines()
        version_info[Position_name] = version_output[0].split(',')[0].split(':')[1]
        print "| " + Position_name + " | " + version_info[Position_name] + " |"

#Function testing
#program_version("GTGW")
#position_version("LTE", "/opt/covmo/parser/")
#position_version("UMTS", "/opt/covmo/parser/")

####################################################################################
#3. java
####################################################################################

def output_java_version(parser_path, parser_folder ,parser_name):
    parser_path = parser_path + parser_folder + "/"
    parser_jar = parser_path + parser_name + ".jar"
    #print parser_path
    #print parser_jar
    return subprocess.Popen(['java','-jar', parser_jar, '-v'], stdout=subprocess.PIPE)

def merge_proc_output(parser_version):
    Branch = ""
    Version = ""
    while True:
        line = parser_version.stdout.readline()
        #print line
        if "Version" in line:
            Version = line.strip() # parser Version: x
            Version = Version.split(':')[1]
            #print "find Version:", Version
        if "Branch" in line:
            Branch = line.strip() # parser Branch: AWK
            Branch = Branch.split(':')[1]
            #print "find Branch:", Branch
        if "v" in line:
            #print "No field info"
            Version = line.strip()
            #print "Version: ", Version
        if line == '' :
            #print "last line"
            break
    #print Branch, Version
    return Branch + Version

def java_version(parser_name, parser_path):
    version_info={} #dictionary? parser as the key
    #print parser_name
#LTE PreCrossFeeder
#java -jar /opt/covmo/parser/crossfeeder/Pre_CrossFeeder_LTE.jar -v
    if parser_name == "Pre_CrossFeeder_LTE" : 
        parser_version = output_java_version(parser_path, "crossfeeder", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + parser_name + " | " + version_info[parser_name] + " |"

#LTE CrossFeeder
#java -jar /opt/covmo/parser/crossfeeder/CrossFeeder_LTE.jar -v
    if parser_name == "CrossFeeder_LTE" : 
        parser_version = output_java_version(parser_path, "crossfeeder", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + parser_name + " | " + version_info[parser_name] + " |"

#UMTS CrossFeeder
#java -jar /opt/covmo/parser/crossfeeder/SwapFeeder.jar -v
    if parser_name == "SwapFeeder" : 
        parser_version = output_java_version(parser_path, "crossfeeder", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + parser_name + " | " + version_info[parser_name] + " |"
#NBO
#found in VIVA
#java -jar /opt/covmo/parser/nbo/nbo.jar -v
    if parser_name == "nbo" : 
        parser_version = output_java_version(parser_path, "nbo", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + parser_name + " | " + version_info[parser_name] + " |"
#GSM NBO
#java -jar /opt/covmo/parser/nbo/nbo_gsm.jar -v
    if parser_name == "nbo_gsm" : 
        parser_version = output_java_version(parser_path, "nbo", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + parser_name + " | " + version_info[parser_name] + " |"

#UMTS NBO rank
#java -jar /opt/covmo/parser/nbo/nbo_rank.jar -v
    if parser_name == "nbo_rank" : 
        parser_version = output_java_version(parser_path, "nbo", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + parser_name + "UMTS" + " | " + version_info[parser_name] + " |"

#LTE NBO
#java -jar /opt/covmo/parser/nbo/nbo_lte.jar -v
    if parser_name == "nbo_lte" : 
        parser_version = output_java_version(parser_path, "nbo", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + parser_name + " | " + version_info[parser_name] + " |"
        
#interNbr
#java -jar /opt/covmo/parser/internbr/interNbr.jar -v
    if parser_name == "interNbr" : 
        parser_version = output_java_version(parser_path, "internbr", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + parser_name + " | " + version_info[parser_name] + " |"

#UMTS indoor
#java -jar /opt/covmo/parser/indoor/Position_Indoor_UMTS.jar.bkp -v
    if parser_name == "Position_Indoor_UMTS" : 
        parser_version = output_java_version(parser_path, "indoor", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + parser_name + " | " + version_info[parser_name] + " |"

#LTE indoor
#java -jar /opt/covmo/parser/indoor/Position_Indoor_LTE.jar -v
    if parser_name == "Position_Indoor_LTE" : 
        parser_version = output_java_version(parser_path, "indoor", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + parser_name + " | " + version_info[parser_name] + " |"
#SCO
#java -jar /opt/covmo/parser/sco/rfopt_all.jar -v
    if parser_name == "rfopt_all" : 
        parser_version = output_java_version(parser_path, "sco", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + "SCO" + " | " + parser_name + version_info[parser_name] + " |"
#SCO
#java -jar /opt/covmo/parser/sco/sco.jar -v
    if parser_name == "sco" : 
        parser_version = output_java_version(parser_path, "sco", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + "SCO" + " | " + parser_name + version_info[parser_name] + " |"

#Voronoi
#all: java -jar /opt/covmo/parser/voronoi/voronoi_all.jar -v
#TODO: check the old version which has voronoi by tech
    if parser_name == "voronoi" : 
        parser_version = output_java_version(parser_path, "voronoi", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + parser_name + " | " + version_info[parser_name] + " |"
#Voronoi_LTE
#java -jar /opt/covmo/parser/voronoi/voronoi_lte.jar -v
    if parser_name == "voronoi_lte" : 
        parser_version = output_java_version(parser_path, "voronoi_lte", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + parser_name + " | " + version_info[parser_name] + " |"
#IRAT
#java -jar /opt/covmo/parser/IRAT/IRAT.jar -v
    if parser_name == "" : 
        parser_version = output_java_version(parser_path, "", parser_name )
        version_info[parser_name] = merge_proc_output(parser_version)
        print "| " + parser_name + " | " + version_info[parser_name] + " |"
#Function testing
#java_version("SwapFeeder", Parser_path )
#java_version("Pre_CrossFeeder_LTE", Parser_path )
#java_version("CrossFeeder_LTE", Parser_path )
#java_version("nbo_gsm", Parser_path )
#java_version("nbo_rank", Parser_path )
#java_version("nbo_lte", Parser_path )
#java_version("Position_Indoor_UMTS", Parser_path )
#java_version("Position_Indoor_LTE", Parser_path )
#java_version("rfopt_all", Parser_path )
#java_version("voronoi_all", Parser_path )
#java_version("interNbr", Parser_path )

####################################################################################
#4. DataBase
####################################################################################
def Database_version(DB_version,DB_address,port):
    version_info = {}
#SP version
#mysql -ucovmo -pcovmo123 -h127.0.0.1 -P3307 -e "select * from gt_gw_main.sp_version"
    if DB_version == 'SP_version':
        sp_version = subprocess.Popen(['mysql','-ucovmo','-pcovmo123','-h', DB_address,'-P', port,'-e','select * from gt_gw_main.sp_version'],stdout=subprocess.PIPE)
        version_output = sp_version.stdout.readlines()
        version_info[DB_version] = version_output[1].split('\t')[0] + "\n"
        version_info[DB_version] = version_info[DB_version] + "LTE:" + " ".join(version_output[1].split('\t')[1:4]) + "\n"
        version_info[DB_version] = version_info[DB_version] + "UMTS:" + " ".join(version_output[1].split('\t')[5:8]) + "\n"
        version_info[DB_version] = version_info[DB_version] + "GSM:" + " ".join(version_output[1].split('\t')[9:12])
        print "| " + DB_version + " | " + version_info[DB_version] + " |"
#Nationwide
#pssh_all sh /opt/covmo/all_sock.sh ' SELECT * FROM `gt_global_statistic`.`sp_version_nw`;'
#NWSP2|N20151118|F20151007|L20151202|U20151214|G20151202
    if DB_version == 'Nationwide':
        sp_version = subprocess.Popen(['mysql','-ucovmo','-pcovmo123','-h', DB_address,'-P', port,'-e','select * from gt_global_statistic.sp_version_nw'],stdout=subprocess.PIPE)
        version_output = sp_version.stdout.readlines()
        print "| " + DB_version + " | " + version_info[DB_version] + " |"

####################################################################################
#5. File
####################################################################################
def file_version(module, module_version_path):
    version_info={}
#NT Parser
#cat /opt/covmo/parser/nt/version.py
    if module == "NT Parser":
        with open(module_version_path, 'r') as file:
            for line in file.readlines():
                line = line.strip()
                if "VER" in line:
                    Branch = line.split('=')[1].split(' ')[0]
                    Version = line.split('=')[1].split(' ')[1]
                else:
                    print "no output"
        file.closed
        version_info[module] = Branch + " Version:" + Version
        print "| %s | %s |" % (module, version_info[module])
#AWK_georpt
#cat /opt/covmo/parser/georpt/bin/sys.version
    if module == "AWK georpt":
        with open(module_version_path, 'r') as file:
            for line in file.readlines():
                line = line.strip()
                if "version" in line:
                    Version = line.split('=')[1]
                else:
                    print "no output"
        file.closed
        version_info[module] = "AWK " + Version
        print "| %s | %s |" % (module, version_info[module])

#gtgw version schema configuration
#/etc/gtgw/sys.config
#umts:
#lte:

####################################################################################
#TODO: clarify the version info for below
#nt_parser
#Project.config
####################################################################################

#Program main body
print ("Start version check on %s" % (datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S'))) 
print "| Module | Version Build_date Build_number |"

Web_page_version("CovMo_war",CovMo_war)
Web_page_version("Data_Processing",Data_Processing)
#file_version("NT Parser","/opt/covmo/parser/nt/version.py")
#Database_version("SP_version","127.0.0.1","3307")
#Database_version("Nationwide","127.0.0.1","3307")
#program_version("GTGW")
java_version("Pre_CrossFeeder_LTE", Parser_path )
java_version("nbo_lte", Parser_path )
#position_version("LTE", "/opt/covmo/parser/")
java_version("Position_Indoor_LTE", Parser_path )
java_version("rfopt_all", Parser_path )
java_version("nbo_rank", Parser_path )
#position_version("UMTS", "/opt/covmo/parser/")
java_version("Position_Indoor_UMTS", Parser_path )
java_version("voronoi", Parser_path )
#java_version("voronoi_lte", Parser_path )
java_version("SwapFeeder", Parser_path )
#file_version("AWK georpt","/opt/covmo/parser/georpt/bin/sys.version")

print ("Version check completed at %s" % (datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S'))) 

#if __name__ == "__main__":
#    import sys
#    Version_check(int(sys.argv[1]))
