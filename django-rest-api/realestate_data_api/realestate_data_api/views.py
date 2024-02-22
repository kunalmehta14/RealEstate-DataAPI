from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .models import (Airbnbdata, Airbnbdataassociations,
                     Citiesdata, Collegesdata, Mortgagedata,
                     Remaxlistings, Remaxlistingsairbnb, 
                     Remaxlistingsameneties, Remaxlistingsassociations, 
                     Remaxlistingscolleges, Remaxlistingsschools, 
                     Remaxlistingsuniversities, Remaxlistingswalkscore, 
                     Schooldata, Universitiesdata, Yelpbusinessdata, 
                     Yelpdata, Zillowlistings, Zillowlistingsairbnb, 
                     Zillowlistingsameneties, Zillowlistingsassociations, 
                     Zillowlistingscolleges, Zillowlistingsschools, 
                     Zillowlistingsuniversities, Zillowlistingswalkscore)
from .serializer import (AirbnbdataModelSerializer, AirbnbdataassociationsModelSerializer, 
                         CitiesdataModelSerializer, CollegesdataModelSerializer, 
                         MortgagedataModelSerializer, RemaxlistingsModelSerializer, 
                         RemaxlistingsairbnbModelSerializer, RemaxlistingsamenetiesModelSerializer, 
                         RemaxlistingsassociationsModelSerializer, RemaxlistingscollegesModelSerializer, 
                         RemaxlistingsschoolsModelSerializer, RemaxlistingsuniversitiesModelSerializer, 
                         RemaxlistingswalkscoreModelSerializer, SchooldataModelSerializer, 
                         UniversitiesdataModelSerializer, YelpbusinessdataModelSerializer, 
                         YelpdataModelSerializer, ZillowlistingsModelSerializer, 
                         ZillowlistingsairbnbModelSerializer, ZillowlistingsamenetiesModelSerializer, 
                         ZillowlistingsassociationsModelSerializer, ZillowlistingscollegesModelSerializer, 
                         ZillowlistingsschoolsModelSerializer, ZillowlistingsuniversitiesModelSerializer,
                         ZillowlistingswalkscoreModelSerializer)

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

class CollegesdataListAPIView(APIView):
  queryset = Collegesdata.objects.all()
  serializer_class = CollegesdataModelSerializer

class MortgagedataListAPIView(APIView):
  queryset = Mortgagedata.objects.all()
  serializer_class = MortgagedataModelSerializer

class RemaxlistingsListAPIView(generics.ListAPIView):
  queryset = Remaxlistings.objects.all()
  serializer_class = RemaxlistingsModelSerializer

class RemaxlistingsairbnbListAPIView(APIView):
  queryset = Remaxlistingsairbnb.objects.all()
  serializer_class = RemaxlistingsairbnbModelSerializer

class RemaxlistingsamenetiesListAPIView(APIView):
  queryset = Remaxlistingsameneties.objects.all()
  serializer_class = RemaxlistingsamenetiesModelSerializer

class RemaxlistingsassociationsListAPIView(APIView):
  queryset = Remaxlistingsassociations.objects.all()
  serializer_class = RemaxlistingsassociationsModelSerializer

class RemaxlistingscollegesListAPIView(APIView):
  queryset = Remaxlistingscolleges.objects.all()
  serializer_class = RemaxlistingscollegesModelSerializer

class RemaxlistingsschoolsListAPIView(APIView):
  queryset = Remaxlistingsschools.objects.all()
  serializer_class = RemaxlistingsschoolsModelSerializer

class RemaxlistingsuniversitiesListAPIView(APIView):
  queryset = Remaxlistingsuniversities.objects.all()
  serializer_class = RemaxlistingsuniversitiesModelSerializer

class RemaxlistingswalkscoreListAPIView(APIView):
  queryset = Remaxlistingswalkscore.objects.all()
  serializer_class = RemaxlistingswalkscoreModelSerializer

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