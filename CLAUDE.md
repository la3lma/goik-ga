# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Build and run the example:**
```bash
cd examples/hexapod_leg
go run .
```

**Run tests:**
```bash
go test ./...
```

**Build the module:**
```bash
go build ./...
```

**Format code:**
```bash
go fmt ./...
```

## Architecture Overview

This Go module (`goikga`) implements hexapod-style kinematics using geometric algebra primitives, specifically focusing on dual quaternion representation for rigid body motions.

### Core Packages

**`pga/` - Practical Geometric Algebra (Production Package)**
- `motor.go`: Dual quaternion-based motors for SE(3) rigid motions. Motors compose rotations and translations using dual quaternions equivalent to PGA motors.
- `point.go`: Basic 3D vector operations (Vec3 struct with add, subtract, cross product, etc.)  
- `jacobian.go`: Minimal Jacobian computation helpers for revolute and prismatic joints

Key types:
- `Motor`: Dual quaternion representing rigid motions (rotation + translation)
- `Vec3`: 3D vector for points and directions

**`cga/` - Conformal Geometric Algebra (API Sketch)**
- `cga.go`: Parallel CGA API that currently aliases to the PGA backend. Provides interface for future full CGA implementation with native circle/sphere operations.
- Contains detailed notes for future implementation (points as null vectors, native planes/spheres)

**`examples/hexapod_leg/`**
- `main.go`: Demonstrates 3-DOF leg forward kinematics using motor composition and Jacobian computation

### Key Design Patterns

1. **Motor Composition**: Rigid motions are composed using `Motor.Mul()` - motors can represent pure rotations, pure translations, or screw motions
2. **Dual Quaternion Math**: Internal quaternion type with multiplication, conjugation, normalization
3. **Geometric Primitives**: Use `Screw()` for joints with both rotation and translation, `FromAxisAngle()` for pure rotations
4. **Jacobian Computation**: `RevoluteColumn()` and `PrismaticColumn()` provide velocity Jacobian columns for kinematic chains

### Module Structure
- Module name: `goikga` (Go 1.22)
- No external dependencies - production-lean implementation
- Import path for PGA: `"goikga/pga"`
- Import path for CGA: `"goikga/cga"`