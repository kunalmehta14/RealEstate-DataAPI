from django.http import Http404, JsonResponse, HttpResponse
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
import requests, json
from django.db.models import OuterRef, Subquery, Max
from .models import (Airbnbdata, Airbnbdataassociations,
                     Citiesdata, Collegesdata, Mortgagedata,
                     Realestatelistings, Realestatelistingsairbnb, 
                     Realestatelistingsameneties, Realestatelistingsassociations, 
                     Realestatelistingscolleges, Realestatelistingsschools,Realestatelistingsdetailed, 
                     Realestatelistingsuniversities, Realestatelistingswalkscore, 
                     Schooldata, Universitiesdata, Yelpbusinessdata, 
                     Yelpdata, Zillowlistings, Zillowlistingsairbnb, 
                     Zillowlistingsameneties, Zillowlistingsassociations, 
                     Zillowlistingscolleges, Zillowlistingsschools, 
                     Zillowlistingsuniversities, Zillowlistingswalkscore)
from .serializer import (AirbnbdataModelSerializer, AirbnbdataassociationsModelSerializer, 
                         CitiesdataModelSerializer, CollegesdataModelSerializer, 
                         MortgagedataModelSerializer, RealestatelistingsModelSerializer, 
                         RealestatelistingsairbnbModelSerializer, RealestatelistingsamenetiesModelSerializer, 
                         RealestatelistingsassociationsModelSerializer, RealestatelistingscollegesModelSerializer, 
                         RealestatelistingsschoolsModelSerializer, RealestatelistingsuniversitiesModelSerializer, 
                         RealestatelistingswalkscoreModelSerializer, RealestatelistingsdetailedModelSerializer, 
                         SchooldataModelSerializer, UniversitiesdataModelSerializer, YelpbusinessdataModelSerializer, 
                         YelpdataModelSerializer, ZillowlistingsModelSerializer, 
                         ZillowlistingsairbnbModelSerializer, ZillowlistingsamenetiesModelSerializer, 
                         ZillowlistingsassociationsModelSerializer, ZillowlistingscollegesModelSerializer, 
                         ZillowlistingsschoolsModelSerializer, ZillowlistingsuniversitiesModelSerializer,
                         ZillowlistingswalkscoreModelSerializer)
from django.utils import timezone
from django.contrib import auth
from django.shortcuts import redirect
import google.generativeai as genai
from django.contrib.auth.models import User

class AirbnbdataListAPIView(APIView):
  queryset = Airbnbdata.objects.all()
  serializer_class = AirbnbdataModelSerializer

class AirbnbdataassociationsListAPIView(APIView):
  queryset = Airbnbdataassociations.objects.all()
  serializer_class = AirbnbdataassociationsModelSerializer

class CitiesdataListAPIView(generics.ListAPIView):
  queryset = Citiesdata.objects.all()
  serializer_class = CitiesdataModelSerializer
  paginate_by = 10
  
class CitiesdataAPIView(APIView):
  queryset = Citiesdata.objects.all()
  serializer_class = CitiesdataModelSerializer

  def get_object(self, cityname):
    try:
      return Citiesdata.objects.get(cityname=cityname)
    except Citiesdata.DoesNotExist:
      raise Http404

  def get(self, request, cityname, format=None):
    city = self.get_object(cityname)
    serializer = CitiesdataModelSerializer(city)
    return Response(serializer.data)

class RealestatelistingListAPIView(generics.ListAPIView):
  serializer_class = RealestatelistingsModelSerializer

  def get_queryset(self):
    # queryset = super().get_queryset()
    cityname = self.request.GET.get('cityname')
    beds = self.request.GET.get('beds')
    if cityname is not None:
      try:
        item = Realestatelistings.objects.filter(cityname=cityname)
        data = list(item.values())
        return JsonResponse(data, safe=False)
      except Exception as e:
        print(e)
    elif beds is not None:
      try:
        item = Realestatelistings.objects.filter(beds=beds)
      except Exception as e:
        print(e)
    elif beds is not None and cityname is not None:
      try:
        item = Realestatelistings.objects.filter(cityname=cityname, 
                                            beds=beds)
        return item
      except Exception as e:
        print(e)
    else:
      try:
        item = Realestatelistings.objects.all()
        return item
      except Exception as e:
        print(e)

# Realestate API View
class RealestatelistingAPIView(generics.RetrieveAPIView):

  serializer_class = RealestatelistingsModelSerializer
  def get_object(self):
    listing_id = self.kwargs.get('pk')
    try:
      item = Realestatelistings.objects.get(pk=listing_id)
      return item
    except Realestatelistings.DoesNotExist:
        raise Http404  

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    try:
      listing_airbnbs = Realestatelistingsairbnb.objects.filter(id=instance.id)
      listing_amenties = Realestatelistingsameneties.objects.filter(id=instance.id)
      listing_colleges = Realestatelistingscolleges.objects.filter(id=instance.id)
      listing_universities = Realestatelistingsuniversities.objects.filter(id=instance.id)
      listing_schools = Realestatelistingsschools.objects.filter(id=instance.id)
      listing_walkscore = Realestatelistingswalkscore.objects.filter(id=instance.id).first()
      listing_price_all = Realestatelistingsassociations.objects.filter(id=instance.id)
      listing_details = Realestatelistingsdetailed.objects.filter(id=instance.id)
    except (Realestatelistings.DoesNotExist):
        return Response(status=404)

    lisitng_serializer = RealestatelistingsModelSerializer(instance)
    listing_airbnbs_serializer = RealestatelistingsairbnbModelSerializer(listing_airbnbs, many=True)
    listing_amenties_serializer = RealestatelistingsamenetiesModelSerializer(listing_amenties, many=True)
    listing_colleges_serializer = RealestatelistingscollegesModelSerializer(listing_colleges, many=True)
    listing_universities_serializer = RealestatelistingsuniversitiesModelSerializer(listing_universities, many=True)
    listing_schools_serializer = RealestatelistingsschoolsModelSerializer(listing_schools, many=True)
    listing_walkscore_serializer = RealestatelistingswalkscoreModelSerializer(listing_walkscore)
    listing_price_serializer = RealestatelistingsassociationsModelSerializer(listing_price_all, many=True)
    listing_details_serializer = RealestatelistingsdetailedModelSerializer(listing_details, many=True)
    return Response({
      'lisitng': lisitng_serializer.data,
      'listing_details': listing_details_serializer.data,
      'listing_price': listing_price_serializer.data,
      'listing_airbnbs': listing_airbnbs_serializer.data,
      'listing_amenties': listing_amenties_serializer.data,
      'listing_colleges': listing_colleges_serializer.data,
      'listing_universities': listing_universities_serializer.data,
      'listing_schools': listing_schools_serializer.data,
      'listing_walkscore': listing_walkscore_serializer.data,
    })

class MortgagedataListAPIView(generics.ListAPIView):
  serializer_class = MortgagedataModelSerializer
  def get(self, request, *args, **kwargs):
    try:
      latest_time = Mortgagedata.objects.filter(lendername=OuterRef('lendername')).order_by('-timestamp').values('timestamp')[:1]
      items = Mortgagedata.objects.filter(timestamp=Subquery(latest_time)).values('lendername', 'variable', 'sixmonths', 
                                                                                  'oneyear', 'twoyears', 'threeyears',
                                                                                  'fouryears', 'fiveyears', 'timestamp')
      return Response(items)
    except Exception as e:
      print(e)
      return Response({'error': 'Something went wrong'}, status=500)

class MortgagedataAPIView(generics.RetrieveAPIView):
  serializer_class = MortgagedataModelSerializer
  queryset = Mortgagedata.objects.all()

  def get_queryset(self):
    lendername = self.kwargs.get('lendername')
    return Mortgagedata.objects.filter(lendername=lendername).order_by('-timestamp')

  def get(self, request, *args, **kwargs):
    lender_data = self.get_queryset()
    if not lender_data.exists():
        raise Http404
    serializer = MortgagedataModelSerializer(lender_data, many=True)
    return Response(serializer.data)

##########################################################
############ USER AUTH/REGISTERATION OPERATIONS ##########
##########################################################
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('cities')
        else:
            error_message = 'Invalid username or password'
            return (request, {'error_message': error_message})
    else:
        return request

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('cities')
            except:
                error_message = 'Error creating account'
                return error_message
        else:
            error_message = 'Password dont match'
            return error_message
    return request

def logout(request):
    auth.logout(request)
    return redirect('cities')

def chatProcessorAPIView(request):
  if request.method == 'POST':
      user_query = request.POST.get('message')
      form_data ={'chat': f'{user_query}'}
      response = requests.post("http://ml-logic-service:8008/vector-search", 
                                data=form_data
                              )
      return HttpResponse(response, content_type="application/json")


class CollegesdataListAPIView(APIView):
  queryset = Collegesdata.objects.all()
  serializer_class = CollegesdataModelSerializer

class SchooldataListAPIView(APIView):
  queryset = Schooldata.objects.all()
  serializer_class = SchooldataModelSerializer

class UniversitiesdataListAPIView(APIView):
  queryset = Universitiesdata.objects.all()
  serializer_class = UniversitiesdataModelSerializer

class YelpbusinessdataListAPIView(APIView):
  queryset = Yelpbusinessdata.objects.all()
  serializer_class = YelpbusinessdataModelSerializer

class YelpdataListAPIView(APIView):
  queryset = Yelpdata.objects.all()
  serializer_class = YelpdataModelSerializer

class ZillowlistingsListAPIView(APIView):
  queryset = Zillowlistings.objects.all()
  serializer_class = ZillowlistingsModelSerializer

class ZillowlistingsairbnbListAPIView(APIView):
  queryset = Zillowlistingsairbnb.objects.all()
  serializer_class = ZillowlistingsairbnbModelSerializer

class ZillowlistingsamenetiesListAPIView(APIView):
  queryset = Zillowlistingsameneties.objects.all()
  serializer_class = ZillowlistingsamenetiesModelSerializer

class ZillowlistingsassociationsListAPIView(APIView):
  queryset = Zillowlistingsassociations.objects.all()
  serializer_class = ZillowlistingsassociationsModelSerializer

class ZillowlistingscollegesListAPIView(APIView):
  queryset = Zillowlistingscolleges.objects.all()
  serializer_class = ZillowlistingscollegesModelSerializer

class ZillowlistingsschoolsListAPIView(APIView):
  queryset = Zillowlistingsschools.objects.all()
  serializer_class = ZillowlistingsschoolsModelSerializer

class ZillowlistingsuniversitiesListAPIView(APIView):
  queryset = Zillowlistingsuniversities.objects.all()
  serializer_class = ZillowlistingsuniversitiesModelSerializer

class ZillowlistingswalkscoreListAPIView(APIView):
  queryset = Zillowlistingswalkscore.objects.all()
  serializer_class = ZillowlistingswalkscoreModelSerializer


  ## RETRIEVE API CODE
  # def get_object(self):
  #   cityname = self.kwargs.get('cityname')
  #   beds = self.kwargs.get('beds')
  #   if cityname is not None:
  #      queryset = queryset.filter(cityname=cityname)
  #   elif beds is not None:
  #     queryset = queryset.filter(beds=beds)
  #   elif beds is not None and cityname is not None:
  #     queryset = queryset.filter(beds=beds, 
  #                                cityname=cityname)
  #   else:
  #     item = Realestatelistings.objects.all()
  #     return item
  # def retrieve(self, request, *args, **kwargs):
  #   try:
  #     instance = self.get_object()
  #     lisitng_serializer = RealestatelistingsModelSerializer(instance)
  #     return Response({
  #         'lisitng': lisitng_serializer.data,
  #       })
  #   except Exception as e:
  #     print(e)

# class RealestatelistingsairbnbListAPIView(APIView):
#   queryset = Realestatelistingsairbnb.objects.all()
#   serializer_class = RealestatelistingsairbnbModelSerializer

# class RealestatelistingsamenetiesListAPIView(APIView):
#   queryset = Realestatelistingsameneties.objects.all()
#   serializer_class = RealestatelistingsamenetiesModelSerializer

# class RealestatelistingsassociationsListAPIView(APIView):
#   queryset = Realestatelistingsassociations.objects.all()
#   serializer_class = RealestatelistingsassociationsModelSerializer

# class RealestatelistingscollegesListAPIView(APIView):
#   queryset = Realestatelistingscolleges.objects.all()
#   serializer_class = RealestatelistingscollegesModelSerializer

# class RealestatelistingsschoolsListAPIView(APIView):
#   queryset = Realestatelistingsschools.objects.all()
#   serializer_class = RealestatelistingsschoolsModelSerializer

# class RealestatelistingsuniversitiesListAPIView(APIView):
#   queryset = Realestatelistingsuniversities.objects.all()
#   serializer_class = RealestatelistingsuniversitiesModelSerializer

# class RealestatelistingswalkscoreListAPIView(APIView):
#   queryset = Realestatelistingswalkscore.objects.all()
#   serializer_class = RealestatelistingswalkscoreModelSerializer