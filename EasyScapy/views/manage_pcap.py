from django.http import HttpResponse,StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from EasyScapy import models
import simplejson

#@require_http_methods(["DELETE","GET"])
@csrf_exempt
@api_view(['DELETE','GET'])
def manage_pcap(request,s=0,o=0):

    SCAPY_MAMSG = "Successfully"


    val = {

        "msg":SCAPY_MAMSG,
        "detail":''
    }

    if request.method == "GET":

        return HttpResponse(models.Easyscapy.objects.all().values())

    elif request.method == "DELETE":

        delpcap(request,val)

    else:
        pass

    return HttpResponse(simplejson.dumps(val))


def delpcap(request,val):

    queryset = models.Easyscapy.objects
    ids_dict = {}
    exec("ids_dict=" + str(dict(request.DATA).keys())[3:-2])
    ids = ids_dict.values()[0]

    try:
        queryset.get(id=ids).delete()
        val['detail'] = "The id = %d recoder has been deleted successfully!" % ids

    except Exception,er:

        if "exist" in str(er):
            val['msg'] = "Failed"
            val["detail"] = "The recode 'id=%s' does not exist" % str(ids)


