# simple-arcgis-wrapper

A simple wrapper for interacting with the ArcGIS Online REST API.

## About

This project is geared towards developers who just want to get data into the ArcGIS Online as easily as possible. The REST API can be pretty confusing if you aren't familiar with ArcGIS-specific concepts, so we created this simple wrapper to abstract some of the difficulties with creating resources and adding data.

## Prerequisites

You will need to have an ArcGIS Online account.

Before you get started, you should know a thing or two about ArcGIS lingo.
Here are few key terms:
Feature service:
Feature layer:
Feature:

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
There are 3 ways to get started:

1. [Tokens](https://developers.arcgis.com/documentation/core-concepts/security-and-authentication/server-based-user-logins/)

```
client = saw.ArcgisApi(access_token=access_token, refresh_token=refresh_token)
```

2. [Client credentials](https://developers.arcgis.com/labs/rest/get-an-access-token/) (not yet implemented)

- This will exchange your credentials for a one-time access token.

```
client = saw.ArcgisApi(client_id=client_id, client_secret=client_secret)
```

3. Username/password login
- Use this scheme to easily manage your own ArcGIS Online account.
- Make sure you store your credentials in environment variables!


```
client = saw.ArcgisApi(access_token, refresh_token)
```

### 2. Create a feature service

A feature service is a container for many feature layers.

```
fs = client.create_feature_service(name="My Project", description="My Project location data")
```

### 3. Create a feature layer in your feature service

A feature layer is where you actually store your geometries like points, lines and polygons.

```
fields = saw.FieldsBuilder()
fields.add_field(name="Date", type=saw.fields.DateField)
fields.add_field(name="Name", type=saw.fields.StringField, default="John Doe")
fields.add_field(name="Altitude", type=saw.fields.DoubleField)

fl = client.create_feature_layer(type='point', name='My Point Layer', description='My amazing points', feature_service_url=fs.url, fields=fields, x_min=10.0, y_min=10.0, 
x_max=20.0, y_max=20.0, wkid=4326)
```


## Testing

Before testing, configure ARCGIS_ACCESS_TOKEN and ARCGIS_REFRESH_TOKEN environment variables.

```
python -m unittest tests/test*.py
```

The token will be automatically refreshed.

## Authors

* **Casey Slaught** - *Initial work* - [Caracal](https://github.com/caracal-cloud)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
