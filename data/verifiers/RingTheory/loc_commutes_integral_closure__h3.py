import sympy
from sympy import ZZ, QQ
from sympy.abc import x

# Top-level setup: named object bindings that the witness expression may reference.
ZZ_x = ZZ[x]
QQ_x = QQ[x]
QQ_frac_x = QQ.frac_field(x)

class DummySubset:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

S_powers_of_2 = DummySubset('2^n')
S_non_zero = DummySubset('Z \\ {0}')

def parse_ring(r):
    if isinstance(r, str):
        s = r
    else:
        s = str(r).replace(' ', '')
    
    if s in ('Z', 'ZZ', 'Integers', 'S.Integers', 'Integers()', 'Domain:ZZ'): return 'Z'
    if s in ('Q', 'QQ', 'Rationals', 'S.Rationals', 'Rationals()', 'Domain:QQ'): return 'Q'
    if s in ('Z[x]', 'ZZ[x]', 'PolyRing(ZZ,x)', 'Domain:ZZ[x]'): return 'Z[x]'
    if s in ('Q[x]', 'QQ[x]', 'PolyRing(QQ,x)', 'Domain:QQ[x]'): return 'Q[x]'
    if s in ('Q(x)', 'QQ(x)', 'FracField(QQ,x)', 'Domain:QQ(x)'): return 'Q(x)'
    if s in ('Z[i]', 'ZZ[I]', 'GaussianIntegers'): return 'Z[i]'
    if s in ('Q(i)', 'QQ(I)', 'GaussianRationals'): return 'Q(i)'
    if s in ('Z[1/2]', 'ZZ[1/2]'): return 'Z[1/2]'
    if s in ('Z[1/2][x]', 'ZZ[1/2][x]'): return 'Z[1/2][x]'
    
    return s

def parse_S(s):
    if isinstance(s, str):
        s_str = s
    else:
        s_str = str(s).replace(' ', '')
    
    if '2**n' in s_str or '2^n' in s_str: return '2^n'
    if '0' not in s_str and ('Z' in s_str or 'Integers' in s_str or 'Naturals' in s_str): 
        return 'Z \\ {0}'
    if s_str in ('S', 'S_2', 'S_Z0'):
        if s_str == 'S_2': return '2^n'
        if s_str == 'S_Z0': return 'Z \\ {0}'
        return '2^n'
        
    try:
        lst = list(s)
        if all(hasattr(x, 'is_Integer') and x.is_Integer for x in lst) or all(isinstance(x, int) for x in lst):
            if 0 in lst:
                return 'contains_0'
            if all((int(x) & (int(x)-1) == 0) and int(x) > 0 for x in lst):
                return '2^n'
            return 'Z \\ {0}'
    except Exception:
        pass
    
    return s_str

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = parse_ring(witness.get('R'))
            K = parse_ring(witness.get('K'))
            L = parse_ring(witness.get('L'))
            A = parse_ring(witness.get('A'))
            S = parse_S(witness.get('S'))
        else:
            R = parse_ring(witness[0])
            K = parse_ring(witness[1])
            L = parse_ring(witness[2])
            A = parse_ring(witness[3])
            S = parse_S(witness[4])
    except Exception:
        return [False] * 6

    # H1: R is an integral domain
    try:
        h1 = R in {'Z', 'Q', 'Z[x]', 'Q[x]', 'Q(x)', 'Z[i]', 'Q(i)', 'Z[1/2]', 'Z[1/2][x]'}
    except Exception:
        h1 = False

    # H2: K is the field of fractions of R
    try:
        expected_K = {
            'Z': 'Q', 'Q': 'Q', 
            'Z[x]': 'Q(x)', 'Q[x]': 'Q(x)', 'Q(x)': 'Q(x)',
            'Z[i]': 'Q(i)', 'Q(i)': 'Q(i)',
            'Z[1/2]': 'Q', 'Z[1/2][x]': 'Q(x)'
        }.get(R)
        h2 = (K == expected_K) and (K is not None)
    except Exception:
        h2 = False

    # H3: A is the integral closure of R in L
    try:
        ic = {
            ('Z', 'Z'): 'Z',
            ('Z', 'Q'): 'Z',
            ('Z', 'Z[x]'): 'Z',
            ('Z', 'Q[x]'): 'Z',
            ('Z', 'Q(x)'): 'Z',
            ('Z', 'Z[i]'): 'Z[i]',
            ('Z', 'Q(i)'): 'Z[i]',
            ('Z', 'Z[1/2]'): 'Z',
            ('Z[x]', 'Z[x]'): 'Z[x]',
            ('Z[x]', 'Q[x]'): 'Z[x]',
            ('Z[x]', 'Q(x)'): 'Z[x]',
            ('Q', 'Q'): 'Q',
            ('Q', 'Q[x]'): 'Q',
            ('Q', 'Q(x)'): 'Q',
        }
        h3 = (A == ic.get((R, L))) and (A is not None)
    except Exception:
        h3 = False

    # H4: S is a multiplicatively closed subset of R
    try:
        if S == '2^n':
            h4 = R in {'Z', 'Q', 'Z[x]', 'Q[x]', 'Q(x)', 'Z[1/2]', 'Z[1/2][x]'}
        elif S == 'Z \\ {0}':
            h4 = R in {'Z', 'Q', 'Z[x]', 'Q[x]', 'Q(x)', 'Z[i]', 'Q(i)'}
        else:
            h4 = False
    except Exception:
        h4 = False

    # H5: 0 is not an element of S
    try:
        h5 = S in {'2^n', 'Z \\ {0}'}
    except Exception:
        h5 = False

    # neg_Q: S^{-1}A is NOT the integral closure of S^{-1}R in L
    # The conclusion fails if and only if S is not invertible in L, 
    # meaning S^{-1}R is not a subring of L.
    try:
        if S == '2^n':
            invertible = L in {'Q', 'Q[x]', 'Q(x)', 'Q(i)', 'Z[1/2]', 'Z[1/2][x]'}
        elif S == 'Z \\ {0}':
            invertible = L in {'Q', 'Q[x]', 'Q(x)', 'Q(i)'}
        else:
            invertible = True
        
        neg_q = not invertible
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: A is the integral closure of R in L",
    "H_4: S is a multiplicatively closed subset of R",
    "H_5: 0 is not an element of S",
    "¬Q: S^{-1}A is not the integral closure of S^{-1}R in L"
]

N_HYP = 5
NEG_Q_INDEX = 5