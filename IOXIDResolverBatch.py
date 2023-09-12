import sys, getopt, ipaddress, socket, eventlet
import threading
from impacket.dcerpc.v5 import transport
from impacket.dcerpc.v5.rpcrt import RPC_C_AUTHN_LEVEL_NONE
from impacket.dcerpc.v5.dcomrt import IObjectExporter


def main(argv):
    opts, args = getopt.getopt(argv, "ht:f:", ["target=","--target-file"])
    if len(opts)==0:
        print('IOXIDResolverBatch.py -t <target ip(support CIDR)> or IOXIDResolver.py -f <target ip file>')
        sys.exit(2)
    target_ip = ""
    target_file = ""

    for opt, arg in opts:
        if opt == '-h':
            print('IOXIDResolverBatch.py -t <target ip(support CIDR)> or IOXIDResolver.py -f <target ip file>')
            sys.exit()
        elif opt in ("-t", "--target"):
            target_ip = ipaddress.ip_network(arg)
        elif opt in ("-f", "--target-file"):
            target_file = open(arg)

        if target_ip != "" and target_file != "":
            print('IOXIDResolver.py -t <target ip(support CIDR)> or IOXIDResolver.py -f <target ip file>')
            sys.exit(2)

        if target_ip != "":
            for i in target_ip:
                t=threading.Thread(target=scan,args=(i,))
                t.start()
        if target_file != "":
            line = target_file.readline()
            while line:
                t = threading.Thread(target=scan, args=(line,))
                t.start()
                line = target_file.readline()


def scan(target_ip):
    target_ip = str(target_ip)
    print("[*]scanning:" + target_ip+"\n")
    authLevel = RPC_C_AUTHN_LEVEL_NONE
    stringBinding = r'ncacn_ip_tcp:%s' % target_ip
    rpctransport = transport.DCERPCTransportFactory(stringBinding)
    rpctransport.set_connect_timeout(2)
    portmap = rpctransport.get_dce_rpc()
    portmap.set_auth_level(authLevel)
    try:
         portmap.connect()
    except Exception as e:
        return 0

    objExporter = IObjectExporter(portmap)
    bindings = objExporter.ServerAlive2()

    print("[*] Retrieving network interface of " + target_ip)
    # NetworkAddr = bindings[0]['aNetworkAddr']
    for binding in bindings:
        NetworkAddr = binding['aNetworkAddr']
        print("Address: " + NetworkAddr)

if __name__ == "__main__":
    main(sys.argv[1:])