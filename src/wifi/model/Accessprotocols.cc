#include "Accessprotocols.h"
#include <cstdlib>
using namespace std;
namespace ns3 {
using namespace std;
void ACCPROTOCOLS::access()
{
    system("python3 src/wifi/model/RAFT.py");
}
void ACCPROTOCOLS::paxos()
{
    system("python3 src/wifi/model/Paxos.py");
}
void ACCPROTOCOLS::viewstamp()
{
    system("python3 src/wifi/model/Viewstamped.py");
}
void ACCPROTOCOLS::pbft()
{
    system("python3 src/wifi/model/Pbft.py");
}
} 
