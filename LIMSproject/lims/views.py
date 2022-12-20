"""LIMS views."""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    """Index view."""
    return render(request, 'base/base.html')

