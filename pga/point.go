package pga

import "math"

// Simple 3D vector for points/directions.
type Vec3 struct{ X, Y, Z float64 }

func V(x, y, z float64) Vec3 { return Vec3{x, y, z} }

func (a Vec3) Add(b Vec3) Vec3      { return Vec3{a.X + b.X, a.Y + b.Y, a.Z + b.Z} }
func (a Vec3) Sub(b Vec3) Vec3      { return Vec3{a.X - b.X, a.Y - b.Y, a.Z - b.Z} }
func (a Vec3) Scale(s float64) Vec3 { return Vec3{s * a.X, s * a.Y, s * a.Z} }

func (a Vec3) Dot(b Vec3) float64 { return a.X*b.X + a.Y*b.Y + a.Z*b.Z }
func (a Vec3) Cross(b Vec3) Vec3 {
	return Vec3{
		a.Y*b.Z - a.Z*b.Y,
		a.Z*b.X - a.X*b.Z,
		a.X*b.Y - a.Y*b.X,
	}
}
func (a Vec3) Norm() float64 { return math.Sqrt(a.Dot(a)) }

func (a Vec3) Normalized() Vec3 {
	n := a.Norm()
	if n == 0 {
		return a
	}
	return a.Scale(1.0 / n)
}
func (a Vec3) Neg() Vec3 { return Vec3{-a.X, -a.Y, -a.Z} }
