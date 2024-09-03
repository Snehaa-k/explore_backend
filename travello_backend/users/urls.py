from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('register/', views.RegisterationApi.as_view(),name="register"),
    path('otpverify/',views.VerifyOtp.as_view(),name = 'verify_otp'),
    path('selectingrole/',views.SelectinTravelleader.as_view(),name = 'selecting-role'),
    path('userpreference/',views.Userpreference.as_view(),name = 'preference1'),
    path('login/',views.CustomTokenObtainPairView.as_view(),name = 'login'),           
    path('send/',views.SendOTPView.as_view(),name = 'send'),
    path('formsubmission/',views.FormSubmissionView.as_view(),name = 'form'),
    path('formview/',views.TravelLeaderListView.as_view(),name = 'formview'),
    path('details/<int:id>/',views.TravelLeaderDetailView.as_view(),name = 'details'),
    path('accept/<int:pk>/', views.AcceptTravelLeaderView.as_view(), name='accept_travel_leader'),
    path('reject/<int:pk>/', views.RejectTravelLeaderView.as_view(), name='reject_travel_leader'),
    path('travellers/', views.TravellersView.as_view(), name='travellers'),
    path('block/<int:pk>/', views.is_Block.as_view(), name='block'),
    path('travellerprofile/', views.TravellerProfile.as_view(), name='travellerprofile'),
    path('editprofile/', views.UserProfileEdit.as_view(), name='editprofile'),
    path('profile/', views.UserProfileCreate.as_view(), name='udateprofile'),
    path('createtrip/', views.CreateTrip.as_view(), name='createtrip'),
    path('viewtrip/', views.ViewTrips.as_view(), name='viewtrip'),
    path('updatetrip/', views.EditTrips.as_view(), name='updatetrip'),
    path('addplaces/', views.AddPlaces.as_view(), name='addplaces'),
    path('viewplaces/<int:id>/', views.ViewPlaces.as_view(), name='viewplaces'),
    path('editplaces/<int:id>/', views.EditPlace.as_view(), name='editplaces'),
    path('deleteplaces/<int:id>', views.DeleteItem.as_view(), name='delete'),
    path('viewalltrips/', views.ViewAllTrips.as_view(), name='view_all_trips'),
    # path('token/refresh/', views.RefreshTokenAPIView.as_view(), name='token_refresh'),







   
    

 



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)