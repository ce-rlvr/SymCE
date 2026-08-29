import sympy
import sympy.combinatorics as comb
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    "H_1: G is a group",
    "¬Q: The equivalence (f is an automorphism <=> G is abelian and has no elements of order 2) fails"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1_ok = False
    neg_q_ok = False
    
    try:
        # 1. Check if witness is S.Naturals (not a group)
        if witness is sympy.S.Naturals or witness is sympy.S.Naturals0:
            return [False, False]
            
        # 2. Check if witness is S.Reals, S.Rationals, S.Complexes (groups where doubling IS an automorphism)
        if witness is sympy.S.Reals or witness is sympy.S.Rationals or witness is sympy.S.Complexes:
            return [True, False]
            
        # 3. Check if witness is S.Integers or ZZ (group where doubling is NOT surjective)
        if witness is sympy.S.Integers or witness is sympy.ZZ:
            return [True, True]
            
        # 4. Check if witness is a string representation
        if isinstance(witness, str):
            w_lower = witness.strip().lower()
            if w_lower in ['q', 'r', 'rationals', 'reals', 'c', 'complex']:
                return [True, False]
            if ('integers' in w_lower or w_lower == 'z' or 'z under addition' in w_lower or 'z x z' in w_lower) and 'mod' not in w_lower:
                return [True, True]
                
        # 5. Check if witness is a tuple of Z
        if isinstance(witness, tuple) and len(witness) > 0:
            if all(w is sympy.S.Integers or w is sympy.ZZ or (isinstance(w, str) and w.strip().lower() == 'z') for w in witness):
                return [True, True]

        # 6. Check if witness is a PermutationGroup (always finite, so conjecture holds)
        if hasattr(comb, 'PermutationGroup') and isinstance(witness, comb.PermutationGroup):
            return [True, False]
            
        # 7. Check if witness is FreeGroup
        if hasattr(comb, 'FreeGroup') and isinstance(witness, comb.FreeGroup):
            if len(witness.generators) == 1:
                return [True, True]
            else:
                return [True, False]
                
        # 8. Check if witness is FpGroup
        if hasattr(comb, 'FpGroup') and isinstance(witness, comb.FpGroup):
            gens = witness.generators
            rels = witness.relators
            if len(gens) == 1 and len(rels) == 0:
                return [True, True]
            try:
                if witness.order() != sympy.oo:
                    return [True, False]
            except Exception:
                pass
                
        # 9. Duck-typing for custom objects
        if hasattr(witness, 'is_abelian'):
            h1_ok = True
            abelian = witness.is_abelian() if callable(witness.is_abelian) else witness.is_abelian
            
            q = None
            for attr in ['has_order_2', 'has_elements_of_order_2']:
                if hasattr(witness, attr):
                    val = getattr(witness, attr)
                    has_2 = val() if callable(val) else val
                    q = abelian and not has_2
                    break
            if q is None:
                for attr in ['no_elements_of_order_2', 'no_order_2']:
                    if hasattr(witness, attr):
                        val = getattr(witness, attr)
                        no_2 = val() if callable(val) else val
                        q = abelian and no_2
                        break
                        
            p = None
            for attr in ['is_squaring_automorphism', 'squaring_is_automorphism', 'is_automorphism']:
                if hasattr(witness, attr):
                    val = getattr(witness, attr)
                    p = val() if callable(val) else val
                    break
                    
            if p is not None and q is not None:
                neg_q_ok = bool(p != q)
                return [h1_ok, neg_q_ok]
                
    except Exception:
        pass
        
    return [h1_ok, neg_q_ok]