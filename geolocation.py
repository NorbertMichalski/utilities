import requests
import json
import math
from time import mktime, gmtime, localtime
import time
from supply.models import Brand, Location

class Locate(object):

    def geolocate(self, address):
        url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&sensor=false"
        resp = requests.get(url)
        # print resp.content
        json_obj = json.loads(resp.content)
        try:
            lat = json_obj["results"][0]["geometry"]["location"]["lat"]
            lng = json_obj["results"][0]["geometry"]["location"]["lng"]
        except:
            lat = 0
            lng = 0
        return (lat, lng)

    def get_zip(self, lat, lng):
        try:
            location = Location.objects.filter(latitude=lat, longitude=lng)[0]
            return location.zip
        except:
            print lat, lng
            url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=true' % (lat, lng)
            resp = requests.get(url)
            json_obj = json.loads(resp.content)
            try:
                if json_obj["results"][0]["address_components"][-1]["types"][0] == 'postal_code':
                    zip = json_obj["results"][0]["address_components"][-1]["short_name"]
                print zip
            except Exception as e:
                print e
                return 0
            return zip


    def get_timezone(self, lat, lng):
        now = int(mktime(gmtime()))
        print now
        url = 'https://maps.googleapis.com/maps/api/timezone/json?location=%s,%s&timestamp=%s&sensor=false' % (lat, lng, now)
        resp = requests.get(url)
        print resp.text
        json_obj = json.loads(resp.content)
        try:
            ds_offset = json_obj["dstOffset"]
            raw_offset = json_obj["rawOffset"]
            time_zone = json_obj["timeZoneName"]
            local_time = localtime(now + raw_offset)
        except Exception as e:
            print e
            time_zone = 'Not found'
        return time_zone

    def get_timediff(self, lat, lng):
        now = int(mktime(gmtime()))
        print now
        url = 'https://maps.googleapis.com/maps/api/timezone/json?location=%s,%s&timestamp=%s&sensor=false' % (lat, lng, now)
        resp = requests.get(url)
        print resp.text
        json_obj = json.loads(resp.content)
        try:
            ds_offset = json_obj["dstOffset"]
            raw_offset = json_obj["rawOffset"]
            time_zone = json_obj["timeZoneName"]
            local_time = localtime(now + raw_offset)
        except Exception as e:
            print e
            return 0
        return raw_offset

    def get_local_time(self, location):
        now = int(mktime(gmtime()))
        try:
            found_locations = Location.objects.filter(slug=location)
            time_delta = found_locations[0].timediff
        except Exception as e:
            print e
            (lat, lng) = self.geolocate(location)
            time_delta = self.get_timediff(lat, lng)
        local_time = localtime(now + time_delta)
        return '%s' % (time.strftime('%I:%M %p', local_time))

    def search_location(self, brand_name, address):
        location = Location()
        try:
            found_locations = Location.objects.select_related().filter(slug=address)
            print found_locations
            for found_location in found_locations:
                if str(found_location.brand) == brand_name:
                    return (found_location.latitude, found_location.longitude)
            else:
                raise IndexError

        except Exception as e:
            print e
            try:
                brand = Brand.objects.get(name=brand_name)
            except Exception as e:
                print e
                brand = Brand()
                brand.name = brand_name
                brand.save()
            location.city_state = address
            location.slug = address
            location.brand = brand
            (location.latitude, location.longitude) = self.geolocate(address)
            print location.latitude
            print location.longitude
            location.zip = self.get_zip(location.latitude, location.longitude)
            location.timezone = self.get_timezone(location.latitude, location.longitude)
            location.timediff = self.get_timediff(location.latitude, location.longitude)

            location.save()
            return (location.latitude, location.longitude)


    def distance(self, origin, destination):
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 3956.6  # mi

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist = radius * c
        return ('%.2f' % dist)
    
    def get_city_state(self, location):
        try:
            found_location = Location.objects.filter(slug=location)[0].city_state
            cleaned_result = ' '.join([x.capitalize() for x in found_location.split(' ')])
            cleaned_result = str(cleaned_result.split(',')[0] + ', ' + cleaned_result.split(',')[1].upper())
            #found_location = str(found_location.split(',')[0].capitalize() + ', ' + found_location.split(',')[1].upper())
            return cleaned_result
        except Exception as e:
            print e
            return location


if __name__ == '__main__':
    mumu = Locate()
    # print mumu.geolocate('Dallas, TX')
    # print mumu.get_zip(32.7801399, -96.80045109999999)
    # print mumu.get_timezone(32.7801399, -96.80045109999999)
    # print mumu.search_location('baldor', 'STE-CLAIRE, QC')
    print mumu.get_local_time('Dallas, TX')