from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserDetails
# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello from Django App")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if email already exists
        if UserDetails.objects.filter(Email=email).exists():
            return render(request, 'signup.html', {
                'error': 'Email already exists'
            })

        # Create new user
        UserDetails.objects.create(
            Username=username,
            Email=email,
            Password=password
        )

        # Redirect to login page after successful signup
        return redirect('login')

    return render(request, 'signup.html')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = UserDetails.objects.filter(
            Email=email,
            Password=password
        ).first()

        if user:
            return render(request, 'success.html')

        return render(request, 'login.html', {
            'error': 'Invalid email or password'
        })

    return render(request, 'login.html')


def get_all_users(request):
    users = UserDetails.objects.all()

    data = []
    for user in users:
        data.append({
            "username": user.Username,
            "email": user.Email,
            "password": user.Password
        })

    return JsonResponse(data, safe=False)

def get_user_by_email(request):
    email = request.GET.get('email')

    if not email:
        return JsonResponse({'error': 'Email parameter is required'})

    try:
        user = UserDetails.objects.get(Email=email)
        data = {
            'username': user.Username,
            'email': user.Email,
            'password': user.Password
        }
        return JsonResponse(data)
    except UserDetails.DoesNotExist:
        return JsonResponse({'error': 'User not found'})

def update_user(request):
    email = request.GET.get('email')
    password = request.GET.get('password')

    if not email:
        return JsonResponse({'error': 'Email is required'})

    try:
        user = UserDetails.objects.get(Email=email)

        if password:
            user.Password = password

        user.save()

        return JsonResponse({
            'message': 'User password updated successfully',
            'email': user.Email
        })

    except UserDetails.DoesNotExist:
        return JsonResponse({'error': 'User not found'})


def delete_user(request):
    email = request.GET.get('email')

    if not email:
        return JsonResponse({'error': 'Email is required'})

    try:
        user = UserDetails.objects.get(Email=email)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'})
    except UserDetails.DoesNotExist:
        return JsonResponse({'error': 'User not found'})
