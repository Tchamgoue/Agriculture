from django.shortcuts import render
from django.http.request import HttpRequest

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
import numpy as np
import sys
import subprocess 
import json



def home(request):
    if isinstance(request, HttpRequest):
        if len(request.POST) > 0:
            pass
        else:
            return render(request, 'index.html', {
                'uid': request.session['uid'] if 'uid' in request.session.keys() else None,
                'username': request.session['username'] if 'username' in request.session.keys() else None,
            })
    else:
        print("not a request from navigator !")


@api_view(['POST'])
def analogy(request):
    similarity = []
    if request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        if tutorial_data:
            with open('/opt/Agriculture/agriculture/refs_array.json', 'w') as outfile:
                json.dump(tutorial_data, outfile)
            command = '/opt/Agriculture/agriculture/analogue_script.sh {0:f} {1:f} {2}'.format(float(tutorial_data['source_lat']), float(tutorial_data['source_long']), "refs_array.json")
            subprocess.run(command, shell=True)
            f = open('/opt/Agriculture/agriculture/similarity.json',)
            similarity = json.load(f)
            f.close()
            return JsonResponse(similarity, status=status.HTTP_200_OK, safe=False) 
        return JsonResponse("Error", status=status.HTTP_400_BAD_REQUEST)
    
