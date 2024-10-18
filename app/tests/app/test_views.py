import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.models import Item 
User = get_user_model()

@pytest.mark.django_db
def test_cadastrar_item_view(client):
    user = User.objects.create_user(username='testuser', password='testpassword123')
    client.login(username='testuser', password='testpassword123')
    
    url = reverse('cadastrar_item')
    response = client.post(url, {
        'nome': 'Novo Item',
        'descricao': 'Descrição do Novo Item'
    })
    
    assert response.status_code == 302
    assert Item.objects.count() == 1
    assert Item.objects.get(nome='Novo Item')
