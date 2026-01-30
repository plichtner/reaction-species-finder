import sys
#from numpy import *
#import numpy as np
#import numpy
#import scipy
#import matplotlib
import datetime
import time


def parse_aq_rxn(line):
  parts = line.split()
  # name = parts[0].strip("'").replace("*", "")
  name = parts[0].strip("'")
  num_basis_species = int(parts[1].strip())
  basis_species = [
    # parts[3 + 2*k].strip("'").replace("*", "")
    parts[3 + 2*k].strip("'")
    for k in range(num_basis_species)
  ]
  all_species = [ name ] + basis_species
  stochiometry = [ 1 ] + [
    float(parts[2 + 2*k])
    for k in range(num_basis_species)
  ]

  return dict(
    name=name,
    num_basis_species=num_basis_species,
    basis_species=basis_species,
    all_species=all_species,
    stochiometry=stochiometry
  )

def parse_gas_or_mineral_rxn(line):
  parts = line.split()
  name = parts[0].strip("'")
  num_basis_species = int(parts[2].strip())
  basis_species = [
    # parts[4 + 2*k].strip("'").replace("*", "")
    parts[4 + 2*k].strip("'")
    for k in range(num_basis_species)
  ]
  all_species = [ name ] + basis_species
  stochiometry = [ 1 ] + [
    float(parts[3 + 2*k])
    for k in range(num_basis_species)
  ]

  return dict(
    name=name,
    num_basis_species=num_basis_species,
    basis_species=basis_species,
    all_species=all_species,
    stochiometry=stochiometry
  )


def rxn_to_string(rxn):
  reactants = " + ".join([
    f"{rxn['stochiometry'][i]} {rxn['all_species'][i]}"
    for i in range(1, len(rxn['all_species']))
  ])
  return f"{rxn['name']} ⇋ {reactants}"


with open('out/aq_spec.dat','r') as file:
  aq_rxns = [parse_aq_rxn(line.strip()) for line in file.readlines()]
with open('out/gases.dat','r') as file:
  gas_rxns = [parse_gas_or_mineral_rxn(line.strip()) for line in file.readlines()]
with open('out/minerals.dat','r') as file:
  mineral_rxns = [parse_gas_or_mineral_rxn(line.strip()) for line in file.readlines()]

with open('aq_skip.dat','r') as file:
  faq_skip = [line.strip().strip("'") for line in file.readlines()]
with open('gas_skip.dat','r') as file:
  fgas_skip = [line.strip().strip("'") for line in file.readlines()]
with open('min_skip.dat','r') as file:
  fmin_skip = [line.strip().strip("'") for line in file.readlines()]


# 
# Filter out reactions listed in faq_skip, fgas_skip, fmin_skip
# 

aq_rxns = [
  rxn for rxn in aq_rxns
  if rxn['name'] not in faq_skip
]

gas_rxns = [
  rxn for rxn in gas_rxns
  if rxn['name'] not in fgas_skip
]

mineral_rxns = [
  rxn for rxn in mineral_rxns
  if rxn['name'] not in fmin_skip
]

all_aq_species = sorted(set([
  species
  for rxn in aq_rxns
  for species in rxn['all_species']
]), key=len)



def get_matching_aq_species(query):
  results = []
  max_num_results = 20

  if (len(query) == 0):
    return []
  
  for aq_spec in all_aq_species:
    if query in aq_spec:
      results.append(aq_spec)

    # if len(results) >= max_num_results:
    #   break

  # print(results)

  return results


def aq_reaction_info(name):
  for rxn in aq_rxns:
    if rxn['name'] == name:
      return rxn


def mineral_reaction_info(name):
  for rxn in mineral_rxns:
    if rxn['name'] == name:
      return rxn


def gas_reaction_info(name):
  for rxn in gas_rxns:
    if rxn['name'] == name:
      return rxn


def calculate_reactions(primary_species):
  '''
  Returns a dictionary containing:
  - primary_species: a list of names of the primary species
  - secondary_species: a list of reactions producing aqueous species
  - gas_species: a list of reactions producing gas species
  - mineral_species: a list of reactions producing mineral species
  '''

  # NB: first run "find_values_no_temp_data.py" to generate text input files
  # before setting this flag to true
  exclude_species_without_temp_data = False
  #exclude_species_without_temp_data = True

  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y.%m.%d %H:%M:%S')

  # print('Author: PCL ',st)
  # print('=============================================')

  """

  Author: P.C. Lichtner
  Date: 10-07-2015

  -----------------------------
  database structures         |
  -----------------------------
  hanford.dat      rxn3.py    |
  -----------------------------
  basis (pri)     basis (pri) |
  aqueous         aqueous     |
  minerals        gases       |
  gases           minerals    |
  srf cmplx       srf cmplex  |
  -----------------------------
  Version 2.0 use python3 [print ()] |
  -----------------------------

  Input files: aq_spec.dat, gases.dat, minerals.dat
  Skip files: aq_skip.dat, gas_skip.dat, min_skip.dat

  Outfiles: chem.out

  It is necessary to consider both standard (normal) and nonstandard ordering of the primary species.
  Standard ordering is in the same order as the database; nonstandard implies swaping of
  basis species (e.g. OH-/H+, CO2(aq)/HCO3-, Al(OH)4-/Al+++, etc.). If a database contains
  reactions with both types of ordering then standard refers to form of the majority of reactions.

  """


  #=============== end of examples ==================

  # check for duplicate primary species
  for pri_spec in primary_species:
    ndup = 0
    ispec = 0
    for pri_spec1 in primary_species:
      ispec = ispec + 1
      if pri_spec == pri_spec1:
        ndup = ndup + 1
        if ndup > 1:
          print ('Error: duplicate primary species:',ispec,pri_spec) 
          exit("Run Stopped")

  # check for presence of H2O in list of primary species
  if 'H2O' not in primary_species:
    print ('Error: H2O missing from list of primary species!')
    exit("Run Stopped")


  def accumulate_secondary_species(primary_species, secondary_species=[]):
    '''
    This is the meat of our algorithm. Given a list of primary and secondary
    species, we look through the list of aq_rxns for matching reactions
    and accumulate them in the list of secondary species. This process is
    repeated until no new reactions are found.
    '''
    
    found_a_new_secondary_species = False
    all_species_so_far = primary_species + [
      rxn['name']
      for rxn in secondary_species
    ]
    # all_species_so_far = primary_species + secondary_species
    
    for rxn in aq_rxns:
      # if exactly 1 species in rxn missing from what we've accumulated so far:
      missing_species = [
        species for species in rxn['all_species']
        if species not in all_species_so_far
      ]

      if len(missing_species) == 1:
        # secondary_species += missing_species
        secondary_species += [dict(name=missing_species[0], rxn=rxn)]
        found_a_new_secondary_species = True

    if found_a_new_secondary_species:
      secondary_species = accumulate_secondary_species(primary_species, secondary_species)

    return secondary_species


  secondary_species = accumulate_secondary_species(primary_species)

  # duplicate check
  secondary_species_names = [rxn['name'] for rxn in secondary_species]
  if (len(list(set(secondary_species_names))) != len(secondary_species_names)):
    print("Uh oh. Somehow we accumulated the same secondary species twice:")
    print(f"Primary species: {', '.join(primary_species)}")
    for rxn in sorted(secondary_species, key=lambda d: d['name']):
      print(rxn['name'] + ": " + rxn_to_string(rxn['rxn']))
    print("That should not happen if the reactions in the database are non-redundant.")

  # 
  # Gas Species
  # 

  all_reactants = primary_species + [rxn['name'] for rxn in secondary_species]

  # if 'O2(aq)' in all_reactants:
  #   all_reactants += ['O2(g)']

  gas_species = [
    gas_rxn['name'] for gas_rxn in gas_rxns
    if set(gas_rxn['basis_species']).issubset(all_reactants)
  ]

  #
  # Mineral Species
  #

  mineral_species = [
    mineral_rxn['name'] for mineral_rxn in mineral_rxns
    if set(mineral_rxn['basis_species']).issubset(all_reactants)
  ]

  # exclude O2(g) from secondaries -- we already have O2(aq)
  secondary_species = [rxn for rxn in secondary_species if rxn['name'] != "O2(g)"]

  return dict(
    primary_species=sorted(primary_species),
    secondary_species=sorted(secondary_species, key=lambda d: d['name']),
    gas_species=sorted(gas_species),
    mineral_species=sorted(mineral_species),
  )


if __name__ == '__main__':
  # calculate_reactions(['A(aq)', 'B(aq)', 'H2O'])
  # calculate_reactions(['AB(aq)', 'B(aq)', 'H2O'])
  # calculate_reactions(['A(aq)', 'A(aq)', 'H2O'])
  # result = calculate_reactions(['UO2++','U+++', 'H+', 'O2(aq)', 'H2O'])
  # result = calculate_reactions([
  #   'Na+', 'K+', 'Ca++', 'H+', 'Cu++', 'Al+++',
  #   'Fe++', 'SiO2(aq)', 'HCO3-', 'SO4--', 'Cl-',
  #   'O2(aq)', 'H2O'
  # ])
  result = calculate_reactions([
    'OH-', 'Al(OH)4-', 'SO4--', 'Ca++', 'H2O'
  ])
  # calculate_reactions(['OH-', 'Al(OH)4-', 'H2O'])
  # result = calculate_reactions(['OH-', 'Al(OH)4-', 'H2O'])
  
  print("PRIMARY_SPECIES")
  print('\n'.join(result['primary_species']))
  print("END")
  print()

  print("SECONDARY_SPECIES")
  print('\n'.join(result['secondary_species']))
  print("END")
  print()

  print("PASSIVE_GAS_SPECIES")
  print('\n'.join(result['gas_species']))
  print("END")
  print()

  print("MINERALS")
  print('\n'.join(result['mineral_species']))
  print("END")
  print()

  print(f"for {len(result['primary_species'])} primary species, found {len(result['secondary_species'])} secondary species, {len(result['gas_species'])} gases, and {len(result['mineral_species'])} minerals.")

  print()
  print(f"Saving to file chem.out...")
  
  with open("chem.out", "w") as file:
    print("#=========================== chemistry ========================================", file=file)
    print("CHEMISTRY", file=file)
    print("  PRIMARY_SPECIES", file=file)
    for spec in result['primary_species']:
      print(f'    {spec}', file=file)
    print("  END", file=file)

    print("  SECONDARY_SPECIES", file=file)
    for spec in result['secondary_species']:
      print(f'    {spec}', file=file)
    print("  END", file=file)

    print("  PASSIVE_GAS_SPECIES", file=file)
    for spec in result['gas_species']:
      print(f'    {spec}', file=file)
    print("  END", file=file)

    print("  MINERALS", file=file)
    for spec in result['mineral_species']:
      print(f'    {spec}', file=file)
    print("  END", file=file)
    print("END", file=file)

  print("done")
