import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import factorint

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if not isinstance(witness, PermutationGroup):
            return [False]
            
        # Check if G is cyclic
        is_cyclic = False
        if hasattr(witness, 'is_cyclic'):
            val = witness.is_cyclic
            is_cyclic = val() if callable(val) else val
        else:
            order = witness.order()
            if order <= 2000:
                is_cyclic = any(g.order() == order for g in witness.elements)
            else:
                return [False]
                
        # Check if all Sylow p-subgroups are cyclic
        order = witness.order()
        primes = list(factorint(order).keys())
        
        all_sylow_cyclic = True
        for p in primes:
            sylow_p = witness.sylow_subgroup(p)
            
            sylow_is_cyclic = False
            if hasattr(sylow_p, 'is_cyclic'):
                val = sylow_p.is_cyclic
                sylow_is_cyclic = val() if callable(val) else val
            else:
                s_order = sylow_p.order()
                if s_order <= 2000:
                    sylow_is_cyclic = any(g.order() == s_order for g in sylow_p.elements)
                else:
                    return [False]
                    
            if not sylow_is_cyclic:
                all_sylow_cyclic = False
                break
                
        neg_Q = (bool(is_cyclic) != bool(all_sylow_cyclic))
        
    except Exception:
        neg_Q = False
        
    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: G is cyclic XOR (for every prime p dividing |G|, the Sylow p-subgroup is cyclic)"
]

N_HYP = 0
NEG_Q_INDEX = 0