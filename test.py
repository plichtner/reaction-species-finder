from rxn3_lib_v2 import calculate_reactions

tests = [
	dict(
		description="""Standard ordering works""",
		primary=['A(aq)', 'B(aq)', 'H2O'],
		secondary=['AB(aq)'],
		gas=['H2O(g)'],
		mineral=['Rock(s)','A(s)','A(s)*','AB(s)','A2(s)']
	),
	dict(
	    description="Non-standard ordering works",
	    primary=['AB(aq)', 'B(aq)', 'H2O'],
	    secondary=['A(aq)'],
	    gas=['H2O(g)'],
	    mineral=['Rock(s)', 'A(s)', 'A(s)*', 'AB(s)', 'A2(s)']
	),
	# dict(
	#     description="No duplicates allowed in primary species",
	#     primary=['A(aq)', 'A(aq)', 'H2O'],
	#     secondary=[],
	#     gas=['H2O(g)'],
	#     mineral=['Rock(s)', 'A(s)', 'A(s)*', 'A2(s)']
	# ),
	dict(
	    description="O2(g) in database becomes O2(aq) in standard ordering",
	    primary=['H2(aq)', 'H2O'],
	    secondary=['O2(aq)'],
	    gas=['H2(g)', 'H2O(g)', 'O2(g)'],
	    mineral=['Rock(s)']
	),
	dict(
	    description="O2(aq) matches O2(g) when checking non-standard ordering",
	    primary=['O2(aq)', 'H2O'],
	    secondary=['H2(aq)'],
	    gas=['H2(g)', 'H2O(g)', 'O2(g)'],
	    mineral=['Rock(s)']
	),
	dict(
	    description="Collecting secondary species from a second pass works",
	    primary=['UO2++','U+++', 'H+', 'O2(aq)', 'H2O'],
	    secondary=[
	        'H2(aq)', 'U++++',
	        '(UO2)2(OH)2++', '(UO2)2OH+++', '(UO2)3(OH)4++', 
	        '(UO2)3(OH)5+', '(UO2)3(OH)7-', '(UO2)4(OH)7+', 
	        'HO2-', 'OH-', 'UO2(OH)2(aq)', 'UO2(OH)3-', 
	        'UO2(OH)4--', 'UO2OH+', 'U(OH)4(aq)', 'UOH+++',
	        'UO2+'
	    ],
	    gas=['H2(g)', 'H2O(g)', 'O2(g)'],
	    mineral=[
	        'Rock(s)', 'Schoepite', 'Schoepite-dehy(.393)', 
	        'Schoepite-dehy(.648)', 'Schoepite-dehy(.85)', 
	        'Schoepite-dehy(.9)', 'Schoepite-dehy(1.0)', 
	        'UO2(am)', 'UO2.3333(beta)', 'UO2.6667', 'Uraninite',
	        'UO2.25', 'UO2.25(beta)'
	    ]
	),
	dict(
	    description="Fe++, Fe+++, H+, H2O works",
	    primary=['Fe++', 'Fe+++', 'H+', 'H2O'],
	    secondary=[
	        'O2(aq)', 'H2(aq)', 'Fe(OH)2(aq)', 'Fe(OH)2+', 'Fe(OH)3(aq)', 
	        'Fe(OH)3-', 'Fe(OH)4-', 'Fe(OH)4--', 'Fe2(OH)2++++', 
	        'Fe3(OH)4(5+)', 'FeOH+', 'FeOH++', 'HO2-', 'OH-'
	    ],
	    gas=['H2(g)', 'H2O(g)', 'O2(g)'],
	    mineral=[
	        'Rock(s)', 'Fe', 'Fe(OH)2', 'Fe(OH)3', 'FeO', 
	        'Ferrihydrite', 'Goethite', 'Hematite', 'Magnetite', 'Wustite'
	    ]
	),
	dict(
	    description="Fe++, Fe+++, OH-, H2O works",
	    primary=['Fe++', 'Fe+++', 'OH-', 'H2O'],
	    secondary=[
	        'O2(aq)', 'H2(aq)', 'Fe(OH)2(aq)', 'Fe(OH)2+', 'Fe(OH)3(aq)', 
	        'Fe(OH)3-', 'Fe(OH)4-', 'Fe(OH)4--', 'Fe2(OH)2++++', 
	        'Fe3(OH)4(5+)', 'FeOH+', 'FeOH++', 'HO2-', 'H+'
	    ],
	    gas=['H2(g)', 'H2O(g)', 'O2(g)'],
	    mineral=[
	        'Rock(s)', 'Fe', 'Fe(OH)2', 'Fe(OH)3', 'FeO', 
	        'Ferrihydrite', 'Goethite', 'Hematite', 'Magnetite', 'Wustite'
	    ]
	),
	dict(
	    description="Exclude Glutarate listed in aq_skip.dat",
	    primary=['Acetic_acid(aq)', 'H+', 'H2O'],
	    secondary=['OH-'],
	    gas=['H2O(g)'],
	    mineral=['Rock(s)']
	),
	dict(
	    description="Exclude NO2 gas in gas_skip.dat",
	    primary=['O2(aq)', 'H+', 'NO3-', 'H2O'],
	    secondary=[
	        'H2(aq)', 'HN3(aq)', 'HNO2(aq)', 'HNO3(aq)', 'HO2-',
	        'N2(aq)', 'N3-', 'NH3(aq)', 'NH4+', 'NO2-', 'OH-'
	    ],
	    gas=['H2(g)', 'H2O(g)', 'N2(g)', 'O2(g)'],
	    mineral=['Rock(s)']
	),
	dict(
	    description="Exclude CO2(s) from min_skip.dat",
	    primary=['CO2(aq)', 'H2O', 'H+'],
	    secondary=['HCO3-', 'CO3--', 'OH-'],
	    gas=['CO2(g)', 'H2O(g)'],
	    mineral=['Rock(s)']
	)
]

for test in tests:
	result = calculate_reactions(test['primary'])

	secondary_correct = set(result['secondary_species']) == set(test['secondary'])
	gas_correct = set(result['gas_species']) == set(test['gas'])
	mineral_correct = set(result['mineral_species']) == set(test['mineral'])
	all_correct = secondary_correct and gas_correct and mineral_correct
	
	if not all_correct:
		print("TEST FAILED")
		print(test['description'])
		print(f"Primary species: {test['primary']}")

		if not secondary_correct:
			print(f"Expected {len(test['secondary'])} secondary species {sorted(test['secondary'])}")
			print(f"Got {len(result['secondary_species'])} secondary species {sorted(result['secondary_species'])}")

		if not gas_correct:
			print(f"Expected {len(test['gas'])} gas species {sorted(test['gas'])}")
			print(f"Got {len(result['gas_species'])} gas species {sorted(result['gas_species'])}")

		if not mineral_correct:
			print(f"Expected {len(test['mineral'])} mineral species {sorted(test['mineral'])}")
			print(f"Got {len(result['mineral_species'])} mineral species {sorted(result['mineral_species'])}")

	else:
		print("TEST PASSED")
		print(test['description'])
	
	print()



# standard ordering works
# =============================================
# PRIMARY_SPECIES
# A(aq)
# B(aq)
# H2O
# END

# SECONDARY_SPECIES
# secondary species coming from first pass: AB(aq)
# END

# PASSIVE_GAS_SPECIES
# H2O(g)
# END

# MINERALS
# Rock(s)
# A(s)
# A(s)*
# AB(s)
# A2(s)
# END

# non-standard ordering works
# =============================================
# PRIMARY_SPECIES
# AB(aq)
# B(aq)
# H2O
# END

# SECONDARY_SPECIES
# secondary species coming from nonstandard ordering: A(aq)
# END

# PASSIVE_GAS_SPECIES
# H2O(g)
# END

# MINERALS
# Rock(s)
# A(s)
# A(s)*
# AB(s)
# A2(s)
# END


# no duplicates allowed in primary species
# =============================================
# Error: duplicate primary species: 2 A(aq)
# Error: duplicate primary species: 2 A(aq)
# PRIMARY_SPECIES
# A(aq)
# A(aq)
# H2O
# END

# SECONDARY_SPECIES
# END

# PASSIVE_GAS_SPECIES
# H2O(g)
# END

# MINERALS
# Rock(s)
# A(s)
# A(s)*
# A2(s)
# END


# O2(g) in database becomes O2(aq) in standard ordering
# =============================================
# PRIMARY_SPECIES
# H2(aq)
# H2O
# END

# SECONDARY_SPECIES
# secondary species coming from nonstandard ordering: O2(aq)
# END

# PASSIVE_GAS_SPECIES
# H2(g)
# H2O(g)
# O2(g)
# END

# MINERALS
# Rock(s)
# END



# O2(aq) matches O2(g) when checking non-standard ordering
# =============================================
# PRIMARY_SPECIES
# O2(aq)
# H2O
# END

# SECONDARY_SPECIES
# secondary species coming from first pass: H2(aq)
# END

# PASSIVE_GAS_SPECIES
# H2(g)
# H2O(g)
# O2(g)
# END

# MINERALS
# Rock(s)
# END


# Collecting secondary species from a second pass works
# =============================================
# PRIMARY_SPECIES
# UO2++
# H+
# O2(aq)
# H2O
# END

# SECONDARY_SPECIES
# secondary species coming from first pass: H2(aq)
# secondary species coming from first pass: U+++
# secondary species coming from first pass: U++++
# secondary species coming from first pass: (UO2)2(OH)2++
# secondary species coming from first pass: (UO2)2OH+++
# secondary species coming from first pass: (UO2)3(OH)4++
# secondary species coming from first pass: (UO2)3(OH)5+
# secondary species coming from first pass: (UO2)3(OH)7-
# secondary species coming from first pass: (UO2)4(OH)7+
# secondary species coming from first pass: HO2-
# secondary species coming from first pass: OH-
# secondary species coming from first pass: UO2(OH)2(aq)
# secondary species coming from first pass: UO2(OH)3-
# secondary species coming from first pass: UO2(OH)4--
# secondary species coming from first pass: UO2OH+
# secondary species coming from second pass: U(OH)4(aq)
# secondary species coming from second pass: UOH+++
# END

# PASSIVE_GAS_SPECIES
# H2(g)
# H2O(g)
# O2(g)
# END

# MINERALS
# Rock(s)
# Schoepite
# Schoepite-dehy(.393)
# Schoepite-dehy(.648)
# Schoepite-dehy(.85)
# Schoepite-dehy(.9)
# Schoepite-dehy(1.0)
# UO2(am)
# UO2.3333(beta)
# UO2.6667
# Uraninite
# END


# Fe++, Fe+++, H+, H2O works
# =============================================
# PRIMARY_SPECIES
# Fe++
# Fe+++
# H+
# H2O
# END

# SECONDARY_SPECIES
# secondary species coming from nonstandard ordering: O2(aq)
# secondary species coming from first pass: H2(aq)
# secondary species coming from first pass: Fe(OH)2(aq)
# secondary species coming from first pass: Fe(OH)2+
# secondary species coming from first pass: Fe(OH)3(aq)
# secondary species coming from first pass: Fe(OH)3-
# secondary species coming from first pass: Fe(OH)4-
# secondary species coming from first pass: Fe(OH)4--
# secondary species coming from first pass: Fe2(OH)2++++
# secondary species coming from first pass: Fe3(OH)4(5+)
# secondary species coming from first pass: FeOH+
# secondary species coming from first pass: FeOH++
# secondary species coming from first pass: HO2-
# secondary species coming from first pass: OH-
# END

# PASSIVE_GAS_SPECIES
# H2(g)
# H2O(g)
# O2(g)
# END

# MINERALS
# Rock(s)
# Fe
# Fe(OH)2
# Fe(OH)3
# FeO
# Ferrihydrite
# Goethite
# Hematite
# Magnetite
# Wustite
# END


# Fe++, Fe+++, OH-, H2O works
# =============================================
# PRIMARY_SPECIES
# Fe++
# Fe+++
# OH-
# H2O
# END

# SECONDARY_SPECIES
# secondary species coming from nonstandard ordering: O2(aq)
# secondary species coming from first pass: H2(aq)
# secondary species coming from first pass: Fe(OH)2(aq)
# secondary species coming from first pass: Fe(OH)2+
# secondary species coming from first pass: Fe(OH)3(aq)
# secondary species coming from first pass: Fe(OH)3-
# secondary species coming from first pass: Fe(OH)4-
# secondary species coming from first pass: Fe(OH)4--
# secondary species coming from first pass: Fe2(OH)2++++
# secondary species coming from first pass: Fe3(OH)4(5+)
# secondary species coming from first pass: FeOH+
# secondary species coming from first pass: FeOH++
# secondary species coming from first pass: HO2-
# secondary species coming from first pass: H+
# END

# PASSIVE_GAS_SPECIES
# H2(g)
# H2O(g)
# O2(g)
# END

# MINERALS
# Rock(s)
# Fe
# Fe(OH)2
# Fe(OH)3
# FeO
# Ferrihydrite
# Goethite
# Hematite
# Magnetite
# Wustite
# END


# Exclude Glutarate listed in aq_skip.dat
# =============================================
# PRIMARY_SPECIES
# Acetic_acid(aq)
# H+
# H2O
# END

# SECONDARY_SPECIES
# secondary species coming from first pass: OH-
# END

# PASSIVE_GAS_SPECIES
# H2O(g)
# END

# MINERALS
# Rock(s)
# END


# Exclude NO2 gas in gas_skip.dat
# =============================================
# PRIMARY_SPECIES
# O2(g)
# H+
# NO3-
# H2O
# END

# SECONDARY_SPECIES
# secondary species coming from first pass: H2(aq)
# secondary species coming from nonstandard ordering: NH3(aq)
# secondary species coming from first pass: HNO3(aq)
# secondary species coming from first pass: HO2-
# secondary species coming from first pass: OH-
# secondary species coming from second pass: N2(aq)
# secondary species coming from second pass: N3-
# secondary species coming from second pass: NO2-
# secondary species coming from second pass: HN3(aq)
# secondary species coming from second pass: HNO2(aq)
# secondary species coming from second pass: NH4+
# END

# PASSIVE_GAS_SPECIES
# H2(g)
# H2O(g)
# N2(g)
# END

# MINERALS
# Rock(s)
# END


# Exclude CO2(s) from min_skip.dat
# =============================================
# PRIMARY_SPECIES
# CO2(aq)
# H2O
# END

# SECONDARY_SPECIES
# secondary species coming from nonstandard ordering: H+
# secondary species coming from nonstandard ordering: HCO3-
# secondary species coming from second pass: CO3--
# secondary species coming from second pass: OH-
# END

# PASSIVE_GAS_SPECIES
# CO2(g)
# H2O(g)
# END

# MINERALS
# Rock(s)
# END

