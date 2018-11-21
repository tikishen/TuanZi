## proj_nps.py
## Skeleton for Project 2, Fall 2018
## ~~~ modify this file, but don't rename it ~~~
from secrets import google_places_key
import requests
import json
from bs4 import BeautifulSoup

FILENAME = 'nps.json'
try:
    with open(FILENAME, 'r') as f:
        cache_dict = json.load(f)
except:
    cache_dict = {}

FILE_NATIONAL_SITE = 'national_site.json'
try:
    with open(FILE_NATIONAL_SITE, 'r') as f:
        cache_site = json.load(f)
except:
    cache_site = {}


class Cache:
    def __init__(self, filename):
        """Load cache from disk, if present"""
        self.filename = filename
        try:
            with open(self.filename, 'r') as cache_file:
                cache_json = cache_file.read()
                self.cache_diction = json.loads(cache_json)
        except:
            self.cache_diction = {}

    def _save_to_disk(self):
        """Save cache to disk"""
        with open(self.filename, 'w') as cache_file:
            cache_json = json.dumps(self.cache_diction)
            cache_file.write(cache_json)

    def get(self, identifier):
        """If unique identifier exists in the cache, return the data associated with it, else return None"""
        identifier = identifier.upper()
        if identifier in self.cache_diction:
            data = self.cache_diction[identifier]
        else:
            data = None
        return data

    def set(self, identifier, data):
        """Add identifier and its associated data to the cache, and save the cache as json"""
        identifier = identifier.upper()
        self.cache_diction[identifier] = data
        self._save_to_disk()


## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)


class NationalSite:
    def __init__(self, type, name, url=None, address_street=None, address_city=None, address_state=None,
                 address_zip=None):
        self.type = type
        self.name = name
        # self.description = desc TODO: add desc into parameter
        self.url = url

        # needs to be changed, obvi.
        self.address_street = address_street
        self.address_city = address_city
        self.address_state = address_state
        self.address_zip = address_zip

    def __repr__(self):
        return '{} ({}): {}, {}, {} {}'.format(self.name, self.type, self.address_street, self.address_city,
                                               self.address_state, self.address_zip)

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)


class NearbyPlace:
    def __init__(self, name, lat, lng):
        self.name = name
        self.lat = lat
        self.lng = lng

    def __str__(self):
        return self.name


## Must return the list of NationalSites for the specified state
## param: the 2-letter state abbreviation, lowercase
##        (OK to make it work for uppercase too)
## returns: all of the NationalSites
##        (e.g., National Parks, National Heritage Sites, etc.) that are listed
##        for the state at nps.gov

def get_sites_for_state(state_abbr):
    parks = []

    baseurl = 'https://www.nps.gov/state/{}/index.htm'.format(state_abbr)
    if baseurl in cache_dict:
        state_soup = BeautifulSoup(cache_dict[baseurl], 'html.parser')
    else:
        state_text = requests.get(baseurl).text
        state_soup = BeautifulSoup(state_text, 'html.parser')
        cache_dict[baseurl] = state_text
        with open(FILENAME, 'w') as f:
            dumped_json = json.dumps(cache_dict, indent=4)
            f.write(dumped_json)

    # (Nice Try) Find all href links of states
    # state_url_lst = []
    # for state_ul in soup.find_all('ul', {'class': 'dropdown-menu'}):
    #     for state_li in state_ul.find_all('li'):
    #         state_url_lst.append(state_li.a.get('href')) # Append the all the link to state page in state_url_lst

    # Go to the state page to find park name and park type, as well as a list a location href.
    park_soup = state_soup.find_all(class_="col-md-9 col-sm-9 col-xs-12 table-cell list_left")
    for park in park_soup:
        park_name = park.find('h3').text
        park_type = park.find('h2').text
        park_desc = park.find('p').text
        park_location_url = park.find('a').get('href')

        # Go to the state location site.
        loc_url = 'https://www.nps.gov{}index.htm'.format(park_location_url)

        # Check whether the site infomration has cached.
        if loc_url in cache_dict:
            loc_soup = BeautifulSoup(cache_dict[loc_url], 'html.parser')
        else:
            site_text = requests.get(loc_url).text
            loc_soup = BeautifulSoup(site_text, 'html.parser')
            cache_dict[loc_url] = site_text
            with open(FILENAME, 'w') as f:
                dumped_json = json.dumps(cache_dict, indent=4)
                f.write(dumped_json)

        # Go to the basic information page to find mailing address.
        # Some sites do not contain information of mailing address. In this case, it would only contain
        # the state address.
        try:
            str_address = loc_soup.find('span', itemprop='streetAddress').string.strip('\n')
            city_address = loc_soup.find('span', itemprop='addressLocality').string
            state_address = loc_soup.find('span', itemprop='addressRegion').string
            zip_address = loc_soup.find('span', itemprop='postalCode').string.strip(' ')
        except:
            str_address = None
            city_address = None
            state_address = state_abbr
            zip_address = None

        # Init the NationalSite class by the parameters retrieved above.
        one_park = NationalSite(park_type, park_name, url=None, address_street=str_address,
                                address_city=city_address, address_state=state_address, address_zip=zip_address)
        parks.append(one_park)
        # TODO add park_desc

    return parks

# print(get_sites_for_state('MI'))

## Must return the list of NearbyPlaces for the specifite NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list

# Utility function provided for your use here (DO NOT CHANGE) -- to create a unique representation of each request without private data like API keys
def params_unique_combination(baseurl, params_d, private_keys=('api_key',)):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)


def get_location_text_search(national_site: NationalSite):
    baseurl = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params_diction = {}
    params_diction['key'] = google_places_key
    params_diction['query'] = national_site.name
    params_diction['type'] = national_site.type

    unique_rep = params_unique_combination(baseurl, params_diction)

    if unique_rep in cache_site:
        site_loc = cache_site[unique_rep]

    else:
        resp = requests.get(baseurl, params=params_diction)
        cache_site[unique_rep] = json.loads(resp.text)
        dumped_json_cache = json.dumps(cache_site, indent=4)
        with open(FILE_NATIONAL_SITE, 'w') as f:
            f.write(dumped_json_cache)
            site_loc = cache_site[unique_rep]
    try:
        lat = site_loc['results'][0]['geometry']['location']['lat']
        lng = site_loc['results'][0]['geometry']['location']['lng']
    except:
        lat = None
        lng = None

    return '{}, {}'.format(lat,lng)


def get_nearby_places_for_site(national_site: NationalSite):
    nearby_places = []

    baseurl = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params_diction = {}
    params_diction['key'] = google_places_key
    params_diction['location'] = get_location_text_search(national_site)
    params_diction['radius'] = 10000

    unique_rep = params_unique_combination(baseurl, params_diction)

    if unique_rep in cache_site:
        nearby_loc = cache_site[unique_rep]

    else:
        resp = requests.get(baseurl, params=params_diction)
        cache_site[unique_rep] = json.loads(resp.text)
        dumped_json_cache = json.dumps(cache_site, indent=4)
        with open(FILE_NATIONAL_SITE, 'w') as f:
            f.write(dumped_json_cache)
            nearby_loc = cache_site[unique_rep]

    for i in range(len(nearby_loc['results'])):
        name = nearby_loc['results'][i]['name']
        nearby_places.append(NearbyPlace(name))

    return nearby_places



## Must plot all of the NationalSites listed for the state on nps.gov
## Note that some NationalSites might actually be located outside the state.
## If any NationalSites are not found by the Google Places API they should
##  be ignored.
## param: the 2-letter state abbreviation
## returns: nothing
## side effects: launches a plotly page in the web browser
def plot_sites_for_state(state_abbr):
    pass

## Must plot up to 20 of the NearbyPlaces found using the Google Places API
## param: the NationalSite around which to search
## returns: nothing
## side effects: launches a plotly page in the web browser
def plot_nearby_for_site(site_object):
    pass

if __name__ == '__main__':
    print(get_location_text_search(NationalSite('Sleeping Bear Dunes', 'National Lakeshore')))
    print(get_nearby_places_for_site(NationalSite('Sleeping Bear Dunes', 'National Lakeshore')))




















