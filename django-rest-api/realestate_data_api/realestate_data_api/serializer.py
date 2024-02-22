from rest_framework import serializers
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

class RemaxlistingsModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Remaxlistings
    fields = "__all__"

class RemaxlistingsairbnbModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Remaxlistingsairbnb
    fields = "__all__"

class RemaxlistingsamenetiesModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Remaxlistingsameneties
    fields = "__all__"

class RemaxlistingsassociationsModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Remaxlistingsassociations
    fields = "__all__"

class RemaxlistingscollegesModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Remaxlistingscolleges
    fields = "__all__"

class RemaxlistingsschoolsModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Remaxlistingsschools
    fields = "__all__"

class RemaxlistingsuniversitiesModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Remaxlistingsuniversities
    fields = "__all__"

class RemaxlistingswalkscoreModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Remaxlistingswalkscore
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

class ZillowlistingsModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Zillowlistings
    fields = "__all__"

class ZillowlistingsairbnbModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Zillowlistingsairbnb
    fields = "__all__"

class ZillowlistingsamenetiesModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Zillowlistingsameneties
    fields = "__all__"

class ZillowlistingsassociationsModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Zillowlistingsassociations
    fields = "__all__"

class ZillowlistingscollegesModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Zillowlistingscolleges
    fields = "__all__"

class ZillowlistingsschoolsModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Zillowlistingsschools
    fields = "__all__"

class ZillowlistingsuniversitiesModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Zillowlistingsuniversities
    fields = "__all__"

class ZillowlistingswalkscoreModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Zillowlistingswalkscore
    fields = "__all__"
