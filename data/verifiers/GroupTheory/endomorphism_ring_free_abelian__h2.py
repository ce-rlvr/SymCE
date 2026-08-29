import sympy
from sympy import oo, S
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        rank = None
        is_free_ab = False
        
        if witness == oo:
            is_free_ab = True
            rank = oo
        elif witness == S.Integers:
            is_free_ab = True
            rank = 1
        elif isinstance(witness, int) or (hasattr(witness, 'is_Integer') and witness.is_Integer):
            try:
                val = int(witness)
                if val >= 0:
                    is_free_ab = True
                    rank = val
            except TypeError:
                pass
        elif isinstance(witness, str) or (hasattr(witness, 'name') and isinstance(getattr(witness, 'name', None), str)):
            s = witness.lower() if isinstance(witness, str) else witness.name.lower()
            if 'free' in s and 'abelian' in s:
                is_free_ab = True
                if 'oo' in s or 'inf' in s:
                    rank = oo
                else:
                    digits = ''.join(filter(str.isdigit, s))
                    if digits:
                        rank = int(digits)
                    else:
                        rank = 1
            elif 'z' in s:
                if '^' in s or '**' in s:
                    is_free_ab = True
                    if 'oo' in s or 'inf' in s:
                        rank = oo
                    else:
                        digits = ''.join(filter(str.isdigit, s))
                        if digits:
                            rank = int(digits)
                        else:
                            rank = 1
                elif s.strip() == 'z':
                    is_free_ab = True
                    rank = 1
                elif 'oo' in s or 'inf' in s:
                    is_free_ab = True
                    rank = oo
                else:
                    is_free_ab = False
        elif isinstance(witness, tuple) and len(witness) > 0:
            if isinstance(witness[0], str):
                s = witness[0].lower()
                if 'free' in s and 'abelian' in s:
                    is_free_ab = True
                    if len(witness) > 1:
                        if witness[1] == oo or str(witness[1]).lower() in ['oo', 'inf', 'infinity']:
                            rank = oo
                        elif isinstance(witness[1], int) and witness[1] >= 0:
                            rank = witness[1]
                        else:
                            rank = 1
                    else:
                        rank = oo
        elif hasattr(witness, 'is_abelian'):
            if not witness.is_abelian:
                is_free_ab = False
            else:
                if hasattr(witness, 'order') and callable(witness.order):
                    if witness.order() == 1:
                        is_free_ab = True
                        rank = 0
                    else:
                        is_free_ab = False
                elif hasattr(witness, 'order'):
                    if witness.order == 1:
                        is_free_ab = True
                        rank = 0
                    else:
                        is_free_ab = False
                elif hasattr(witness, 'generators'):
                    if not hasattr(witness, 'relators'):
                        if len(witness.generators) <= 1:
                            is_free_ab = True
                            rank = len(witness.generators)
                        else:
                            is_free_ab = False
                    else:
                        gens = witness.generators
                        rels = witness.relators
                        n = len(gens)
                        expected_rels = n * (n - 1) // 2
                        if len(rels) == expected_rels:
                            if all(len(r) == 4 for r in rels):
                                is_free_ab = True
                                rank = n
                            elif n <= 1 and len(rels) == 0:
                                is_free_ab = True
                                rank = n
                            else:
                                is_free_ab = False
                        else:
                            is_free_ab = False
                            
        if is_free_ab:
            h1 = True
            # The conclusion fails (End(F) is NOT isomorphic to M_n(Z) for any finite n)
            # if and only if the free abelian group has infinite rank.
            if rank == oo:
                neg_q = True
            else:
                neg_q = False
                
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free abelian group",
    "¬Q: The endomorphism ring End(F) is not isomorphic to the matrix ring M_n(Z) for any finite n"
]

N_HYP = 1
NEG_Q_INDEX = 1