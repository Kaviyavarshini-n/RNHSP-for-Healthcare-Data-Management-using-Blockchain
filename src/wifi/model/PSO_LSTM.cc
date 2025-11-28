#include "PSO_LSTM.h"
#include <cstdlib>
using namespace std;
namespace ns3 {
using namespace std;
void PSO_LSTM::train()
{
    system("python3 src/wifi/model/PSO_LSTM.py");
}
} 
