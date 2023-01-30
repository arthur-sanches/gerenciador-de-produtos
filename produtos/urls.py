from django.urls import path

from .views import ProdutoList, ProdutoDetail


urlpatterns = [
    path('<int:pk>/', ProdutoDetail.as_view()),
    path('', ProdutoList.as_view()),
]