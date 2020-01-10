# simple-arcgis-wrapper

A simple wrapper for interacting with the ArcGIS Online REST API.

## About

This project is geared towards developers who just want to get data into the ArcGIS Online as easily as possible. The REST API can be pretty confusing if you aren't familiar with ArcGIS jargon, so we created this simple wrapper to abstract some of the difficulties with creating resources and adding data.

## Prerequisites

First you will need an ArcGIS Online account and an app registered on the Developer portal.

Then you will need to know a thing or two about ArcGIS lingo.
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

### 0. Import
```
import simple_arcgis_wrapper as saw
```

### 1. Identify yourself

You will need a registered app and tokens obtained through the OAuth flow. Check out [this link](https://developers.arcgis.com/documentation/core-concepts/security-and-authentication/server-based-user-logins/) to learn more about setting up OAuth.

```
api = saw.ArcgisAPI(
    access_token='ACCESS_TOKEN',   # access token obtained from user
    refresh_token='REFRESH_TOKEN', # refresh token obtained from user
    username='USERNAME',           # username obtained from user
    client_id='CLIENT_ID'          # your OAuth app's client ID
)
```

### 2. Create a feature service

A feature service is like a container for many feature layers.

```
service = api.services.create_feature_service('NAME', 'DESCRIPTION')

print(service.id, service.name, service.url) # service is a FeatureService object
```

### 3. Create a feature layer in the feature service

A feature layer is where you actually store your geometric features like points, lines and polygons.

```
# First specify additional attribute columns.
fields = saw.fields.Fields()
fields.add_field('Date', saw.fields.DateField)
fields.add_field('Name', saw.fields.StringField)
fields.add_field('Altitude', saw.fields.DoubleField)

layer = api.services.create_feature_layer(
    layer_type='point',                      # point, line, or polygon
    name=name,                               # name of the layer
    description='My test description',       # description of the layer
    feature_service_url=feature_service.url, # the URL of the feature service that the layer will be added to
    fields=layer_fields,                     # a Fields instance
    x_min=10.0, y_min=10.0,                  # min bounding box parameters
    x_max=20.0, y_max=20.0,                  # max bounding box parameters
    wkid=4326                                # well-known ID spatial reference
)

print(layer.id, layer.name, layer.url) # layer is a FeatureLayer object

```

### 4. Add a point to the feature layer

```
# Specify an attributes with keys that match the layer's columns
attributes = {
    'Date': '2020-01-01 15:30:45',
    'Name': 'John Doe',
    'Altitude': 12.5
}

point_feature = api.services.add_point(lon=10.0, lat=20.0, layer_url=layer.url, attributes=attributes)

print(point_feature.id) # point_feature is a Feature object
```

### 5. Delete a feature layer

```
api.services.delete_feature_layers([layer.id], service.url)
```

### 6. Delete a feature service

```
api.services.delete_feature_service(service.id)
```


## Testing

Before testing, configure the following environment variables:
- ARCGIS_ACCESS_TOKEN
- ARCGIS_REFRESH_TOKEN
- ARCGIS_CLIENT_ID
- ARCGIS_USERNAME

By running the tests you will incur a (very) small charge to your account.

```
python -m unittest tests/test*.py
```

## Authors

* **Casey Slaught** - *Lead developer* - [Caracal](https://github.com/caracal-cloud)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) for details

