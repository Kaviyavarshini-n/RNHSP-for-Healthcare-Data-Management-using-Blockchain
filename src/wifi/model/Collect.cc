#include "Collect.h"
#include <cstdlib>
using namespace std;
namespace ns3 {
using namespace std;
void Collect::coll_data()
{
    system("python3 src/wifi/model/Collect.py");
}
} 
