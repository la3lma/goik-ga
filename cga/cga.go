package cga

// This is a *parallel sketch* of a Conformal Geometric Algebra (CGA) API.
// It mirrors the PGA motor API in spirit but uses CGA-native entities
// (points as null vectors, rotors including translators, spheres/planes natively).
//
// A complete CGA engine is non-trivial; this file outlines the interface and provides
// minimal fallbacks using an internal dual-quaternion backend so you can wire code now
// and later swap for a full CGA core.
//
// Key ideas:
// - Points are represented as null-vectors P = x + 0.5 x^2 * e_inf + e_0
// - Rotors act by sandwich: X' = R X ~R
// - Translations are rotors in CGA (no special-casing), planes/spheres are native.
//
// For now, we alias to a tiny dual-quaternion backend to keep examples runnable.

import "goikga/pga"

type Rotor struct {
	M pga.Motor
}

type Vec3 = pga.Vec3

func Identity() Rotor { return Rotor{M: pga.Identity()} }
func FromAxisAngle(u Vec3, theta float64) Rotor { return Rotor{M: pga.FromAxisAngle(u, theta)} }
func Translator(t Vec3) Rotor { return Rotor{M: pga.Translator(t)} }
func Screw(p Vec3, u Vec3, theta float64, pitch float64) Rotor {
	return Rotor{M: pga.Screw(p, u, theta, pitch)}
}

func (a Rotor) Mul(b Rotor) Rotor { return Rotor{M: a.M.Mul(b.M)} }
func (a Rotor) Inv() Rotor       { return Rotor{M: a.M.Inv()} }

func (a Rotor) ActPoint(p Vec3) Vec3 { return a.M.ActPoint(p) }
func (a Rotor) ActDir(v Vec3) Vec3   { return a.M.ActDir(v) }

// Notes for future full CGA:
// - Represent meet/join (∧, ∨) to project points onto planes/spheres.
// - Use inner product nullity to compute distances robustly.
// - Provide primitive constructors: Plane(n, d), Sphere(center, r), etc.
