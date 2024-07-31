from django.urls import path
from .views import CreateUpdatePhoto, FarmDetail, FarmList, PersonDetail, PersonList, PhotoList, CreateFarm, CreatePerson
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('farm/', FarmList.as_view(), name='farm_list'),
    path('farm/create/', CreateFarm.as_view(), name='create_farm'),
    path('farm/<int:pk>/', FarmDetail.as_view(), name='farm_detail'),
    
    path('person/', PersonList.as_view(), name='person_list'),
    path('person/create/', CreatePerson.as_view(), name='create_person'),
    path('person/<str:name>/', PersonDetail.as_view(), name='person_detail'),

    path('photo/', PhotoList.as_view(), name='upload_photo'),
    path('photo/upload/', CreateUpdatePhoto.as_view(), name='upload_photo'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
