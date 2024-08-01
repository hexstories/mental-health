from django.urls import path,include

app_name = 'api'



urlpatterns = [
    path('counselors/', include('apps.counselors.urls')),
    path('students/', include('apps.student.urls')),
    path('self_help/', include('apps.self_help.urls')),
    path('home/', include('apps.home.urls')),

]