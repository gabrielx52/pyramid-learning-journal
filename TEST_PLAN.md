#Pyramid Learning Journal Test Plan

## Main view tests
+ Main view response has the db items in a list
+ New entries exist and are in the response

## Detail view tests
+ Detail view for specific entries include entry details.
+ 404 for non existant entries

## Create view tests
+ New entry is in database query
+ Incomplete data should return dict with 'Title and body requried.'

## Edit view tests
+ Edited entries should be edited

## Delete view tests
+ Deleted post should be removed from db

### Step4 coverage: 83% 
We never went over how to test an update. I tried for a while to make some but I honestly have no idea how to do it.
