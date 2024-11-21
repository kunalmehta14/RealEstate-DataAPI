from rest_framework import serializers
from .models import (Airbnbdata, Airbnbdataassociations,
                     Citiesdata, Collegesdata, Mortgagedata,
                     Realestatelistings, Realestatelistingsairbnb, 
                     Realestatelistingsameneties, Realestatelistingsassociations, 
                     Realestatelistingscolleges, Realestatelistingsschools, 
                     Realestatelistingsuniversities, Realestatelistingswalkscore,
                     Realestatelistingsdetailed, 
                     Schooldata, Universitiesdata, Yelpbusinessdata, 
                     Yelpdata)

class AirbnbdataModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Airbnbdata
    fields = "__all__"

class AirbnbdataassociationsModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Airbnbdataassociations
    fields = "__all__"

class CitiesdataModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Citiesdata
    fields = "__all__"

class CollegesdataModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Collegesdata
    fields = "__all__"

class MortgagedataModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Mortgagedata
    fields = "__all__"

class RealestatelistingsModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Realestatelistings
    fields = "__all__"

class RealestatelistingsairbnbModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Realestatelistingsairbnb
    fields = "__all__"

class RealestatelistingsamenetiesModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Realestatelistingsameneties
    fields = "__all__"

class RealestatelistingsassociationsModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Realestatelistingsassociations
    fields = "__all__"

class RealestatelistingsdetailedModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Realestatelistingsdetailed
    fields = "__all__"

class RealestatelistingscollegesModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Realestatelistingscolleges
    fields = "__all__"

class RealestatelistingsschoolsModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Realestatelistingsschools
    fields = "__all__"

class RealestatelistingsuniversitiesModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Realestatelistingsuniversities
    fields = "__all__"

class RealestatelistingswalkscoreModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Realestatelistingswalkscore
    fields = "__all__"

class SchooldataModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Schooldata
    fields = "__all__"

class UniversitiesdataModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Universitiesdata
    fields = "__all__"

class YelpbusinessdataModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Yelpbusinessdata
    fields = "__all__"

class YelpdataModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Yelpdata
    fields = "__all__"