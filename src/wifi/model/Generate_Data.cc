#include "Generate_Data.h"
#include <cstdlib>
using namespace std;
namespace ns3 {
using namespace std;
void Generate_Data::gen_data()
{
    system("python3 src/wifi/model/Generate_Data.py");
}
} 
