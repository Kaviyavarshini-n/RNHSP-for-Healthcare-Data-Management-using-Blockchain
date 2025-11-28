#include "Preprocess.h"
#include <cstdlib>
using namespace std;
namespace ns3 {
using namespace std;
void Preprocess::normalize()
{
    system("python3 src/wifi/model/Preprocess.py");
}

} 
