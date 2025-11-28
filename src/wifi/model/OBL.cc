#include "OBL.h"
#include <cstdlib>
using namespace std;
namespace ns3 {
using namespace std;
void OBL::optimize()
{
    system("python3 src/wifi/model/OBL.py");
}
} 
