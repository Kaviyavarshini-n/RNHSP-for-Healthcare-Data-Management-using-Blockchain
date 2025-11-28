#include "Generate_IOT_Data.h"
#include <cstdlib>
using namespace std;
namespace ns3 {
using namespace std;
void Generate_IOT_Data::data()
{
    system("python3 src/wifi/model/GenerateIoTData.py");
}

} 
