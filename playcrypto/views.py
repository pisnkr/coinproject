import os
from django.conf import settings
from django.shortcuts import render
from google.cloud import storage
import datetime
# Create your views here

def main(request):
    current_date = datetime.datetime.now().strftime('%Y%m%d')

    image_path = f'https://storage.googleapis.com/jinman_team_project/btcusdt_1day_{current_date}_forecast.png'
    image_path2 = f'https://storage.googleapis.com/jinman_team_project/ethusdt_1day_{current_date}_forecast.png'

    context = {
        'image_path': image_path,
        'image_path2': image_path2,  # image_path2도 context에 추가
    }

    return render(request, 'playcrypto/index.html', context)


def charts(request):
    return render(request, 'playcrypto/charts.html')

def layout_sidenav_light(request):
    return render(request, 'playcrypto/layout_sidenav_light.html')

def layout_static(request):
    return render(request, 'playcrypto/layout_static.html')

def tables(request):
    return render(request, 'playcrypto/tables.html')