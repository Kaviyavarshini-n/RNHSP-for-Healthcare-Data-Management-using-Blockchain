**RNHSP-for-Healthcare-Data-Management-using-Blockchain**

**‎Description:**
This is an NS-3 network simulation project of healthcare-data management on a blockchain-oriented architecture. The custom work is concentrated in the scratch/ directory, which has four scenario programs, namely, Raft Net Health Sync Protocol (RNHSP), Paxos, Viewstamped Replication, and PBFT. The source tree of the wider NS-3 is also found in the repository as src/ and image resources in img/.
The code is a model of a healthcare communication network and a comparison of various consensus/access - control methods of sharing data over the network safely. The simulation phases depicted in code in the case of RNHSP are: network building, generated data generation, attribute-based cryptography, rankings in SG-MCDF-based storage, access control and data sharing, NetAnim visualization and performance-metric plotting.

**‎Dataset Information:**
The project relies on a generated dataset, which is produced during the execution of the simulation and carried out to analyze experimentally the healthcare data management based on blockchains.
It is a simulated dataset which is generated within the organization to simulate behavior of healthcare-networks, protocols performance and secure conditions of data-sharing in the presence of various consensus mechanisms.The outputs of the generated dataset are simulation output files:
ACT.txt
TPT.txt
CR.txt
ACC.txt
TP.txt

This information is stored in files which have derived performance metrics through simulation which are evaluated. The dataset technically is generated values associated with:
access or processing time
performance of the transaction or transmission.
communication rate
accuracy-related performance
throughput-related performance

This data set will be used in protocol comparison and performance measurement, in the simulated environment. It can thus be defined as an simulated, run-time created assessment dataset on healthcare blockchain network analysis.
‎

**Code Information:**
The project is implemented as an NS-3 based C++ simulation framework designed to evaluate blockchain-enabled healthcare data management under different consensus protocols.
Each scenario file represents a separate experimental configuration implementing a specific consensus or access-control protocol. All scenarios share a common simulation pipeline but differ in the protocol-specific execution stage.
The network model includes:
User nodes (≈100)
Base stations (≈2)
Blockchain node (≈1)

Networking Stack
The simulation uses multiple NS-3 modules:
Wi-Fi for wireless communication
AODV for routing
CSMA for wired links
Mobility models (Random Waypoint, Constant Position)
Internet stack (IPv4/IPv6)
6LoWPAN support
FlowMonitor for performance tracking
NetAnim for visualization

Functional Components
The simulation workflow is composed of the following functional stages:
1. Data Generation
Synthetic healthcare-related data is generated for simulation input

2. Network Initialization
Node creation, device configuration, IP assignment, and mobility setup

3.Security Layer
Attribute-Based Cryptography (ABC) for secure data handling

4. Decision and Storage Layer
SG-MCDF (multi-criteria decision framework) for ranking and blockchain storage

5. Protocol Execution
Scenario-specific implementation:
RNHSP (Raft-based protocol)
Paxos
Viewstamped Replication
PBFT

6. Performance Metrics Generation
Metrics are generated and written to output files:
ACT.txt, TPT.txt, CR.txt, ACC.txt, TP.txt

7. Monitoring and Visualization
FlowMonitor collects packet-level statistics
NetAnim generates XML-based animation output

**‎Usage Instructions:**

Install the necessary environment using NS-3, Ganache, IPFS, and the required Python packages and put the project into the NS-3 working directory and compile with the NS-3 build system. Change to the scratch/ directory and run any of scenario files to execute the simulation. The data set is created automatically on the fly and there is no need to load data manually. Upon execution, it also produces performance metrics files (ACT.txt, TPT.txt, CR.txt, ACC.txt, TP.txt) and NetAnim XML files may be analyzed and examined to understand network behavior.

**‎Requirements:**

Ganache Blockchain Environment:
fuse
libfuse2
ganache-2.7.1-linux-x86_64.AppImage

IPFS Storage Environment:
ipfs-desktop-0.37.0-linux-x86_64.AppImage

NS-3 Environment:
ns-allinone-3.35
build-essential
autoconf
automake
libxmu-dev
g++
python3
python3-dev
pkg-config
sqlite3
cmake
python3-setuptools
git
qtbase5-dev
qtchooser
qt5-qmake
qtbase5-dev-tools
gir1.2-goocanvas-2.0
python3-gi
python3-gi-cairo
python3-pygraphviz
gir1.2-gtk-3.0
ipython3
openmpi-bin
openmpi-common
openmpi-doc
libopenmpi-dev
cvs
bzr
unrar
gsl-bin
libgsl-dev
libgslcblas0
wireshark
tcpdump
sqlite
libsqlite3-dev
libxml2
libxml2-dev
libc6-dev
libc6-dev-i386
libclang-dev
llvm-dev
python3-pip
libboost-all-dev

Python Environment:
cryptography
matplotlib
mplcyberpunk
qbstyles
numpy
hashlib
scikit-learn
pandas
crypto
requests
pycryptodome
pycryptodomex
getpass
torch
py-solc-x
web3
pyswarm
scrypt

**‎Methodology:**

The project is based on a simulation-based approach where synthetic healthcare data is created and subsequently employed to create a network model comprising of user nodes, base stations, and a blockchain node. NS-3 modules used in configuring communication and mobility include Wi-Fi, AODV routing, CSMA links, 6LoWPAN and mobility models. The system then provides performance metrics and stores them in the form of text outputs. The attribute-based cryptography layer includes security, and multi-criteria decision mechanism (SG-MCDF) ranks and blockchain storage. Recently, RNHSP (Raft), Paxos, Viewstamped Replication, and PBFT protocols are implemented in various scenarios to allow comparing them. NetAnim is used to visualize the simulation results and the network-level performance metrics, including the packet delivery and the delay, can be collected by using an analysis tool, FlowMonitor.
