from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import sys
import time
import os

#print os.getcwd()
PHASE1_LOG = os.path.expanduser('~') + '/ik2220-assign-phase1-team6/results/phase_1_report'
#PHASE1_LOG = 'PHASE1_LOG'
 
class MyTopo(Topo):

    def __init__( self ):
        Topo.__init__( self )

	h1 = self.addHost('h1', ip = '100.0.0.11/24', mac='00:00:00:00:00:11')
	h2 = self.addHost('h2', ip = '100.0.0.12/24', mac='00:00:00:00:00:12')
	h3 = self.addHost('h3', ip = '100.0.0.51/24', mac='00:00:00:00:00:51')
	h4 = self.addHost('h4', ip = '100.0.0.52/24', mac='00:00:00:00:00:52')

	ds1 = self.addHost('ds1', ip = '100.0.0.20/24', mac='00:00:00:00:00:20')
	ds2 = self.addHost('ds2', ip = '100.0.0.21/24', mac='00:00:00:00:00:21')
	ds3 = self.addHost('ds3', ip = '100.0.0.22/24', mac='00:00:00:00:00:22')

	ws1 = self.addHost('ws1', ip = '100.0.0.40/24', mac='00:00:00:00:00:40')
	ws2 = self.addHost('ws2', ip = '100.0.0.41/24', mac='00:00:00:00:00:41')
	ws3 = self.addHost('ws3', ip = '100.0.0.42/24', mac='00:00:00:00:00:42')

	insp = self.addHost('insp', ip = '100.0.0.30/24', mac='00:00:00:00:00:30')

	sw1 = self.addSwitch('sw1')
	sw2 = self.addSwitch('sw2')
	sw3 = self.addSwitch('sw3')
	sw4 = self.addSwitch('sw4')
	sw5 = self.addSwitch('sw5')

	fw1 = self.addSwitch('fw6')
	fw2 = self.addSwitch('fw7')

	lb1 = self.addSwitch('lb8')
	lb2 = self.addSwitch('lb9')

	ids = self.addSwitch('ids10')
	napt = self.addSwitch('napt11')

	self.addLink(ds1,sw3)
	self.addLink(ds2,sw3)
	self.addLink(ds3,sw3)
	self.addLink(sw3,lb1)
	self.addLink(lb1,sw2)
	self.addLink(sw2,ids)
	self.addLink(ids,insp)
	self.addLink(ids,lb2)
	self.addLink(lb2,sw4)
	self.addLink(sw4,ws1)
	self.addLink(sw4,ws2)
	self.addLink(sw4,ws3)
	self.addLink(sw1,h1)
	self.addLink(sw1,h2)
	self.addLink(sw1,fw1)
	self.addLink(fw1,sw2)
	self.addLink(sw2,fw2)
	self.addLink(fw2,napt)
	self.addLink(napt,sw5)
	self.addLink(sw5,h3)
	self.addLink(sw5,h4)


def Phase1():
    c0 = RemoteController('c0', ip='127.0.0.1', port=6633)
    net = Mininet(topo=MyTopo(), controller=c0)
    net.start()

    ds1 = net.get('ds1')
    ws1 = net.get('ws1')

    ds1.cmd('python dns.py &')
    ws1.cmd('python -m SimpleHTTPServer 80 &')

    #CLI(net)
    test(net)
    net.stop()

def test(net):
    log = open(PHASE1_LOG, 'w+') 

    h1 = net.get('h1')
    h3 = net.get('h3')
    ds1 = net.get('ds1')
    ws1 = net.get('ws1')
    
    #1 h1 icmp h3
    result=h1.cmdPrint('ping -c1', h3.IP())
    log.write('===Case 1. h1 ping h3===\n'+result+'\n\n')

    #2 h3 icmp h1
    result=h3.cmdPrint('ping -c1', h1.IP())
    log.write('===Case 2. h3 ping h1===\n'+result+'\n\n')

    #3 h1 icmp ds1
    result=h1.cmdPrint('ping -c1', ds1.IP())
    log.write('===Case 3. h1 ping ds1===\n'+result+'\n\n')

    #4 h3 icmp ds1
    result=h3.cmdPrint('ping -c1', ds1.IP())
    log.write('===Case 4. h3 ping ds1===\n'+result+'\n\n')

    #5 h3 TCP ws1
    result=h3.cmdPrint('curl ', ws1.IP())
    log.write('===Case 5. h3 curl ws1===\n'+result+'\n\n')

    #6 h1 TCP ws1
    result=h1.cmdPrint('curl ', ws1.IP())
    log.write('===Case 6. h1 curl ws1===\n'+result+'\n\n')

    #7 h3 UDP ds1
    dig = ''.join(['dig @', ds1.IP(), ' server1.com'])
    result=h3.cmdPrint(dig)
    log.write('===Case 7. h3 dig ds1===\n'+result+'\n\n')
    
    #8 h1 UDP ds1
    dig = ''.join(['dig @', ds1.IP(), ' server1.com'])
    result=h1.cmdPrint(dig)
    log.write('===Case 8. h1 dig ds1===\n'+result+'\n\n')

    log.close()

if __name__ == '__main__':
    setLogLevel('info')
    Phase1()

