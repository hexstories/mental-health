from django.urls import path,include

app_name = 'api'



urlpatterns = [
    path("appointments/", include("apps.appointment.urls")),
    path('counselors/', include('apps.counselors.urls')),
    path('students/', include('apps.student.urls')),
    path('self_help/', include('apps.self_help.urls')),
    path('home/', include('apps.home.urls')),

]