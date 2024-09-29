from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('/login/')
