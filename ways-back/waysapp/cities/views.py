from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from cities.models import City, User_data, Link, Recommendations
from django.contrib.auth.models import User
from cities.serializers import CitySerializer, UserDataSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from waysapp.custom_authentication import MyCustomAuthentication
from rest_framework.permissions import AllowAny

from django.db.models.signals import post_save

# return list of cities based on user input
class ListCities(APIView):

    def get(self, request, format=None):
        city = request.GET.__getitem__('city').title()  # get city url parameter
        cities = City.objects.filter(name__startswith=city)[:5] # filter results and limit response to 5
        serializer = CitySerializer(cities, many=True)
        return JsonResponse(serializer.data, safe=False)


# Add city to the user model
# generate random number that is unique
# add number as link id to the city and user model
# return city name
# return link id
class AddCity(APIView):

    def put(self, request, format=None):
        #get city_id
        city_id = request.data['city_id']
        #add city to user model
        user = request.user
        city = City.objects.get(pk=city_id)
        # update User_data
        u = User_data.objects.get(user = user)
        # update Link -- check if link exists
        if Link.objects.filter(user_id = request.user.id, city_id = city_id):
            pass
        else:
            #create link for the user
            l = Link.objects.create(city=city, user=u)
            # update Recommendations
            r = Recommendations.objects.create(link=l)
        #serialize response
        data = {
            'name': city.name,
            'link': Link.objects.get(user_id=request.user.id, city_id=city_id).id
        }
        return JsonResponse(data, safe=False)
    

#take link_id --> find link and return info to frontend: city name, user name, city lt ln
class FindLink(APIView):
    authentication_classes = (MyCustomAuthentication,)
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        #get link id from the request
        link_id = request.GET['link_id']
        #get the link object from the database
        link_data = Link.objects.get(id=link_id)
        #get city objects from the database
        city_data = City.objects.get(id=link_data.city_id)
        #get user data
        user_data = User.objects.get(id=link_data.user_id)
        #create response
        data = {
            'name': city_data.name,
            'country': city_data.country,
            'lat': city_data.lat,
            'lng': city_data.lng,
            'first_name': user_data.first_name
        }
        return JsonResponse(data, safe=False)

#get places from Google Places API
class FindPlace(APIView):
    pass