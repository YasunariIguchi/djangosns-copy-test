from django.shortcuts import render

# Create your views here.
def cafe(request):
    context = {}
    return render(request, 'cafe/cafe.html', context)