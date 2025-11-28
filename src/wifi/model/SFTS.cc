#include "SFTS.h"
#include <cstdlib>
using namespace std;
namespace ns3 {
using namespace std;
void SFTS::validate()
{
    system("python3 src/wifi/model/SFTS.py");
}
} 
