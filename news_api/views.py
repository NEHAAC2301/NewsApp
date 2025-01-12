
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
API_KEY = '371cd36dae2db9a650f241adea89b572'

def home(request):
    """
    Display some general details or top headlines on the home page.
    """
    url = f'https://gnews.io/api/v4/top-headlines?apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])  # Handle cases where 'articles' might be missing

    context = {
        'articles': articles[:5],  # Display only the top 5 articles on the home page
    }
    return render(request, 'news_api/home.html', context)

def search_news(request):
    """
    Handle user input and display news based on search criteria.
    """
    country = request.GET.get('country')
    category = request.GET.get('category')
    
    articles = []
    if country:
        url = f'https://gnews.io/api/v4/search?q=example&country={country}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data.get('articles', [])
    elif category:
        url = f'https://gnews.io/api/v4/top-headlines?category={category}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data.get('articles', [])

    context = {
        'articles': articles,
    }
    return render(request, 'news_api/search.html', context)



# User login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

# Admin login view (if you have a custom admin)
def admin_login(request):
    if request.method == 'POST':
        admin_username = request.POST['admin_username']
        admin_password = request.POST['admin_password']
        admin = authenticate(request, username=admin_username, password=admin_password)
        
        if admin is not None and admin.is_staff:  # Admin check (is_staff)
            login(request, admin)
            return redirect('admin_dashboard')  # Redirect to an admin dashboard or a specific admin page
        else:
            messages.error(request, 'Invalid admin credentials')
    return render(request, 'login.html')  # Re-render the login page if credentials are incorrect
