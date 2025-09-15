package pga

// Motor implements rigid motions in SE(3) using a dual quaternion representation.
// This is practically equivalent to PGA motors for rigid motions and composes nicely.
// We expose only what we need: constructors for rotation/translation/screw, composition,
// action on points, and inversion.
//
// References:
// - Kavan et al., "Skinning with Dual Quaternions"
// - Dorst, "Geometric Algebra for Computer Science" (motors / bivector exponentials)

import "math"

// Quaternion: w + xi + yj + zk
type quat struct {
	w, x, y, z float64
}

func q(w, x, y, z float64) quat { return quat{w, x, y, z} }

func (a quat) Mul(b quat) quat {
	return quat{
		w: a.w*b.w - a.x*b.x - a.y*b.y - a.z*b.z,
		x: a.w*b.x + a.x*b.w + a.y*b.z - a.z*b.y,
		y: a.w*b.y - a.x*b.z + a.y*b.w + a.z*b.x,
		z: a.w*b.z + a.x*b.y - a.y*b.x + a.z*b.w,
	}
}

func (a quat) Conj() quat { return quat{a.w, -a.x, -a.y, -a.z} }

func (a quat) Norm() float64 { return math.Sqrt(a.w*a.w + a.x*a.x + a.y*a.y + a.z*a.z) }

func (a quat) Normalize() quat {
	n := a.Norm()
	if n == 0 {
		return q(1, 0, 0, 0)
	}
	return q(a.w/n, a.x/n, a.y/n, a.z/n)
}

func pure(v Vec3) quat { return quat{0, v.X, v.Y, v.Z} }

// Motor is a dual quaternion (r + ε d), where r is unit rotation, d encodes translation.
type Motor struct {
	r quat // real part (rotation)
	d quat // dual part
}

// Identity motor
func Identity() Motor { return Motor{r: q(1, 0, 0, 0), d: q(0, 0, 0, 0)} }

// FromAxisAngle creates a pure rotation about unit axis u by angle theta (radians).
func FromAxisAngle(u Vec3, theta float64) Motor {
	uhat := u.Normalized()
	half := 0.5 * theta
	s := math.Sin(half)
	r := q(math.Cos(half), uhat.X*s, uhat.Y*s, uhat.Z*s)
	return Motor{r: r, d: q(0, 0, 0, 0)}
}

// Translator creates a pure translation by t (meters, or your units).
func Translator(t Vec3) Motor {
	// d = 0.5 * t * r  with r = 1 (no rotation), so d = 0.5 * pure(t).
	return Motor{r: q(1, 0, 0, 0), d: q(0, 0.5*t.X, 0.5*t.Y, 0.5*t.Z)}
}

// Screw creates a rotation about axis u through point p, with angle theta and pitch h.
// Implementation: translate to axis, rotate, translate back plus pitch.
func Screw(p Vec3, u Vec3, theta float64, pitch float64) Motor {
	// Normalize axis
	u = u.Normalized()
	// Rotation about u
	R := FromAxisAngle(u, theta)

	// Translation along axis by h*theta (convention: pitch per radian)
	Tpitch := Translator(u.Scale(pitch * theta))

	// Conjugate by translation to rotate about a line through p:
	// M = T(p) * R * T(-p) * Tpitch
	Tp := Translator(p)
	Tm := Translator(p.Neg())
	return Tp.Mul(R).Mul(Tm).Mul(Tpitch)
}

// Mul composes two motors: this followed by b.
func (a Motor) Mul(b Motor) Motor {
	// (r1 + ε d1)(r2 + ε d2) = r1 r2 + ε(r1 d2 + d1 r2)
	r := a.r.Mul(b.r)
	d := a.r.Mul(b.d)
	d = quat{d.w + a.d.Mul(b.r).w, d.x + a.d.Mul(b.r).x, d.y + a.d.Mul(b.r).y, d.z + a.d.Mul(b.r).z}
	return Motor{r: r, d: d}
}

// Inv returns the inverse motor.
func (a Motor) Inv() Motor {
	rc := a.r.Conj()
	// For unit r: inverse is r* + ε(- r* d r*)
	dr := rc.Mul(a.d).Mul(rc)
	return Motor{r: rc, d: q(-dr.w, -dr.x, -dr.y, -dr.z)}
}

// ActPoint applies the motor to a point p (as a Vec3).
func (a Motor) ActPoint(p Vec3) Vec3 {
	// Rotate
	rp := a.r.Mul(pure(p)).Mul(a.r.Conj())
	rot := Vec3{rp.x, rp.y, rp.z}
	// Translation vector t = 2 * (d * r_conj).vector
	tr := a.d.Mul(a.r.Conj())
	t := Vec3{2 * tr.x, 2 * tr.y, 2 * tr.z}
	return rot.Add(t)
}

// ActDir applies only rotation to a direction vector.
func (a Motor) ActDir(v Vec3) Vec3 {
	rp := a.r.Mul(pure(v)).Mul(a.r.Conj())
	return Vec3{rp.x, rp.y, rp.z}
}
