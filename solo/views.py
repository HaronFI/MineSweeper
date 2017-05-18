from django.shortcuts import render,redirect
from django.http import HttpResponse
import time


def index(request):

	return render(request, 'solo/index.html')
	
def processing(request):

	return render(request, 'solo/processing.html')
