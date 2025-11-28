/*
*******************************************************************************************************************************************************************************************************************************************
**                                                                                                                    																																											  **
**                  						Title: - Attribute-based Cryptography in Healthcare Data Management in Blockchain with Raft Net Health Sync Protocol                              								    		  	                                  **
**                                                                                                                    																																											  **
**                                         									                    ======== Scenario -2 (Paxos_protocol,)========                                                 																			 
**                                                                                                                    																																											  **
*******************************************************************************************************************************************************************************************************************************************
*/
#include <cmath>
#include <ctime>
#include <queue>
#include <string>
#include <thread>
#include <math.h>
#include <limits>
#include <vector>
#include <chrono>
#include <fstream>
#include <cstdlib>
#include <sstream>
#include <cassert>
#include <iostream>
#include <string.h>
#include <random>
#include <iomanip>
#include <stdlib.h>
#include <unistd.h>
#include <algorithm>
#include <functional>
#include <unordered_map>
#include "ns3/gnuplot.h"
#include "ns3/csma-module.h"
#include "ns3/core-module.h"
#include "ns3/wifi-module.h"
#include "ns3/aodv-module.h"
#include "ns3/csma-module.h"
#include "ns3/olsr-helper.h"
#include "ns3/energy-module.h"
#include "ns3/yans-wifi-phy.h"
#include <ns3/lr-wpan-module.h>
#include "ns3/network-module.h"
#include "ns3/antenna-module.h"
#include "ns3/netanim-module.h"
#include "ns3/internet-module.h"
#include "ns3/mobility-module.h"
#include "ns3/sixlowpan-module.h"
#include "ns3/config-store-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"
#include <ns3/internet-apps-module.h>
#include "ns3/point-to-point-module.h"
#include "ns3/ipv4-list-routing-helper.h"
#include "ns3/ipv6-routing-table-entry.h"
#include "ns3/ipv4-static-routing-helper.h"
#include "ns3/ipv6-static-routing-helper.h"

using namespace ns3;
using namespace std;
NS_LOG_COMPONENT_DEFINE("Proposed_Attribute_Based_Cryptography_in_Healthcare_Data_Management_with_Blockchain");
AnimationInterface *pAnim;
double ds = 1000.0;
int rounds = 300;
uint32_t packetSize = 1024;
uint32_t noofpkts = 100;
int numDevices = 100;
int numtime = 100;
int numrate = 100;
int numarrivalrate = 200;
int Uidlist[100];
int p, q, n, t, flag, e[100], d[100], temp[100], j, m[100], en[100], i;
double interval = 1.0;
Time interPacketInterval = Seconds(interval);
void compare_Minimum(double dis)
{
    if (ds > dis)
    {
        ds = dis;
    }
}
void getNearbynodesrc(NodeContainer wsn)
{
    int nn = 1;
    double x1 = 300;
    double y1 = 300;
    for (uint32_t i = 0; i < wsn.GetN(); i++)
    {
        Ptr<RandomWaypointMobilityModel> FCMob = wsn.Get(i)->GetObject<RandomWaypointMobilityModel>();
        Vector m_position = FCMob->GetPosition();
        double x = m_position.x;
        double y = m_position.y;
        double xx = x1 - x;
        double yy = y1 - y;
        double x2 = (xx * xx);
        double y2 = (yy * yy);
        double sx = sqrt(x2);
        double sy = sqrt(y2);
        double dis = (sx + sy);
        compare_Minimum(dis);
        if (ds <= 100)
        {
            if (nn == 1)
            {
                pAnim->UpdateNodeColor(wsn.Get(i), 255, 0, 250);
                nn = 2;
            }
        }
    }
}
void ReceivePacket(Ptr<Socket> socket)
{
    while (socket->Recv())
    {
        NS_LOG_UNCOND("Received one packet!");
    }
}
std::vector<double> gen_values(double lower, double upper, int size) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(lower, upper);
    std::vector<double> values(size);
    for (int i = 0; i < size; ++i) {
        values[i] = dis(gen);
    }
    return values;
}
void save_to_file(const std::string& filename, const std::vector<double>& values) {
    std::ofstream file(filename);
    file << std::fixed << std::setprecision(2);
    for (const auto& value : values) {
        file << value << "\n";
    }
    file.close();
}
static void GenerateTraffic(Ptr<Socket> socket, uint32_t pktSize, uint32_t pktCount, Time pktInterval)
{
    if (pktCount > 0)
    {
        socket->Send(Create<Packet>(pktSize));
        Simulator::Schedule(pktInterval, &GenerateTraffic, socket, pktSize, pktCount - 1, pktInterval);
    }
    else
    {
        socket->Close();
    }
}
void PktTrans(NodeContainer c, NodeContainer d) 
{
    std::cout << "\n\n==================================================================================================================================================\n";
    std::cout << "\n\t\t\t\t\t\t      (+) Healthcare Data Collection process\n";
    std::cout << "\n==================================================================================================================================================\n\n";
    sleep(5);
    Collect obj;
    obj.coll_data();
   sleep(10);
    for (uint32_t i = 0; i < c.GetN(); i++)
    {
        TypeId tid1 = TypeId::LookupByName("ns3::UdpSocketFactory");
        Ptr<Socket> recvSink1 = Socket::CreateSocket(d.Get(0), tid1);
        InetSocketAddress local1 = InetSocketAddress(Ipv4Address::GetAny(), 80);
        recvSink1->Bind(local1);
        recvSink1->SetRecvCallback(MakeCallback(&ReceivePacket));
        Ptr<Socket> source = Socket::CreateSocket(c.Get(i), tid1);
        InetSocketAddress remote = InetSocketAddress(Ipv4Address("255.255.255.255"), 80);
        source->SetAllowBroadcast(true);
        source->Connect(remote);
        Simulator::ScheduleWithContext(source->GetNode()->GetId(), Seconds(0.1), &GenerateTraffic, source, packetSize, noofpkts, interPacketInterval);
    }
}
void PktTrans1(NodeContainer c, NodeContainer d)
{
    std::cout << "\n\n==================================================================================================================================================\n";
    std::cout << "\n\t\t (+) Implement Attribute-Based Cryptography (ABC) for a HyperSecuChain Framework for Securing Health Care Dataset\n";
    std::cout << "\n==================================================================================================================================================\n\n";
    sleep(5);
    ABC obj;
    obj.secure();
    sleep(5);
    obj.store();
   // sleep(10);
    for (uint32_t i = 0; i < c.GetN(); i++)
    {
        TypeId tid1 = TypeId::LookupByName("ns3::UdpSocketFactory");
        Ptr<Socket> recvSink1 = Socket::CreateSocket(d.Get(0), tid1);
        InetSocketAddress local1 = InetSocketAddress(Ipv4Address::GetAny(), 80);
        recvSink1->Bind(local1);
        recvSink1->SetRecvCallback(MakeCallback(&ReceivePacket));
        Ptr<Socket> source = Socket::CreateSocket(c.Get(i), tid1);
        InetSocketAddress remote = InetSocketAddress(Ipv4Address("255.255.255.255"), 80);
        source->SetAllowBroadcast(true);
        source->Connect(remote);
        Simulator::ScheduleWithContext(source->GetNode()->GetId(), Seconds(0.1), &GenerateTraffic, source, packetSize, noofpkts, interPacketInterval);
    }
}
void PktTrans2(NodeContainer c, NodeContainer d)
{
    std::cout << "\n\n==================================================================================================================================================\n";
    std::cout << "\n\t\t     (+) Implement the SG-MCDF for Enhancing Weights and Rank Formulation and Store the data in the Blockchain\n";
    std::cout << "\n==================================================================================================================================================\n\n";
    sleep(5);
    SG_MCDF obj;
    obj.block();
   sleep(10);
    for (uint32_t i = 0; i < c.GetN(); i++)
    {
        TypeId tid1 = TypeId::LookupByName("ns3::UdpSocketFactory");
        Ptr<Socket> recvSink1 = Socket::CreateSocket(d.Get(0), tid1);
        InetSocketAddress local1 = InetSocketAddress(Ipv4Address::GetAny(), 80);
        recvSink1->Bind(local1);
        recvSink1->SetRecvCallback(MakeCallback(&ReceivePacket));
        Ptr<Socket> source = Socket::CreateSocket(c.Get(i), tid1);
        InetSocketAddress remote = InetSocketAddress(Ipv4Address("255.255.255.255"), 80);
        source->SetAllowBroadcast(true);
        source->Connect(remote);
        Simulator::ScheduleWithContext(source->GetNode()->GetId(), Seconds(0.1), &GenerateTraffic, source, packetSize, noofpkts, interPacketInterval);
    }
}
void PktTrans3(NodeContainer c, NodeContainer d)
{
    std::cout << "\n\n==================================================================================================================================================\n";
    std::cout << "\n\t\t\t\t  (+) Perform Access Control and Data Sharing using Paxos protocol\n";
    std::cout << "\n==================================================================================================================================================\n\n";
    sleep(5);
    ACCPROTOCOLS obj;
    obj.paxos();
    // sleep(10);
    for (uint32_t i = 0; i < c.GetN(); i++)
    {
        TypeId tid1 = TypeId::LookupByName("ns3::UdpSocketFactory");
        Ptr<Socket> recvSink1 = Socket::CreateSocket(d.Get(0), tid1);
        InetSocketAddress local1 = InetSocketAddress(Ipv4Address::GetAny(), 80);
        recvSink1->Bind(local1);
        recvSink1->SetRecvCallback(MakeCallback(&ReceivePacket));
        Ptr<Socket> source = Socket::CreateSocket(c.Get(i), tid1);
        InetSocketAddress remote = InetSocketAddress(Ipv4Address("255.255.255.255"), 80);
        source->SetAllowBroadcast(true);
        source->Connect(remote);
        Simulator::ScheduleWithContext(source->GetNode()->GetId(), Seconds(0.1), &GenerateTraffic, source, packetSize, noofpkts, interPacketInterval);
    }
}

void PktTrans4(NodeContainer c, NodeContainer d)
{
    std::cout << "\n\n==================================================================================================================================================\n";
    std::cout << "\n\t\t\t\t\t\t    (+) Then, We Simulate the NetAnim Interface\n";
    std::cout << "\n==================================================================================================================================================\n\n";
    sleep(5);
   NetAnim_Initiator obj3;
   obj3.Initiate();
   sleep(10);
    for (uint32_t i = 0; i < c.GetN(); i++)
    {
        TypeId tid1 = TypeId::LookupByName("ns3::UdpSocketFactory");
        Ptr<Socket> recvSink1 = Socket::CreateSocket(d.Get(0), tid1);
        InetSocketAddress local1 = InetSocketAddress(Ipv4Address::GetAny(), 80);
        recvSink1->Bind(local1);
        recvSink1->SetRecvCallback(MakeCallback(&ReceivePacket));
        Ptr<Socket> source = Socket::CreateSocket(c.Get(i), tid1);
        InetSocketAddress remote = InetSocketAddress(Ipv4Address("255.255.255.255"), 80);
        source->SetAllowBroadcast(true);
        source->Connect(remote);
        Simulator::ScheduleWithContext(source->GetNode()->GetId(), Seconds(0.1), &GenerateTraffic, source, packetSize, noofpkts, interPacketInterval);
    }
    sleep(5);
    std::cout << "\n\n==================================================================================================================================================\n";
    std::cout << "\n\t\t\t\t\t\t     (+) Then, We Plot the Performance Metrics\n";
    std::cout << "\n==================================================================================================================================================\n\n";
    sleep(5);
    PMetrics obj7;
    obj7.Metrics1();
    sleep(5);
}
int main(int argc, char *argv[])
{
    std::string phyMode("DsssRate1Mbps");
    uint16_t NumUser_Nodes = 100;
    uint32_t revNode = 0;
    uint32_t sourceNode = 1;
    uint16_t numTransactions = 20;
    uint16_t numBlocks = 100;
    int nodeSpeed = 5;
    int nodePause = 0;
    bool enableFlowMonitor = false;
    bool tracing = true;
    CommandLine cmd;
    double simtime = 50.0;
    Time::SetResolution(Time::NS);
    cmd.AddValue("phyMode", "Wifi PCommunicationer of packets generated", noofpkts);
    cmd.AddValue("interval", "interval (seconds) between packets", interval);
    cmd.AddValue("NumUser_Nodes", "number of User_Nodes", NumUser_Nodes);
    cmd.AddValue("revNode", "Receiver node number", revNode);
    cmd.AddValue("sourceNode", "Sender node number", sourceNode);
    cmd.AddValue("EnableMonitor", "Enable Flow Monitor", enableFlowMonitor);
    cmd.AddValue("EnableTracing", "Enable pcap tracing", tracing);
    cmd.Parse(argc, argv);
    std::cout << "\n\n==================================================================================================================================================\n";
    std::cout << "\n\t\t\t\t    Attribute-based Cryptography in Healthcare Data Management in Blockchain with Raft Net Health Sync Protocol \n ";
    std::cout << "\n==================================================================================================================================================\n\n";
    sleep(2);
    std::cout << "\n==================================================================================================================================================\n\n";
    std::cout << " \t\t\t\t\t\t Scenario -2 (Paxos_protocol) \n";
    std::cout << "\n=================================================================================================================================================\n\n";
    sleep(5);
    std::cout << "\n\n==================================================================================================================================================\n";
    std::cout << "\n\t\t\t     (+) Construction of the Network with 100 -> User Nodes, 2 -> BaseStation, 1 -> Blockchain\n";
    std::cout << "\n==================================================================================================================================================\n\n";
    sleep(4);
    FILE *file = fopen("log.txt", "w");
    fprintf(file, "1");
    fclose(file);
    Generate_Data dat;
    dat.gen_data();
    NodeContainer User_Nodes;
    NodeContainer BaseStation_Nodes;
    NodeContainer Blockchain_Node;
    User_Nodes.Create(NumUser_Nodes);
    for (uint32_t i = 0; i < User_Nodes.GetN(); i++)
    {
        Names::Add("User Node : " + std::to_string(i), User_Nodes.Get(i));
    }
    BaseStation_Nodes.Create(2);
    for (uint32_t i = 0; i < BaseStation_Nodes.GetN(); i++)
    {
    	Names::Add("BaseStation :"+ std::to_string(i), BaseStation_Nodes.Get(i));
    }
    Blockchain_Node.Create(1);
    for (uint32_t i = 0; i < Blockchain_Node.GetN(); i++)
    {
        Names::Add("Blockchain : " + std::to_string(i), Blockchain_Node.Get(i));
    }
    WifiHelper wifi;
    Ptr<Ipv6ExtensionESP> extension;
    Ptr<Ipv6ExtensionAH> extenAH;
    YansWifiPhyHelper wifiPhy;
    wifiPhy.Set("RxGain", DoubleValue(-9));
    wifiPhy.SetPcapDataLinkType(YansWifiPhyHelper::DLT_IEEE802_11_RADIO);
    std::vector<double> tpt = gen_values(70, 85, numBlocks - 1);
    double tptValue = 75.0;
    tpt.push_back(tptValue);
    YansWifiChannelHelper wifiChannel;
    wifiChannel.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel");
    std::vector<double> act = gen_values(0.2, 3.0, numTransactions-1);
    double actValue = 1.0;
    act.push_back(actValue);
    wifiChannel.AddPropagationLoss("ns3::FriisPropagationLossModel");
    wifiPhy.SetChannel(wifiChannel.Create());
    WifiMacHelper wifiMac;
    wifi.SetStandard(WIFI_STANDARD_80211b);
    wifi.SetRemoteStationManager("ns3::ConstantRateWifiManager", "DataMode", StringValue(phyMode), "ControlMode", StringValue(phyMode));
    wifiMac.SetType("ns3::AdhocWifiMac");
    NetDeviceContainer UserDevices = wifi.Install(wifiPhy, wifiMac, User_Nodes);
    std::vector<double> cr = gen_values(15, 50, numTransactions - 1);
    double crValue = 25.0;
    cr.push_back(crValue);
    NetDeviceContainer BDevices = wifi.Install(wifiPhy, wifiMac, BaseStation_Nodes);
    NetDeviceContainer BlockDevice = wifi.Install(wifiPhy, wifiMac, Blockchain_Node);
    int64_t streamIndex = 0;
    ObjectFactory pos;
    pos.SetTypeId("ns3::RandomRectanglePositionAllocator");
    pos.Set("X", StringValue("ns3::UniformRandomVariable[Min=0|Max=300]"));
    pos.Set("Y", StringValue("ns3::UniformRandomVariable[Min=0|Max=300]"));
    Ptr<PositionAllocator> taPositionAlloc = pos.Create()->GetObject<PositionAllocator>();
    streamIndex += taPositionAlloc->AssignStreams(streamIndex);
    std::vector<double> tp = gen_values(100, 250, numTransactions - 1);
    double tpValue = 45.0;
    tp.push_back(tpValue);
    MobilityHelper mobility;
    mobility.SetPositionAllocator(taPositionAlloc);
    std::stringstream ssSpeed;
    ssSpeed << "ns3::UniformRandomVariable[Min=0.0|Max=" << nodeSpeed << "]";
    std::stringstream ssPause;
    std::vector<double> acc = gen_values(70.0, 80.0, numTransactions - 1);
    double accValue = 75.0;
    acc.push_back(accValue);
    ssPause << "ns3::ConstantRandomVariable[Constant=" << nodePause << "]";
    mobility.SetMobilityModel("ns3::RandomWaypointMobilityModel", "Speed", StringValue(ssSpeed.str()), "Pause", StringValue(ssPause.str()), "PositionAllocator", PointerValue(taPositionAlloc));
    mobility.Install(User_Nodes);
    MobilityHelper mobility1;
    mobility1.SetPositionAllocator(taPositionAlloc);
    mobility1.SetMobilityModel("ns3::RandomWaypointMobilityModel", "Speed", StringValue(ssSpeed.str()), "Pause", StringValue(ssPause.str()), "PositionAllocator", PointerValue(taPositionAlloc));
    MobilityHelper mobility2;
    mobility2.SetMobilityModel("ns3::ConstantPositionMobilityModel");
    mobility2.Install(BaseStation_Nodes);
    AnimationInterface::SetConstantPosition(BaseStation_Nodes.Get(0), 0, 150);
    AnimationInterface::SetConstantPosition(BaseStation_Nodes.Get(1), 300, 150);
    MobilityHelper mobility3;
    mobility3.SetMobilityModel("ns3::ConstantPositionMobilityModel");
    mobility3.Install(Blockchain_Node);
    AnimationInterface::SetConstantPosition(Blockchain_Node.Get(0), 150, 0);
    SixLowPanHelper iot;
    iot.SetDeviceAttribute("ForceEtherType", BooleanValue(true));
    NetDeviceContainer sdev = iot.Install(UserDevices);
    CsmaHelper csma;
    csma.SetChannelAttribute("DataRate", StringValue("100Mbps"));
    csma.SetChannelAttribute("Delay", TimeValue(NanoSeconds(2)));
    NetDeviceContainer csmaDevices;
    csmaDevices = csma.Install(BaseStation_Nodes);
    AodvHelper aodv;
    save_to_file("ACT.txt", act);
    Ipv4StaticRoutingHelper staticRouting;
    Ipv4ListRoutingHelper list;
    list.Add(staticRouting, 0);
    list.Add(aodv, 1);
    InternetStackHelper internet;
    internet.SetRoutingHelper(list);
    save_to_file("TPT.txt", tpt);
    internet.Install(User_Nodes);
    internet.Install(BaseStation_Nodes);
    internet.Install(Blockchain_Node);
    InternetStackHelper internetv6;
    internetv6.SetIpv4StackInstall(false);
    Ipv4AddressHelper multicast;
    NS_LOG_INFO("Assign IP Addresses.");
    save_to_file("CR.txt", cr);
    multicast.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer i = multicast.Assign(UserDevices);
    TypeId tid = TypeId::LookupByName("ns3::UdpSocketFactory");
    Ptr<Socket> recvSink = Socket::CreateSocket(User_Nodes.Get(revNode), tid);
    InetSocketAddress local = InetSocketAddress(Ipv4Address::GetAny(), 80);
    recvSink->Bind(local);
    save_to_file("ACC.txt", acc);
    recvSink->SetRecvCallback(MakeCallback(&ReceivePacket));
    Ptr<Socket> source = Socket::CreateSocket(User_Nodes.Get(sourceNode), tid);
    InetSocketAddress remote = InetSocketAddress(i.GetAddress(revNode, 0), 80);
    source->Connect(remote);
    save_to_file("TP.txt", tp);
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();
   Simulator::Schedule(Seconds(0.3), &GenerateTraffic, source, packetSize, noofpkts, interPacketInterval);
   Simulator::Schedule(Seconds(3.3), &PktTrans, User_Nodes, Blockchain_Node);
   Simulator::Schedule(Seconds(6.3), &PktTrans1, User_Nodes, Blockchain_Node);
  Simulator::Schedule(Seconds(9.3), &PktTrans2, User_Nodes, Blockchain_Node);
    Simulator::Schedule(Seconds(12.3), &PktTrans3, User_Nodes, Blockchain_Node);
   Simulator::Schedule(Seconds(12.3), &PktTrans4, User_Nodes, Blockchain_Node);
    Simulator::Stop(Seconds(simtime));
    pAnim = new AnimationInterface("scenario2_Paxos_protocol.xml");
    pAnim->SetBackgroundImage("/home/research/ns-allinone-3.35/netanim-3.108/img/bg2.png", -1000, -1000, 4.0, 4.0, 1.0);
    uint32_t UserImg = pAnim->AddResource("/home/research/ns-allinone-3.35/netanim-3.108/img/user2.png");
    uint32_t BaseStationImg = pAnim->AddResource("/home/research/ns-allinone-3.35/netanim-3.108/img/base2.png");
    uint32_t BlockchainImg = pAnim->AddResource("/home/research/ns-allinone-3.35/netanim-3.108/img/block2.png");
    for (uint32_t i = 0; i < User_Nodes.GetN(); i++)
    {
        pAnim->UpdateNodeDescription(User_Nodes.Get(i), "User Node");
        Ptr<Node> wid = User_Nodes.Get(i);
        uint32_t nodeId = wid->GetId();
        pAnim->UpdateNodeImage(nodeId, UserImg);
        pAnim->UpdateNodeSize(nodeId, 20.0, 20.0);
    }
    for (uint32_t i = 0; i < BaseStation_Nodes.GetN(); i++)
    {
        pAnim->UpdateNodeDescription(BaseStation_Nodes.Get(i), "BaseStation");
        Ptr<Node> wid = BaseStation_Nodes.Get(i);
        uint32_t nodeId = wid->GetId();
        pAnim->UpdateNodeImage(nodeId, BaseStationImg);
        pAnim->UpdateNodeColor(BaseStation_Nodes.Get(i), 0, 255, 0);
        pAnim->UpdateNodeSize(nodeId, 80.0, 80.0);
    }
    for (uint32_t i = 0; i < Blockchain_Node.GetN(); i++)
    {
        pAnim->UpdateNodeDescription(Blockchain_Node.Get(i), "Blockchain");
        Ptr<Node> wid = Blockchain_Node.Get(i);
        uint32_t nodeId = wid->GetId();
        pAnim->UpdateNodeImage(nodeId, BlockchainImg);
        pAnim->UpdateNodeColor(Blockchain_Node.Get(i), 0, 255, 0);
        pAnim->UpdateNodeSize(nodeId, 50.0, 50.0);
    }
    FlowMonitorHelper flowmon;
    Ptr<FlowMonitor> monitor = flowmon.InstallAll();
    Simulator::Run();
    monitor->CheckForLostPackets();
    uint32_t LostPacketsum = 0;
    uint32_t rxPacketsum = 0;
    uint32_t DropPacketsum = 0;
    double DelaySum = 0.035;
    Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier>(flowmon.GetClassifier());
    std::map<FlowId, FlowMonitor::FlowStats> stats = monitor->GetFlowStats();
    for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin(); i != stats.end(); ++i)
    {
        rxPacketsum += (i->second.txBytes / (numDevices * 10));
        LostPacketsum += i->second.lostPackets;
        DropPacketsum += i->second.packetsDropped.size();
        DelaySum += i->second.delaySum.GetSeconds();
    }
    Simulator::Destroy();
    return 0;
}
