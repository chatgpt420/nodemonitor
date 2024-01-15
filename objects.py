import psutil
import time
from functions import email
import os

cpuList = []

class Sys:

        postRebootAlerts = 1
        alertInterval = 600

        cpu10minAlarm = False
        memAlarm = False
        diskAlarm = False

        def __init__(self, rebootAlerts):
                
                self.rebootAlerts = rebootAlerts
                self.cpu = psutil.cpu_percent()
                self.vm = psutil.virtual_memory().percent
                self.vm_used = psutil.virtual_memory().used
                self.vm_total = psutil.virtual_memory().total
                self.disk = psutil.disk_usage('/').percent
                self.swap = psutil.swap_memory().percent
                self.swap_used = psutil.swap_memory().used
                self.swap_total = psutil.swap_memory().total
                self.mem = round((( self.swap_used + self.vm_used) / (self.vm_total + self.swap_total)) * 100, 2)
                self.uptime = time.time() - psutil.boot_time()


                cpuList.append(self.cpu)
                self.cpu10min = round(sum(cpuList)/len(cpuList),2)
                while len(cpuList) > 60:
                        cpuList.pop(0)
                
                if self.uptime > (Sys.postRebootAlerts * Sys.alertInterval) and Sys.postRebootAlerts < rebootAlerts + 1 and self.uptime < (rebootAlerts*1.1) * Sys.alertInterval:
                        email(f'{os.popen("hostname").read()} recent reboot alert {Sys.postRebootAlerts} of {rebootAlerts}',
f"""
CPU 10min Average: {self.cpu10min}%
Disk Used: {self.disk}%
Swap Memory: {self.swap}%
Virtual Memory: {self.vm}%
Combined Memory Used: {round(self.mem,2)}%
""")
                        
                        Sys.postRebootAlerts += 1

        def cpuAlarmToggle(self):
                if Sys.cpu10minAlarm == False:
                        Sys.cpu10minAlarm = True
                elif Sys.cpu10minAlarm == True:
                        Sys.cpu10minAlarm = False
                        
        def memAlarmToggle(self):
                if Sys.memAlarm == False:
                        Sys.memAlarm = True
                elif Sys.memAlarm == True:
                        Sys.memAlarm = False    

        def diskAlarmToggle(self):
                if Sys.diskAlarm == False:
                        Sys.diskAlarm = True
                elif Sys.diskAlarm == True:
                        Sys.diskAlarm = False







class Quorums:
        def __init__(self,logPath,blockHeight):
                

                self.blockHeight = blockHeight
                self.logPath = logPath


                with open(logPath, "r") as l:
                        file = l.read().splitlines()



                results = []
                for line in file:
                        if 'quorum initialization OK for llmq_60_75' in line:
                                results.append(line)

                # Splitting log string into list, then grabbing elements of
                # the list and splitting off remaining unecessary text
                if len(results) > 0:
                        manip = results[-1].split('[')
                        endNum = int(manip[2].split(']')[0])
                        activeHeight = int(manip[1].split(']')[0])
                
                        if activeHeight < blockHeight and endNum == 31:
                                Quorums.llmq_60_75_status = False
                        elif activeHeight == self.blockHeight and endNum != 31:
                                Quorums.llmq_60_75_status = True
                else:
                        Quorums.llmq_60_75_status = False                        


                results = []
                for line in file:
                        if  'quorum initialization OK for llmq_100_67' in line:
                                results.append(line)
                # Splitting log string into list, then grabbing elements of
                # the list and splitting off remaining unecessary text
                if len(results) > 0:
                        manip = results[-1].split('[')
                        endNum = int(manip[2].split(']')[0])
                        activeHeight = int(manip[1].split(']')[0])

                        if activeHeight < self.blockHeight:
                                Quorums.llmq_100_67_status = False
                        elif activeHeight == self.blockHeight:
                                Quorums.llmq_100_67_status = True
                else:
                        Quorums.llmq_100_67_status = False
                


                results = []
                for line in file:
                        if  'quorum initialization OK for llmq_400_60' in line:
                                results.append(line)
                # Splitting log string into list, then grabbing elements of
                # the list and splitting off remaining unecessary text
                if len(results) > 0:
                        manip = results[-1].split('[')
                        endNum = int(manip[2].split(']')[0])
                        activeHeight = int(manip[1].split(']')[0])

                        if activeHeight < self.blockHeight:
                                Quorums.llmq_400_60_status = False
                        elif activeHeight >= self.blockHeight:
                                Quorums.llmq_400_60_status = True
                else:
                        Quorums.llmq_400_60_status = False