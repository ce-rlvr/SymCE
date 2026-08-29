import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, phi = witness
        else:
            n = witness
            phi = None
    except Exception:
        n = witness
        phi = None

    try:
        n_int = int(n)
        h1 = (n == n_int) and n_int >= 3 and n_int != 6
    except Exception:
        h1 = False

    try:
        n_int = int(n)
        h2 = (n == n_int) and n_int > 0
    except Exception:
        h2 = False

    try:
        if not h1:
            is_inner = False
        else:
            n_int = int(n)
            if isinstance(phi, Permutation):
                try:
                    if phi.size <= n_int or phi.array_form == list(range(phi.size)):
                        is_inner = True
                    else:
                        is_inner = False
                except Exception:
                    is_inner = False
            elif not (hasattr(phi, 'domain') or isinstance(phi, dict) or callable(phi)):
                is_inner = False
            else:
                Sn = SymmetricGroup(n_int)
                is_inner = False
                
                if hasattr(phi, 'is_isomorphism') and hasattr(phi, 'domain') and hasattr(phi, 'codomain'):
                    try:
                        if phi.domain == Sn and phi.codomain == Sn and phi.is_isomorphism():
                            is_inner = True
                    except Exception:
                        pass
                
                if not is_inner and n_int <= 8:
                    for g in Sn.elements:
                        g_is_inner = True
                        for gen in Sn.generators:
                            try:
                                if hasattr(phi, 'domain'):
                                    val = phi(gen)
                                elif isinstance(phi, dict):
                                    val = phi[gen]
                                else:
                                    val = phi(gen)
                            except Exception:
                                val = None
                            
                            if val != g * gen * g**-1:
                                g_is_inner = False
                                break
                        if g_is_inner:
                            is_inner = True
                            break
        
        neg_q = not is_inner
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 3 and n != 6",
    "H_2: S_n is the symmetric group on n letters",
    "¬Q: phi is not an inner automorphism, or Aut(S_n) is not isomorphic to S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2