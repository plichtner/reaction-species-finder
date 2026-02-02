from rxn3_lib_v2 import db_aq_rxns, db_gas_rxns, db_mineral_rxns
from collections import Counter

aq_log_ks = []
for rxn in db_aq_rxns:
  log_k_string = "".join([
    "_" if k == 500 else "+"
    for k in rxn['log_ks']
  ])
  aq_log_ks.append(log_k_string)

aq_counts = Counter(aq_log_ks)

gas_log_ks = []
for rxn in db_gas_rxns:
  log_k_string = "".join([
    "_" if k == 500 else "+"
    for k in rxn['log_ks']
  ])
  gas_log_ks.append(log_k_string)

gas_counts = Counter(gas_log_ks)

mineral_log_ks = []
for rxn in db_mineral_rxns:
  log_k_string = "".join([
    "_" if k == 500 else "+"
    for k in rxn['log_ks']
  ])
  mineral_log_ks.append(log_k_string)

mineral_counts = Counter(mineral_log_ks)

print("\naqueous 500s:")
print(aq_counts)
print("\ngas 500s:")
print(gas_counts)
print("\nmineral 500s:")
print(mineral_counts)
