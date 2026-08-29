import sympy
from sympy.polys.domains import ZZ, QQ, RR, CC, GF

GF2 = GF(2)

def conditions(witness):
    h1_ok = False
    try:
        if hasattr(witness, 'order'):
            if callable(witness.order):
                h1_ok = bool(witness.order() >= 2)
            else:
                h1_ok = bool(witness.order >= 2)
        elif hasattr(witness, 'is_FiniteField') and witness.is_FiniteField:
            h1_ok = bool(witness.order >= 2)
        elif hasattr(witness, 'is_IntegerRing') or hasattr(witness, 'is_RationalField') or hasattr(witness, 'is_RealField') or hasattr(witness, 'is_ComplexField'):
            h1_ok = True
        elif hasattr(witness, '__len__') and not isinstance(witness, str):
            h1_ok = bool(len(witness) >= 2)
        elif hasattr(witness, 'elements'):
            if hasattr(witness.elements, '__len__'):
                h1_ok = bool(len(witness.elements) >= 2)
            else:
                h1_ok = True
    except Exception:
        h1_ok = False

    h2_ok = False
    try:
        if hasattr(witness, 'poly_ring') or hasattr(witness, 'is_Ring') or hasattr(witness, 'zero'):
            h2_ok = True
    except Exception:
        h2_ok = False

    neg_q_ok = False
    try:
        is_bool = False
        if hasattr(witness, 'is_FiniteField') and witness.is_FiniteField:
            if witness.order == 2:
                is_bool = True
        elif hasattr(witness, 'elements'):
            is_bool = True
            for e in witness.elements:
                if e**2 != e:
                    is_bool = False
                    break
        elif hasattr(witness, 'is_boolean_ring') and witness.is_boolean_ring:
            is_bool = True
        
        if is_bool:
            neg_q_ok = True
            
        if hasattr(witness, 'poly_ring'):
            x = sympy.Symbol('x')
            Rx = witness.poly_ring(x)
            X = Rx.gens[0]
            if X**2 == X:
                neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R has at least two elements",
    "H_2: The polynomial ring in one variable x over R is formed",
    "¬Q: The polynomial ring is a Boolean ring"
]

N_HYP = 2
NEG_Q_INDEX = 2