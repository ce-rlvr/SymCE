import sympy

Z2_ring = {
    'elements': [0, 1],
    'add': lambda a, b: (a + b) % 2,
    'mul': lambda a, b: (a * b) % 2,
    'zero': 0
}

Z3_ring = {
    'elements': [0, 1, 2],
    'add': lambda a, b: (a + b) % 3,
    'mul': lambda a, b: (a * b) % 3,
    'zero': 0
}

Z4_ring = {
    'elements': [0, 1, 2, 3],
    'add': lambda a, b: (a + b) % 4,
    'mul': lambda a, b: (a * b) % 4,
    'zero': 0
}

Z6_ring = {
    'elements': [0, 1, 2, 3, 4, 5],
    'add': lambda a, b: (a + b) % 6,
    'mul': lambda a, b: (a * b) % 6,
    'zero': 0
}

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (R, I) where R is a ring and I is a subset of R.
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
            
        R, I = witness
        
        h1 = False
        is_dict_ring = isinstance(R, dict) and 'elements' in R
        
        if is_dict_ring:
            h1 = True
        elif R in [sympy.ZZ, sympy.QQ]:
            h1 = True
        elif hasattr(R, 'is_commutative') and getattr(R, 'is_commutative', False):
            h1 = True
            
        h2 = True if h1 else False
        
        neg_q = False
        if h1 and h2:
            if isinstance(I, (int, sympy.Integer)):
                I_elements = [I]
            elif isinstance(I, (list, set, tuple)):
                I_elements = list(I)
            else:
                I_elements = [I]
                
            if is_dict_ring:
                elements = R['elements']
                add = R['add']
                mul = R['mul']
                zero = R.get('zero', 0)
                
                I_set = set(I_elements)
                is_ideal = True
                if not I_set:
                    is_ideal = False
                elif zero not in I_set:
                    is_ideal = False
                else:
                    for x in I_set:
                        for y in I_set:
                            if add(x, y) not in I_set:
                                is_ideal = False
                        for r in elements:
                            if mul(r, x) not in I_set:
                                is_ideal = False
                neg_q = not is_ideal
            elif R == sympy.ZZ or R == sympy.QQ:
                I_set = set(I_elements)
                if I_set == {0} or I_set == {sympy.Integer(0)}:
                    is_ideal = True
                else:
                    is_ideal = False
                neg_q = not is_ideal
            else:
                I_set = set(I_elements)
                try:
                    zero = R.zero
                except Exception:
                    zero = 0
                if I_set == {zero} or I_set == {0}:
                    is_ideal = True
                else:
                    is_ideal = False
                neg_q = not is_ideal
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: pi is the natural ring homomorphism on the polynomial ring",
    "¬Q: The kernel of pi is not the ideal of polynomials with coefficients in I"
]

N_HYP = 2
NEG_Q_INDEX = 2