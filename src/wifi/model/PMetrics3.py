import matplotlib.pyplot as plt
import numpy as np
import os
import mplcyberpunk
from qbstyles import mpl_style

plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.family'] = 'Gurajada'
plt.rcParams['font.size'] = 16 

def PerformanceMetrics():
    def read_values(filename):
        values = []
        with open(filename, 'r') as file:
            for line in file:
                values.append(float(line.strip()))
        return values
        
    def Data_Storage_Efficiency():
        font = {'family': 'Gurajada', 'color': 'black', 'size': 18, 'weight':'bold'}
        f2 = "ACT.txt"
        a_c_t = read_values(f2)
        indices = range(1, len(a_c_t) + 1)
        plt.style.use('ggplot')
        plt.rcParams['font.weight'] = 'bold'
        plt.rcParams['font.family'] = 'Gurajada'
        plt.rcParams['font.size'] = 14
        plt.bar(indices, a_c_t,  color='#673AB7', edgecolor='#32CD32', linewidth=2, label= 'Scenario -3 (Viewstamped  Replication)')
        plt.title(' Number of Transactions vs Data Storage Efficiency (MB/block)', fontdict=font)
        plt.xlabel('Number of Transactions', fontdict=font)
        plt.ylabel('Data Storage Efficiency (MB/block)', fontdict=font)
        print("\n========================================\n  2. Data Storage Efficiency Graph\n========================================\n")
        plt.legend()
        plt.grid(True)
        plt.show()
        os.remove(f2)
    
    def Latency():
        font = {'family': 'Gurajada', 'color': 'black', 'size': 18, 'weight':'bold'} 
        f3 = "CR.txt"
        c_r = read_values(f3)
        indices = range(1, len(c_r) + 1)
        plt.style.use('ggplot')
        plt.rcParams['font.weight'] = 'bold'
        plt.rcParams['font.family'] = 'Gurajada'
        plt.rcParams['font.size'] = 14
        plt.plot(indices, c_r, color='#D2691E', marker='s',markersize = 7,mfc= '#40E0D0', mec='#40E0D0', linestyle='--', linewidth=2, label= 'Scenario -3 (Viewstamped  Replication)')
        plt.title(' Number of Transactions vs Transaction Latency (ms)', fontdict=font)
        plt.xlabel('Number of Transactions', fontdict=font)
        plt.ylabel('Transaction Latency (ms)', fontdict=font)
        print("\n========================================\n  3. Transaction Latency Graph\n========================================\n")
        plt.legend()
        plt.grid(True)
        plt.show()
        os.remove(f3)

    def Confidentiality():
        font = {'family': 'Gurajada', 'size': 18, 'weight':'bold'}
        f5 = "ACC.txt"
        a_c_c = read_values(f5)
        indices = range(1, len(a_c_c) + 1)
        plt.style.use('cyberpunk')
        plt.rcParams['font.weight'] = 'bold'
        plt.rcParams['font.family'] = 'Gurajada'
        plt.rcParams['font.size'] = 14
        plt.plot(indices, a_c_c, color='yellow', marker='s', mfc='red', mec='red', linestyle='-.', linewidth=2, label= 'Scenario -3 (Viewstamped  Replication)')
        plt.title('Number of Transactions vs Confidentiality (%)', fontdict=font)
        plt.xlabel('Number of Transactions', fontdict=font)
        plt.ylabel('Confidentiality (%)', fontdict=font)
        print("\n========================================\n  5. Confidentiality   Graph\n========================================\n")
        plt.legend()
        mplcyberpunk.add_glow_effects(gradient_fill=True)
        plt.grid(True)
        plt.show()
        os.remove(f5)
    
    def Throughput():
        font = {'family': 'Gurajada', 'size': 18, 'weight':'bold'}
        f4 = "TP.txt"
        t_p = read_values(f4)
        indices = range(1, len(t_p) + 1)
        plt.style.use('cyberpunk')
        plt.rcParams['font.weight'] = 'bold'
        plt.rcParams['font.family'] = 'Gurajada'
        plt.rcParams['font.size'] = 14
        plt.bar(indices, t_p,  color='#A9A9A9', edgecolor='#FF00FF', linewidth=2, label=  'Scenario -3 (Viewstamped_Replication)')
        plt.title('Number of Transactions vs Transaction Throughput(kbps)', fontdict=font)
        plt.xlabel('Number of Transactions', fontdict=font)
        plt.ylabel('Transaction Throughput(kbps)', fontdict=font)
        print("\n========================================\n  4. Transaction Throughput  Graph\n========================================\n")
        plt.legend()
        plt.grid(True)
        plt.show()
        os.remove(f4)
        
    def Data_Integrity():
        font = {'family': 'Gurajada', 'color': 'black', 'size': 18, 'weight':'bold'} 
        f1 = "TPT.txt"
        t_p_t = read_values(f1)
        indices = range(1, len(t_p_t) + 1)
        plt.style.use('ggplot')
        plt.rcParams['font.weight'] = 'bold'
        plt.rcParams['font.family'] = 'Gurajada'
        plt.rcParams['font.size'] = 14
        plt.plot(indices, t_p_t, color='#FF69B4', marker='D',markersize = 7,mfc= '#708090', mec='#708090', linestyle='--', linewidth=2, label=  'Scenario -3 (Viewstamped  Replication)')
        plt.title('Number of Blocks vs. Data Integrity (%) ', fontdict=font)
        plt.xlabel('Number of Blocks', fontdict=font)
        plt.ylabel('Data Integrity (%)', fontdict=font)
        print("\n========================================\n  1. Data Integrity   Graph\n========================================\n")
        plt.legend()
        plt.grid(True)
        plt.show()
        os.remove(f1)

    Data_Integrity() 
    Data_Storage_Efficiency()  
    Latency()  
    Throughput()  
    Confidentiality()  
    
PerformanceMetrics()


