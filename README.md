# JWS_portscan
基于多线程快速端口扫描脚本，支持目标批量导入、结果导出。如果扫描公网资产，为了提升扫描的精准性，建议放到服务器运行。

### 用法
依赖安装：pip3 install -r requriement.txt

脚本运行：
python3 JWS_portscan.py --host=127.0.0.1                          (默认情况下扫描常见开放web端口)
python3 JWS_portscan.py --host=127.0.0.1 --port=1-65535           (全端口扫描)
python3 JWS_portscan.py --file=targets.txt --port=80,8000-8080    (从文件中导入目标，进行扫描)  

更多参数：python3 JWS_portscan.py --help

![截图](https://github.com/jammny/JWS_portscan/blob/main/pic.jpg)
