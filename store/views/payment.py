from django.shortcuts import render, get_object_or_404, redirect

def process(request):
    result = request.json()
    print(request)
    return redirect('home')