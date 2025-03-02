from django.shortcuts import render, redirect
from leads.models import Agent, Client
from leads.forms import ClientForm

# Create your views here.
def lead_list(request):
    clients = Client.objects.all()
    context = {'clients': clients}
    return render(request, 'lead/lead_list.html', context)

def lead_detail(request, pk):
    client = Client.objects.get(id=pk)
    context = {'client': client}
    return render(request, 'lead/lead_detail.html', context)

def lead_add(request):
    form = ClientForm()

    if request.user.is_active:
        if request.method == 'POST':
            form = ClientForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/leads')

    context = {'form': form}
    return render(request, 'lead/lead_form.html',context)

def lead_update(request, pk):
    client = Client.objects.get(id=pk)
    form = ClientForm(instance=client)

    if request.user.is_active:
        if request.method == 'POST':
            form = ClientForm(request.POST, instance=client)
            if form.is_valid():
                form.save()
                return redirect(f'/leads/{client.id}/')

    context = {'form': form, 'client': client}
    return render(request,'lead/lead_update.html', context)

def lead_delete(request, pk):
    client = Client.objects.get(id=pk)
    client.delete()
    return redirect('/leads')

def landing_page(request):
    return render(request, 'partials/landing-page.html')