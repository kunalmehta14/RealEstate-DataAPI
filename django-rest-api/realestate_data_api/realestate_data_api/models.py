from django.db import models


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

class Remaxlistings(models.Model):
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

    class Meta:
        managed = False
        db_table = 'RemaxListings'

class Remaxlistingsairbnb(models.Model):
    id = models.OneToOneField(Remaxlistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, AirbnbId) found, that is not supported. The first column is selected.
    airbnbid = models.ForeignKey(Airbnbdata, models.DO_NOTHING, db_column='AirbnbId')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RemaxListingsAirbnb'
        unique_together = (('id', 'airbnbid'),)

class Remaxlistingsameneties(models.Model):
    id = models.OneToOneField(Remaxlistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, YelpDataId) found, that is not supported. The first column is selected.
    yelpdataid = models.ForeignKey('Yelpdata', models.DO_NOTHING, db_column='YelpDataId')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RemaxListingsAmeneties'
        unique_together = (('id', 'yelpdataid'),)

class Remaxlistingsassociations(models.Model):
    id = models.OneToOneField(Remaxlistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, timestamp) found, that is not supported. The first column is selected.
    price = models.IntegerField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    salestatus = models.CharField(db_column='SaleStatus', max_length=50, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'RemaxListingsAssociations'
        unique_together = (('id', 'timestamp'),)

class Remaxlistingscolleges(models.Model):
    id = models.OneToOneField(Remaxlistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, CollegeName) found, that is not supported. The first column is selected.
    collegename = models.ForeignKey(Collegesdata, models.DO_NOTHING, db_column='CollegeName')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RemaxListingsColleges'
        unique_together = (('id', 'collegename'),)

class Remaxlistingsschools(models.Model):
    id = models.OneToOneField(Remaxlistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, SchoolId) found, that is not supported. The first column is selected.
    schoolid = models.ForeignKey('Schooldata', models.DO_NOTHING, db_column='SchoolId')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RemaxListingsSchools'
        unique_together = (('id', 'schoolid'),)

class Remaxlistingsuniversities(models.Model):
    id = models.OneToOneField(Remaxlistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase. The composite primary key (Id, UniversityName) found, that is not supported. The first column is selected.
    universityname = models.ForeignKey('Universitiesdata', models.DO_NOTHING, db_column='UniversityName')  # Field name made lowercase.
    distance = models.DecimalField(db_column='Distance', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RemaxListingsUniversities'
        unique_together = (('id', 'universityname'),)

class Remaxlistingswalkscore(models.Model):
    id = models.OneToOneField(Remaxlistings, models.DO_NOTHING, db_column='Id', primary_key=True)  # Field name made lowercase.
    walkscore = models.DecimalField(db_column='WalkScore', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    transitscore = models.DecimalField(db_column='TransitScore', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RemaxListingsWalkscore'

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