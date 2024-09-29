from django.shortcuts import render
import json
import os
import threading
import time
from django.conf import settings
from django.http import JsonResponse


def show_map(request):
    """Render the map HTML."""
    return render(request, 'map/map.html')
