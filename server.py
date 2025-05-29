import hyperdiv as hd

from rxn3_lib_v2 import calculate_reaction, get_matching_aq_species


class floating_footer(hd.box):
    position = hd.Prop(
        hd.CSSField(
            "position",
            hd.OneOf("relative", "absolute", "fixed")
        ),
        "relative"
    )

    bottom = hd.Prop(
    	hd.CSSField(
            "bottom",
            hd.Any
        ),
        "0px"
    )

    left = hd.Prop(
    	hd.CSSField(
            "left",
            hd.Any
        ),
        "0px"
    )

    right = hd.Prop(
    	hd.CSSField(
            "right",
            hd.Any
        ),
        "0px"
    )


def as_plfotran_file(reaction_result):
	return f'''
#=========================== chemistry ========================================
CHEMISTRY
  PRIMARY_SPECIES
    { '\n    '.join(reaction_result['primary_species']) }
  END

  SECONDARY_SPECIES
  	{ '\n    '.join(reaction_result['secondary_species']) }
  END

  PASSIVE_GAS_SPECIES
  	{ '\n    '.join(reaction_result['gas_species']) }
  END

  MINERALS
  	{ '\n    '.join(reaction_result['mineral_species']) }
  END

END'''


def main():

	state = hd.state(
		reaction_result=None,
		primary_species=["H2O"],
	)

	if state.reaction_result is not None:
		pflotran_dialog = hd.dialog("PFLOTRAN Input File")
		with pflotran_dialog:
			hd.markdown(f'''
```
{ as_plfotran_file(state.reaction_result) }
```
''')

		with floating_footer(position="fixed", justify="end", direction="horizontal", padding=1):
			pflotran_download_button = hd.button("PFLOTRAN", prefix_icon="download")
			if pflotran_download_button.clicked:
				pflotran_dialog.opened = True

	help_dialog = hd.dialog("About")
	with help_dialog:
		hd.markdown('''
**Reaction Species Finder** is a web tool for finding secondary species, 
  gases and minerals given a set of primary species.

Use the **Search for Species** input to select a set of primary species for your system of interest. The secondary species, gases and minerals will appear to the right.

Click the **download button** to download your results in a **[PFLOTRAN](https://www.pflotran.org)** input file.

**Reaction Species Finder** is built with Python 3.13.3 using **[Hyperdiv](https://hyperdiv.io)**.

''')

	with hd.box():

		with hd.box(direction="horizontal", background_color="#ccc", justify="space-between", align="center", padding=1):
			hd.h1("Reaction Species Finder")

			help_button = hd.icon_button(name="question-circle", font_size="28px")
			if help_button.clicked:
				help_dialog.opened = True

		with hd.box(direction="horizontal", margin=2, gap=2):
			with hd.box(gap=1):
				# primary_species = hd.text_input(value="Fe++,Fe+++,H+,H2O")
				hd.h3("Search for species:")
				species_query = hd.text_input(placeholder="E.g.: Fe++, OH-, U+++", value="")

				matching_species = []
				if len(species_query.value) > 1:
					matching_species = get_matching_aq_species(species_query.value)

				if len(matching_species) > 0:
					with hd.menu() as menu:
						for i, species in enumerate(matching_species):
							with hd.scope(i):
							# print(species)
								item = hd.menu_item(species)
								if item.clicked:
									state.primary_species = state.primary_species + [item.label]
									species_query.value = ''
				
			with hd.box(gap=1):
				hd.h3("Primary Species")
				
				for i, species in enumerate(state.primary_species):
					with hd.scope(i):
						with hd.card():
							with hd.hbox(justify="space-between", align="center"):
								hd.text(species)
								if species != "H2O":
									delete = hd.icon_button("trash")
									if delete.clicked:
										state.primary_species = [p for p in state.primary_species if p != species]

				# with hd.card() as card:
				#     with hd.hbox(slot=card.header, justify="space-between", align="center"):
				#         hd.text("Settings")
				#         hd.icon_button("gear")
				#     hd.text("This card has a header.")

			if len(state.primary_species) > 0:
				state.reaction_result = calculate_reaction(state.primary_species)

			if state.reaction_result is not None:
				with hd.box(gap=1):
					table_data = dict()
					table_title = f"Secondary Species ({len(state.reaction_result['secondary_species'])})"
					table_data[table_title] = sorted(state.reaction_result['secondary_species'])
					hd.data_table(table_data, rows_per_page=100, show_select_column=False, id_column_name=table_title)

				with hd.box(gap=1):
					table_data = dict()
					table_title = f"Passive Gas Species ({len(state.reaction_result['gas_species'])})"
					table_data[table_title] = sorted(state.reaction_result['gas_species'])
					hd.data_table(table_data, rows_per_page=100, show_select_column=False, id_column_name=table_title)

				with hd.box(gap=1):
					table_data = dict()
					table_title = f"Mineral Species ({len(state.reaction_result['mineral_species'])})"
					table_data[table_title] = sorted(state.reaction_result['mineral_species'])
					hd.data_table(table_data, rows_per_page=100, show_select_column=False, id_column_name=table_title)

			# with hd.box():
			# 	primary_species = hd.text_input(value="Fe++,Fe+++,OH-,H2O")
			# 	submit = hd.button("Calculate secondary species")
		
			# 	if submit.clicked:
			# 		state.reaction_result_right = calculate_reaction(primary_species.value.split(","))

			# 	if state.reaction_result_right is not None:
			# 		table_data = dict()
			# 		table_title = f"Secondary Species ({len(state.reaction_result_right['secondary_species'])})"
			# 		table_data[table_title] = sorted(state.reaction_result_right['secondary_species'])
			# 		hd.data_table(table_data, rows_per_page=100)

			# 		table_data = dict()
			# 		table_title = f"Passive Gas Species ({len(state.reaction_result_right['gas_species'])})"
			# 		table_data[table_title] = sorted(state.reaction_result_right['gas_species'])
			# 		hd.data_table(table_data, rows_per_page=100)

			# 		table_data = dict()
			# 		table_title = f"Mineral Species ({len(state.reaction_result_right['mineral_species'])})"
			# 		table_data[table_title] = sorted(state.reaction_result_right['mineral_species'])
			# 		hd.data_table(table_data, rows_per_page=100)

hd.run(main)
