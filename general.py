# =========================
# Imports & Setup
# =========================
from fractions import Fraction
import logging

import numpy as np
import sympy as sp
import math
from scipy.spatial import ConvexHull

log = logging.getLogger(__name__)   
 
# =========================
# Parsing Utilities
# =========================
def parse_pairs(s):
    """Parse string like [[a,b],[c,d]] into list of pairs."""
    if not s:
        return []

    s = s.replace(" ", "")
    pair_strings = s.split("],[")

    pair_strings[0] = pair_strings[0].lstrip("[")
    pair_strings[-1] = pair_strings[-1].rstrip("]")

    pairs = []
    for pstr in pair_strings:
        a_str, b_str = pstr.split(",")
        a = rationalize(sp.sympify(a_str))
        b = rationalize(sp.sympify(b_str))
        pairs.append([a, b])

    return pairs

 
def parse_triplets(s):
    """Parse string like [[a,b,c],[d,e,f]] into list of triplets."""
    if not s:
        return []

    s = s.replace(" ", "")
    triplet_strings = s.split("],[")

    triplet_strings[0] = triplet_strings[0].lstrip("[")
    triplet_strings[-1] = triplet_strings[-1].rstrip("]")

    triplets = []
    for trstr in triplet_strings:
        elems = trstr.split(",")

        if len(elems) != 3:
            log.error(f"Error in parse_triplets with input: {s}")
            return []

        parsed = [rationalize(sp.sympify(e)) for e in elems]
        triplets.append(parsed)

    return triplets



# =========================
# Conversion / Formatting
# =========================
def toString(obj):
    """Convert objects recursively into readable string."""
    if isinstance(obj, str):
        return obj
    
    if isinstance(obj, Fraction):
        return f"{toString(obj.numerator)}/{toString(obj.denominator)}"

    if isinstance(obj, (int, float)):
        return str(obj)

    if isinstance(obj, (list, np.ndarray)):
        inner = ", ".join(toString(e) for e in obj)
        return f"[{inner}]"

    if isinstance(obj, tuple):
        inner = ", ".join(toString(e) for e in obj)
        return f"({inner})"

    try:
        return str(obj)
    except Exception:
        return None 


def rationalize(x):
    """Convert numeric values (recursively) to Fractions."""
    if isinstance(x, float):
        return Fraction(x).limit_denominator()

    if isinstance(x, sp.Float):
        return rationalize(float(x))

    if isinstance(x, (list, np.ndarray)):
        return [rationalize(v) for v in x]

    if isinstance(x, tuple):
        return tuple(rationalize(v) for v in x)

    if isinstance(x, (str, bool, sp.Basic)):
        return x

    return Fraction(x).limit_denominator()


def normalize(pqcond):
    pqcond = [pqcond[0], pqcond[1], -pqcond[2]]
    if pqcond[0] > 0:
        new = [1, pqcond[1] / pqcond[0], pqcond[2] / pqcond[0]]
    elif pqcond[0] < 0:
        new = [-1, -pqcond[1] / pqcond[0], -pqcond[2] / pqcond[0]]
    elif pqcond[1] > 0:
        new = [pqcond[0] / pqcond[1], 1, pqcond[2] / pqcond[1]]
    else:
        new = [-pqcond[0] / pqcond[1], -1, -pqcond[2] / pqcond[1]]
    new = rationalize(new)
    prod_den = (
        new[0].denominator * new[1].denominator * new[2].denominator
    )
    new = [x * prod_den for x in new]
    gcd = math.gcd(new[0].numerator, new[1].numerator)
    return [new[0] / gcd, new[1] / gcd, new[2] / gcd]



### Helper functions
def is_sharp(pqcondition, pt):
    return pqcondition[0] * pt[0] + pqcondition[1] * pt[1] == pqcondition[2]

def is_strict(pqcondition, adm_pts, adm_lines):
    is_strict_pts = not any(
        pt[2] for pt in adm_pts if is_sharp(pqcondition, pt)
    )
    is_strict_lines = not any(
        line[2]
        for line in adm_lines
        if is_sharp(pqcondition, line[0]) and is_sharp(pqcondition, line[1])
    )
    return is_strict_pts and is_strict_lines


def is_exceptional_pt(est, pqcondition):
    return (not est[2]) and (
        pqcondition[0] * est[0] + pqcondition[1] * est[1] == pqcondition[2]
    )


def is_exceptional_line(line, pqcondition):
    return (
        (not line[2])
        and is_exceptional_pt([line[0][0], line[0][1], False], pqcondition)
        and is_exceptional_pt([line[1][0], line[1][1], False], pqcondition)
    )



# =========================
# Symbolic Utilities
# =========================

def plugin(D, expressions):
    """Substitute all free symbols in expressions with D."""
    if isinstance(expressions, list):
        return [plugin(D, exp) for exp in expressions]

    if isinstance(expressions, tuple):
        return tuple(plugin(D, exp) for exp in expressions)

    if isinstance(expressions, sp.Basic):
        return expressions.subs({sym: D for sym in expressions.free_symbols})

    return expressions


def extract_symbol(exprs):
    """Extract all SymPy symbols from nested expressions."""
    symbols = set()

    if isinstance(exprs, sp.Basic):
        symbols.update(exprs.free_symbols)

    elif isinstance(exprs, (list, tuple)):
        for expr in exprs:
            symbols.update(extract_symbol(expr))

    return symbols


# =========================
# File Handling
# =========================

def modify_filenames(v, D, base_name):
    mapping = {
        1: "_WeakTypeEst",
        2: "_LorentzEst",
        3: "_WeakStrongEst",
        4: "_StrongWeakEst",
        5: "_LebesgueEst",
    }

    suffix = f"{mapping.get(v)}_D={D}"

    return (
        f"{base_name}{suffix}.pdf",
        f"{base_name}{suffix}.jpg",
    )


# =========================
# Geometry / Convex Hull
# =========================

def hull_estimates(estimates):
    """Return convex hull vertices."""
    try:
        hull = ConvexHull([[e[0], e[1]] for e in estimates])
        return [estimates[i] for i in hull.vertices]
    except Exception:
        msg = "Data does not provide estimates for (1/p,1/q) from an open set."
        log.warning(msg)
        return estimates


def inside_outside_bdry(hull_points, p):
    """Check if point is inside, outside, or on boundary."""

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    sign = None
    n = len(hull_points)

    for i in range(n):
        o = hull_points[i]
        a = hull_points[(i + 1) % n]
        c = cross(o, a, p)

        if c == 0:
            return "bdry"

        if sign is None:
            sign = c > 0
        elif (c > 0) != sign:
            return "outside"

    return "inside"


def is_on_boundary_of_convex_hull(hull_points, p):
    return inside_outside_bdry(hull_points, p) == "bdry"


def boundary_estimates(estimates):
    hull_pts = [[e[0], e[1]] for e in hull_estimates(estimates)]
    return [
        est for est in estimates
        if is_on_boundary_of_convex_hull(hull_pts, [est[0], est[1]])
    ]


# =========================
# Estimate Reduction Logic
# =========================

def reduce_dyadic_estimates(dyadic_estimates):
    """Remove dominated duplicates."""
    result = dyadic_estimates.copy()

    for est1 in dyadic_estimates:
        for est2 in dyadic_estimates:
            if (est1[0], est1[1]) == (est2[0], est2[1]) and est1[2] > est2[2]:
                result = [e for e in result if e != est1]

    return result


def better_estimate(swf1, swf2):
    """Compare estimate types."""
    if swf1 == "f":
        return swf2

    if swf1 == "ww" and swf2 != "f":
        return swf2

    if swf1 == "ws":
        if swf2 != "sw":
            return "swws"
        if swf2 not in ("f", "ww"):
            return swf2

    if swf1 == "sw":
        if swf2 != "ws":
            return "swws"
        if swf2 not in ("f", "ww"):
            return swf2

    return swf1


def reduce_estimates(estimates):
    """Reduce redundant estimates."""

    if len(estimates) <= 1:
        return estimates

    if len(estimates) == 2:
        a, b = estimates
        if a[0] == b[1] and a[1] == b[0] and a[2] == b[2]:
            return [a]

    new_estimates = []

    for est in estimates:
        same_point = [
            ne for ne in new_estimates if ne[0] == est[0] and ne[1] == est[1]
        ]

        if not same_point:
            new_estimates.append(est)
            continue

        for ne in same_point:
            if better_estimate(est[2], ne[2]) != ne[2]:
                new_estimates.remove(ne)
                new_estimates.append(est)

    return new_estimates