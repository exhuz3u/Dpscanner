from __future__ import print_function
from fake_useragent import UserAgent
from bs4 import  BeautifulSoup
import sys
import ctypes
import threadpool
import requests
import argparse
import os
os.system("color")

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
FOREGROUND_GREEN = 0x0a
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
url=""
delay="1"
thread="10"
current_progress=0
totle_progress=0

print("")
print(
'''\n\033[0;36;40m
 ____       ____                                  
|  _ \ _ __/ ___|  ___ __ _ _ __  _ __   ___ _ __ 
| | | | '_ \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
| |_| | |_) |__) | (_| (_| | | | | | | |  __/ |   
|____/| .__/____/ \___\__,_|_| |_|_| |_|\___|_|   
      |_|  
                                          
   A domain port scanner       Version: 1.0.0
\033[0m''')

def is_valid_domain(domain):
    check=True
    correct_str="1234567890.—qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM"
    domain_list=list(domain)
    for s in domain_list:
        if correct_str.find(s) == -1 :
            check=False
    if check==True:
        return True
    else:
        return False
            


def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool
 
 
def show(current_progress):
    percent=current_progress/totle_progress
    res = int(20*percent)*'■'
    pes=  (20-int(20*percent))*'□'
    sys.stdout.write('\r Scan progress: [%s%s] %d%%'%(res,pes,int(100 * percent))+'\r')
    


def req(port):
    global current_progress
    try:
        if int(port) == 443:
            complete_url="https://{}".format(url)
        else:
            complete_url="http://{}:{}".format(url,port)
        headers = {"User-Agent": str(UserAgent().random)}
        result=requests.get(complete_url,headers=headers,timeout=int(delay))
        pagelength=len(result.content)
        code=result.status_code
        try:
            soup = BeautifulSoup(result.text,'html.parser')
            pagetitle = soup.find("title")
        except:
            pagetitle="Error getting title"
        sys.stdout.write(" Port:%-5s "%port+"  |  Status_code:%-3s "%code+"  |  Length:%-8s "%pagelength+"  |  Title:%s"%pagetitle.string+"\n")
        current_progress+=1
        show(current_progress)
    except:
        current_progress+=1
        show(current_progress)
        pass

    

def threads_pool(ports):
    global totle_progress
    port_list=[]
    if "-" in ports and ports.split("-")[0].isdigit() and ports.split("-")[1].isdigit():
        start_port=ports.split("-")[0]
        end_port=ports.split("-")[1]
        for i in range(int(start_port),int(end_port)+1):
            port_list.append(i)
    elif "," in ports:
        port_list=ports.split(",")
        for i in port_list:
            if i.isdigit():
                pass
            else:
                print("\n\033[0;31;40m   The format of the -p parameter is incorrect\033[0m")
                return
            
    elif ports.isdigit():
        port_list.append(ports)
    else:
        print("\n\033[0;31;40m   The format of the -p parameter is incorrect\033[0m")
        return
    totle_progress=len(port_list)
    set_cmd_text_color(FOREGROUND_GREEN)
    pool = threadpool.ThreadPool(int(thread))
    requests = threadpool.makeRequests(req, port_list)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    


def main():
    global url,delay,thread
    parser = argparse.ArgumentParser(usage="-h | -u www.baidu.com -p 80,443,9999(or 50-80 stands for scanning 50 to 80 ports) -d 1 ")
    parser.add_argument('-u',help='Set the request domain for the scanner     | eg: -u www.baidu.com')
    parser.add_argument('-p',help='Set the request port the scanner           | eg: -p 20,80,443 or -p 50-80')
    parser.add_argument('-d',help='Set the request delay for the scanner      | eg: -d 1 (integer) or -d 1.5 (decimal)',default="1")
    parser.add_argument('-t',help='Set the request thread for the scanner     | eg: -t 10',default="10")
    args = parser.parse_args()
    if args.u is None or args.p is None:
        print("\n\033[0;31;40m   -u and -p must be given at the same time\033[0m")
        return
    if is_valid_domain(args.u):
        pass
    else:
        print("\n\033[0;31;40m   The domain name entered is invalid\033[0m")
        return
    if args.t.isdigit():
        pass
    else:
        print("\n\033[0;31;40m   -t the specified must be a integer type\033[0m")
        return
    if args.d.isdigit():
        url=args.u
        delay=args.d
        thread=args.t
        threads_pool(args.p)
    elif args.d.count(".")==1 and not args.d.startswith(".") and not args.d.endswith("."):
        if args.d.split(".")[0].isdigit() and args.d.split(".")[1].isdigit():
            url=args.u
            delay=args.d
            thread=args.t
            threads_pool(args.p)
        else:
            print("\n\033[0;31;40m   -d the specified must be a numeric type\033[0m")
    else:
        print("\n\033[0;31;40m   -d the specified must be a numeric type\033[0m")



if __name__=="__main__":
    main()
