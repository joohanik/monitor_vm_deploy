monitor_vm_deploy
==========
This tool is the real-time database monitor that deployment status in CCR(Core Cyber Range) virtual machine management system.


## How to use
  [root@localhost lab]# python monitor_vm_deploy.py 
  [+] VM deployment monitoring tool v0.1 Beta
  [+] Contact to hijoo@coresec.co.kr
  [+] Copyright (C) 2019 Coresecurity


  Usage : monitor_vm_deploy.py [OPTIONS] [FILE or DIRECTORY]
    -d,  --deplyed
    print deployed blueprints statistics
    -u,  --username USERNAME
    print deployed blueprints who specified users
  [root@localhost lab]# 


## Example
  [root@localhost lab]# python monitor_vm_deploy.py -u "teacher"
  
  [+] VM deployment monitoring tool v0.1 Beta
  [+] Contact to hijoo@coresec.co.kr
  [+] Copyright (C) 2019 Korean Army Signal School


  [2019-1-15 17:12:44] [INFO] 현재 가상자원 배포진행 상황은 다음과 같습니다.
  [*] 'teacher' 사용자에게 'CCR-Linux_System_Fundamental' 세트가 배포되고 있습니다.


  [2019-1-15 17:12:44] [INFO] 현재 까지의 계정별 가상자원 배포 상황 다음과 같습니다.
  사용자 계정 : 'teacher'
  [*] 'CCR-Linux_System_Fundamental'
  세트들을 배포 받았습니다.
  
  
## Contacts
This tool was written by joohanik(hijoo@coresec.co.kr). Feel free to send me an E-mail if you have any questions.
