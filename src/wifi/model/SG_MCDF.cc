#include "SG_MCDF.h"
#include <cstdlib>
using namespace std;
namespace ns3 {
using namespace std;
void SG_MCDF::block()
{
    system("python3 src/wifi/model/SG_MCDF.py");
}
} 
