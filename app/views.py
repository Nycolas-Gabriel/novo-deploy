from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomPasswordChangeForm  
from django.contrib import messages
from .forms import ItemForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES) 
        if form.is_valid():
            user = form.save()  
            messages.success(request, 'Cadastro realizado com sucesso!')  
            return redirect('login')  
        form = CustomUserCreationForm() 
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('items')  
        else:
            messages.error(request, 'Credenciais inválidas.')
    
    return render(request, 'login.html')



@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Senha alterada com sucesso!') 
            return redirect('login')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


# View para lista de itens paginada
@login_required
def item_list_view(request):
    # Obtendo o parâmetro de busca
    search_query = request.GET.get('search', '')
    
    # Filtrando itens com base na busca
    if search_query:
        item_list = Item.objects.filter(nome__icontains=search_query)  # Filtra itens pelo nome
    else:
        item_list = Item.objects.all()
        
    paginator = Paginator(item_list, 10)  # Mostra 10 itens por página
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)

    total_items = item_list.count()  # Total de itens para exibição

    return render(request, 'items.html', {'items': items, 'total_items': total_items, 'search_query': search_query})


def cadastrar_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item cadastrado com sucesso!')
            return redirect('listar_itens')  # Redireciona para a lista de itens, ou outro local de sua escolha
    else:
        form = ItemForm()

    return render(request, 'cadastrar_item.html', {'form': form})


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)