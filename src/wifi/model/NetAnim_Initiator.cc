#include "NetAnim_Initiator.h"
#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <bitset>
#include <array>

#define BIG_double (INFINITY)

using namespace std;

namespace ns3 {

void NetAnim_Initiator::Initiate()
{
    system("python3 src/wifi/model/NetAnim_Initiator.py");
}
} 
