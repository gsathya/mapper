import urllib

urls = "http://www.zillow.com/static/shp/ZillowNeighborhoods-%s.zip"
states = [
    "AK",
    "AL",
    "AR",
    "AZ",
    "CA",
    "CO",
    "CT",
    "DC",
    "FL",
    "GA",
    "HI",
    "IA",
    "ID",
    "IL",
    "IN",
    "KS",
    "KY",
    "LA",
    "MA",
    "MD",
    "ME",
    "MI",
    "MN",
    "MO",
    "MS",
    "MT",
    "NC",
    "NE",
    "NJ",
    "NM",
    "NV",
    "NY",
    "OH",
    "OR",
    "PA",
    "RI",
    "TN",
    "TX",
    "UT",
    "VA",
    "WA",
    "WI"
]

for state in states:
    url = urls % state
    print url
    urllib.urlretrieve(url, state.lower()+'.zip')
