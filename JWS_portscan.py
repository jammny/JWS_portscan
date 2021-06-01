'''
    JWS-portscan是JWS系统的端口扫描模块。
                                        ——by-jammny
'''
from socket import AF_INET, SOCK_STREAM, socket
from queue import Queue
from time import time
from threading import Thread
from sys import stdout
from colorama import init, Fore
import argparse, os


class PortScan:
    def __init__(self, port, host, thread):
        self.port = port
        self.host = host
        self.thread = int(thread)
        self.result = []

    def add_queue(self):
        queue = Queue()
        put = queue.put
        port = self.port
        split = port.split
        if "," in port and "-" in port:
            port_list = split(',')
            length = len(port_list)
            for i in range(0, length):
                split = port_list[i].split
                if "-" in port_list[i]:
                    p_list = split('-')
                    start = int(p_list[0])
                    end = int(p_list[1]) + 1
                    for l in range(start, end):
                        put(l)
                else:
                    put(int(port_list[i]))
        elif "-" in port:
            port_list = split('-')
            start = int(port_list[0])
            end = int(port_list[1]) + 1
            for i in range(start, end):
                put(i)
        elif "," in port:
            port_list = split(',')
            length = len(port_list)
            for i in range(0, length):
                put(int(port_list[i]))
        else:
            print(int(port))
            put(int(port))
        return queue

    def tcp_scan(self, queue):
        while not queue.empty():
            try:
                port = queue.get()
                conn = socket(AF_INET, SOCK_STREAM)
                conn.settimeout(1)
                conn.connect((self.host, port))
                stdout.write(Fore.GREEN + "[+] {}/TCP OPEN\n".format(port))
                conn.close()
                self.result.append("{}:{}\n".format(self.host, port))
            except:
                pass

    def save_result(self, ):
        with open("result/{}.txt".format(self.host), mode='w', encoding='utf-8') as f:
            for result in self.result:
                f.write(result)

    def run(self):
        queue = self.add_queue()
        thread_pool = [Thread(target=self.tcp_scan, args=[queue]) for _ in range(self.thread)]
        print(Fore.MAGENTA + '\n获取目标:{},线程数:{}'.format(self.host, self.thread))
        s_time = time()
        for i in range(self.thread):
            thread_pool[i].start()
        for i in range(self.thread):
            thread_pool[i].join()
        e_time = time()
        print(Fore.MAGENTA + "[+] 总计开放端口：{}".format(len(self.result)))
        print(Fore.MAGENTA + '[+] 扫描结束！总共耗时{}'.format((e_time - s_time)))
        if os.path.exists("result"):
            pass
        else:
            os.mkdir("result")
        self.save_result()
        print(Fore.MAGENTA + "[+] 结果保存路径：./result/{}.txt".format(self.host))


if __name__ == "__main__":
    init(autoreset=True)  # 初始化，并且设置颜色设置自动恢复
    print(Fore.MAGENTA + r'''
       ___          _______       _____           _                       
      | \ \        / / ____|     |  __ \         | |                      
      | |\ \  /\  / / (___ ______| |__) |__  _ __| |_ ___  ___ __ _ _ __  
  _   | | \ \/  \/ / \___ \______|  ___/ _ \| '__| __/ __|/ __/ _` | '_ \ 
 | |__| |  \  /\  /  ____) |     | |  | (_) | |  | |_\__ \ (_| (_| | | | |
  \____/    \/  \/  |_____/      |_|   \___/|_|   \__|___/\___\__,_|_| |_|

                                                                            ——by jammny.2021.5.31

    用法：python3 JWS_portscan.py -h
    ''')
    parser = argparse.ArgumentParser(description='用法：python3 JWS_portscan.py <host> <port>')
    parser.add_argument('--host', type=str, help="--host=127.0.0.1")
    parser.add_argument('--file', type=str, help="--file=targets.txt")
    parser.add_argument('--port', type=str, default="1-65535", help="--port=1-65535")
    parser.add_argument('--thread', type=str, default="3000", help="默认线程3000，--thread=3000")

    args = parser.parse_args()
    if args.file:
        with open(args.file, mode="r", encoding='utf-8') as f:
            c_list = f.readlines()
        for ip in c_list:
            port = args.port
            host = ip.strip("\n")
            thread = args.thread
            scan = PortScan(port, host, thread)
            scan.run()
    elif args.host:
        port = args.port
        host = args.host
        thread = args.thread
        scan = PortScan(port, host, thread)
        scan.run()
    else:
        print(Fore.RED + "请输入正确参数！")
