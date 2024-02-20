from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from .views import (UserRegistrationView,
                    CreateDocumentView, logoutview, getdoc, DocSearch, DocEdit, DocDelete, GetDocByIdAPIView,
                    GetUserView, ViewEditMode)

urlpatterns = [
    path('register', (UserRegistrationView.as_view()), name='user_register'),
    # path('login', UserLoginView.as_view(), name='user_login'),
    # path('getusers', GetUser.as_view()),
    path('createdocument', CreateDocumentView.as_view(), name='document-list-create'),
    path('logout', logoutview.as_view(),name='logout'),
    path('getdoc', getdoc.as_view(), name='getdoc'),
    path('docsearch', DocSearch.as_view(), name='docsearch'),
    path('editdoc', DocEdit.as_view(), name='edit_doc'),
    path('getdocid/<int:document_id>/', GetDocByIdAPIView.as_view(), name='get_doc_by_id'),
    path('deletedoc/<int:document_id>', DocDelete.as_view(), name='doc_delete'),
    path('userdetails', GetUserView.as_view(), name='authenticated-user'),
    path('viewedit', ViewEditMode.as_view(), name='viewedit')
]