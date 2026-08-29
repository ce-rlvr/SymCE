import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z, t
from sympy.polys import Poly

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
    if isinstance(witness, (tuple, list)) and len(witness) == 5 and all(isinstance(val, bool) for val in witness):
        return list(witness)
        
    if isinstance(witness, dict):
        if any(k in witness for k in ['H1', 'h1', 'H_1']):
            try:
                h1 = bool(witness.get('H1', witness.get('h1', witness.get('H_1', False))))
                h2 = bool(witness.get('H2', witness.get('h2', witness.get('H_2', False))))
                h3 = bool(witness.get('H3', witness.get('h3', witness.get('H_3', False))))
                h4 = bool(witness.get('H4', witness.get('h4', witness.get('H_4', False))))
                neg_q = bool(witness.get('neg_Q', witness.get('neg_q', witness.get('neg_Q_ok', False))))
                return [h1, h2, h3, h4, neg_q]
            except Exception:
                pass
                
        try:
            h1 = bool(witness.get('is_irreducible', witness.get('irreducible', False)))
            h2 = bool(witness.get('is_separable', witness.get('separable', False)))
            h3 = bool(witness.get('degree_is_n', witness.get('degree') == witness.get('n', -1)))
            h4 = bool(witness.get('is_splitting_field', witness.get('splitting_field', False)))
            neg_q = not bool(witness.get('acts_faithfully_and_transitively', witness.get('transitive', True)))
            return [h1, h2, h3, h4, neg_q]
        except Exception:
            pass

    if hasattr(witness, 'is_irreducible') or hasattr(witness, 'irreducible') or hasattr(witness, 'H1') or hasattr(witness, 'h1'):
        try:
            if hasattr(witness, 'H1') or hasattr(witness, 'h1'):
                h1 = bool(getattr(witness, 'H1', getattr(witness, 'h1', False)))
                h2 = bool(getattr(witness, 'H2', getattr(witness, 'h2', False)))
                h3 = bool(getattr(witness, 'H3', getattr(witness, 'h3', False)))
                h4 = bool(getattr(witness, 'H4', getattr(witness, 'h4', False)))
                neg_q = bool(getattr(witness, 'neg_Q', getattr(witness, 'neg_q', False)))
                return [h1, h2, h3, h4, neg_q]
                
            h1 = bool(getattr(witness, 'is_irreducible', getattr(witness, 'irreducible', False)))
            h2 = bool(getattr(witness, 'is_separable', getattr(witness, 'separable', False)))
            
            if hasattr(witness, 'degree_is_n'):
                h3 = bool(witness.degree_is_n)
            elif hasattr(witness, 'degree') and hasattr(witness, 'n'):
                h3 = bool(witness.degree == witness.n)
            else:
                h3 = False
                
            h4 = bool(getattr(witness, 'is_splitting_field', getattr(witness, 'splitting_field', False)))
            
            transitive = getattr(witness, 'acts_faithfully_and_transitively', getattr(witness, 'transitive', True))
            neg_q = not bool(transitive)
            
            return [h1, h2, h3, h4, neg_q]
        except Exception:
            pass

    try:
        if isinstance(witness, (tuple, list)):
            f_val = witness[0]
            n_val = witness[1] if len(witness) > 1 else None
        else:
            f_val = witness
            n_val = None

        f = Poly(f_val)
        
        h1 = bool(f.is_irreducible)
        h2 = bool(f.is_sqf)
        
        if n_val is not None:
            h3 = bool(f.degree() == n_val)
        else:
            h3 = True
            
        h4 = True
        neg_q = not h1
        
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: f is an irreducible polynomial over F",
    "H_2: f is a separable polynomial",
    "H_3: The degree of f is n",
    "H_4: K is the splitting field of f over F",
    "not Q: Gal(K/F) does not act faithfully and transitively on the roots of f"
]

N_HYP = 4
NEG_Q_INDEX = 4