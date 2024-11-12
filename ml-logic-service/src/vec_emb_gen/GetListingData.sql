SELECT RL.AddressStreet, RL.Beds, RL.Baths, 
RL.CityName, CID.CityType, CID.Division, RL.ListingType, RL.ListingDate,
RL.Area,
(
	SELECT RLA2.Price 
	FROM RealEstateListingsAssociations RLA2 
	WHERE RLA2.Id = RL.Id
	ORDER BY RLA2.`timestamp` ASC
	LIMIT 1
) AS OrignalPrice,
(
	SELECT RLA1.Price 
	FROM RealEstateListingsAssociations RLA1 
	WHERE RLA1.Id = RL.Id
	ORDER BY RLA1.`timestamp` DESC
	LIMIT 1
) AS CurrentPrice,
DATEDIFF((
	SELECT RLA3.`timestamp`
	FROM RealEstateListingsAssociations RLA3 
	WHERE RLA3.Id = RL.Id
	ORDER BY RLA3.`timestamp` DESC
	LIMIT 1 
), RL.ListingDate) AS DaysOnTheMarket,
ST_X(RL.ListingCoordinates) AS lon, 
ST_Y(RL.ListingCoordinates) AS lat,
COUNT(
    DISTINCT RLS.SchoolId
    ) AS NumberOfSchools,
GROUP_CONCAT(
    DISTINCT SD.SchoolName ORDER BY SD.Id SEPARATOR ', '
    ) AS Schools,
COUNT(
    DISTINCT RLC.CollegeName
    ) AS NumberOfColleges,
GROUP_CONCAT(
    DISTINCT CD.CollegeName ORDER BY CD.CollegeName SEPARATOR ', '
    ) AS Colleges,
COUNT(
    DISTINCT RLU.UniversityName
    ) AS Universities,
GROUP_CONCAT(
    DISTINCT UD.UniversityName ORDER BY UD.UniversityName SEPARATOR ', '
    ) AS Universities,
COUNT(
    DISTINCT RLAM.YelpDataId
    ) AS NumberOfAmeneties,
GROUP_CONCAT(
    DISTINCT CONCAT(
        'BusinessName: ', YD.BusinessName, ', ', 'Tags: ', YBD.Categories
            ) ORDER BY YBD.Id SEPARATOR '| '
    ) AS Ameneties,
COUNT(
    DISTINCT RLAB.AirbnbId
    ) AS NumberOfAirbnbs,
ROUND(AVG(ADA.Price), 0) AS AirbnbsAvergePrice,
RLW.WalkScore, RLW.TransitScore,
RLD.Basement, RLD.TaxAmount, RLD.Fireplace,
RLD.Garage, RLD.Heating, RLD.Sewer, RLD.Description
FROM RealEstateListingsAssociations RLA 
LEFT JOIN 
    RealEstateListings RL ON RL.Id = RLA.Id
LEFT JOIN
    CitiesData CID ON RL.CityName = CID.CityName
LEFT JOIN 
    RealEstateListingsWalkscore RLW ON RL.Id = RLW.Id
LEFT JOIN 
    RealEstateListingsDetailed RLD ON RL.Id = RLD.Id
LEFT JOIN 
    RealEstateListingsSchools RLS ON RL.Id = RLS.Id
LEFT JOIN 
    SchoolData SD ON RLS.SchoolId = SD.Id
LEFT JOIN 
    RealEstateListingsColleges RLC ON RL.Id = RLC.Id
LEFT JOIN 
    CollegesData CD ON RLC.CollegeName = CD.CollegeName
LEFT JOIN 
    RealEstateListingsUniversities RLU ON RL.Id = RLU.Id
LEFT JOIN 
    UniversitiesData UD ON RLU.UniversityName = UD.UniversityName
LEFT JOIN 
    RealEstateListingsAmeneties RLAM ON RL.Id = RLAM.Id
LEFT JOIN 
    YelpData YD ON RLAM.YelpDataId = YD.Id
LEFT JOIN 
    YelpBusinessData YBD ON RLAM.YelpDataId = YBD.Id
LEFT JOIN 
    RealEstateListingsAirbnb RLAB ON RL.Id = RLAB.Id
LEFT JOIN 
    AirbnbDataAssociations ADA ON RLAB.AirbnbId = ADA.Id
WHERE 
    RL.ID = '??'
GROUP BY 
    RL.Id