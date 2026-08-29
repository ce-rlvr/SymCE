import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: Let sigma and tau be permutations in the symmetric group S_n.",
    "¬Q: sigma and tau are conjugate in S_n if and only if they have the same cycle type."
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    n_val = None
    has_G = False
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                if isinstance(witness[0], int):
                    n_val, sigma, tau = witness
                    has_G = False
                else:
                    G, sigma, tau = witness
                    has_G = True
            elif len(witness) == 2:
                sigma, tau = witness
                has_G = False
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H1: Let sigma and tau be permutations in the symmetric group S_n.
    try:
        h1 = isinstance(sigma, Permutation) and isinstance(tau, Permutation)
        if has_G:
            h1 = h1 and (sigma in G) and (tau in G)
    except Exception:
        h1 = False
        
    # Conclusion: sigma and tau are conjugate in S_n if and only if they have the same cycle type.
    try:
        same_cycle_type = (sigma.cycle_structure == tau.cycle_structure)
        
        if has_G:
            if G.order() > 5000:
                conjugate = False
            else:
                conjugate = False
                for g in list(G.elements):
                    if g * sigma * ~g == tau:
                        conjugate = True
                        break
        else:
            n = max(sigma.size, tau.size)
            if n_val is not None:
                n = max(n, n_val)
            
            s_array = sigma.array_form + list(range(sigma.size, n))
            t_array = tau.array_form + list(range(tau.size, n))
            s_pad = Permutation(s_array)
            t_pad = Permutation(t_array)
            
            conjugate = (s_pad.cycle_structure == t_pad.cycle_structure)
            
        conclusion = (conjugate == same_cycle_type)
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, neg_q]