# goik-ga

A minimal Go code package that refactors hexapod-style kinematics into **geometric algebra** (GA) primitives.

- **pga/**: Practical rigid-motion GA using **motors** implemented as **dual quaternions** (equivalent to PGA motors for SE(3) actions). This gives you compact FK/IK building blocks without frame-juggling.
- **cga/**: Parallel **Conformal Geometric Algebra** (CGA) *API sketch* with detailed notes and placeholders. Useful when you need circles/spheres/distances natively. (Full implementation is non-trivial; stubs provided to illustrate the parallel interface.)
- **examples/**: Sketch of a single-leg FK/IK using the `pga` package.
- **docs/**: LaTeX write-up explaining the mapping, with a separate BibTeX file.

## Quick start

```bash
cd examples/hexapod_leg
go run .
```

## Status

- `pga` is production-lean (no external deps), focused on:
  - Motors (compose rotations/translations),
  - Acting on points,
  - Simple Jacobian columns for a toe point given joint axes.
- `cga` exposes a similar API surface so you can later swap the backend when you want native incidence/distance ops.

