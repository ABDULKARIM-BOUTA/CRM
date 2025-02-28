from django.shortcuts import render
from leads.models import Agent, Client
from leads.forms import ClientForm
# Create your views here.
def lead_list(request):
    clients = Client.objects.all()
    context = {'clients': clients}
    return render(request, 'lead_list.html', context)

def lead_detail(request, pk):
    client = Client.objects.get(id=pk)
    context = {'client': client}
    return render(request, 'lead_detail.html', context)

def lead_form(request):
    form = ClientForm()

    if request.user.is_active:
        if request.method == 'POST':
            form = ClientForm(request.POST)
            if form.is_valid():
                form.save()

    context = {'form': form}
    return render(request, 'lead_form.html',context)