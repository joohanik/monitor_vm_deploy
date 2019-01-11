# -*- coding: utf-8 -*- 

# Copyright (C) 2019 Korean Army Signal School
# Author : Han Ik Joo (hijoo@coresec.co.kr)

import sys
import MySQLdb         
from datetime import datetime
from array import *
from threading import Event
import signal
import os

exit = Event()


def main(argv):   
    clear = lambda: os.system('clear')


 
    while not exit.is_set():
        ###############################################################################################
        # connect to "moodle" database
        ###############################################################################################
        hDatabase = MySQLdb.connect("192.168.11.243","moodle","core1234","moodle" )
        cursor = hDatabase.cursor()

        ###############################################################################################
        # Collect "mdl_user" table contents    
        ###############################################################################################
        cursor.execute("SELECT * FROM mdl_user")
        results_mdl_user =  cursor.fetchall()

        dict_userid_username = dict()    
        dict_userid_username = Func_userid_username_mapping(results_mdl_user)

        ###############################################################################################
        # Collect "vstp_vapp" table contents    
        ###############################################################################################
        cursor.execute("SELECT * FROM vstp_vapp")
        results_vstp_vapp =  cursor.fetchall()


        ###############################################################################################
        # Collect "vstp_blueprint" table contents
        ###############################################################################################
        cursor.execute("SELECT * FROM vstp_blueprint")
        results_vstp_blueprint = cursor.fetchall()


        dict_blueprintvmsetid_blueprintvmsetname = dict()
        dict_blueprintvmsetid_blueprintvmsetname = Func_blueprintsetid_blueprintsetname_mapping(results_vstp_blueprint)


        ###############################################################################################
        # Collect "vstp_vapp_vsystem" table contents.
        # vstp_vapp_vsystem.req_cmd column describes the status of VM. Whether "복제 요청" or "-" or "??"
        ###############################################################################################
        cursor.execute("SELECT * FROM vstp_vapp_vsystem")
        results_vstp_vapp_vsystem = cursor.fetchall()
    
        clear()
        Func_banner()
        Func_display_users_name_in_queue(dict_userid_username, results_vstp_vapp_vsystem, dict_blueprintvmsetid_blueprintvmsetname)
        Func_display_users_name_deploy_complete(dict_userid_username, results_vstp_vapp_vsystem, dict_blueprintvmsetid_blueprintvmsetname)
        Func_display_blueprint_name_count_deploy_complete(results_vstp_vapp, dict_blueprintvmsetid_blueprintvmsetname)
        exit.wait(5)
        hDatabase.close()






def Func_userid_username_mapping(results_mdl_user):
    dict_userid_username = dict()
    for rows_mdl_user in results_mdl_user:
        dict_userid_username[rows_mdl_user[0]] = rows_mdl_user[7]
    return dict_userid_username


def Func_blueprintsetid_blueprintsetname_mapping(results_vstp_blueprint):
    dict_blueprintsetid_blueprintsetname = dict()
    for rows_vstp_blueprint in results_vstp_blueprint:
        dict_blueprintsetid_blueprintsetname[rows_vstp_blueprint[0]] = rows_vstp_blueprint[1]
    return dict_blueprintsetid_blueprintsetname


def Func_display_users_name_in_queue(dict_userid_username, results_vstp_vapp_vsystem, dict_blueprintvmsetid_blueprintvmsetname):
    dict_users_vm_name_in_queue = dict()
    for rows_vstp_vapp_vsystem in results_vstp_vapp_vsystem:
        if(rows_vstp_vapp_vsystem[11] == "복제 요청" or rows_vstp_vapp_vsystem[11] == "-"):
            dict_users_vm_name_in_queue[dict_userid_username[rows_vstp_vapp_vsystem[7]]] = dict_blueprintvmsetid_blueprintvmsetname[rows_vstp_vapp_vsystem[3]]  

    if len(dict_users_vm_name_in_queue) != 0:
        print "[%s-%s-%s %s:%s:%s] [INFO] 현재 가상자원 배포진행 상황은 다음과 같습니다." % (datetime.now().year, 
                                                                                    datetime.now().month, 
                                                                                    datetime.now().day, 
                                                                                    datetime.now().hour, 
                                                                                    datetime.now().minute, 
                                                                                    datetime.now().second)
        for username,blueprintvmsetname in dict_users_vm_name_in_queue.items():
            print CGRE + "[*] " + CRED +  "'%s\'" % username + CEND + CGRE + " 사용자에게 \'%s\' 세트가 배포되고 있습니다." % blueprintvmsetname + CEND
    else:
        print "[%s-%s-%s %s:%s:%s] [INFO] 현재 진행되고 있는 가상자원 배포 작업이 없습니다." % (datetime.now().year, 
                                                                                    datetime.now().month, 
                                                                                    datetime.now().day, 
                                                                                    datetime.now().hour, 
                                                                                    datetime.now().minute, 
                                                                                    datetime.now().second)

def Func_display_users_name_deploy_complete(dict_userid_username, results_vstp_vapp_vsystem, dict_blueprintvmsetid_blueprintvmsetname):
    ###############################################################################################
    # 배포된 가상머신이 속한 가상머신 세트 이름과 배포된 사용자 이름을 추출함 
    # vstp_vapp_vsystem.req_cmd의 값이 배포 대기중('-')과 배포 진행중('복제 요청')이 아닌 복제 왼료된 레코드만 추출
    ###############################################################################################
    list_blueprintvmset_user_name = []
    for rows_vstp_vapp_vsystem in results_vstp_vapp_vsystem:
        if(rows_vstp_vapp_vsystem[11] != "복제 요청" and rows_vstp_vapp_vsystem[11] != "-"):
            list_blueprintvmset_user_name.append([dict_blueprintvmsetid_blueprintvmsetname[rows_vstp_vapp_vsystem[3]],dict_userid_username[rows_vstp_vapp_vsystem[7]]])

    if len(list_blueprintvmset_user_name) != 0:    
        ### 위에서 추출한 레코드가 중복되므로 중복된 요소를 제거함    
        list_blueprintvmset_user_name = list_uniq(list_blueprintvmset_user_name)


        ### 사용자 이름만 별도로 추출함. 
        userlist = []
        for blueprintvmsetname, username in list_blueprintvmset_user_name:
            userlist.append(username)
        userlist = list(set(userlist))


        ###############################################################################################
        # 사용자별로 배포된 가상머신 세트명을 출력함
        ############################################################################################### 
        print "\n\n[%s-%s-%s %s:%s:%s] [INFO] 현재 까지의 계정별 가상자원 배포 상황 다음과 같습니다." % (datetime.now().year, 
                                                                                            datetime.now().month, 
                                                                                            datetime.now().day, 
                                                                                            datetime.now().hour, 
                                                                                            datetime.now().minute, 
                                                                                            datetime.now().second)
        for i in range(len(userlist)):
            print CGRE + "사용자 계정 : " + CRED + "\'%s\'" % userlist[i] + CEND
            for blueprintvmsetname, username in list_blueprintvmset_user_name:
                if(username == userlist[i]):
                    print CGRE + "[*] \'%s\'" % blueprintvmsetname + CEND
            print "세트들을 배포 받았습니다.\n"

    else:
            print "\n\n[%s-%s-%s %s:%s:%s] [INFO] 배포된 가상자원 세트가 없습니다." % (datetime.now().year, 
                                                                                datetime.now().month, 
                                                                                datetime.now().day, 
                                                                                datetime.now().hour, 
                                                                                datetime.now().minute, 
                                                                                datetime.now().second)







def Func_display_blueprint_name_count_deploy_complete(results_vstp_vapp, dict_blueprintvmsetid_blueprintvmsetname):
    ###############################################################################################
    # 배포된 블루프린트 세트의 개수 정보를 가져옵니다. 
    # vstp_vapp.vstp_blueprint_mor_id 필드에 있는 플루프린트 ID의 중복 등장빈도를 계산합니다.
    ###############################################################################################


    if(len(results_vstp_vapp) != 0):
        list_blueprintvmset_id = []
        for rows_vstp_vapp in results_vstp_vapp:
            list_blueprintvmset_id.append(rows_vstp_vapp[1])

        list_blueprintvmset_id_uniq = list(set(list_blueprintvmset_id))

        print "\n[%s-%s-%s %s:%s:%s] [INFO] 현재 까지의 가상머신 세트별 배포완료 회수는 다음과 같습니다." % (datetime.now().year, 
                                                                                                datetime.now().month, 
                                                                                                datetime.now().day, 
                                                                                                datetime.now().hour, 
                                                                                                datetime.now().minute, 
                                                                                                datetime.now().second)
        for i in range(len(list_blueprintvmset_id_uniq)):
            print "[*] 현재" + CGRE + "\'%s(%s)\'" % (dict_blueprintvmsetid_blueprintvmsetname[list_blueprintvmset_id_uniq[i]], 
                                                    list_blueprintvmset_id_uniq[i]) + CEND + "세트는 " + CRED + "%s개" % list_blueprintvmset_id.count(list_blueprintvmset_id_uniq[i]) + CEND + " 배포 되었습니다."

        print "[*] 현재까지 배포된 가상머신 세트의 총 개수는 " + CRED + "%s개" % len(results_vstp_vapp) + CEND + "입니다." 



def list_uniq(aList):
    return [x for i, x in enumerate(aList) if x not in aList[:i]]


def Func_banner():
    global CYEL
    CYEL = "\033[93m"
    global CGRE
    CGRE = "\033[92m"
    global CEND
    CEND = "\033[0m"
    global CRED
    CRED = "\033[91m"
    print CYEL + "[+] VM deployment monitoring tool v0.1 Beta" + CEND
    print CYEL + "[+] Contact to hijoo@coresec.co.kr" + CEND
    print CYEL + "[+] Copyright (C) 2019 Korean Army Signal School\n\n" + CEND


def quit(signo, _frame):
    print("Interrupted by %d.\n\n[+] Shuting down." % signo)
    exit.set()

# ====================================================================================================    
# __Main__ Code 
# ====================================================================================================


for sig in ('TERM', 'HUP', 'INT'):
    signal.signal(getattr(signal, 'SIG'+sig), quit);

if __name__ == "__main__":                 # __name__ is Global Variable
    main(sys.argv[1:])                     # Chop first Argument off and pass rest of the list

