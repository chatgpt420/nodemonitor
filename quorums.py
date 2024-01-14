import os
import requests as r
from bs4 import BeautifulSoup
from objects import Quorums
from time import sleep
from functions import log


try:
    node = []
    for root,dirs,files in os.walk("/home", topdown=False):
        if 'debug.log' in files:
            tag = [x for x in root.split('/') if x not in ['home','.dashcore','.','']]
            node.append([tag[0],root+'/debug.log'])

    for x in node:
        print(x)

    while True:

        url = 'https://chainz.cryptoid.info/dash/'
        data = r.get(url).text
        soup = BeautifulSoup(data,'html.parser')
        blockHeight = int(soup.find(id="up-to-block")['block'])
        
        llmq_60_75 = []
        llmq_100_67 = []
        llmq_400_60 = []
        
        for id in node:

            name = id[0]
            logPath = id[1]
            
            stats = Quorums(logPath,blockHeight)

            if stats.llmq_60_75_status == True:
                llmq_60_75.append(name)

            if stats.llmq_100_67_status == True:
                llmq_100_67.append(name)
            
            if stats.llmq_400_60_status == True:
                llmq_400_60.append(name)
            
            
        print(f"llmq_60_75  -  {llmq_60_75}")
        print(f"llmq_100_67  -  {llmq_100_67}")
        print(f"llmq_400_60  -  {llmq_400_60}")
        print('---')
        
        

        sleep(20)

except Exception as E:
    log('quorums',E)
except KeyboardInterrupt:
    print("Bye!")