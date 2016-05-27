from django.conf.urls import patterns, include, url

from . import view

urlpatterns = patterns('',


    url(r'analysis/(?P<s>\d+(\.\d+)?)/(?P<o>\d+(\.\d+)?)/$', view.decode_pcap.decode_pcap),


    url(r'pcapfiles/((?P<s>(-)?\d+(\.\d+)?)/((?P<o>\d+(\.\d+)?)/))?' , view.manage_pcap.manage_pcap),


    url(r'sniffer/', view.control_sniff.controls),



)