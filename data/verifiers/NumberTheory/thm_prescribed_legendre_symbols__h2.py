import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def parse_witness(witness):
    """
    Helper to extract primes and epsilons from various possible witness formats.
    """
    if isinstance(witness, dict):
        if 'primes' in witness and 'epsilons' in witness:
            return list(witness['primes']), list(witness['epsilons'])
    if isinstance(witness, list) and len(witness) > 0 and isinstance(witness[0], (tuple, list)) and len(witness[0]) == 2:
        primes = [x[0] for x in witness]
        epsilons = [x[1] for x in witness]
        return primes, epsilons
    if isinstance(witness, tuple) and len(witness) == 2:
        return list(witness[0]), list(witness[1])
    raise ValueError("Unrecognized witness format")

def conditions(witness) -> list[bool]:
    # H_1: p_1, p_2, \dots, p_k are distinct odd prime numbers
    try:
        primes, epsilons = parse_witness(witness)
        h1_ok = True
        if len(primes) != len(epsilons) or len(primes) == 0:
            h1_ok = False
        elif len(set(primes)) != len(primes):
            h1_ok = False
        else:
            for p in primes:
                if not isinstance(p, (int, sympy.Integer)) or not sympy.ntheory.isprime(p) or p % 2 == 0:
                    h1_ok = False
                    break
            for e in epsilons:
                if not isinstance(e, (int, sympy.Integer)):
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # neg_Q: There does NOT exist an integer x such that (x/p_i) = \epsilon_i for all i
    try:
        primes, epsilons = parse_witness(witness)
        neg_q_ok = False
        
        # Group required epsilons by prime
        reqs = {}
        for p, eps in zip(primes, epsilons):
            if p not in reqs:
                reqs[p] = set()
            reqs[p].add(eps)
            
        for p, eps_set in reqs.items():
            # If a single prime requires multiple different Legendre symbols, no such x exists
            if len(eps_set) > 1:
                neg_q_ok = True
                break
            
            eps = list(eps_set)[0]
            
            # The Legendre symbol only takes values in {-1, 0, 1}.
            # If any epsilon is outside this set, no such x can exist.
            if eps not in (-1, 0, 1):
                neg_q_ok = True
                break
            
            # For completeness, if p is not prime (though H1 would fail), check if the Jacobi symbol can attain eps
            if not sympy.ntheory.isprime(p) and isinstance(p, (int, sympy.Integer)) and 0 < p <= 10000:
                found = False
                for x in range(int(p)):
                    try:
                        if sympy.ntheory.jacobi_symbol(int(x), int(p)) == eps:
                            found = True
                            break
                    except Exception:
                        pass
                if not found:
                    neg_q_ok = True
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p_1, p_2, ..., p_k are distinct odd prime numbers",
    "¬Q: There does not exist an integer x such that (x/p_i) = epsilon_i for all i"
]

N_HYP = 1
NEG_Q_INDEX = 1