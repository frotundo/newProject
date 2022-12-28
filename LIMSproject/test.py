
from django.shortcuts import render, redirect
from .forms import EditForm
from .models import MyModel

def edit_view(request, pk):
    object = MyModel.objects.get(pk=pk)

    if request.method == 'POST':
        form = EditForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect('success_url')
    else:
        form = EditForm(instance=object)

    return render(request, 'edit.html', {'form': form})



