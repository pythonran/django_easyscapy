import simplejson
from pyshark import *
from rest_framework.decorators import api_view
from django.http import HttpResponse
from EasyScapy import models
#from threading import Thread
import sys
# Create your views here.

Max_json_length = 200
count = 0
# MSG_YES = "successfully"
# MSG_NO = "failed"
MSG_CODE = (0,1)
display_json = {
                'code': MSG_CODE[1],
                'msg' : '',
                'packets': [],
}

start_time = -1
over_time = -1
str = 'null'

@api_view(['GET'])
def decode_pcap(request,s,o,length = 200):

    global Max_json_length,start_time,over_time,count
    Max_json_length = length
    queryset = models.Easyscapy.objects
    start_time = s
    over_time = o

    dst = queryset.extra(where=['stime < %s and otime > %s'], params=[s, o])

    if not dst.count():
        dst = queryset.extra(where=['stime < %s and otime > %s'], params=[o, s])

    queryset_fp = dst.values('filepath')
    fplist = []

    for fp in queryset_fp:

         fplist.append(fp['filepath'])

    if not fplist:
        display_json['msg'] = 'There is no packet for a given time period!'

    for fname in fplist:

        fp = '/tmp/.EasyScapy/pcapfiles/%s' % fname
        file_num = fplist.index(fname) + 1
        display_json["msg"] = "%d pcap files has been analyzed!" % file_num

        cap = FileCapture(fp,keep_packets=False)
        cap.load_packets(timeout=5)

        if len(cap) == 0:

            return HttpResponse("No packets found")
        try:
            cap.apply_on_packets(decode_pkts)

        except SystemExit,val:

            display_json['code'] = MSG_CODE[0]
            cap.clear()
            cap.close()
            break

        cap.close()

    return HttpResponse(simplejson.dumps(display_json))

def decode_pkts(pkt):

    global count, display_json,Max_json_length,start_time,over_time,str
    pktinfo = {}

    # try:
    #     print pkt.tcp.port,"####",pkt.tcp.srcport,"####",pkt.tcp.dstport,"####\n"
    # except:
    #     try:
    #         print pkt.udp.port,"@@@@",pkt.udp.srcport,"@@@@",pkt.udp.dstport,"@@@@"
    #     except:
    #         print pkt

    if pkt.sniff_timestamp < over_time and pkt.sniff_timestamp > start_time:

        count += 1

        if count <= Max_json_length:
            new_prols_key = pkt.layers[-1].layer_name

            if count == 1:
                display_json['packets'].append({})
            else:
                pass

            if display_json['packets'][0] == {}:

                display_json['packets'][0]['total'] = 1

            else:

                display_json['packets'][0]['total'] += 1

            if new_prols_key in display_json['packets'][0].keys():

                display_json['packets'][0][new_prols_key] += 1

            else:

                display_json['packets'][0][new_prols_key] = 1

            pktinfo['time'] = pkt.sniff_timestamp
            pktinfo['prols'] = new_prols_key

            try:

                pktinfo['src'] = pkt.ip.src
                pktinfo['dst'] = pkt.ip.dst
                pktinfo['srcport'] = pkt.tcp.srcport
                pktinfo['dstport'] = pkt.tcp.dstport

            except:

                try:
                    pktinfo['src'] = pkt.ipv6.src
                    pktinfo['dst'] = pkt.ipv6.dst
                    pktinfo['srcport'] = pkt.udp.srcport
                    pktinfo['dstport'] = pkt.udp.dstport
                except:
                    pass

            pktinfo['length'] = pkt.length
            display_json['packets'].append(pktinfo)
        else:
            sys.exit(1)
    elif pkt.sniff_timestamp > over_time:

        display_json['code'] = MSG_CODE[1]
        display_json["msg"] = "Quantity is not enough, but the time is up!"

    else:
        pass