import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample to the false conjecture:
    "Surjective Endomorphisms of Groups are Automorphisms" (dropped hypothesis: G is finite).
    
    The witness must represent an infinite group G and a surjective endomorphism \phi 
    that is not an automorphism (i.e., not injective).
    """
    
    # 1. Try to evaluate as a finite group with elements and a mapping (e.g. Sympy PermutationGroup)
    if isinstance(witness, tuple) and len(witness) == 2:
        G, phi = witness
        if hasattr(G, 'elements'):
            try:
                elements = list(G.elements)
                
                def apply_phi(x):
                    if isinstance(phi, dict): return phi[x]
                    return phi(x)
                
                is_endo = True
                for x in elements:
                    for y in elements:
                        if apply_phi(x * y) != apply_phi(x) * apply_phi(y):
                            is_endo = False
                            break
                    if not is_endo: break
                
                image = {apply_phi(x) for x in elements}
                is_surj = (len(image) == len(elements)) and all(y in image for y in elements)
                
                is_inj = len(set(apply_phi(x) for x in elements)) == len(elements)
                is_auto = is_endo and is_surj and is_inj
                
                return [is_endo, is_surj, not is_auto]
            except Exception:
                pass

    # 2. Try to evaluate as a tuple of (elements, operation, mapping)
    if isinstance(witness, tuple) and len(witness) == 3:
        elements, op, phi = witness
        try:
            elements_list = list(elements)
            
            def apply_phi(x):
                if isinstance(phi, dict): return phi[x]
                return phi(x)
            
            is_endo = True
            for x in elements_list:
                for y in elements_list:
                    if apply_phi(op(x, y)) != op(apply_phi(x), apply_phi(y)):
                        is_endo = False
                        break
                if not is_endo: break
            
            image = {apply_phi(x) for x in elements_list}
            is_surj = (len(image) == len(elements_list)) and all(y in image for y in elements_list)
            
            is_inj = len(set(apply_phi(x) for x in elements_list)) == len(elements_list)
            is_auto = is_endo and is_surj and is_inj
            
            return [is_endo, is_surj, not is_auto]
        except Exception:
            pass

    # 3. Fallback to checking properties on a custom object (necessary for infinite groups)
    def get_prop(w, prop_name):
        if hasattr(w, prop_name):
            attr = getattr(w, prop_name)
            return attr() if callable(attr) else attr
        if isinstance(w, dict) and prop_name in w:
            val = w[prop_name]
            return val() if callable(val) else val
        if isinstance(w, tuple) and len(w) >= 2:
            G = w[0]
            phi = w[1]
            if hasattr(G, prop_name):
                attr = getattr(G, prop_name)
                return attr(phi) if callable(attr) else attr
            if hasattr(phi, prop_name):
                attr = getattr(phi, prop_name)
                return attr(G) if callable(attr) else attr
        raise ValueError(f"Property {prop_name} not found")

    try:
        h1 = bool(get_prop(witness, 'is_endomorphism'))
    except Exception:
        h1 = False

    try:
        h2 = bool(get_prop(witness, 'is_surjective'))
    except Exception:
        h2 = False

    try:
        neg_q = not bool(get_prop(witness, 'is_automorphism'))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: \phi is an endomorphism of G",
    "H_2: \phi is surjective",
    "¬Q: \phi is not an automorphism of G"
]

N_HYP = 2
NEG_Q_INDEX = 2