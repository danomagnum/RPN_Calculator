import rpncalc
import rpn_types
import operators
import math
from decimal import Decimal

def convert(factor):
        return lambda interp, a: [rpn_types.Value( a.val * factor)]

factors = {'mm_to_in': 1.0 / 25.4,
           'm_to_in': 1000.0 / 25.4,
           'm_to_ft': 1000.0 / 25.4 / 12.0,
           'mm_to_ft': 1.0 / 25.4 / 12.0,
           'in_to_mm': 25.4,
           'in_to_m': 25.4 / 1000,
           'ft_to_m': 12.0 * 25.4 / 1000,
           'ft_to_mm': 25.4 / 12.0,
           'N_to_lb': 0.22480894244319,
           'lb_to_N': 4.448221628250858,
           'kN_to_ton': 0.22480894244319 / 2.0,
           'ton_to_kN': 4.448221628250858 * 2.0}

def register():
        result = {}
        for factor in factors:
          result['conv.{}'.format(factor)] = convert(Decimal(factors[factor]))
        return result


