from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem, Favorite
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

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


def logout_view(request):
    logout(request)
    return JsonResponse({"success": True})


@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        product_name = request.POST.get("product_name")
        price = float(request.POST.get("price"))

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={
                "product_name": product_name,
                "price": price,
                "quantity": quantity,
            },
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({"success": True, "message": "商品已加入購物車"})
    return JsonResponse({"success": False, "error": "無效的請求"})


@login_required
def update_cart_item(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        quantity = int(request.POST.get("quantity", 1))

        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({"success": True})
        except CartItem.DoesNotExist:
            return JsonResponse({"success": False, "error": "商品不存在"})
    return JsonResponse({"success": False, "error": "無效的請求"})


@login_required
def remove_cart_item(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")

        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            return JsonResponse({"success": True})
        except CartItem.DoesNotExist:
            return JsonResponse({"success": False, "error": "商品不存在"})
    return JsonResponse({"success": False, "error": "無效的請求"})


@login_required
def get_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    cart_data = [
        {
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product_name,
            "price": float(item.price),
            "quantity": item.quantity,
        }
        for item in items
    ]
    return JsonResponse({"items": cart_data})


@login_required
@require_POST
def add_to_favorites(request):
    try:
        data = json.loads(request.body)
        product_id = data.get("product_id")
        product_name = data.get("product_name")
        price = data.get("price")

        if not all([product_id, product_name, price]):
            return JsonResponse({"success": False, "error": "缺少必要資訊"})

        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            product_id=product_id,
            defaults={"product_name": product_name, "price": price},
        )

        if not created:
            return JsonResponse({"success": False, "error": "商品已在收藏清單中"})

        return JsonResponse({"success": True, "message": "已加入收藏"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
@require_POST
def remove_from_favorites(request):
    try:
        data = json.loads(request.body)
        product_id = data.get("product_id")

        if not product_id:
            return JsonResponse({"success": False, "error": "缺少商品ID"})

        Favorite.objects.filter(user=request.user, product_id=product_id).delete()
        return JsonResponse({"success": True, "message": "已從收藏清單中移除"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def get_favorites(request):
    try:
        favorites = Favorite.objects.filter(user=request.user)
        favorites_list = [
            {
                "id": fav.id,
                "product_id": fav.product_id,
                "product_name": fav.product_name,
                "price": float(fav.price),
            }
            for fav in favorites
        ]
        return JsonResponse({"success": True, "favorites": favorites_list})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
