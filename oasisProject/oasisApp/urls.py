from django.urls import path
from . import views
urlpatterns = [
   path('Home', views.Home,name='Home'),
   path('', views.Login,name='Login'),
   path('RegisterPage/', views.Register,name='Register'),
   path('Logout/', views.Logout,name='Logout'),
   path('About/', views.AboutUs,name='About'),
   path('Contact/', views.ContactUs,name='Contact'),
   path('Viewhistory/', views.history,name='Viewhistory'),
   path('Chat/', views.Chat,name='Chat'),
   path('video/', views.video,name='video'),
   path('Dashboard/', views.Dashboard,name='Dashboard'),
   path('AddUser/', views.Adduser,name='AddUser'),
   path('UpdateUser/', views.UpdateUser,name='UpdateUser'),
   path('DeleteUser/', views.DeleteUser,name='DeleteUser'),
   path('Users/', views.Users,name='Users'),
   path('managecomplaints/', views.managecomplaints, name='managecomplaints'),
   path('respondcomplaint/<int:complaint_id>/', views.respond_complaint_view, name='respond_complaint'),
   path('upload/', views.upload_image, name='upload_image')
]
