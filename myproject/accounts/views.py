from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

# 1. REGISTER PAGE
def register_page(request):
    if request.method == 'POST':
        # Get form data from request
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        # Basic validation
        if not username or not password1 or not password2:
            return render(request, 'register.html', {'error': "All fields are required"})

        if password1 != password2:
            return render(request, 'register.html', {'error': "Passwords don't match"})

        try:
            # Create user manually
            user = User.objects.create_user(username=username, password=password1)
            #login(request, user)  # Auto-login after registration
            return redirect('login')  # Redirect to home after success
        except IntegrityError:  # Handle duplicate username error
            return render(request, 'register.html', {'error': "Username already exists"})
    
    # Show empty form for GET requests
    return render(request, 'register.html')

# 2. LOGIN PAGE
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        user = authenticate(request, username=username, password=password)
        if user is not None:  # If login successful
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'login.html')

# 3. LOGOUT ACTION
def logout_user(request):
    logout(request)
    return redirect('login')  # Send back to login page
from .models import Book
# 4. HOME PAGE
def home_page(request):
    if not request.user.is_authenticated:  # If not logged in
        return redirect('login')
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book_name = request.POST.get('book_name')
        book_content = request.POST.get('book_content')
        author = request.POST.get('author')

        # Basic validation
        if book_id and book_name and book_content and author:
            Book.objects.create(
                user=request.user,
                book_id=book_id,
                book_name=book_name,
                book_content=book_content,
                author=author
            )
            return redirect('home')

    # Show only books belonging to the current user
    user_books = Book.objects.filter(user=request.user)
    return render(request, 'home.html', {'books': user_books})
