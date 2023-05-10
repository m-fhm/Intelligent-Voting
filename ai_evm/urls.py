from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from . import views 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('detect_face/',include('detect_face.urls'), name = 'detect_face'),
    path('', views.start, name = 'start'),
    path('dbg/',views.dbg, name = 'dbg'),
    path('detect_person/', include('detect_person.urls'), name = 'detect_person'),
    path('detect_mask/', include('detect_mask.urls'), name = 'detect_mask'),
    path('recognize_face/', include('recognize_face.urls'), name = 'recognize_face'),
    path('user/', include('user_control.urls'), name = 'user'),

    path('voters/', views.voter_list, name='voter_list'),
    path('voter_create/', views.voter_create, name='voter_create'),
    path('<str:pk>/update/', views.voter_update, name='voter_update'),
    path('<str:pk>/delete/', views.voter_delete, name='voter_delete'),
   
    path('parties/', views.party_list, name='party_list'),
    path('party_create/', views.party_create, name='party_create'),
    path('update/<int:pk>/', views.party_update, name='party_update'),
    path('delete/<int:pk>/', views.party_delete, name='party_delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



