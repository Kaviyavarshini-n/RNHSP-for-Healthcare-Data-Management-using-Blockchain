import os
import sys
import subprocess

class NetAnim_Initiator:
    def Initiate(self):
        login_name = os.getlogin()
        if login_name is not None:
            print("Logged in user:", login_name)
        else:
            print("Failed to get login name.")
            return
        netanim_directory = "/home/" + login_name + "/ns-allinone-3.35/netanim-3.108/"
        netanim_command = netanim_directory + "NetAnim"
        netanim_process = subprocess.Popen(netanim_command, shell=True)
        netanim_process.communicate()
        sys.exit("NetAnim process has terminated.")
netanim_initiator = NetAnim_Initiator()
netanim_initiator.Initiate()
