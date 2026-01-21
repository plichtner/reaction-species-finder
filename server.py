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

    z_index = hd.Prop(
    	hd.CSSField(
    		"z-index",
    		hd.Any
    	),
    	"10"
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


def make_help_dialog(state):
	dialog = hd.dialog("About")
	with dialog:
		hd.markdown('''
**Reaction Species Finder** is a web tool for finding secondary species, 
  gases and minerals given a set of primary species.

Use the **Search for Species** input to select a set of primary species for your system of interest. The secondary species, gases and minerals will appear to the right.

Click the **download button** to download your results in a **[PFLOTRAN](https://www.pflotran.org)** input file.

**Reaction Species Finder** is built by Benny and Peter Lichtner with Python 3.13.3 using **[Hyperdiv](https://hyperdiv.io)**.

To clone the source code or leave a comment, visit [our github repo](https://github.com/plichtner/reaction-species-finder).

''')
	return dialog


def make_pflotran_download_button(state):
	if state.reaction_result is not None:
		pflotran_dialog = hd.dialog("PFLOTRAN Input File")
		with pflotran_dialog:
			hd.text("The file below has been copied to your clipboard.", padding_bottom=1)
			hd.markdown(f'''```{ as_plfotran_file(state.reaction_result) }''')

		with floating_footer(position="fixed", justify="end", direction="horizontal", padding=1):
			pflotran_download_button = hd.button("PFLOTRAN", prefix_icon="download")
			if pflotran_download_button.clicked:
				pflotran_dialog.opened = True
				hd.clipboard().write(as_plfotran_file(state.reaction_result))


def update_query_string(state):
	pass


def main():

	state = hd.state(
		reaction_result=None,
		primary_species=["H2O"],
	)

	make_pflotran_download_button(state)

	help_dialog = make_help_dialog(state)

	with hd.box():

		# Header
		with hd.box(direction="horizontal", background_color="neutral-300", justify="space-between", align="center", padding=1):
			hd.h1("Reaction Species Finder")

			help_button = hd.icon_button(name="question-circle", font_size="28px")
			if help_button.clicked:
				help_dialog.opened = True

		# Body
		with hd.box(direction="horizontal", margin=2, gap=2):

			# Search column
			with hd.box():
				search_column(state)
			
			# Primary species column
			with hd.box(gap=1):
				primary_species_column(state)

			if len(state.primary_species) > 0:
				state.reaction_result = calculate_reaction(state.primary_species)

			# Results columns
			hd.divider(vertical=True, spacing=0)
			
			# Secondary species
			with hd.box(gap=1):
				species_list = sorted(state.reaction_result['secondary_species'])
				title = f"Secondary Species ({len(species_list)})"
				species_table(title, species_list)

			# Gas Species
			with hd.box(gap=1):
				species_list = sorted(state.reaction_result['gas_species'])
				title = f"Passive Gas Species ({len(species_list)})"
				species_table(title, species_list)

			# Mineral Species
			with hd.box(gap=1):
				species_list = sorted(state.reaction_result['mineral_species'])
				title = f"Mineral Species ({len(species_list)})"
				species_table(title, species_list)


def search_column(state):
	with hd.box(gap=1, background_color="neutral-200", padding=1, border_radius=0.4):
		# primary_species = hd.text_input(value="Fe++,Fe+++,H+,H2O")
		hd.h3("Add primary species:")
		species_query = hd.text_input(placeholder="E.g.: Fe++", value="")

		matching_species = []
		if len(species_query.value) > 1:
			matching_species = get_matching_aq_species(species_query.value)

		matching_species = [
			species for species in matching_species
			if (species not in state.primary_species)
			and (species not in state.reaction_result['secondary_species'])
		]

		if len(matching_species) > 0:
			with hd.menu() as menu:
				for i, species in enumerate(matching_species):
					with hd.scope(i):
					# print(species)
						item = hd.menu_item(species)
						if item.clicked:
							state.primary_species = state.primary_species + [item.label]
							species_query.value = ''
							update_query_string(state)


def primary_species_column(state):
	with hd.box_list():
		species_list = state.primary_species
		hd.box_list_item(f"Primary Species ({len(species_list)})", font_weight="bold", background_color="neutral-200", padding=0.5, border="1px solid neutral-200")

		for i, species in enumerate(species_list):
			with hd.scope(i):
				
				if i == (len(species_list) - 1):
					border_bottom = "1px solid neutral-200"
				else:
					border_bottom = "none"
				
				with hd.box_list_item(padding=0.5, border_top="1px solid neutral-200", border_left="1px solid neutral-200", border_right="1px solid neutral-200", border_bottom=border_bottom):
					with hd.hbox(justify="space-between", align="center"):
						hd.text(species)
						if species != "H2O":
							delete_button = hd.icon_button("trash")
							if delete_button.clicked:
								state.primary_species = [p for p in state.primary_species if p != species]


def species_table(title, species_list):
	with hd.box_list():
		hd.box_list_item(title, font_weight="bold", background_color="neutral-200", padding=0.5, border="1px solid neutral-200")
		for i, species in enumerate(species_list):
			with hd.scope(i):
				if i == (len(species_list) - 1):
					hd.box_list_item(species, padding=0.5, border="1px solid neutral-200")
				else:
					hd.box_list_item(species, padding=0.5, border_top="1px solid neutral-200", border_left="1px solid neutral-200", border_right="1px solid neutral-200")

hd.run(main)
