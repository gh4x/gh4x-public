from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from django.contrib import messages
from .forms import SignUpForm
# Create your views here.

def home(request):
    
    form = SignUpForm(request.POST or None)
    
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.save()
        messages.success(request, 'Your in!')
        return HttpResponseRedirect('/thank-you')
    
    return render_to_response("signup.html",
                              locals(),
                              context_instance=RequestContext(request))

def thankyou(request):
    
    return render_to_response("thankyou.html",
                              locals(),
                              context_instance=RequestContext(request))

def aboutgrant(request):
    
    return render_to_response("aboutgrant.html",
                              locals(),
                              context_instance=RequestContext(request))