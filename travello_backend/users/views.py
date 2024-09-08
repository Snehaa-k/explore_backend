from datetime import datetime, timezone
import json
from tokenize import TokenError
from django.shortcuts import render
from .models import Post, Usermodels,UserProfile,TravelLeaderForm,Country,Trips,Place,ArticlePost,Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions,generics
from .serializer import UserSerializer,ProfileSerializer,FormSubmission,TripSerializer,PlaceSerializer,PostSerializer,ArticleSerilizer,CommentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import update_last_login
from django.contrib.contenttypes.models import ContentType
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db.models import Case, When

# Create your views here.

class RegisterationApi(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            return Response({"message": "User created successfully. OTP sent.",
                             "user": user_data }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class VerifyOtp(APIView):
    def post(self,request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        print(email,"hiii")
        
        print(otp)
        try:
            user = Usermodels.objects.get(email= email)
            print(user)
            print(user.otp)
        except Usermodels.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        
        
    
        if user.otp == otp:
            user.is_verified = True
            user.otp = ''
            # user.otp_expiration = None  
            user.save()
            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        
        else: 
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)


class SelectinTravelleader(APIView):
    def post(self,request):
        email = request.data.get('email')
        role = request.data.get('role')
        roles = "traveller"
        print(email,"hiii")
        print(role)
        try:
            user = Usermodels.objects.get(email= email)
            print(user)
        except Usermodels.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
        if role == "traveller":
            user.is_travel_leader = False
        elif role == "travel_leader":
            user.is_travel_leader = True
        else:
            return Response({"error": "Invalid role selection."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.save()
        user_data = UserSerializer(user).data
        return Response({"message": "Role selected successfully.","user": user_data }, status=status.HTTP_200_OK)

class Userpreference(APIView):
    def post(self,request):
        email = request.data.get('email')
        preference = request.data.get('selectedPreference')
       
        print(email,"hiii")
        print(preference)
        try:
            user = Usermodels.objects.get(email= email)
            print(user)
        except Usermodels.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
        if preference:
            user.user_preference = preference
       
        else:
            return Response({"error": "Invalid role selection."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.save()
        user_data = UserSerializer(user).data
        return Response({"message": "preference selected successfully.","user": user_data }, status=status.HTTP_200_OK)


class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = Usermodels.objects.get(email=email)
            if not user.is_verified:
                user.generate_otp()  
                return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User is already verified."}, status=status.HTTP_400_BAD_REQUEST)
        except Usermodels.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        


# class resendOtp(APIView):
#     def post(self,request):
#         email = request.data.get('email')
#         try:
#             user = Usermodels.objects.get(email = email)
#             user.generate_otp()
#             return Response({"messege":"OTP sent successfully."},status = status.HTTP_200_OK)
#         except Usermodels.DoesNotExist:
#             return Response({"messege":"User not found."},status=status.HTTP_404_NOT_FOUND)





class CustomTokenObtainPairView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        print(f"emailfail{email}")
        try:
            user = Usermodels.objects.get(email=email)
        except Usermodels.DoesNotExist:
            return Response({'error': 'User not found or invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        
        if not check_password(password, user.password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
       

        
        
        if user.is_superuser == False:

        
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
               
               
            })
        else:
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'admin': UserSerializer(user).data
            })


class FormSubmissionView(APIView):
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request):
        user = request.data.get('email')
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        visited_countries = request.data.getlist('selectedCountries[]') 
        # email = request.data.get('email')
        mobile = request.data.get('mobile')
        cv_file = request.FILES.get('cvFile')
        id_file = request.FILES.get('idFile')
        
        try:
            user_id = Usermodels.objects.get(email=user)
            print(user)
        except Usermodels.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if not all([firstname, lastname, user, mobile]):
            return Response({"error": "Missing required fields"}, status=400)
        
        
        form_submission = TravelLeaderForm.objects.create(
            user_id = user_id,
            firstname=firstname,
            lastname=lastname,
            email=user,
            mobile=mobile,
            cv=cv_file,
            id_proof=id_file

        )
        for country_name in visited_countries:
            country, created = Country.objects.get_or_create(name=country_name)
            form_submission.visited_countries.add(country)
        form_submission.save()
        
        # Return a success response
        return Response({"message": "Form submitted successfully."}, status=200)


class TravelLeaderListView(generics.ListAPIView):
    serializer_class = FormSubmission

    def get_queryset(self):
       
        queryset = TravelLeaderForm.objects.select_related('user_id')

       
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(is_approved=status_filter)

        
        ordering = Case(
            When(is_approved='pending', then=0),
            When(is_approved='accepted', then=1),
            When(is_approved='rejected', then=2),
        )

        return queryset.order_by(ordering)




class TravelLeaderDetailView(generics.RetrieveAPIView):
    queryset = TravelLeaderForm.objects.select_related('user_id').prefetch_related('visited_countries')
    serializer_class = FormSubmission
    lookup_field = 'id'
    def get(self, request, *args, **kwargs):
        print(f"Requested ID: {kwargs.get('id')}")
        return super().get(request, *args, **kwargs)


class AcceptTravelLeaderView(APIView):
  
    # permission_classes = [IsAuthenticated]
    def post(self, request, pk, *args, **kwargs):
        
       
        try:
            form = TravelLeaderForm.objects.get(id=pk)
            user = Usermodels.objects.get(email = form.user_id.email)
        except TravelLeaderForm.DoesNotExist:
            return Response({'error': 'Travel Leader Form not found'}, status=status.HTTP_404_NOT_FOUND)
        
        form.is_approved = "accepted"
        form.save()
        user.is_approve_leader=True
        user.save()
        
        return Response({'status': 'Accepted'}, status=status.HTTP_200_OK)


class RejectTravelLeaderView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, pk, *args, **kwargs):
       
        try:
            form = TravelLeaderForm.objects.get(id=pk)
            user = Usermodels.objects.get(email = form.user_id.email)
            
        except TravelLeaderForm.DoesNotExist:
            return Response({'error': 'Travel Leader Form not found'}, status=status.HTTP_404_NOT_FOUND)
        
        form.is_approved = "rejected"
        form.save()
        user.is_approve_leader=True
        user.save()
      
        return Response({'status': 'Rejected'}, status=status.HTTP_200_OK)


class TravellersView(generics.ListAPIView):
    queryset = Usermodels.objects.filter(~Q(is_superuser=True) & ~Q(is_travel_leader=True))
    serializer_class = UserSerializer



class is_Block(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, pk, *args, **kwargs):
       
        try:
           user = Usermodels.objects.get(id = pk)  
        except Usermodels.DoesNotExist:
            return Response({'error': 'Travel Leader Form not found'}, status=status.HTTP_404_NOT_FOUND)
        user.is_block = not user.is_block
        user.save()
        return Response({'status': 'Rejected'}, status=status.HTTP_200_OK)


class TravellerProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            
            user = Usermodels.objects.get(id=request.user.id)

            
            try:
                detail = UserProfile.objects.get(user=request.user.id)
                user_serializer = UserSerializer(user)

                profile_serializer = ProfileSerializer(detail)
                return Response({"profile":profile_serializer.data,"user":user_serializer.data}, status=status.HTTP_200_OK)
            except UserProfile.DoesNotExist:
                
                user_serializer = UserSerializer(user)
                return Response({"user":user_serializer.data}, status=status.HTTP_200_OK)

        except Usermodels.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    

        


    

class UserProfileEdit(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        print(user_id)
        try:
            profile = Usermodels.objects.get(id=user_id)

            print(profile)
            
        except Usermodels.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(profile)
        return Response(serializer.data)
    

    

class UserProfileCreate(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        print(request.data)
        
        
        userprofile, created = UserProfile.objects.get_or_create(user_id=user_id)
        
        address = request.data.get('address')
        bio = request.data.get('bio')
        country_state = request.data.get('country_state')
        image_file = request.FILES.get('profile_image') 
        
        if image_file:
            userprofile.profile_image = image_file
        
        userprofile.address = address
        userprofile.bio = bio
        userprofile.country_state = country_state
        userprofile.save()
        
        if created:
            message = "Profile created successfully"
        else:
            message = "Profile updated successfully"
        
        return Response({"message": message}, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        print(user_id)
        try:
            profile = UserProfile.objects.get(user=user_id)

            print(profile)
            
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class CreateTrip(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print(request.data,"hii")
        print(request.user.id)
        try:
            user = Usermodels.objects.get(id = request.user.id)
        
        except Usermodels.DoesNotExist:
            return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TripSerializer(data=request.data,context={'request': request})

        if serializer.is_valid():
            trip = serializer.save()
            user_data = TripSerializer(trip).data
            return Response({"message": "trip created successfully",
                             "user": user_data }, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewTrips(APIView):
     def get(self, request, *args, **kwargs):
        user_id = request.user.id
        print(user_id)
        try:
            trip = Trips.objects.filter(travelead=user_id)

            print(trip)
            
        except Trips.DoesNotExist:
            return Response({'error': 'trip not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TripSerializer(trip,many=True,context={'request': request})
        # print(serializer.data)
        return Response({'trip':serializer.data}, status=status.HTTP_201_CREATED)
     


class EditTrips(APIView):
    
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        trip_id = request.data.get('id')
        print(trip_id,"trip-id")
        print(request.data)
        
        try:
            trips, created = Trips.objects.get_or_create(id = trip_id)
        except Trips.DoesNotExist:
            return Response({'error': 'trip not found'}, status=status.HTTP_404_NOT_FOUND)

        


        
        accommodation = request.data.get('accommodation')
        transportation = request.data.get('transportation')
        participant = request.data.get('participant_limit')
        amount = request.data.get('amount')
        duration = request.data.get('duration') 
        start_date = request.data.get('start_date')
        
        
        
        trips.accomodation = accommodation
        trips.transportation = transportation
        trips.participant_limit = participant
        trips.duration = duration
        trips.start_date = start_date
        trips.amount = amount
        trips.save()
        
        if created:
            message = "trip created successfully"
        else:
            message = "trip updated successfully"
        
        return Response({"message": message}, status=status.HTTP_200_OK)

class AddPlaces(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print(request.data,"hii")
        trip_id = request.data.get('tripId')
        print(trip_id)
        try:
            trip  = Trips.objects.get(id = trip_id )
        
        except Trips.DoesNotExist:
            return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlaceSerializer(data=request.data)

        if serializer.is_valid():
            trip = serializer.save()
            user_data = PlaceSerializer(trip).data
            return Response({"message": "places added successfully. OTP sent.",
                             "places": user_data }, status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   




class ViewPlaces(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,id, *args, **kwargs):
        
        # trip_id = request.data.get('tripId')
        user = Usermodels.objects.get(id = request.user.id)
        if user:
        
        # print(trip_id)
            try:
                trip_obj = Trips.objects.get(id = id)
                trip = Place.objects.filter(trip = trip_obj)
                print("asdfasdfasdf",trip)
            except Trips.DoesNotExist:
                return Response({'error': 'trip not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = PlaceSerializer(trip,many=True)
            # print(serializer.data)

            return Response({'trip':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)


class EditPlace(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id, *args, **kwargs):
        user_id = request.user.id
        place_name = request.data.get('place_name')
        accommodation = request.data.get('accomodation')
        transportation = request.data.get('transportation')
        description = request.data.get('description')
        
       
        try:
            place = Place.objects.get(id=id)
        except Place.DoesNotExist:
            return Response({'error': 'Place not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            trip = Trips.objects.get(id=request.data.get('trip_id'), travelead=user_id)
        except Trips.DoesNotExist:
            return Response({'error': 'Trip not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)

        place.trip = trip  
        place.place_name = place_name
        place.accomodation = accommodation
        place.Transportation = transportation
        place.description = description

        place.save()

        return Response({"message": "Place updated successfully"}, status=status.HTTP_200_OK)


class DeleteItem(APIView):
    def delete(self, request, id, *args, **kwargs):
        try:
            item = Place.objects.get(id=id)
            item.delete()
            return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)
        except Place.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)   


class ViewAllTrips(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        print(user_id)
        try:
            user = Usermodels.objects.get(id = user_id)
        except Usermodels.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        if user:

            try:
                trip = Trips.objects.select_related('travelead').all()
                # print(trip)
                
            except Trips.DoesNotExist:
                return Response({'error': 'trip not found'},status=status.HTTP_404_NOT_FOUND)
            
        

        
        serializer = TripSerializer(trip,many=True,context={'request': request})
        return Response({'trip':serializer.data}, status=status.HTTP_201_CREATED)


class TripDetails(APIView):
    def get(self, request,id, *args, **kwargs):
        user_id = request.user.id
        print(user_id)
        try:
            user = Usermodels.objects.get(id = user_id)
        except Usermodels.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        if user:

            try:
                trip = Trips.objects.select_related('travelead').get(id = id)
                print(trip)
                
            except Trips.DoesNotExist:
                return Response({'error': 'trip not found'},status=status.HTTP_404_NOT_FOUND)
            
        

        
        serializer = TripSerializer(trip,context={'request': request})
        return Response({'trip':serializer.data}, status=status.HTTP_201_CREATED)

    
class PlaceDetails(APIView):
    def get(self, request,id, *args, **kwargs):
        user_id = request.user.id
        print(user_id)
        try:
            user = Usermodels.objects.get(id = user_id)
        except Usermodels.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        if user:

            try:
                trip = Place.objects.select_related('trip').filter( trip = id)
                # print(trip)
                
            except Place.DoesNotExist:
                return Response({'error': 'trip not found'},status=status.HTTP_404_NOT_FOUND)
            
        

        
        serializer = PlaceSerializer(trip,many=True)
        return Response({'trip':serializer.data}, status=status.HTTP_201_CREATED)



class PostCreation(APIView):
    def post(self, request):
        try:
            user = Usermodels.objects.get(id=request.user.id)
        except Usermodels.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(data=request.data, context={'request': request})


        if serializer.is_valid():
            post = serializer.save()
            post_data = PostSerializer(post).data
            # print(post_data)
            return Response({"message": "Post created successfully.", "posts": post_data}, status=status.HTTP_201_CREATED)
        
        # Debugging line to show errors
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ArticlePosts(APIView):
    def post(self, request):
        try:
            user = Usermodels.objects.get(id=request.user.id)
        except Usermodels.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ArticleSerilizer(data=request.data, context={'request': request})


        if serializer.is_valid():
            post = serializer.save()
            post_data = ArticleSerilizer(post).data
            # print(post_data)
            return Response({"message": "Post created successfully.", "posts": post_data}, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class ViewPosts(APIView):
    def get(self, request, *args, **kwargs):
        try:
            
            user = Usermodels.objects.get(id=request.user.id)
            
            try:
                posts = Post.objects.select_related('travel_leader')
                article = ArticlePost.objects.select_related('travel_leader')
                print(article)
                

                posts_serializer = PostSerializer(posts,many=True,context={'request': request})
                article_serilizer = ArticleSerilizer(article,many=True)

                # print(posts_serializer.data)
                return Response({"posts":posts_serializer.data,"article":article_serilizer.data}, status=status.HTTP_200_OK)
            except Post.DoesNotExist:
                
                return Response({"message":"no posts"}, status=status.HTTP_404_NOT_FOUND)

        except Usermodels.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)


class ViewArticle(APIView):
    def get(self, request, *args, **kwargs):
        try:
            
            user = Usermodels.objects.get(id=request.user.id)
            
            try:
                article = ArticlePost.objects.select_related('travel_leader')
                print(article)
                

                article_serilizer = ArticleSerilizer(article,many=True,context={'request': request})
                # print(posts_serializer.data)
                return Response({"article":article_serilizer.data,}, status=status.HTTP_200_OK)
            except Post.DoesNotExist:
                
                return Response({"message":"no posts"}, status=status.HTTP_404_NOT_FOUND)

        except Usermodels.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        



class ViewUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            user = Usermodels.objects.get(id = user_id)
            profile_img = UserProfile.objects.get(user = user)
        except Usermodels.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user_serializer = UserSerializer(user)
        profile = ProfileSerializer(profile_img)
        print(user_serializer)
        return Response({"user":user_serializer.data,"profile":profile.data}, status=status.HTTP_200_OK)
    

# comment and likes section..................

class LikeTravelPostAPIView(APIView):
    def post(self, request, id):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            message = "Like removed"
        else:
            post.likes.add(request.user)
            message = "Like added"

        serializer = PostSerializer(post, context={'request': request})
        likes_count = post.likes.count()
        print(likes_count)
        return Response({'message': message, 'data': serializer.data,'likes':likes_count}, status=status.HTTP_200_OK)




class LikeArticleView(APIView):
    def post(self, request, id):
        try:
            article = ArticlePost.objects.get(id=id)
        except ArticlePost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)
            message = "Like removed"
        else:
            article.likes.add(request.user)
            message = "Like added"

        serializer = PostSerializer(article, context={'request': request})
        likes_count = article.likes.count()
        print(likes_count)
        return Response({'message': message, 'data': serializer.data,'likes':likes_count}, status=status.HTTP_200_OK)


# comment section.................

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  

    def create(self, request, *args, **kwargs):
        content_type = request.data.get('content_type')
        object_id = request.data.get('object_id')
        text = request.data.get('text')

        try:
            content_type_obj = ContentType.objects.get(id=content_type)
        except ContentType.DoesNotExist:
            return Response({"error": "Invalid content type"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            user=request.user,
            content_type=content_type_obj,
            object_id=object_id,
            text=text,
        )

        serializer = self.get_serializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')

        try:
            content_type_obj = ContentType.objects.get(id=content_type)
        except ContentType.DoesNotExist:
            return Comment.objects.none()

        return Comment.objects.filter(content_type=content_type_obj, object_id=object_id)





    









    

    
    
    
    
