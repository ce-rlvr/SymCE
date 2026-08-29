import sympy
import math
from functools import reduce

# Top-level setup for the witness namespace
Z = sympy.S.Integers
QQ = sympy.QQ

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: J is an ideal of R",
    "¬Q: The product ideal IJ is not a subset of I \\cap J"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, I, J = witness
            elif len(witness) == 2:
                I, J = witness
                R = sympy.S.Integers
            else:
                return [False, False, False]
        else:
            return [False, False, False]

        # H1: R is a ring
        h1 = (R == sympy.S.Integers) or hasattr(R, 'is_Ring') or hasattr(R, 'domain')
        
        # H2: J is an ideal of R
        h2 = False
        if R == sympy.S.Integers:
            if isinstance(J, int) or (hasattr(J, 'is_Integer') and J.is_Integer):
                j_gen = int(J)
                h2 = True
            elif isinstance(J, (list, set, tuple)):
                if not all(isinstance(x, int) or (hasattr(x, 'is_Integer') and x.is_Integer) for x in J):
                    return [bool(h1), False, False]
                j_gen = reduce(math.gcd, [int(x) for x in J]) if J else 0
                h2 = True
        else:
            if hasattr(J, 'is_Ideal') and J.is_Ideal:
                h2 = True
            elif isinstance(J, (list, set, tuple)):
                h2 = True

        # neg_Q: IJ is not a subset of I \cap J
        neg_q = False
        if R == sympy.S.Integers:
            if isinstance(I, int) or (hasattr(I, 'is_Integer') and I.is_Integer):
                i_gen = int(I)
                lcm = (i_gen * j_gen) // math.gcd(i_gen, j_gen) if i_gen and j_gen else 0
                ij_gen = i_gen * j_gen
                if lcm == 0:
                    is_subset = (ij_gen == 0)
                else:
                    is_subset = (ij_gen % lcm == 0)
            elif isinstance(I, (list, set, tuple)):
                if not all(isinstance(x, int) or (hasattr(x, 'is_Integer') and x.is_Integer) for x in I):
                    return [bool(h1), bool(h2), False]
                
                if j_gen == 0:
                    I_cap_J = set(int(x) for x in I if int(x) == 0)
                else:
                    I_cap_J = set(int(x) for x in I if int(x) % j_gen == 0)
                
                ij_gens = [int(i) * j_gen for i in I]
                ij_gen = reduce(math.gcd, ij_gens) if ij_gens else 0
                
                if ij_gen == 0:
                    is_subset = (0 in I_cap_J)
                else:
                    # An infinite ideal cannot be a subset of a finite set
                    is_subset = False
            else:
                return [bool(h1), bool(h2), False]
                
            neg_q = not is_subset

        else:
            if hasattr(J, 'is_Ideal'):
                J_ideal = J
            else:
                J_ideal = R.ideal(*J)

            if hasattr(I, 'is_Ideal'):
                I_ideal = I
                I_cap_J = I_ideal.intersect(J_ideal)
                IJ_ideal = I_ideal * J_ideal
                is_subset = all(I_cap_J.contains(g) for g in IJ_ideal.gens)
            elif isinstance(I, (list, set, tuple)):
                I_cap_J = set(x for x in I if J_ideal.contains(x))
                ij_gens = []
                for i in I:
                    for j in J_ideal.gens:
                        ij_gens.append(i * j)
                IJ_ideal = R.ideal(*ij_gens)
                if IJ_ideal.is_zero():
                    is_subset = (R.zero in I_cap_J)
                else:
                    is_subset = False
            else:
                return [bool(h1), bool(h2), False]
                
            neg_q = not is_subset

        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]