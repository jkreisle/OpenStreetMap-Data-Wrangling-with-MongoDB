Map data found here:  https://mapzen.com/data/metro-extracts/metro/chicago_illinois/

## Objective

Parse and clean open map data to find top trends for the city of Chicago.

###Skills applied

    - Python
    - MongoDB
    - JSON
    - ElementTree
    - Regular expression

## Summary

Since the file was so large (2GB), I created a sample of the data for quicker work. The sample file is 205MB.

I began by parsing the data to discover tag and attribute values. The following problems were revealed:
  
    -Abbreviated street names
    -Map coverage area
    -Postal code length
    -Inconsistent city names
    
Once these problems were resolved using code, I was able to organize the data and export into a JSON schema. 

Then, using MongoDB, I was able to find top trends for the city.

## Findings

My report includes findings for the following categories:

  Data Summary:
  
    -Number of documents
    -Number of nodes
    -Number of ways
    -Top contributing users
  
  Geograpgical Insights:
  
    -Top postcodes tagged
    -Top neighborhoods tagged
    -Top amenities tagged
    -Top cuisines tagged
    
These findings rely on abundunt and accurate information from users.

## Resources

    1) https://discussions.udacity.com/t/how-to-use-the-compile-variables-for-tag-types/198286
    2) https://discussions.udacity.com/t/apply-tag-types-function/181950
    3) https://discussions.udacity.com/t/case-study-iterative-parsing/165972/3
    4) https://discussions.udacity.com/t/exploring-users/172717/10
    5) https://discussions.udacity.com/t/tag-types-and-improving-street-names-locally/46437/19
    6) https://discussions.udacity.com/t/preparing-for-database-final-project/182917/3
    7) https://discussions.udacity.com/t/updating-zip-codes/43619/12
    8) https://discussions.udacity.com/t/pymongo-queries/186434
    9) https://discussions.udacity.com/t/last-quiz-preparing-for-database-in-lesson-6-mongodb/44559/30
    10) https://discussions.udacity.com/t/cleaning-postcode/195512/6
    11) https://api.mongodb.com/python/current/examples/index.html
