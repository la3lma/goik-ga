# goik-ga: Geometric Algebra Kinematics

A minimal Go library implementing hexapod-style kinematics using geometric algebra (GA) primitives. This is a refactoring of Hans Jørgen Grimstad's [goik](https://github.com/hansj66/goik/tree/main/goik) into dual quaternion-based motors for SE(3) rigid motions.

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Bootstrap and Build
Run these commands in sequence to set up and build the repository:

```bash
# Navigate to repository root
cd /path/to/goik-ga

# Tidy dependencies (takes ~3 seconds)
go mod tidy

# Build all packages (takes ~5 seconds) 
go build ./...

# Format code (takes <1 second)
go fmt ./...

# Run static analysis (takes <1 second)
go vet ./...

# Run tests - currently no test files exist (takes ~2 seconds)
go test ./...
```

### Development Workflow
Use the Makefile for common development tasks:

```bash
# Complete development workflow: format, vet, test, build, example (takes <1 second total)
make dev

# Build and run the hexapod leg example (takes <1 second)
make run-example

# Run tests with verbose output (takes ~2 seconds)
make test

# Generate test coverage report (takes ~2 seconds) 
make coverage

# Run benchmarks (takes <1 second - no benchmarks currently exist)
make bench

# Check for required tools (Go, pdflatex, bibtex)
make check-tools

# Clean all build artifacts
make clean
```

### Documentation
Build the LaTeX documentation:

```bash
# Install LaTeX tools if not available
sudo apt-get update && sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-bibtex-extra

# Build PDF documentation (takes <1 second) 
# Note: May show bibtex warning about no citations - this is expected
make pdf

# Clean LaTeX intermediate files only
make clean-latex
```

## Validation

### Manual Testing
Always validate changes by running the working example:

```bash
# Navigate to example directory
cd examples/hexapod_leg

# Run the hexapod leg forward kinematics example (takes <1 second)
go run .
```

**Expected output:**
```
Toe: {X:0.1879168356409856 Y:0.06839613469081296 Z:0.05183064269966951}
Jacobian columns (linear part):
J1={X:-0.06839613469081296 Y:0.1879168356409856 Z:0}
J2={X:0.05183064269966951 Y:0 Z:-0.1379168356409856}
J3={X:0.05183064269966951 Y:-0 Z:0.0620831643590144}
```

### Pre-commit Validation
Always run these commands before committing changes:

```bash
# Format and validate code
go fmt ./...
go vet ./...

# Run tests (even though currently no test files exist)
go test ./...

# Ensure packages build successfully
go build ./...

# Test the example still works
cd examples/hexapod_leg && go run .
```

## Repository Architecture

### Core Packages

**`pga/` - Practical Geometric Algebra (Production Package)**
- `motor.go`: Dual quaternion-based motors for SE(3) rigid motions. Primary interface for composing rotations and translations.
- `point.go`: Basic 3D vector operations (Vec3 struct with add, subtract, cross product, etc.)
- `jacobian.go`: Jacobian computation helpers for revolute and prismatic joints

Key types:
- `Motor`: Dual quaternion representing rigid motions (rotation + translation)
- `Vec3`: 3D vector for points and directions

**`cga/` - Conformal Geometric Algebra (API Sketch)**
- `cga.go`: Parallel CGA API that currently aliases to the PGA backend. Interface for future full CGA implementation.
- Contains detailed implementation notes for future native circle/sphere operations

**`examples/hexapod_leg/`**
- `main.go`: Demonstrates 3-DOF leg forward kinematics using motor composition and Jacobian computation

**`docs/`**
- `main.tex`: LaTeX documentation explaining the geometric algebra mapping
- `refs.bib`: Bibliography file  
- `main.pdf`: Generated documentation (build artifact)

### Key Design Patterns

1. **Motor Composition**: Rigid motions compose using `Motor.Mul()` - can represent pure rotations, pure translations, or screw motions
2. **Dual Quaternion Math**: Internal quaternion type with multiplication, conjugation, normalization  
3. **Geometric Primitives**: Use `Screw()` for joints with rotation and translation, `FromAxisAngle()` for pure rotations
4. **Jacobian Computation**: `RevoluteColumn()` and `PrismaticColumn()` provide velocity Jacobian columns for kinematic chains

### Module Details
- Module name: `goikga` (Go 1.22 required)
- Zero external dependencies - production-lean implementation
- Import path for PGA: `"goikga/pga"`
- Import path for CGA: `"goikga/cga"`

## Important Notes

- **No Test Files**: Currently the repository has no test files. This is expected behavior.
- **Documentation Build**: PDF generation may show bibtex warnings about missing citations - this is harmless.
- **CGA Package**: The conformal geometric algebra package is an API sketch that aliases to PGA backend.
- **Go Version**: Requires Go 1.22 or later.
- **Build Time**: All operations are very fast (<5 seconds). No long-running builds or tests.

## Common Tasks

### Adding New Functionality
When adding new geometric algebra operations:

1. Implement in `pga/` package first (production implementation)
2. Add parallel API in `cga/` package (aliases to PGA for now)
3. Update the hexapod example if relevant
4. Run full validation: `make dev && make run-example`

### Working with Motors
Motors are the core abstraction for rigid motions:

```go
// Import the PGA package
import "goikga/pga"

// Create motors for different motion types
identity := pga.Identity()
rotation := pga.FromAxisAngle(axis, angle)
translation := pga.Translator(translation_vector)
screw := pga.Screw(point, axis, angle, pitch)

// Compose motors
combined := motor1.Mul(motor2).Mul(motor3)

// Apply to points and directions
new_point := motor.ActPoint(point)
new_direction := motor.ActDir(direction)
```

### Working with Jacobians
For kinematic chains requiring velocity analysis:

```go
// Get Jacobian column for revolute joint
j_col := pga.RevoluteColumn(joint_center, joint_axis, end_effector_point)

// Get Jacobian column for prismatic joint  
j_col := pga.PrismaticColumn(joint_axis)
```

## File Listings

### Repository Root
```
.
├── .github/
│   └── copilot-instructions.md
├── CLAUDE.md
├── Makefile
├── README.md
├── cga/
│   └── cga.go
├── docs/
│   ├── main.tex
│   ├── refs.bib
│   └── main.pdf
├── examples/
│   └── hexapod_leg/
│       └── main.go
├── go.mod
└── pga/
    ├── jacobian.go
    ├── motor.go
    └── point.go
```

### Key Commands Reference
All timing measurements were validated during instruction creation:

| Command | Purpose | Typical Time |
|---------|---------|--------------|
| `go mod tidy` | Update dependencies | ~3 seconds |
| `go build ./...` | Build all packages | ~5 seconds |
| `go test ./...` | Run tests | ~2 seconds |
| `go fmt ./...` | Format code | <1 second |
| `go vet ./...` | Static analysis | <1 second |
| `make dev` | Full dev workflow | <1 second |
| `make run-example` | Run example | <1 second |
| `make pdf` | Build documentation | <1 second |
| `make coverage` | Generate coverage | ~2 seconds |