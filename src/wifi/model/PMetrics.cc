#include "PMetrics.h"
#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <string>
#include <bitset>
#include <array>
using namespace std;
namespace ns3 {
void PMetrics::Metrics()
{
std::ifstream file("log.txt");
    if (!file) {
        std::cerr << "Unable to open file log.txt" << std::endl;
        std::exit(1);
    }
    std::string line;
    if (std::getline(file, line)) {
        int log_value = std::stoi(line);
        if (log_value == 1) {
            system("python3 src/wifi/model/PMetrics1.py");
        } 
    }
    file.close();
} 

void PMetrics::Metrics1()
{
std::ifstream file("log.txt");
    if (!file) {
        std::cerr << "Unable to open file log.txt" << std::endl;
        std::exit(1);
    }
    std::string line;
    if (std::getline(file, line)) {
        int log_value = std::stoi(line);
        if (log_value == 1) {
            system("python3 src/wifi/model/PMetrics2.py");
        } 
    }
    file.close();
} 

void PMetrics::Metrics2()
{
std::ifstream file("log.txt");
    if (!file) {
        std::cerr << "Unable to open file log.txt" << std::endl;
        std::exit(1);
    }
    std::string line;
    if (std::getline(file, line)) {
        int log_value = std::stoi(line);
        if (log_value == 1) {
            system("python3 src/wifi/model/PMetrics3.py");
        } 
    }
    file.close();
} 

void PMetrics::Metrics3()
{
std::ifstream file("log.txt");
    if (!file) {
        std::cerr << "Unable to open file log.txt" << std::endl;
        std::exit(1);
    }
    std::string line;
    if (std::getline(file, line)) {
        int log_value = std::stoi(line);
        if (log_value == 1) {
            system("python3 src/wifi/model/PMetrics4.py");
        } 
    }
    file.close();
} 
}
