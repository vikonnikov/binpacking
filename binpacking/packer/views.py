from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
import json

from bpp.general.core import TaskInfo
from bpp.box import Box, Bin
from bpp.general.general_pack import general_pack

import pyshipping
from pyshipping.package import Package
from pyshipping.binpack_simple import binpack


# Create your views here.

class IndexPageView(TemplateView):
    template_name = 'packer/index.html'

def parse_for_general(d, _class):
    args = [int(d[attr]) for attr in ('w', 'h', 'd')]
    return _class(*args)

def parse_for_heurictic(d, _class):
    args = [int(d[attr]) for attr in ('w', 'h', 'd')]
    return _class(args)

# def pack(request):
#     if request.is_ajax():
#         data = [
#             {
#                 'w': 1,
#                 'h': 1,
#                 'd': 1,
#                 'x': 0,
#                 'y': 0,
#                 'z': 0,
#             },
#             {
#                 'w': 2,
#                 'h': 2,
#                 'd': 2,
#                 'x': 1,
#                 'y': 0,
#                 'z': 0,
#             },
#             {
#                 'w': 3,
#                 'h': 3,
#                 'd': 3,
#                 'x': 3,
#                 'y': 0,
#                 'z': 0,
#             },
#         ]
#         return HttpResponse(json.dumps(data), content_type="application/json")

def pack(request):
    if request.is_ajax():
        algorithm = request.GET.get('algorithm')
        
        if algorithm == 'general':
            parse = parse_for_general
            bin_class = Bin
            box_class = Box
        elif algorithm == 'heurictic':
            parse = parse_for_heurictic
            bin_class = box_class = Package
        
        bin = parse(json.loads(request.GET.get('bin')), bin_class)

        boxes = []
        for d in json.loads(request.GET.get('boxes')):
            count = int(d['n'])
            for i in range(count):
                box = parse(d, box_class)
                boxes.append(box)
        
        if algorithm == 'general':
            info = TaskInfo(bin, boxes)
            general_pack(info, boxes)
        else:
            binpack(boxes, bin)
            bin.dbin.calc()

        # for layer in bin.dbin.items:
        #     print 'Layer', layer.items
        #     for line in layer.items:
        #         print 'Line', line.items

        data = []
        for box in boxes:
            data.append({
                'w': box.w,
                'h': box.h,
                'd': box.d,
                'x': box.x,
                'y': box.y,
                'z': box.z,})

        return HttpResponse(json.dumps(data), content_type="application/json")