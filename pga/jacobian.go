package pga

// Minimal Jacobian helpers: Given a joint axis (through point c with direction u)
// and a toe point p, return the linear velocity column for an infinitesimal rotation dθ.
// v = ω × (p - c)  with ω = u (unit) and dθ absorbed later by the solver.
//
// For translations (prismatic), column is simply the axis direction.

func RevoluteColumn(axisPoint Vec3, axisDir Vec3, toe Vec3) Vec3 {
	u := axisDir.Normalized()
	r := toe.Sub(axisPoint)
	return u.Cross(r) // linear velocity direction per unit angular rate
}

func PrismaticColumn(axisDir Vec3) Vec3 {
	return axisDir.Normalized()
}
