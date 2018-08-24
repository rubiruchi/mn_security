#!/usr/bin/python

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.node import Node
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
import sys

class RandomFiles( Node ):

	def config( self, **params ):
		super( RandomFiles, self).config( **params )
		self.cmd("mkdir /var/www/html/ipsec")
		self.cmd("openssl rand -out /var/www/html/ipsec/10K 10000")
		self.cmd("openssl rand -out /var/www/html/ipsec/100K 100000")
		self.cmd("openssl rand -out /var/www/html/ipsec/1M 1000000")
		self.cmd("openssl rand -out /var/www/html/ipsec/10M 10000000")
		self.cmd("openssl rand -out /var/www/html/ipsec/100M 100000000")

	def terminate( self ):
		self.cmd("rm -r /var/www/html/ipsec")
		super( RandomFiles, self ).terminate()

class LimitedBwTopo(Topo):
    
	"N hosts connected through a switch"

	def build(self, bandwidth=10):
	
		bandwidth=int(bandwidth)
	
		# Add hosts and switch
		centralSwitch = self.addSwitch('s1')
		hostAlice = self.addHost('alice', ip='10.0.0.1/24', cls=RandomFiles, mac='00:00:00:00:00:01')
		hostBob = self.addHost('bob', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
	
		self.addLink( centralSwitch, hostAlice, bw=bandwidth)
		self.addLink( centralSwitch, hostBob, bw=bandwidth)
        
def limitedBwTopo(): 
	if(len(sys.argv) > 1 and sys.argv[1].isdigit()):
		topo = LimitedBwTopo(sys.argv[1])
	else:
		topo = LimitedBwTopo()
	net = Mininet(topo, link=TCLink)
	net.start()
	CLI(net)
	net.stop()


if __name__ == '__main__':
	setLogLevel( 'info' )
	limitedBwTopo() 
