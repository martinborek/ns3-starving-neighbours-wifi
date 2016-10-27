# /*
#  * This program is free software; you can redistribute it and/or modify
#  * it under the terms of the GNU General Public License version 2 as
#  * published by the Free Software Foundation;
#  *
#  * This program is distributed in the hope that it will be useful,
#  * but WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  * GNU General Public License for more details.
#  *
#  * You should have received a copy of the GNU General Public License
#  * along with this program; if not, write to the Free Software
#  * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#  */

#import ns.applications
#import ns.core
#import ns.config
#import ns.internet
#import ns.network
#import ns.wifi
#import ns.point_to_point

import ns.core
import ns.network
import ns.point_to_point
import ns.applications
import ns.wifi
import ns.mobility
import ns.csma
import ns.internet
import sys


#ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
#ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)

# enable rts/cts
ns.core.Config.SetDefault("ns3::WifiRemoteStationManager::RtsCtsThreshold", ns.core.StringValue("0"))

ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)

wifiNodes = ns.network.NodeContainer()
wifiNodes.Create(4)
#apA = wifiNodes.Get(2)
#ha = wifiNodes.Get(1)
#apB = wifiNodes.Get(3)
#hb = wifiNodes.Get(0)
apA = wifiNodes.Get(0)
ha = wifiNodes.Get(1)
apB = wifiNodes.Get(3)
hb = wifiNodes.Get(2)


channelA = ns.wifi.YansWifiChannelHelper.Default()
channelA.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel")
channelA.AddPropagationLoss("ns3::RangePropagationLossModel", "MaxRange", ns.core.DoubleValue (3.0))

phyA = ns.wifi.YansWifiPhyHelper.Default()
phyA.Set("ChannelNumber", ns.core.StringValue('1'))
#phyB.setFrequency(2400)
#phyA.Configure80211b() #todo: check
phyA.SetChannel(channelA.Create())


wifiA = ns.wifi.WifiHelper.Default()
wifiA.SetStandard(ns.wifi.WIFI_PHY_STANDARD_80211b)
#wifiA.SetRemoteStationManager("ns3::AarfWifiManager")
wifiA.SetRemoteStationManager("ns3::ConstantRateWifiManager", "DataMode", ns.core.StringValue("DsssRate11Mbps"), "ControlMode",ns.core.StringValue("DsssRate11Mbps"))

#wifiA.SetRemoteStationManager("ns3::ConstantRateWifiManager", "DataMode", ns.core.StringValue("DsssRate11Mbps"))
macA = ns.wifi.NqosWifiMacHelper.Default()
wifiDevices = wifiA.Install(phyA, macA, wifiNodes)
'''
macA = ns.wifi.NqosWifiMacHelper.Default()
ssidA = ns.wifi.Ssid ("AP-A")

macA.SetType ("ns3::StaWifiMac", "Ssid", ns.wifi.SsidValue(ssidA), "ActiveProbing", ns.core.BooleanValue(False))
dev_ha = wifiA.Install(phyA, macA, ha)

macA.SetType("ns3::ApWifiMac","Ssid", ns.wifi.SsidValue (ssidA))
dev_apA = wifiA.Install(phyA, macA, apA)


channelB = ns.wifi.YansWifiChannelHelper.Default()
#channelB.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel")
#channelB.AddPropagationLoss("ns3::RangePropagationLossModel", "MaxRange", ns.core.DoubleValue (3.0))


phyB = ns.wifi.YansWifiPhyHelper.Default()
phyB.Set("ChannelNumber", ns.core.StringValue('2'))
#phyB.setFrequency(2400)
#phyB.Configure80211b()
phyB.SetChannel(channelA.Create())
#phyB.SetChannel(channelB.Create())


wifiB = ns.wifi.WifiHelper.Default()
wifiB.SetStandard(ns.wifi.WIFI_PHY_STANDARD_80211b)
#wifiB.SetRemoteStationManager("ns3::AarfWifiManager")

macB = ns.wifi.NqosWifiMacHelper.Default()
ssidB = ns.wifi.Ssid ("AP-B")

macB.SetType ("ns3::StaWifiMac", "Ssid", ns.wifi.SsidValue(ssidB), "ActiveProbing", ns.core.BooleanValue(False))
dev_hb = wifiB.Install(phyB, macB, hb)

macB.SetType("ns3::ApWifiMac","Ssid", ns.wifi.SsidValue (ssidB))
dev_apB = wifiB.Install(phyB, macB, apB)
'''

mobility = ns.mobility.MobilityHelper()
mobility.SetPositionAllocator ("ns3::GridPositionAllocator", "MinX", ns.core.DoubleValue(0.0), 
								"MinY", ns.core.DoubleValue (0.0), "DeltaX", ns.core.DoubleValue(2.0), "DeltaY", ns.core.DoubleValue(0.0), 
                                 "GridWidth", ns.core.UintegerValue(4), "LayoutType", ns.core.StringValue("RowFirst"))

mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")
mobility.Install(wifiNodes)


stack = ns.internet.InternetStackHelper()
stack.Install(wifiNodes)


address = ns.internet.Ipv4AddressHelper()

address.SetBase(ns.network.Ipv4Address("10.1.3.0"), ns.network.Ipv4Mask("255.255.255.0"))
wifiInterfaces = address.Assign(wifiDevices)
'''
inter_ha = address.Assign(dev_ha)
inter_apA = address.Assign(dev_apA)
inter_hb = address.Assign(dev_apA)
inter_apB = address.Assign(dev_apA)
'''
'''
address.SetBase(ns.network.Ipv4Address("10.1.4.0"), ns.network.Ipv4Mask("255.255.255.0"))
inter_hb = address.Assign(dev_hb)
inter_apB = address.Assign(dev_apB)
'''


echoServer = ns.applications.UdpEchoServerHelper(9)

serverApps = echoServer.Install(hb)
serverApps.Start(ns.core.Seconds(1.0))
serverApps.Stop(ns.core.Seconds(200.0))


#echoClient = ns.applications.UdpEchoClientHelper(inter_hb.GetAddress(0), 9)
echoClient = ns.applications.UdpEchoClientHelper(wifiInterfaces.GetAddress(2), 9)
echoClient.SetAttribute("MaxPackets", ns.core.UintegerValue(99999999))
echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds (0.1)))
echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(2000))

clientApps = echoClient.Install(apB)
clientApps.Start(ns.core.Seconds(2.0))
clientApps.Stop(ns.core.Seconds(200.0))


#Trying with onoff application
'''
sinkHelper = ns.applications.PacketSinkHelper("ns3::UdpSocketFactory",wifiInterfaces.GetAddress(2))
sinkApp = sinkHelper.Install(hb)
sinkApp.Start(ns.core.Seconds(0.0))
sinkApp.Stop(ns.core.Seconds(200.0))'''

#tostadora = ns.core.ConstantVariable(1)
#help(ns.core)
#ns.core.RandonVariableStream
'''
randomUp = ns.core.ConstantRandomVariable()

randomUp.SetAttribute("Constant",ns.core.DoubleValue(1.0))

randomDown = ns.core.ConstantRandomVariable()
randomDown.SetAttribute("Constant",ns.core.DoubleValue(1.0))
sourceHelper = ns.applications.OnOffHelper("ns3::UdpSocketFactory",wifiInterfaces.GetAddress(2))
sourceHelper.SetAttribute("OnTime",ns3.RandomVariableValue(randomUp))#RandomVariableValue Does not exist in python!!!
sourceHelper.SetAttribute("OffTime",ns3.RandomVariableValue(randomDown))
remoteAddress = ns.core.InetSocketAddress((inter_hb.getAdress(0)),9)
sourceHelper.SetAttribute("Remote",remoteAddress)
sourceHelper.SetAttribute("DataRate",ns.core.DataRateValue(ns.core.DataRate(ns.core.SringValue("1Mbps"))))
sourceHelper.SetAttribute("PacketSize",ns.core.UintegerValue(1500))

sourceApp = sourceHelper.Install(apB)
sourceApp.Start(ns.core.Seconds(1.0))
sourceApp.Stop(ns.core.Seconds(200.0))'''


ns.internet.Ipv4GlobalRoutingHelper.PopulateRoutingTables()

ns.core.Simulator.Stop(ns.core.Seconds(200.0))

phyA.EnablePcapAll("problem1-a")
'''
phyA.EnablePcap("problem1a", dev_apA.Get(0))
phyA.EnablePcap("problem1a", dev_ha.Get(0))
phyA.EnablePcap("problem1a", dev_apB.Get(0))
phyA.EnablePcap("problem1a", dev_hb.Get(0))

phyB.EnablePcap("problem2a", dev_apA.Get(0))
phyB.EnablePcap("problem2a", dev_ha.Get(0))
phyB.EnablePcap("problem2a", dev_apB.Get(0))
phyB.EnablePcap("problem2a", dev_hb.Get(0))
'''

ns.core.Simulator.Run()
ns.core.Simulator.Destroy()
