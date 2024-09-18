from rest_framework import serializers
from .models import Usermodels,UserProfile,TravelLeaderForm,Country,Trips,Place,Post,ArticlePost,Comment,Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usermodels
        fields = ['id', 'is_travel_leader', 'email', 'password','username','is_verified','is_block','user_preference','is_approve_leader','date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        
       
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def create(self, validated_data):
        user = Usermodels.objects.create_user(**validated_data)
        user.generate_otp()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','profile_image','address','bio','country_state','user']


class CountryField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        
        if isinstance(data, list):
            country_names = data
            countries = Country.objects.filter(name__in=country_names)
            if countries.count() != len(country_names):
                raise serializers.ValidationError("Some country names are invalid.")
            return countries
        return super().to_internal_value(data)
    

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country  
        fields = ['id','name']  


    

class FormSubmission(serializers.ModelSerializer):
    visited_countries = CountrySerializer(many=True, read_only=True)
    selectedCountries = CountryField(
        queryset=Country.objects.all(), 
        many=True, 
        required=False, 
        allow_empty=True,
        source='visited_countries'
    )
    user_id = UserSerializer()

    class Meta:
        model = TravelLeaderForm
        fields = ['id', 'visited_countries', 'firstname', 'lastname', 'cv', 'id_proof', 'is_approved', 'mobile', 'user_id','selectedCountries']

    def create(self, validated_data):
        selected_countries = validated_data.pop('visited_countries', [])
        instance = super().create(validated_data)
        instance.visited_countries.set(selected_countries)
        return instance

    def update(self, instance, validated_data):
        selected_countries = validated_data.pop('visited_countries', [])
        instance = super().update(instance, validated_data)
        instance.visited_countries.set(selected_countries)
        return instance
    

class PaymentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'trip',
            'amount',
            'status',
            'created_at',
           
            'user_username',
            'user_email',
        ]
    

class TripSerializer(serializers.ModelSerializer):
    travelead_username = serializers.CharField(source='travelead.username', read_only=True)
    travelead_email = serializers.CharField(source='travelead.email', read_only=True)
   
    booked_customers = PaymentSerializer(many=True, read_only=True, source='payment_set')
    travelead_profile_image = serializers.SerializerMethodField()
    travelead_bio = serializers.SerializerMethodField()
    travelead_address = serializers.SerializerMethodField()
    class Meta:
        model = Trips
        fields = [
            'id',
            'travelead_username',
            'travelead_email',
            'Trip_image', 
            'location', 
            'trip_type',  
            'start_date', 
            'end_date',    
            'duration', 
            'description', 
            'accomodation', 
            'transportation', 
            'amount', 
            'participant_limit' ,
            'travelead_profile_image' ,
            'booked_customers',
            'is_completed',
            'travelead',
            'travelead_bio',
            'travelead_address',
        ]
        extra_kwargs = {
            'travelead': {'read_only': True}  
        }
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        
        trip = Trips.objects.create(travelead=user, **validated_data)
        return trip
    
    def get_travelead_profile_image(self, obj):
        try:
            user_profile = UserProfile.objects.get(user=obj.travelead)
            
            if user_profile.profile_image:
                request = self.context.get('request')
                
                
                if request:
                    return request.build_absolute_uri(user_profile.profile_image.url)
            return None
        except UserProfile.DoesNotExist:
            return None
    
    def get_travelead_bio(self, obj):
        try:
            user_profile = UserProfile.objects.get(user=obj.travelead)
            return user_profile.bio if user_profile.bio else None
        except UserProfile.DoesNotExist:
            return None
    
    def get_travelead_address(self, obj):
        try:
            user_profile = UserProfile.objects.get(user=obj.travelead)
            return user_profile.address if user_profile.address else None
        except UserProfile.DoesNotExist:
            return None


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'trip', 'place_name', 'description', 'accomodation','Transportation']
    
    
    
    
class PostSerializer(serializers.ModelSerializer):
    travelead_username = serializers.CharField(source='travel_leader.username', read_only=True)
    total_likes = serializers.IntegerField( read_only=True)
    travelead_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','travel_leader','post_image','description','created_at','travelead_profile_image',"travelead_username",'likes',"total_likes"]
        read_only_fields = ['id', 'travel_leader', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        print(request)
        user = request.user

        validated_data['travel_leader'] = user
        likes_data = validated_data.pop('likes', None)
    
        # post = Post.objects.create(**validated_data)
    
        if likes_data:
            post.likes.set(likes_data)  

        post = Post.objects.create(**validated_data)
        return post
    
    # def create(self, validated_data):
    #     likes_data = validated_data.pop('likes', None)
    
    #     post = Post.objects.create(**validated_data)
    
    #     if likes_data:
    #         post.likes.set(likes_data)  
    #     return post
    
   
    def get_travelead_profile_image(self,obj):
        try:
            print(obj)
            user_profile = UserProfile.objects.get(user=obj.travel_leader)
            if user_profile.profile_image:
                request = self.context.get('request')
                
                
                if request:
                    return request.build_absolute_uri(user_profile.profile_image.url)
            return None
        except UserProfile.DoesNotExist:
            return None



class ArticleSerilizer(serializers.ModelSerializer):
    travelead_username = serializers.CharField(source='travel_leader.username', read_only=True)

    travelead_profile_image = serializers.SerializerMethodField()
    class Meta:
        model = ArticlePost
        fields = '__all__'
        read_only_fields = ['id', 'travel_leader', 'created_at']
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        validated_data['travel_leader'] = user
        likes_data = validated_data.pop('likes', None)
    
        # post = ArticlePost.objects.create(**validated_data)
    
        if likes_data:
            post.likes.set(likes_data)  

        post = ArticlePost.objects.create(**validated_data)
        return post
    def get_travelead_profile_image(self,obj):
        try:
            print(obj)
            user_profile = UserProfile.objects.get(user=obj.travel_leader)
            if user_profile.profile_image:
                request = self.context.get('request')
                
                
                if request:
                    return request.build_absolute_uri(user_profile.profile_image.url)
            return None
        except UserProfile.DoesNotExist:
            return None

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at', 'content_type', 'object_id','profile_image']

    def get_profile_image(self, obj):
        request = self.context.get('request')
        if hasattr(obj.user, 'profile_image') and obj.user.profile_image:
            return request.build_absolute_uri(obj.user.profile_image.url)
        return None
    
    def create(self, validated_data):
        request = self.context.get('request')
        content_object = validated_data.get('content_object')
        return Comment.objects.create(
            user=request.user,
            content_object=content_object,
            text=validated_data.get('text')
        )


