# simple-arcgis-wrapper

A simple wrapper for interacting with the ArcGIS Online REST API.

## About

This project is geared towards developers who want to get data into the ArcGIS Online as easily as possible. The REST API can be pretty confusing if you aren't familiar with ArcGIS jargon and the ArcGIS API for Python is cumbersome for cloud-based programs, so we created this simple wrapper to abstract some of the difficulties with creating resources and adding data.

## Prerequisites

First you will need an ArcGIS Online account. If you plan on using token authentication, rather than a username and password, you will need an app registered on the Developer portal.

Then you will need to know a thing or two about ArcGIS.
### Feature service: 
- "Feature services allow you to serve features over the Internet and provide the symbology to use when displaying the features."
- A feature service can store many feature layers.

### Feature layer
- "A feature layer is a grouping of similar geographic features, for example, buildings, parcels, cities, roads, and earthquake epicenters."
- A feature layer can store many geometric features.

### Feature
- "Feature classes are collections of common features, each having the same spatial representation, such as points, lines, or polygons, and a common set of attribute columns."


## Installing

```
pip install simple-arcgis-wrapper
```

## Usage

### Import it
```
import simple_arcgis_wrapper as saw
```

### Identify yourself

#### Token-based  authentication
You will need a registered app and tokens obtained through the OAuth flow. Check out [this link](https://developers.arcgis.com/documentation/core-concepts/security-and-authentication/server-based-user-logins/) to learn more about setting up OAuth.

```
api = saw.ArcgisAPI(
    access_token='ACCESS_TOKEN',   # access token obtained from user
    refresh_token='REFRESH_TOKEN', # refresh token obtained from user
    username='USERNAME',           # username obtained from user
    client_id='CLIENT_ID'          # your OAuth app's client ID
)
```

#### Username and password authentication
If you just want to add data to your own account you can use this authentication scheme. Use this for one-off tasks, as this scheme will only be valid for 1 hour. Use OAuth tokens for longer-lived operations.
```
api = saw.ArcgisAPI.fromusernamepassword(
    username='username', 
    password='password'
)
```

### Create a feature service

```
service = api.services.create_feature_service('NAME', 'DESCRIPTION')

# service is a FeatureService object
print(service.id, service.name, service.url)
```

### Create a feature layer in the feature service

A feature layer stores your features, so you need to define the layer type and any additional fields.

```
fields = saw.fields.Fields()
fields.add_field('Date', saw.fields.DateField)
fields.add_field('Name', saw.fields.StringField)
fields.add_field('Altitude', saw.fields.DoubleField)

layer = api.services.create_feature_layer(
    layer_type='point',                      # point, line, or polygon
    name='NAME',                               
    description='DESCRIPTION',       
    feature_service_url=service.url,
    fields=fields,                     
    x_min=10.0, y_min=10.0,                  # min bounding box parameters
    x_max=20.0, y_max=20.0,                  # max bounding box parameters
    wkid=4326                                # well-known ID spatial reference
)

# layer is a FeatureLayer object
print(layer.id, layer.name, layer.url)

```

### Create a table in the feature service

A table is like a feature layer except it doesn't have coordinates. 

```
fields = saw.fields.Fields()
fields.add_field('Date', saw.fields.DateField)
fields.add_field('Name', saw.fields.StringField)
fields.add_field('Email', saw.fields.StringField)

table = api.services.create_table(
    name="TABLE_NAME", 
    description="TABLE_DESCRIPTION",
    feature_service_url=feature_service.url,
    fields=fields
)

# table is a Table object
print(table.id, table.name, table.url)
```

### Add one point to the feature layer

```
# attribute keys must match the layer's fields
attributes = {
    'Date': '2020-01-01 15:30:45',
    'Name': 'John Doe',
    'Altitude': 12.5
}

success = api.services.add_point(
    lon=10.0, 
    lat=20.0, 
    attributes=attributes
    layer_id=layer.id, 
    feature_service_url=service.url
)

print(success) # True or False
```

### Add multiple points to the feature layer

```
attributes = {
    "Date": "2020-01-01 15:30:45",
    "Name": "John Doe",
    "DeviceId": "abc123",
}

p1 = {
    'lon': 10.0, 'lat': 20.0,
    'Date': "2020-01-01 12:12:12",
    'Name': 'John Doe',
    'DeviceId': 'abc123'
}

p2 = {
    'lon': 10.0, 'lat': 20.0,
    'Date': "2020-01-01 12:12:12",
    'Name': 'John Doe',
    'DeviceId': 'abc123'
}

adds = api.services.add_points(
    points=[p1, p2], 
    layer_id=layer.id, 
    feature_service_url=service.url
)

# adds is a dict where key is object ID and value is success
for object_id, success in adds.items():
    print(object_id, success)
```


### Get a feature service
Get a feature service by passing the exact name of the service.
```
other_service = self.api.services.get_feature_service('OTHER_NAME')
```

### Get a feature layer
Get a layer from a feature service by looking up it's ID or exact name.
```
layer_by_id = api.services.get_feature_layer(service.url, layer_id=0)
layer_by_name = api.services.get_feature_layer(service.url, layer_name="other layer")
```

### Get features
You can get features from a feature layer by passing an SQL 92 formatted _where_ clause as described [here](https://developers.arcgis.com/rest/services-reference/query-feature-service-layer-.htm). Specify the attributes you want returned with the _out_fields_ argument.

>Pro tip: return all features with _where="1=1"_

>Only point features supported right now.
```
point_features = api.services.get_features(
    where="DeviceId = 'abc123'",
    layer_id=layer.id,
    feature_service_url=service.url,
    out_fields=['OBJECTID']
)

# point is a PointFeature object
point = point_features[0]
print(point.id, point.x, point.y)
```

### Update a feature service
>Only updating the service's _title_ supported right now.

```
success = api.services.update_feature_service(
    feature_service_id=service.id, 
    title="New Title"
)

print(success) # True or False
```

### Update features
Update multiple features by passing a list of tuples which contain an object ID, attributes to update and geometry respectively. If you want to update features based on a where clause, first get the features you want as described above.

>If you are not updating attributes or geometry, pass None.
```
updates_list = [
    (0, {"Name": "John Doe II"}, {"x": 10.1, "y": 20.1}),
    (1, None, {"x": 10.3, "y": 20.2}),
    (1, {"Name": "John Doe II"}, None),
]

updates = api.services.update_features(
    updates=updates_list, 
    layer_id=layer.id, 
    feature_service_url=service.url
)

for object_id, success in updates.items():
    print(object_id, success)
```

### Update table rows
Update multiple table rows by passing a list of tuples which contain an object ID and attributes to update. You can use a where clause to filter the affected rows.

```
updates_list = [
    (0, {"Name": "John Doe II", "Email": "johndoe2@example.com"}),
    (1, {"Name": "John Doe II", "Email": "johndoe2@example.com"})
]

updates = api.services.update_table_rows(
    updates=updates_list, 
    table_id=table.id, 
    feature_service_url=service.url
)

for object_id, success in updates.items():
    print(object_id, success)
```


### Delete features from a feature layer or table

Delete features by passing an SQL 92 _where_ clause.
```
deletes = api.services.delete_features(
    where="DeviceId = 'abc123'",
    layer_id=layer.id,
    feature_service_url=service.url
)

for object_id, success in deletes.items():
    print(object_id, success)
```

### Delete a feature layer

```
api.services.delete_feature_layers([layer.id], service.url)
```

### Delete a feature service

```
api.services.delete_feature_service(service.id)
```

### Exceptions
Invalid arguments to ArcGIS may result in an error. You can catch them with _ArcGISException_ which includes the message returned from ArcGIS.
```
try:
    # try to create a duplicate feature service
    api.services.create_feature_service('NAME', 'DESCRIPTION')
except saw.exceptions.ArcGISException as e:
    print(e)
```

## Testing

Before testing, configure the following environment variables:
- ARCGIS_ACCESS_TOKEN
- ARCGIS_REFRESH_TOKEN
- ARCGIS_CLIENT_ID
- ARCGIS_USERNAME
- ARCGIS_PASSWORD

By running the tests you will incur a small charge to your account.

```
python -m unittest tests/test*.py
```

## Authors

* **Casey Slaught** - *Lead developer* - [Caracal](https://github.com/caracal-cloud)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) for details

