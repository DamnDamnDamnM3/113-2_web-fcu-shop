from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(f"Login attempt - Username: {username}, Password: {password}")
        user = authenticate(request, username=username, password=password)
        print(f"Authenticated user: {user}")
        if user is not None:
            login(request, user)
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True})
            return redirect("/")  # 登入成功後導向首頁，可依需求修改
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "error": "帳號或密碼錯誤"})
            messages.error(request, "帳號或密碼錯誤")
    return render(request, "accounts/login.html")
