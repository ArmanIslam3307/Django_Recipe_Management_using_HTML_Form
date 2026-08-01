from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Recipe, Ingredient, CustomUser

# ── Auth ─────────────────────────────────────────────────
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST.get('phone', '')
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            return render(request, 'recipes/register.html', {'error': 'Passwords do not match'})

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'recipes/register.html', {'error': 'Username already taken'})

        user = CustomUser.objects.create_user(
            username=username, email=email,
            password=password, phone=phone
        )
        login(request, user)
        return redirect('recipe_list')
    return render(request, 'recipes/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('recipe_list')
        return render(request, 'recipes/login.html', {'error': 'Invalid credentials'})
    return render(request, 'recipes/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('recipe_list')


# ── Recipe CRUD (login required) ─────────────────────────
@login_required
def recipe_list(request):
    recipes = Recipe.objects.filter(owner=request.user)
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    ingredients = recipe.ingredients.all()
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe, 'ingredients': ingredients
    })

@login_required
def recipe_create(request):
    if request.method == 'POST':
        Recipe.objects.create(
            owner=request.user,
            name=request.POST['name'],
            description=request.POST['description'],
            category=request.POST['category'],
            recipe_image=request.FILES.get('recipe_image')
        )
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_form.html', {'title': 'Add Recipe'})

@login_required
def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    if request.method == 'POST':
        recipe.name = request.POST['name']
        recipe.description = request.POST['description']
        recipe.category = request.POST['category']
        if request.FILES.get('recipe_image'):
            recipe.recipe_image = request.FILES['recipe_image']
        recipe.save()
        return redirect('recipe_detail', pk=pk)
    return render(request, 'recipes/recipe_form.html', {
        'title': 'Edit Recipe', 'recipe': recipe
    })

@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})


# ── Ingredient CRUD ──────────────────────────────────────
@login_required
def ingredient_add(request, recipe_pk):
    recipe = get_object_or_404(Recipe, pk=recipe_pk, owner=request.user)
    if request.method == 'POST':
        Ingredient.objects.create(
            recipe=recipe,
            name=request.POST['name'],
            quantity=float(request.POST['quantity']),
            unit_price=float(request.POST['unit_price'])
        )
        return redirect('recipe_detail', pk=recipe_pk)
    return render(request, 'recipes/ingredient_form.html', {
        'recipe': recipe, 'title': 'Add Ingredient'
    })

@login_required
def ingredient_update(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk, recipe__owner=request.user)
    if request.method == 'POST':
        ingredient.name = request.POST['name']
        ingredient.quantity = float(request.POST['quantity'])
        ingredient.unit_price = float(request.POST['unit_price'])
        ingredient.save()
        return redirect('recipe_detail', pk=ingredient.recipe.pk)
    return render(request, 'recipes/ingredient_form.html', {
        'ingredient': ingredient, 'recipe': ingredient.recipe, 'title': 'Edit Ingredient'
    })

@login_required
def ingredient_delete(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk, recipe__owner=request.user)
    recipe_pk = ingredient.recipe.pk
    if request.method == 'POST':
        ingredient.delete()
        return redirect('recipe_detail', pk=recipe_pk)
    return render(request, 'recipes/ingredient_confirm_delete.html', {'ingredient': ingredient})
