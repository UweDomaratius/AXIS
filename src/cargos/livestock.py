from firs import Cargo

cargo = Cargo(id = 'livestock',
              number = '4',
              type_name = '19',
              unit_name = '51',
              type_abbreviation = '147',
              sprite = 'NEW_CARGO_SPRITE',
              weight = '0.1875',
              station_list_colour = '209',
              cargo_payment_list_colour = '209',
              is_freight = '1',
              cargo_classes = 'bitmask(CC_PIECE_GOODS)',
              cargo_label = '"LVST"',
              town_growth_effect = 'TOWNGROWTH_NONE',
              town_growth_multiplier = '1.0',
              units_of_cargo = '83',
              items_of_cargo = '115',
              penalty_lowerbound = '0',
              single_penalty_length = '22',
              price_factor = '124.073982239',
              capacity_multiplier = '1')

cargo.economy_variations['BASIC_TROPIC']['disabled'] = True
