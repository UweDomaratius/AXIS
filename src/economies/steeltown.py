from economy import Economy
economy = Economy(id = "STEELTOWN",
                  numeric_id = 5,
                  # as of May 2015 the following cargos must have fixed positions if used by an economy:
                  # passengers: 0, mail: 2, goods 5, food 11
                  # keep the rest of the cargos alphabetised
                  # bump the min. compatible version if this list changes
                  cargos = ['passengers',
                            'acid',
                            'mail',
                            'alloy_steel',
                            'aluminium',
                            'carbon_black',
                            'carbon_steel',
                            'cast_iron',
                            'cement',
                            'chlorine',
                            'vehicles', # no goods?
                            'food',
                            'coal',
                            'coal_tar',
                            'coke',
                            'electrical_machines',
                            'engineering_supplies',
                            'farm_supplies',
                            'ferrochrome',
                            'galvanised_steel',
                            'glass',
                            'iron_ore',
                            'limestone',
                            'manganese',
                            'oxygen',
                            'paints_and_coatings',
                            'petrol',
                            'pig_iron',
                            'pipe',
                            'plastics',
                            'quicklime',
                            'rebar',
                            'rubber',
                            'salt',
                            'sand',
                            'scrap_metal',
                            'slag',
                            'soda_ash',
                            'stainless_steel',
                            'steel_wire',
                            'sulphur',
                            'tyres',
                            'vehicle_bodies',
                            'vehicle_engines',
                            'vehicle_parts',
                            'zinc'])
