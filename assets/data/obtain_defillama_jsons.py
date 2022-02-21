# %%
import pandas as pd
import json
import requests
import re
from collections import Counter, defaultdict
import datetime as dt

# %% [markdown]
# # Protocols JSON

# %%
protocols = requests.get('https://api.llama.fi/lite/protocols2')
config = requests.get('https://api.llama.fi/config')

# %%
protocols = protocols.json()
config = config.json()

# %%
# get tvl per protocol for ordering
protocols_TVL = {}
for protocol in protocols['protocols']:
    protocols_TVL[protocol['name']] = protocol['tvl']

protocols_TVL = list(protocols_TVL.items())
protocols_TVL.sort(key = lambda x:x[1], reverse=True)
protocols_TVL_names = [x[0] for x in protocols_TVL]

# %%
# move stakewise first in list of liquid staking protocols
old_stakewise_position = protocols_TVL_names.index('StakeWise')
protocols_TVL_names.insert(0, 'StakeWise')
del protocols_TVL_names[old_stakewise_position + 1]

# %%
protocols_data_by_name = {}

# loop over protocols
for i,protocol_name in enumerate(protocols_TVL_names):
    protocol = [x for x in config['protocols'] if x['name'] == protocol_name][0]

    # add protocols
    protocols_data_by_name[protocol_name] = {
        'id': i,
        'category': protocol['category'],
        'url': protocol['url'],
    }

# %%
protocols_data = {'protocols':[]}

# loop over protocols
for i,protocol_name in enumerate(protocols_TVL_names):
    protocol = [x for x in config['protocols'] if x['name'] == protocol_name][0]


    # add protocols basic info
    protocols_data['protocols'].append({
        'id': i,
        'name': protocol_name,
        'category': protocol['category'],
        'url': protocol['url']
    })
    # add protocol details that protocols may not have
    # token status
    try:
        protocols_data['protocols'][i]['has_token'] = [False if not protocol['address'] else True][0]
    except:
        protocols_data['protocols'][i]['has_token'] = False
    
    # token address
    try:
        protocols_data['protocols'][i]['address'] = [None if protocol['address'] in ["-", None] else re.sub(r'\w{1,}:', r'',protocol['address'])][0]
    except:
        protocols_data['protocols'][i]['address'] = None

    # token symbol
    try:
        protocols_data['protocols'][i]['symbol'] = [None if protocol['symbol'] == "-" else protocol['symbol']][0]
    except:
        protocols_data['protocols'][i]['symbol'] = None
    
    # audit status
    try:
        protocols_data['protocols'][i]['is_audited'] = [False if not protocol['audit_links'] else True][0]
    except:
        protocols_data['protocols'][i]['is_audited'] = False
    
    # audit links:
    try:
        protocols_data['protocols'][i]['audits'] = protocol['audit_links']
    except:
        protocols_data['protocols'][i]['audits'] = None

# %%
# loop over protocols
for protocol in protocols['protocols']:

    # add chains by checking category and name
    try:
        if protocol['category'] == protocols_data_by_name[protocol['name']]['category']:
            protocol_id = protocols_data_by_name[protocol['name']]['id']
            protocols_data['protocols'][protocol_id]['chains'] = protocol['chains']
    except:
        continue

# %%
for i,d in enumerate(protocols_data['protocols']):
    if 'chains' not in d.keys():
        del protocols_data['protocols'][i]

# %%
# removing shit protocols that either failed or rugpulled
list_of_shame = [
    'StakeHound',
    'SharedStake'
]

protocols_data = {'protocols':[x for x in protocols_data['protocols'] if x['name'] not in list_of_shame]}

# %%
# All categories counter to join some as 'other'
all_cats = [x['category'] for x in protocols_data['protocols']]
all_cats = Counter(all_cats)

for protocol in protocols_data['protocols']:
    if all_cats[protocol['category']] < 5:
        protocol['subcategory'] = protocol['category']
        protocol['category'] = 'Other'

# %%
with open('./assets/data/protocols.json','w') as f:
    json.dump(protocols_data, f, indent=4)

# %% [markdown]
# # Chains protocols JSON

# %%
chains = []

for protocol in protocols_data['protocols']:
    try:
        for chain in protocol['chains']:
            if chain not in chains:
                chains.append(chain)
            else:
                pass
    except:
        continue

# %%
chains_protocols_audit = {chain:{'audited':defaultdict(list), 'unaudited':defaultdict(list)} for chain in chains}

for chain in chains:
    for protocol in protocols_data['protocols']:
        p_id = protocol['id']
        if chain in protocol['chains']:
            if protocol['audits']:
                chains_protocols_audit[chain]['audited']['apps'].append(protocol['name'])
                chains_protocols_audit[chain]['audited']['ids'].append(p_id)
            else:
                chains_protocols_audit[chain]['unaudited']['apps'].append(protocol['name'])
                chains_protocols_audit[chain]['unaudited']['ids'].append(p_id)

# %%
chains_protocols_token = {chain:{'token':defaultdict(list), 'no_token':defaultdict(list)} for chain in chains}

for chain in chains:
    for protocol in protocols_data['protocols']:
        p_id = protocol['id']
        if chain in protocol['chains']:
            if protocol['address']:
                chains_protocols_token[chain]['token']['apps'].append(protocol['name'])
                chains_protocols_token[chain]['token']['ids'].append(p_id)
            else:
                chains_protocols_token[chain]['no_token']['apps'].append(protocol['name'])
                chains_protocols_token[chain]['no_token']['ids'].append(p_id)


# %% [markdown]
# #### Chains categories

# %%
categories = {}

for protocol in protocols_data['protocols']:
    if protocol['category'] not in categories:
        categories[protocol['category']] = []
    else:
        pass

# %%
for chain, d in chains_protocols_audit.items():
    for audit_status, ptcs in d.items():
        audit_status = True if audit_status == 'audited' else False
        ids = ptcs['ids']
        protocols_in_this_chain = [x for x in protocols_data['protocols'] if chain in x['chains'] and x['is_audited'] == audit_status]
        

        for protocol in protocols_in_this_chain:
            chains_present = [x['chain'] for x in categories[protocol['category']]]
            if chain in protocol['chains'] and chain not in chains_present:
                if audit_status == True:
                    item_to_insert = {'chain':chain, 'has_audited':True, 'has_unaudited':False, 'has_token':False, 'has_no_token':False}
                else:
                    item_to_insert = {'chain':chain, 'has_audited':False, 'has_unaudited':True, 'has_token':False, 'has_no_token':False}
                categories[protocol['category']].append(item_to_insert)
            else:
                object_in_list = [x for x in categories[protocol['category']] if x['chain'] == chain][0]
                element_index = categories[protocol['category']].index(object_in_list)
                if audit_status == True:
                    categories[protocol['category']][element_index]['has_audited'] = True
                else:
                    categories[protocol['category']][element_index]['has_unaudited'] = True


# %%
for chain, d in chains_protocols_token.items():
    for token_status, ptcs in d.items():
        token_status = True if token_status == 'token' else False
        ids = ptcs['ids']
        protocols_in_this_chain = [x for x in protocols_data['protocols'] if chain in x['chains'] and x['has_token'] == token_status]
        

        for protocol in protocols_in_this_chain:
            object_in_list = [x for x in categories[protocol['category']] if x['chain'] == chain][0]
            element_index = categories[protocol['category']].index(object_in_list)
            if token_status == True:
                categories[protocol['category']][element_index]['has_token'] = True
            else:
                categories[protocol['category']][element_index]['has_no_token'] = True


# %%
with open('./assets/data/categories.json','w') as f:
    json.dump(categories, f, indent=4)

with open('./assets/data/last_data_update.json','w') as f:
    now = {'data_last_updated':dt.datetime.now().strftime("%Y-%m-%d")}
    json.dump(now, f, indent=4)


