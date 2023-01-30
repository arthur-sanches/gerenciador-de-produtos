from django.urls import path

from .views import ProdutoList, ProdutoDetail, ProdutoImportCSV, ProdutoExportCSV


urlpatterns = [
    path('<int:pk>/', ProdutoDetail.as_view()),
    path('', ProdutoList.as_view()),
    path('import-csv/', ProdutoImportCSV.as_view(), name='import-csv'),
    path('export-csv/', ProdutoExportCSV.as_view(), name='export-csv'),
]