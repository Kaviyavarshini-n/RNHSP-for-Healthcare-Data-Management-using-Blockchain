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
        plt.bar(indices, a_c_t,  color='#FF69B4', edgecolor='#708090', linewidth=2, label=  'Scenario -4 (PBFT protocol)')
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
        plt.plot(indices, c_r, color='#800000', marker='s',markersize = 7,mfc= '#20B2AA', mec='#20B2AA', linestyle='--', linewidth=2, label= 'Scenario -4 (PBFT protocol)')
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
        plt.plot(indices, a_c_c, color='#87CEEB', marker='s', mfc='#EE2C2C', mec='#EE2C2C', linestyle='-.', linewidth=2, label= 'Scenario -4 (PBFT protocol)')
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
        plt.bar(indices, t_p,  color='#556B2F', edgecolor='#FFDAB9', linewidth=2, label= 'Scenario -4 (PBFT protocol)')
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
        plt.plot(indices, t_p_t, color='#DC143C', marker='D',markersize = 7,mfc= '#00FF00', mec='#8B1A1A', linestyle='--', linewidth=2, label= 'Scenario -4 (PBFT protocol)')
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


