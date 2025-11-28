#include "ABC.h"
#include <cstdlib>
using namespace std;
namespace ns3 {
using namespace std;
void ABC::secure()
{
    system("python3 src/wifi/model/Abc.py");
}
void ABC::secure1()
{
    system("python3 src/wifi/model/Ibe.py");
}
void ABC::secure2()
{
    system("python3 src/wifi/model/Ciphertext.py");
}
void ABC::secure3()
{
    system("python3 src/wifi/model/Pencrypt.py");
}
void ABC::store()
{
    system("python3 src/wifi/model/Fabric.py");
}
} 
