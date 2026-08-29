import sympy
from sympy.abc import x, y, z, t
from sympy import S

ZZ = S.Integers
QQ = S.Rationals
RR = S.Reals
CC = S.Complexes

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R_obj = witness.get('k', witness.get('R'))
            a_list = witness.get('a', witness.get('a_list', witness.get('exponents')))
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            R_obj, a_list = witness
        else:
            return [False, False, False]
            
        h1 = False
        if isinstance(a_list, (list, tuple)):
            if isinstance(R_obj, (int, sympy.Integer)) and (R_obj >= 2 or R_obj == 0):
                h1 = True
            elif hasattr(R_obj, 'domain') or hasattr(R_obj, 'is_commutative'):
                h1 = True
            elif isinstance(R_obj, str):
                h1 = True
            elif R_obj in (ZZ, QQ, RR, CC):
                h1 = True
            elif hasattr(R_obj, 'is_Ring') and getattr(R_obj, 'is_Ring'):
                h1 = True
                
        h2 = False
        if isinstance(a_list, (list, tuple)) and len(a_list) > 0:
            if all(isinstance(a, (int, sympy.Integer)) and a > 0 for a in a_list):
                h2 = True
                
        neg_q = False
        if h1 and h2:
            domain_to_check = R_obj
            if hasattr(R_obj, 'domain'):
                domain_to_check = R_obj.domain
                
            is_domain = True
            if isinstance(domain_to_check, (int, sympy.Integer)):
                if domain_to_check == 0:
                    is_domain = True
                else:
                    is_domain = sympy.isprime(int(domain_to_check))
            elif isinstance(domain_to_check, str):
                s_str = domain_to_check.replace(' ', '')
                if s_str.startswith('Z/') and s_str.endswith('Z'):
                    m_str = s_str[2:-1]
                    if m_str.isdigit():
                        is_domain = sympy.isprime(int(m_str))
                elif s_str.startswith('Z_'):
                    m_str = s_str[2:]
                    if m_str.isdigit():
                        is_domain = sympy.isprime(int(m_str))
            else:
                if hasattr(domain_to_check, 'is_Field') and getattr(domain_to_check, 'is_Field'):
                    is_domain = True
                elif hasattr(domain_to_check, 'has_zero_divisors'):
                    is_domain = not getattr(domain_to_check, 'has_zero_divisors')
                else:
                    s_str = str(domain_to_check)
                    if 'GF' in s_str:
                        is_domain = True
                    elif s_str in ['ZZ', 'QQ', 'RR', 'CC', 'Integers', 'Reals', 'Rationals', 'Complexes']:
                        is_domain = True
                    elif 'ZZ' in s_str and ('quo' in s_str or '/' in s_str):
                        nums = ''.join(c if c.isdigit() else ' ' for c in s_str).split()
                        if len(nums) == 1:
                            is_domain = sympy.isprime(int(nums[0]))
                    elif domain_to_check in (ZZ, QQ, RR, CC):
                        is_domain = True
            
            neg_q = not is_domain
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a polynomial ring over k",
    "H_2: a_i are positive integers",
    "¬Q: The ideal is NOT primary"
]

N_HYP = 2
NEG_Q_INDEX = 2