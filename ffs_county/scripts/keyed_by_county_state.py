import json
import pandas as pd

ssa_to_fips_counties = pd.read_csv('../data/ssa_fips_state_county2015.csv', dtype=str)

ssa_to_fips = {}
for index, row in ssa_to_fips_counties.iterrows():
    if not row.ssastate in ssa_to_fips:
      ssa_to_fips[row.ssastate] = row.fipsstate

data = pd.read_json('https://data.cms.gov/resource/vfca-ven7.json?$limit=4000', dtype=str)

keyed_by_county_and_state = {}

for i, item in data.iterrows():
    ssa_state = item['state_id']
    if ssa_state in ssa_to_fips:    
      fips_state = ssa_to_fips[ssa_state]
      county_and_state_key = fips_state + '-' + item['county_name']
      keyed_by_county_and_state[county_and_state_key] = item.to_dict()

with open('ffs_keyed_by_state_county.json', 'w') as outfile:
    json.dump(keyed_by_county_and_state, outfile)
