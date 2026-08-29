import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard groups
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    h1_ok = False
    neg_q_ok = False

    try:
        if isinstance(witness, PermutationGroup):
            # For finite groups, having central chief factors is equivalent to being nilpotent.
            val = witness.is_nilpotent
            is_nilp = val() if callable(val) else val
            h1_ok = bool(is_nilp)
            neg_q_ok = not bool(is_nilp)
            
        elif type(witness).__name__ == 'FreeGroup':
            # Infinite free groups have no chief series, so the hypothesis is vacuously true.
            h1_ok = True
            # Free groups of rank <= 1 are abelian (hence nilpotent). Rank >= 2 are not.
            is_nilp = (len(witness.generators) <= 1)
            neg_q_ok = not is_nilp
            
        elif type(witness).__name__ == 'FpGroup':
            gens = witness.generators
            rels = witness.relators
            
            # Check for the infinite dihedral group D_infty: <x, y | x^2, y^2>
            is_D_infty = False
            if len(gens) == 2 and len(rels) == 2:
                r_set = set(rels)
                if r_set == {gens[0]**2, gens[1]**2} or r_set == {gens[0]**-2, gens[1]**-2}:
                    is_D_infty = True
            
            if is_D_infty:
                # D_infty has no chief series (vacuously true) and is not nilpotent.
                h1_ok = True
                neg_q_ok = True
            else:
                # Attempt to evaluate as a finite group
                pg = witness.to_permutation_group()
                val = pg.is_nilpotent
                is_nilp = val() if callable(val) else val
                h1_ok = bool(is_nilp)
                neg_q_ok = not bool(is_nilp)
                
        else:
            # Fallback for other types
            if hasattr(witness, 'is_nilpotent'):
                val = witness.is_nilpotent
                is_nilp = val() if callable(val) else val
                h1_ok = bool(is_nilp)
                neg_q_ok = not bool(is_nilp)
            elif hasattr(witness, 'is_abelian') and witness.is_abelian:
                h1_ok = True
                neg_q_ok = False
                
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: For every chief series of G, all chief factors are contained in the center of their respective quotient groups",
    "¬Q: G is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1