from firs import Cargo

cargo = Cargo(id = 'farm_supplies',
              number = '21',
              type_name = 'string(STR_CARGO_NAME_FARM_SUPPLIES)',
              unit_name = 'string(STR_CARGO_NAME_FARM_SUPPLIES)',
              type_abbreviation = 'string(STR_CID_FARM_SUPPLIES)',
              sprite = 'NEW_CARGO_SPRITE',
              weight = '0.5625',
              station_list_colour = '75',
              cargo_payment_list_colour = '75',
              is_freight = '1',
              cargo_classes = 'bitmask(CC_EXPRESS, CC_PIECE_GOODS)',
              cargo_label = '"FMSP"',
              town_growth_effect = 'TOWNGROWTH_NONE',
              town_growth_multiplier = '1.0',
              units_of_cargo = '84',
              items_of_cargo = 'string(STR_CARGO_UNIT_FMSP)',
              penalty_lowerbound = '6',
              single_penalty_length = '36',
              price_factor = '128.11088562',
              capacity_multiplier = '1')

