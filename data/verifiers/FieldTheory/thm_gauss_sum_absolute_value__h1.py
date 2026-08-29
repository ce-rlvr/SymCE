import math
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: χ is a non-trivial multiplicative character of F_q",
    "H_2: ψ is a non-trivial additive character of F_q",
    "¬Q: The absolute value of the Gauss sum G(χ, ψ) is not equal to √q"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_witness_components(witness):
    if isinstance(witness, tuple) and len(witness) == 3:
        q, chi_list, psi_list = witness
        elements = list(range(q))
        add = lambda x, y: (x + y) % q
        mul = lambda x, y: (x * y) % q
        zero = 0
        one = 1
        chi = lambda x: chi_list[x]
        psi = lambda x: psi_list[x]
        return q, elements, add, mul, zero, one, chi, psi
    elif hasattr(witness, 'chi') and hasattr(witness, 'psi'):
        if hasattr(witness, 'elements'):
            elements = witness.elements
        elif hasattr(witness, 'q'):
            elements = list(range(witness.q))
        else:
            raise ValueError("No elements or q provided in witness")
            
        q = getattr(witness, 'q', len(elements))
        
        if hasattr(witness, 'add'):
            add = witness.add
        else:
            add = lambda x, y: (x + y) % q
            
        if hasattr(witness, 'mul'):
            mul = witness.mul
        else:
            mul = lambda x, y: (x * y) % q
            
        zero = getattr(witness, 'zero', 0)
        one = getattr(witness, 'one', 1)
        
        chi_attr = witness.chi
        if callable(chi_attr):
            chi = chi_attr
        else:
            chi = lambda x: chi_attr[x]
            
        psi_attr = witness.psi
        if callable(psi_attr):
            psi = psi_attr
        else:
            psi = lambda x: psi_attr[x]
            
        return q, elements, add, mul, zero, one, chi, psi
    elif isinstance(witness, dict):
        if 'elements' in witness:
            elements = witness['elements']
        elif 'q' in witness:
            elements = list(range(witness['q']))
        else:
            raise ValueError("No elements or q provided in witness")
            
        q = witness.get('q', len(elements))
        add = witness.get('add', lambda x, y: (x + y) % q)
        mul = witness.get('mul', lambda x, y: (x * y) % q)
        zero = witness.get('zero', 0)
        one = witness.get('one', 1)
        
        chi_val = witness['chi']
        if callable(chi_val):
            chi = chi_val
        else:
            chi = lambda x: chi_val[x]
            
        psi_val = witness['psi']
        if callable(psi_val):
            psi = psi_val
        else:
            psi = lambda x: psi_val[x]
            
        return q, elements, add, mul, zero, one, chi, psi
    else:
        raise ValueError("Unknown witness format")

def conditions(witness):
    try:
        q, elements, add, mul, zero, one, chi, psi = get_witness_components(witness)
    except Exception:
        return [False, False, False]
        
    # H_1: χ is a non-trivial multiplicative character
    h1 = False
    try:
        if abs(complex(chi(one)) - 1) <= 1e-7:
            mult_ok = True
            for x in elements:
                cx = complex(chi(x))
                for y in elements:
                    cy = complex(chi(y))
                    cxy = complex(chi(mul(x, y)))
                    if abs(cxy - cx * cy) > 1e-7:
                        mult_ok = False
                        break
                if not mult_ok:
                    break
            if mult_ok:
                is_trivial = True
                for x in elements:
                    c = complex(chi(x))
                    if abs(c) > 1e-7 and abs(c - 1) > 1e-7:
                        is_trivial = False
                        break
                h1 = not is_trivial
    except Exception:
        h1 = False

    # H_2: ψ is a non-trivial additive character
    h2 = False
    try:
        if abs(complex(psi(zero)) - 1) <= 1e-7:
            add_ok = True
            for x in elements:
                px = complex(psi(x))
                for y in elements:
                    py = complex(psi(y))
                    pxy = complex(psi(add(x, y)))
                    if abs(pxy - px * py) > 1e-7:
                        add_ok = False
                        break
                if not add_ok:
                    break
            if add_ok:
                is_trivial = True
                for x in elements:
                    if abs(complex(psi(x)) - 1) > 1e-7:
                        is_trivial = False
                        break
                h2 = not is_trivial
    except Exception:
        h2 = False

    # ¬Q: The absolute value of the Gauss sum G(χ, ψ) is not equal to √q
    neg_q = False
    try:
        G = sum(complex(chi(x)) * complex(psi(x)) for x in elements)
        abs_G = abs(G)
        neg_q = abs(abs_G - math.sqrt(float(q))) > 1e-5
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]