package main

import (
	"fmt"
	"math"

	"goikga/pga"
)

func main() {
	// Example: 3-DoF leg FK using motors.
	// Hip at origin; axes:
	// L1: yaw about +Z, L2: pitch about +Y at hip->thigh joint, L3: pitch about +Y at knee.
	// Link lengths (example values):
	l1 := 0.05 // hip offset to thigh (m)
	l2 := 0.20 // thigh length
	l3 := 0.20 // shank length

	// Joint centers:
	hip := pga.V(0, 0, 0)
	thighJ := hip.Add(pga.V(l1, 0, 0))
	kneeJ := thighJ.Add(pga.V(l2, 0, 0))

	// Axes:
	z := pga.V(0, 0, 1)
	y := pga.V(0, 1, 0)

	// Angles:
	theta1 := 20 * math.Pi / 180
	theta2 := -10 * math.Pi / 180
	theta3 := 30 * math.Pi / 180

	// Build motor chain:
	M := pga.Identity().
		Mul(pga.Screw(hip, z, theta1, 0)).
		Mul(pga.Screw(thighJ, y, theta2, 0)).
		Mul(pga.Screw(kneeJ, y, theta3, 0)).
		Mul(pga.Translator(pga.V(l3, 0, 0))) // toe from knee along x

	// Toe in world:
	toe0 := pga.V(0, 0, 0) // relative toe origin before chain
	toe := M.ActPoint(toe0)
	fmt.Printf("Toe: %+v\n", toe)

	// Jacobian columns at current pose (linear velocity for each revolute joint)
	J1 := pga.RevoluteColumn(hip, z, toe)
	J2 := pga.RevoluteColumn(thighJ, y, toe)
	J3 := pga.RevoluteColumn(kneeJ, y, toe)
	fmt.Printf("Jacobian columns (linear part):\nJ1=%+v\nJ2=%+v\nJ3=%+v\n", J1, J2, J3)
}
