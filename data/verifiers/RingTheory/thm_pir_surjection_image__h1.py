import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: f: R -> S is a surjective ring homomorphism",
    "H_2: R is a principal ideal ring",
    "¬Q: S is not a principal ideal ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    # 1. Check if witness is an integer n (representing the natural projection Z -> Z/nZ)
    # In the context of this false conjecture, "Principal Ideal Ring" is often confused with 
    # "Principal Ideal Domain" (PID). Z/nZ is a PID iff n is prime.
    try:
        if isinstance(witness, int) or (hasattr(witness, 'is_integer') and witness.is_integer):
            n = int(witness)
            if n > 1:
                h1 = True
                h2 = True
                from sympy import isprime
                neg_q = not isprime(n)
                return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Check if witness is a SymPy QuotientRing
    try:
        if hasattr(witness, 'ring') and hasattr(witness, 'base_ideal'):
            h1 = True
            R = witness.ring
            S = witness
            
            if hasattr(R, 'is_principal_ideal_ring'):
                h2 = bool(R.is_principal_ideal_ring)
            elif hasattr(R, 'is_PID'):
                h2 = bool(R.is_PID)
            else:
                h2 = False
                
            if hasattr(S, 'is_principal_ideal_ring'):
                neg_q = not bool(S.is_principal_ideal_ring)
            elif hasattr(S, 'is_PID'):
                neg_q = not bool(S.is_PID)
            else:
                if R.__class__.__name__ in ('IntegerRing', 'GMPYIntegerRing', 'PythonIntegerRing'):
                    gens = S.base_ideal.gens
                    if len(gens) == 1:
                        n = gens[0]
                        from sympy import isprime
                        neg_q = not isprime(n)
                    else:
                        neg_q = True
                else:
                    try:
                        gens = S.base_ideal.gens
                        if len(gens) == 1:
                            gen = gens[0]
                            if hasattr(gen, 'is_irreducible'):
                                neg_q = not bool(gen.is_irreducible)
                            else:
                                if hasattr(R, 'to_sympy'):
                                    expr = R.to_sympy(gen)
                                    from sympy.polys.polytools import is_irreducible
                                    neg_q = not is_irreducible(expr)
                                else:
                                    neg_q = True
                        else:
                            neg_q = True
                    except Exception:
                        neg_q = True
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Check if witness is a tuple (R, I) representing the projection R -> R/I
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            if hasattr(R, 'quotient_ring') or hasattr(R, 'ideal'):
                h1 = True
                if hasattr(R, 'is_principal_ideal_ring'):
                    h2 = bool(R.is_principal_ideal_ring)
                elif hasattr(R, 'is_PID'):
                    h2 = bool(R.is_PID)
                else:
                    h2 = False
                
                if R.__class__.__name__ in ('IntegerRing', 'GMPYIntegerRing', 'PythonIntegerRing'):
                    if hasattr(I, 'gens') and len(I.gens) == 1:
                        n = I.gens[0]
                        from sympy import isprime
                        neg_q = not isprime(n)
                    elif isinstance(I, (int, Integer)):
                        from sympy import isprime
                        neg_q = not isprime(int(I))
                    else:
                        neg_q = True
                else:
                    try:
                        if hasattr(I, 'gens') and len(I.gens) == 1:
                            gen = I.gens[0]
                            if hasattr(gen, 'is_irreducible'):
                                neg_q = not bool(gen.is_irreducible)
                            else:
                                if hasattr(R, 'to_sympy'):
                                    expr = R.to_sympy(gen)
                                    from sympy.polys.polytools import is_irreducible
                                    neg_q = not is_irreducible(expr)
                                else:
                                    neg_q = True
                        else:
                            neg_q = True
                    except Exception:
                        neg_q = True
                return [h1, h2, neg_q]
    except Exception:
        pass

    # 4. Check if witness is an object with explicit properties or a dictionary
    try:
        f = None
        if hasattr(witness, 'is_surjective') and hasattr(witness, 'is_homomorphism'):
            f = witness
        elif hasattr(witness, 'f'):
            f = witness.f
        elif isinstance(witness, dict) and 'f' in witness:
            f = witness['f']
        elif isinstance(witness, tuple) and len(witness) >= 3:
            f = witness[2]
            
        if f is not None:
            if hasattr(f, 'is_surjective') and hasattr(f, 'is_homomorphism'):
                h1 = bool(f.is_surjective and f.is_homomorphism)
            elif isinstance(f, dict):
                h1 = bool(f.get('is_surjective') and f.get('is_homomorphism'))
            else:
                h1 = True
        else:
            h1 = False

        R = None
        if hasattr(witness, 'R'):
            R = witness.R
        elif hasattr(witness, 'domain'):
            R = witness.domain
        elif isinstance(witness, dict) and 'R' in witness:
            R = witness['R']
        elif isinstance(witness, tuple) and len(witness) >= 1:
            R = witness[0]
            
        if R is not None:
            if hasattr(R, 'is_principal_ideal_ring'):
                h2 = bool(R.is_principal_ideal_ring)
            elif hasattr(R, 'is_PID'):
                h2 = bool(R.is_PID)
            elif isinstance(R, dict) and 'is_principal_ideal_ring' in R:
                h2 = bool(R['is_principal_ideal_ring'])
            elif isinstance(R, dict) and 'is_PID' in R:
                h2 = bool(R['is_PID'])
            else:
                h2 = False

        S = None
        if hasattr(witness, 'S'):
            S = witness.S
        elif hasattr(witness, 'codomain'):
            S = witness.codomain
        elif isinstance(witness, dict) and 'S' in witness:
            S = witness['S']
        elif isinstance(witness, tuple) and len(witness) >= 2:
            S = witness[1]
            
        if S is not None:
            if hasattr(S, 'is_principal_ideal_ring'):
                neg_q = not bool(S.is_principal_ideal_ring)
            elif hasattr(S, 'is_PID'):
                neg_q = not bool(S.is_PID)
            elif isinstance(S, dict) and 'is_principal_ideal_ring' in S:
                neg_q = not bool(S['is_principal_ideal_ring'])
            elif isinstance(S, dict) and 'is_PID' in S:
                neg_q = not bool(S['is_PID'])
            else:
                neg_q = False

        if h1 or h2 or neg_q:
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]