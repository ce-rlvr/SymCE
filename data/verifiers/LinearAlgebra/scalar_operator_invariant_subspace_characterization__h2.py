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

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        p, n = None, None
        T_map_raw = None
        vectors = None
        
        if isinstance(witness, tuple):
            if len(witness) == 3:
                p, n, T = witness
            elif len(witness) == 2:
                a, b = witness
                if isinstance(a, int):
                    n, T = a, b
                    p = 3
                elif isinstance(a, list):
                    vectors = a
                    n = len(vectors[0]) if isinstance(vectors[0], tuple) else 1
                    p = max(max(v) if isinstance(v, tuple) else v for v in vectors) + 1
                    T = b
                else:
                    return [False, False]
            else:
                return [False, False]
                
            if vectors is None:
                vectors = list(itertools.product(range(p), repeat=n))
                
            if callable(T):
                T_map_raw = {}
                for v in vectors:
                    try:
                        res = T(*v)
                    except Exception:
                        res = T(v)
                    T_map_raw[v] = res
            elif isinstance(T, dict):
                T_map_raw = T
            elif isinstance(T, list):
                T_map_raw = {vectors[i]: T[i] for i in range(len(vectors))}
                
        elif isinstance(witness, dict):
            T_map_raw = witness
            
        elif isinstance(witness, list):
            p = len(witness)
            n = 1
            vectors = [(i,) for i in range(p)]
            T_map_raw = {(i,): witness[i] for i in range(p)}
            
        elif callable(witness):
            p = 3
            for test_n in [1, 2, 3]:
                test_vectors = list(itertools.product(range(p), repeat=test_n))
                try:
                    T_map_raw = {}
                    for v in test_vectors:
                        try:
                            res = witness(*v)
                        except Exception:
                            res = witness(v)
                        T_map_raw[v] = res
                    n = test_n
                    vectors = test_vectors
                    break
                except Exception:
                    T_map_raw = None
                    continue
                    
        if T_map_raw is None:
            return [False, False]
            
        T_map = {}
        for v, val in T_map_raw.items():
            if isinstance(v, (int, float, sympy.Basic)):
                v_norm = (int(v),)
            else:
                v_norm = tuple(int(x) for x in v)
                
            if isinstance(val, (int, float, sympy.Basic)):
                val_norm = (int(val),)
            else:
                val_norm = tuple(int(x) for x in val)
                
            T_map[v_norm] = val_norm
            
        if vectors is None:
            keys = list(T_map.keys())
            n = len(keys[0])
            p = max(max(v) for v in keys) + 1
            vectors = list(itertools.product(range(p), repeat=n))
            
        norm_vectors = []
        for v in vectors:
            if isinstance(v, (int, float, sympy.Basic)):
                norm_vectors.append((int(v),))
            else:
                norm_vectors.append(tuple(int(x) for x in v))
        vectors = norm_vectors
        
        if n > 3 or p**n > 64:
            return [False, False]
            
        if not sympy.ntheory.isprime(p):
            return [False, False]
            
        T_map = {v: tuple(x % p for x in val) for v, val in T_map.items()}
        
        for v in vectors:
            if v not in T_map:
                return [False, False]
            if len(T_map[v]) != n:
                return [False, False]
                
        h1 = True
        
        def span(generators):
            subspace = set([(0,)*n])
            for gen in generators:
                new_subspace = set(subspace)
                for c in range(1, p):
                    for v in subspace:
                        new_v = tuple((v[i] + c * gen[i]) % p for i in range(n))
                        new_subspace.add(new_v)
                subspace = new_subspace
            return frozenset(subspace)
            
        subspaces = set()
        for k in range(n + 1):
            for gens in itertools.combinations(vectors, k):
                subspaces.add(span(gens))
                
        all_invariant = True
        for W in subspaces:
            for w in W:
                if T_map[w] not in W:
                    all_invariant = False
                    break
            if not all_invariant:
                break
                
        is_cI = False
        for c in range(p):
            cI_correct = True
            for v in vectors:
                expected = tuple((c * v[i]) % p for i in range(n))
                if T_map[v] != expected:
                    cI_correct = False
                    break
            if cI_correct:
                is_cI = True
                break
                
        neg_q = all_invariant and not is_cI
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "¬Q: Every subspace is T-invariant but T != cI"
]

N_HYP = 1
NEG_Q_INDEX = 1