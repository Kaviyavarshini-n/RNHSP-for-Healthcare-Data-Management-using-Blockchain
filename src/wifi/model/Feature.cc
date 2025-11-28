#include "Feature.h"
#include <cstdlib>
using namespace std;
namespace ns3 {
using namespace std;
void Feature::extract()
{
    system("python3 src/wifi/model/Feature.py");
}
} 
