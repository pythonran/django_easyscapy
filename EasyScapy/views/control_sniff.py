from scapy.all import *
import os
from rest_framework.decorators import api_view
from django.http import HttpResponse,HttpRequest
import simplejson
from django.views.decorators.csrf import csrf_protect,csrf_exempt

@csrf_protect
@csrf_exempt
@api_view(["POST"])
def controls(request):

    SCAPY_NOSTATUS = 'no'
    SCAPY_NOPARAMS = "No this params"
    SCAPY_CORRECT = 'yes'
    SCAPY_YES = "sucessfully"
    SCAPY_NO = "failed"


    json = {
        'status': SCAPY_CORRECT,
        'msg': SCAPY_NO,
    }
    params_dict = dict(request.DATA)
    params = "./controls python2.7 /tmp/Sniff/start_sniff.py "

    exec("params_dict = " + str(params_dict.keys())[3:-2])

    params_list = params_dict.keys()


    if 'status' not in params_list:

        json['status'] = SCAPY_NOSTATUS
        json['msg'] = "The 'status' value error,must set 'start' or 'stop' "
        return HttpResponse(simplejson.dumps(json))

    else:

        json['status'] = params_dict['status']
        params = params + params_dict['status'] + ' '
        params_list.remove('status')

    plist = ['count','filter','pktcs']

    for tmp in params_list:

        if  tmp in plist and tmp != 'filter':

            ts = tmp + '=' + str(params_dict[tmp]) + ' '
            params += ts
            json[tmp] = SCAPY_CORRECT

        elif 'filter' is tmp:

            fs = tmp + '=' + "'" + str(params_dict[tmp]) + "'" + " "
            params += fs
            json[tmp] = SCAPY_CORRECT

        else:

            json[tmp] = SCAPY_NOPARAMS
            json['msg'] = SCAPY_NO
            return HttpResponse(simplejson.dumps(json))
    try:
        os.chdir("/tmp/Sniff/")
        if os.path.exists("/tmp/.EasyScapy/expid.pid") and json['status'] == 'start':
            json['msg'] = "The sniffer is running,please stop it before start anther!"
        else:
            os.system(params)

    except:
        json['exception'] = "Please wait a time while the service is busy."

    if os.path.exists("/tmp/.EasyScapy/expid.pid") and params_dict['status'] in ['start','restart']:
        json['msg'] = SCAPY_YES

    elif not os.path.exists("/tmp/.EasyScapy/expid.pid") and params_dict['status'] == 'stop':
        json['msg'] = SCAPY_YES

    return HttpResponse(simplejson.dumps(json))
