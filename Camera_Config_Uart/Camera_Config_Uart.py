import argparse
import time
import re
from pynq import MMIO

uart1=MMIO(0x43c00000,0x10000)

def uart_write(uid,wr_addr,data):
   if(uid==1):
      uart1.write(wr_addr,data)
      print("addr =",hex(wr_addr)," data =",hex(data))
   if(uid==2):
      uart2.write(wr_addr,data)
      print("addr =",hex(wr_addr)," data =",hex(data))

def uart_read(uid,rd_addr):
   if(uid==1):
       for i in range (20):
         d=uart1.read(rd_addr)
         print("output data =", hex(d))
         time.sleep(0.3)
   if(uid==2):
      for i in range (20):
         d=uart2.read(rd_addr)
         print("output data =", hex(d))
         time.sleep(0.3)

def extract_addr_value(addr_value_str):
     li = addr_value_str.strip()
     var =li.split("(")[0]
     assign=li.split("(")[1]
     var1 = var.split(".")[0]
     li = assign.strip()
     var = li.split(")")[0]
     val = var.strip()
     val1 = val.split(",")[0]
     val2 = val.split(",")[1]
     addr = (int(val1, 16))
     value = (int(val2, 16))
     return (addr, value)

def run_uart(cid,serial_cmd):
    ascii_words = open("Source/"+serial_cmd,'r')
    lines = ascii_words.readlines()
    print("FCR - enable the fifo")
    uart_write(cid,0x1008,0xf)
    print("IER - enable the empty & data available interrupts")
    uart_write(cid,0x1004,0x3)
    print("------writing data to THR-------")
    for line in lines:
        addr,value = extract_addr_value(line)
        uart_write(cid,addr,value)
    print("------writing CR to THR-------")
    uart_write(cid,0x1000,0xd)
    print("-----reading RBR-------")
    uart_read(cid,0x1000)

parser = argparse.ArgumentParser(description='''Enter read/r or write/w
                                                To read choose from  ---> getsot/getsvm/getssf/getclm
                                                To write choose from ---> sot/svm/ssf/clm and give value of the parameter 
                                              ''')
parser.add_argument('-O','--option',type=str,help='read or write',required=True)
parser.add_argument('-R','--read',type=str,help='read parameter')
parser.add_argument('-W','--write',type=str,help='write parameter')
parser.add_argument('-V','--value',type=str,help='value of the parameter')

args = parser.parse_args()
while True:
    if args.option == "r" or args.option == "read":
        if args.read == "getsot":
            run_uart(1, "getsot")
            break
        elif args.read == "getsvm":
            run_uart(1, "getsvm")
            break
        elif args.read == "getssf":
            run_uart(1, "getssf")
            break
        elif args.read == "getclm":
            run_uart(1, "getclm")
            break
        else :
            print("Please Try again with correct option")
            break
    elif args.option == "w" or  args.option == "write":
        if  args.write == "setsot40":
            print(int(re.search(r'\d+', args.write).group()))
                run_uart(1, "sot40")
                break
            elif args.value == str(60):
                run_uart(1, "sot60")
                break
            elif args.value == str(80):
                run_uart(1, "sot80")
                break
            else :
                print("Please Try again with correct option")
                break
        elif args.write == "clm":
            if args.value == "medium":
                run_uart(1, "clm14") 
                break
            elif args.value == "base":
                run_uart(1, "clm5")
                break
            else :
                print("Please Try again with correct option")
                break
        elif args.write == "ssf":
            if args.value == str(3000):
                run_uart(1, "ssf3000")
                break
            if args.value == str(6000):
                run_uart(1, "ssf6000")
                break
            if args.value == str(7000):
                run_uart(1, "ssf7000")
                break
            elif args.value == str(10000):
                run_uart(1, "ssf10000")
                break
            elif args.value == str(17500):
                run_uart(1, "ssf17500")
                break
            else :
                print("Please Try again with correct option")
                break
        elif args.write == "svm":
            if args.value == "aa5500":
                run_uart(1, "svm1") 
                break
            elif args.value == "aa55":
                run_uart(1, "svm4")
                break
            elif args.value == "00ff":
                run_uart(1, "svm5")  
                break
            else :
                print("Please Try again with correct option")
                break
