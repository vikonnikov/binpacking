from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
import json

# from bpp.general.core import TaskInfo
# from bpp.box import Box, Bin
# from bpp.general.general_pack import general_pack

# Create your views here.

class IndexPageView(TemplateView):
    template_name = 'packer/index.html'

def parse(d, _class):
    args = [int(d[attr]) for attr in ('w', 'h', 'd')]
    return _class(*args)

def pack(request):
    if request.is_ajax():
        data = [
            {
                'w': 1,
                'h': 1,
                'd': 1,
                'x': 0,
                'y': 0,
                'z': 0,
            },
            {
                'w': 2,
                'h': 2,
                'd': 2,
                'x': 1,
                'y': 0,
                'z': 0,
            },
            {
                'w': 3,
                'h': 3,
                'd': 3,
                'x': 3,
                'y': 0,
                'z': 0,
            },
        ]
        return HttpResponse(json.dumps(data), content_type="application/json")

# def pack(request):
#     if request.is_ajax():
#         bin = parse(json.loads(request.GET.get('bin')), Bin)
#
#         boxes = []
#         for d in json.loads(request.GET.get('boxes')):
#             count = int(d['n'])
#             for i in range(count):
#                 box = parse(d, Box)
#                 boxes.append(box)
#
#         info = TaskInfo(bin, boxes)
#         general_pack(info, boxes)
#
#         data = []
#         for box in boxes:
#             data.append({
#                 'w': box.w,
#                 'h': box.h,
#                 'd': box.d,
#                 'x': box.x,
#                 'y': box.y,
#                 'z': box.z,})
#
#         return HttpResponse(json.dumps(data), content_type="application/json")