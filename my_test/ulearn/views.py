from django.shortcuts import render, redirect
import pandas as pd
import json
import math
import numpy as np

def index_page(request):
    return render(request, 'index.html')


def demand(request):
    return render(request, 'demand.html', )

