# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Userchathistorysessions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.CharField(primary_key = True, editable = False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.session

    class Meta:
        managed = True
        db_table = 'realestate_data_api_userchathistorysessions'

class Userchathistorymessages(models.Model):
    message_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(Userchathistorysessions, on_delete=models.CASCADE) 
    message = models.CharField(max_length=256)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = True
        db_table = 'realestate_data_api_userchathistorymessages'

class Airbnbdata(models.Model):
    id = models.BigIntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    listingname = models.CharField(db_column='ListingName', max_length=300, blank=True, null=True)  # Field name made lowercase.
    listingobjtype = models.CharField(db_column='ListingObjType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cityname = models.ForeignKey('Citiesdata', models.DO_NOTHING, db_column='CityName')  # Field name made lowercase.
    listingcoordinates = models.TextField(db_column='ListingCoordinates')  # Field name made lowercase. This field type is a guess.
    roomtypecategory = models.CharField(db_column='RoomTypeCategory', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AirbnbData'


class Airbnbdataassociations(models.Model):
    id = models.OneToOneField(Airbnbdata, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, timestamp) found, that is not supported. The first column is selected.
    price = models.IntegerField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'AirbnbDataAssociations'
        unique_together = (('id', 'timestamp'),)


class Citiesdata(models.Model):
    cityname = models.CharField(db_column='CityName', primary_key=True, max_length=200)  # Field name made lowercase.
    citytype = models.CharField(db_column='CityType', max_length=100)  # Field name made lowercase.
    division = models.CharField(db_column='Division', max_length=100)  # Field name made lowercase.
    populationlatest = models.BigIntegerField(db_column='PopulationLatest')  # Field name made lowercase.
    populationprevious = models.BigIntegerField(db_column='PopulationPrevious')  # Field name made lowercase.
    area = models.BigIntegerField(db_column='Area')  # Field name made lowercase.
    averageprice = models.IntegerField(db_column='AveragePrice', blank=True, null=True)  # Field name made lowercase.
    averagerentalprice = models.IntegerField(db_column='AverageRentalPrice', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CitiesData'


class Collegesdata(models.Model):
    collegename = models.CharField(db_column='CollegeName', primary_key=True, max_length=100)  # Field name made lowercase. The composite primary key (CollegeName, CityName) found, that is not supported. The first column is selected.
    cityname = models.ForeignKey(Citiesdata, models.DO_NOTHING, db_column='CityName')  # Field name made lowercase.
    collegeaddress = models.CharField(db_column='CollegeAddress', max_length=300)  # Field name made lowercase.
    collegecoordinates = models.TextField(db_column='CollegeCoordinates')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'CollegesData'
        unique_together = (('collegename', 'cityname'),)


class Mortgagedata(models.Model):
    lendername = models.CharField(db_column='LenderName', primary_key=True, max_length=100)  # Field name made lowercase. The composite primary key (LenderName, timestamp) found, that is not supported. The first column is selected.
    variable = models.FloatField(db_column='Variable', blank=True, null=True)  # Field name made lowercase.
    sixmonths = models.FloatField(db_column='SixMonths', blank=True, null=True)  # Field name made lowercase.
    oneyear = models.FloatField(db_column='OneYear', blank=True, null=True)  # Field name made lowercase.
    twoyears = models.FloatField(db_column='TwoYears', blank=True, null=True)  # Field name made lowercase.
    threeyears = models.FloatField(db_column='ThreeYears', blank=True, null=True)  # Field name made lowercase.
    fouryears = models.FloatField(db_column='FourYears', blank=True, null=True)  # Field name made lowercase.
    fiveyears = models.FloatField(db_column='FiveYears', blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'MortgageData'
        unique_together = (('lendername', 'timestamp'),)


class Neighborhooddata(models.Model):
    cityname = models.OneToOneField(Citiesdata, models.DO_NOTHING, db_column='CityName', primary_key=True)  # Field name made lowercase. The composite primary key (CityName, PostalCode) found, that is not supported. The first column is selected.
    postalcode = models.CharField(db_column='PostalCode', max_length=7)  # Field name made lowercase.
    neighborhood = models.CharField(db_column='Neighborhood', max_length=50, blank=True, null=True)  # Field name made lowercase.
    coordinates = models.TextField(db_column='Coordinates', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'NeighborhoodData'
        unique_together = (('cityname', 'postalcode'),)


class Realestatelistings(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=50)  # Field name made lowercase.
    addressstreet = models.CharField(db_column='AddressStreet', max_length=300)  # Field name made lowercase.
    cityname = models.ForeignKey(Citiesdata, models.DO_NOTHING, db_column='CityName')  # Field name made lowercase.
    beds = models.IntegerField(db_column='Beds', blank=True, null=True)  # Field name made lowercase.
    baths = models.IntegerField(db_column='Baths', blank=True, null=True)  # Field name made lowercase.
    listingcoordinates = models.TextField(db_column='ListingCoordinates')  # Field name made lowercase. This field type is a guess.
    listingtype = models.CharField(db_column='ListingType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    listingdate = models.DateTimeField(db_column='ListingDate', blank=True, null=True)  # Field name made lowercase.
    area = models.IntegerField(db_column='Area', blank=True, null=True)  # Field name made lowercase.
    listingurl = models.CharField(db_column='ListingUrl', max_length=2083, blank=True, null=True)  # Field name made lowercase.
    postalcode = models.CharField(db_column='PostalCode', max_length=7, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RealEstateListings'


class Realestatelistingsairbnb(models.Model):
    id = models.OneToOneField(Realestatelistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, AirbnbId) found, that is not supported. The first column is selected.
    airbnbid = models.ForeignKey(Airbnbdata, models.DO_NOTHING, db_column='AirbnbId')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RealEstateListingsAirbnb'
        unique_together = (('id', 'airbnbid'),)


class Realestatelistingsameneties(models.Model):
    id = models.OneToOneField(Realestatelistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, YelpDataId) found, that is not supported. The first column is selected.
    yelpdataid = models.ForeignKey('Yelpdata', models.DO_NOTHING, db_column='YelpDataId')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RealEstateListingsAmeneties'
        unique_together = (('id', 'yelpdataid'),)


class Realestatelistingsassociations(models.Model):
    id = models.OneToOneField(Realestatelistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, timestamp) found, that is not supported. The first column is selected.
    price = models.IntegerField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    salestatus = models.CharField(db_column='SaleStatus', max_length=50, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'RealEstateListingsAssociations'
        unique_together = (('id', 'timestamp'),)


class Realestatelistingscolleges(models.Model):
    id = models.OneToOneField(Realestatelistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, CollegeName) found, that is not supported. The first column is selected.
    collegename = models.ForeignKey(Collegesdata, models.DO_NOTHING, db_column='CollegeName')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RealEstateListingsColleges'
        unique_together = (('id', 'collegename'),)


class Realestatelistingsdetailed(models.Model):
    id = models.OneToOneField(Realestatelistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase.
    agentid = models.IntegerField(db_column='AgentId', blank=True, null=True)  # Field name made lowercase.
    agentname = models.CharField(db_column='AgentName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    agentoffice = models.CharField(db_column='AgentOffice', max_length=100, blank=True, null=True)  # Field name made lowercase.
    agentemail = models.CharField(db_column='AgentEmail', max_length=50, blank=True, null=True)  # Field name made lowercase.
    agentphone = models.CharField(db_column='AgentPhone', max_length=15, blank=True, null=True)  # Field name made lowercase.
    basement = models.CharField(db_column='Basement', max_length=50, blank=True, null=True)  # Field name made lowercase.
    taxamount = models.IntegerField(db_column='TaxAmount', blank=True, null=True)  # Field name made lowercase.
    fireplace = models.IntegerField(db_column='Fireplace', blank=True, null=True)  # Field name made lowercase.
    garage = models.IntegerField(db_column='Garage', blank=True, null=True)  # Field name made lowercase.
    heating = models.CharField(db_column='Heating', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sewer = models.CharField(db_column='Sewer', max_length=50, blank=True, null=True)  # Field name made lowercase.
    subdivision = models.CharField(db_column='SubDivision', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2083, blank=True, null=True)  # Field name made lowercase.
    images = models.JSONField(db_column='Images', blank=True, null=True)  # Field name made lowercase.
    mls = models.CharField(db_column='Mls', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RealEstateListingsDetailed'


class Realestatelistingsschools(models.Model):
    id = models.OneToOneField(Realestatelistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, SchoolId) found, that is not supported. The first column is selected.
    schoolid = models.ForeignKey('Schooldata', models.DO_NOTHING, db_column='SchoolId')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RealEstateListingsSchools'
        unique_together = (('id', 'schoolid'),)


class Realestatelistingsuniversities(models.Model):
    id = models.OneToOneField(Realestatelistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, UniversityName) found, that is not supported. The first column is selected.
    universityname = models.ForeignKey('Universitiesdata', models.DO_NOTHING, db_column='UniversityName')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RealEstateListingsUniversities'
        unique_together = (('id', 'universityname'),)


class Realestatelistingswalkscore(models.Model):
    id = models.OneToOneField(Realestatelistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase.
    walkscore = models.DecimalField(db_column='WalkScore', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    transitscore = models.DecimalField(db_column='TransitScore', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RealEstateListingsWalkscore'


class Schooldata(models.Model):
    id = models.BigIntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    schoolname = models.CharField(db_column='SchoolName', max_length=100)  # Field name made lowercase.
    schooladdress = models.CharField(db_column='SchoolAddress', max_length=300)  # Field name made lowercase.
    schoolcoordinates = models.TextField(db_column='SchoolCoordinates')  # Field name made lowercase. This field type is a guess.
    cityname = models.ForeignKey(Citiesdata, models.DO_NOTHING, db_column='CityName')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SchoolData'


class Universitiesdata(models.Model):
    universityname = models.CharField(db_column='UniversityName', primary_key=True, max_length=100)  # Field name made lowercase. The composite primary key (UniversityName, CityName) found, that is not supported. The first column is selected.
    cityname = models.ForeignKey(Citiesdata, models.DO_NOTHING, db_column='CityName')  # Field name made lowercase.
    universityaddress = models.CharField(db_column='UniversityAddress', max_length=300)  # Field name made lowercase.
    universitycoordinates = models.TextField(db_column='UniversityCoordinates')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'UniversitiesData'
        unique_together = (('universityname', 'cityname'),)


class Yelpbusinessdata(models.Model):
    id = models.OneToOneField('Yelpdata', models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase.
    categories = models.JSONField(db_column='Categories', blank=True, null=True)  # Field name made lowercase.
    pricerange = models.CharField(db_column='PriceRange', max_length=5, blank=True, null=True)  # Field name made lowercase.
    businessurl = models.CharField(db_column='BusinessUrl', max_length=2083, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'YelpBusinessData'


class Yelpdata(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=50)  # Field name made lowercase.
    businessname = models.CharField(db_column='BusinessName', max_length=300, blank=True, null=True)  # Field name made lowercase.
    rating = models.FloatField(db_column='Rating', blank=True, null=True)  # Field name made lowercase.
    reviews = models.IntegerField(db_column='Reviews', blank=True, null=True)  # Field name made lowercase.
    businessaddress = models.CharField(db_column='BusinessAddress', max_length=300, blank=True, null=True)  # Field name made lowercase.
    cityname = models.ForeignKey(Citiesdata, models.DO_NOTHING, db_column='CityName')  # Field name made lowercase.
    businesscoordinates = models.TextField(db_column='BusinessCoordinates')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'YelpData'


class Zillowlistings(models.Model):
    id = models.BigIntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=300)  # Field name made lowercase.
    cityname = models.ForeignKey(Citiesdata, models.DO_NOTHING, db_column='CityName')  # Field name made lowercase.
    beds = models.IntegerField(db_column='Beds', blank=True, null=True)  # Field name made lowercase.
    baths = models.IntegerField(db_column='Baths', blank=True, null=True)  # Field name made lowercase.
    listingcoordinates = models.TextField(db_column='ListingCoordinates')  # Field name made lowercase. This field type is a guess.
    listingtype = models.CharField(db_column='ListingType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addressstreet = models.CharField(db_column='AddressStreet', max_length=300)  # Field name made lowercase.
    listingurl = models.CharField(db_column='ListingUrl', max_length=2083, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZillowListings'


class Zillowlistingsairbnb(models.Model):
    id = models.OneToOneField(Zillowlistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, AirbnbId) found, that is not supported. The first column is selected.
    airbnbid = models.ForeignKey(Airbnbdata, models.DO_NOTHING, db_column='AirbnbId')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZillowListingsAirbnb'
        unique_together = (('id', 'airbnbid'),)


class Zillowlistingsameneties(models.Model):
    id = models.OneToOneField(Zillowlistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, YelpDataId) found, that is not supported. The first column is selected.
    yelpdataid = models.ForeignKey(Yelpdata, models.DO_NOTHING, db_column='YelpDataId')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZillowListingsAmeneties'
        unique_together = (('id', 'yelpdataid'),)


class Zillowlistingsassociations(models.Model):
    id = models.OneToOneField(Zillowlistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, timestamp) found, that is not supported. The first column is selected.
    price = models.IntegerField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    salestatus = models.CharField(db_column='SaleStatus', max_length=50, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ZillowListingsAssociations'
        unique_together = (('id', 'timestamp'),)


class Zillowlistingscolleges(models.Model):
    id = models.OneToOneField(Zillowlistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, CollegeName) found, that is not supported. The first column is selected.
    collegename = models.ForeignKey(Collegesdata, models.DO_NOTHING, db_column='CollegeName')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZillowListingsColleges'
        unique_together = (('id', 'collegename'),)


class Zillowlistingsschools(models.Model):
    id = models.OneToOneField(Zillowlistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, SchoolId) found, that is not supported. The first column is selected.
    schoolid = models.ForeignKey(Schooldata, models.DO_NOTHING, db_column='SchoolId')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZillowListingsSchools'
        unique_together = (('id', 'schoolid'),)


class Zillowlistingsuniversities(models.Model):
    id = models.OneToOneField(Zillowlistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, UniversityName) found, that is not supported. The first column is selected.
    universityname = models.ForeignKey(Universitiesdata, models.DO_NOTHING, db_column='UniversityName')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZillowListingsUniversities'
        unique_together = (('id', 'universityname'),)


class Zillowlistingswalkscore(models.Model):
    id = models.OneToOneField(Zillowlistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase.
    walkscore = models.DecimalField(db_column='WalkScore', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    transitscore = models.DecimalField(db_column='TransitScore', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZillowListingsWalkscore'
