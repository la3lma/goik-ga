#!/usr/bin/env python3
"""
Generate 3D visualization of hexapod leg configuration.

This script creates a 3D plot showing the leg structure, joint positions,
and coordinate frames for the example configuration used in the Go code.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

class Arrow3D(FancyArrowPatch):
    """3D arrow patch for matplotlib."""
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_points(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        return np.min(zs)

def rotation_matrix_z(theta):
    """Rotation matrix about Z-axis."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0],
                     [s,  c, 0],
                     [0,  0, 1]])

def rotation_matrix_y(theta):
    """Rotation matrix about Y-axis."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[ c, 0, s],
                     [ 0, 1, 0],
                     [-s, 0, c]])

def create_leg_visualization():
    """Create the main leg visualization."""
    
    # Parameters from the Go example
    l1 = 0.05  # hip offset to thigh (m)
    l2 = 0.20  # thigh length
    l3 = 0.20  # shank length
    
    # Joint angles from the example
    theta1 = 20 * np.pi / 180  # Hip yaw
    theta2 = -10 * np.pi / 180  # Thigh pitch
    theta3 = 30 * np.pi / 180   # Knee pitch
    
    # Calculate joint positions using forward kinematics
    # Hip at origin
    hip = np.array([0, 0, 0])
    
    # Thigh joint after hip yaw
    thigh_local = np.array([l1, 0, 0])
    R1 = rotation_matrix_z(theta1)
    thigh = R1 @ thigh_local
    
    # Knee joint after thigh pitch
    knee_local = np.array([l2, 0, 0])
    R2 = rotation_matrix_y(theta2)
    knee_rel = R2 @ knee_local
    knee = thigh + R1 @ knee_rel
    
    # Toe position after knee pitch
    toe_local = np.array([l3, 0, 0])
    R3 = rotation_matrix_y(theta3)
    toe_rel = R3 @ toe_local
    toe = knee + R1 @ R2 @ toe_rel
    
    # Create 3D plot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot leg links
    joints = np.array([hip, thigh, knee, toe])
    
    # Draw the leg structure
    ax.plot([hip[0], thigh[0]], [hip[1], thigh[1]], [hip[2], thigh[2]], 
            'b-', linewidth=8, label='Hip Link', alpha=0.7)
    ax.plot([thigh[0], knee[0]], [thigh[1], knee[1]], [thigh[2], knee[2]], 
            'g-', linewidth=6, label='Thigh Link', alpha=0.7)
    ax.plot([knee[0], toe[0]], [knee[1], toe[1]], [knee[2], toe[2]], 
            'r-', linewidth=6, label='Shank Link', alpha=0.7)
    
    # Draw joints
    ax.scatter(*hip, color='black', s=200, label='Hip Joint')
    ax.scatter(*thigh, color='blue', s=150, label='Thigh Joint')
    ax.scatter(*knee, color='green', s=150, label='Knee Joint')
    ax.scatter(*toe, color='red', s=200, label='Toe')
    
    # Draw coordinate frames
    scale = 0.05
    
    # World frame at hip
    ax.quiver(hip[0], hip[1], hip[2], scale, 0, 0, color='red', alpha=0.8, arrow_length_ratio=0.1)
    ax.quiver(hip[0], hip[1], hip[2], 0, scale, 0, color='green', alpha=0.8, arrow_length_ratio=0.1)
    ax.quiver(hip[0], hip[1], hip[2], 0, 0, scale, color='blue', alpha=0.8, arrow_length_ratio=0.1)
    
    # Add annotations
    ax.text(hip[0]-0.02, hip[1]-0.02, hip[2]+0.03, 'Hip\n(0,0,0)', fontsize=10)
    ax.text(thigh[0], thigh[1]+0.02, thigh[2]+0.03, f'Thigh\n({thigh[0]:.3f},{thigh[1]:.3f},{thigh[2]:.3f})', fontsize=9)
    ax.text(knee[0], knee[1]+0.02, knee[2]+0.03, f'Knee\n({knee[0]:.3f},{knee[1]:.3f},{knee[2]:.3f})', fontsize=9)
    ax.text(toe[0], toe[1]+0.02, toe[2]+0.03, f'Toe\n({toe[0]:.3f},{toe[1]:.3f},{toe[2]:.3f})', fontsize=9, weight='bold')
    
    # Add angle annotations
    ax.text(hip[0]+0.03, hip[1], hip[2]+0.05, f'θ₁={theta1*180/np.pi:.1f}°', fontsize=10, color='blue')
    ax.text(thigh[0], thigh[1]-0.05, thigh[2], f'θ₂={theta2*180/np.pi:.1f}°', fontsize=10, color='green')
    ax.text(knee[0], knee[1]-0.05, knee[2], f'θ₃={theta3*180/np.pi:.1f}°', fontsize=10, color='red')
    
    # Set equal aspect ratio and limits
    max_range = 0.25
    ax.set_xlim([-0.05, max_range])
    ax.set_ylim([-0.1, 0.15])
    ax.set_zlim([-0.05, 0.15])
    
    # Labels and title
    ax.set_xlabel('X (Forward) [m]')
    ax.set_ylabel('Y (Lateral) [m]')
    ax.set_zlabel('Z (Vertical) [m]')
    ax.set_title('Hexapod Leg Configuration\n3-DOF Forward Kinematics Example', fontsize=14, weight='bold')
    
    # Legend
    ax.legend(loc='upper left', bbox_to_anchor=(0.02, 0.98))
    
    # Add parameter box
    param_text = f'''Parameters:
    l₁ = {l1:.3f} m (hip offset)
    l₂ = {l2:.3f} m (thigh length)
    l₃ = {l3:.3f} m (shank length)
    
    Joint Angles:
    θ₁ = {theta1*180/np.pi:.1f}° (hip yaw)
    θ₂ = {theta2*180/np.pi:.1f}° (thigh pitch)
    θ₃ = {theta3*180/np.pi:.1f}° (knee pitch)'''
    
    ax.text2D(0.02, 0.02, param_text, transform=ax.transAxes, fontsize=9,
              bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.8))
    
    # Adjust view angle
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.savefig('leg_configuration-py.png', dpi=300, bbox_inches='tight')
    print("Generated leg_configuration-py.png")

if __name__ == "__main__":
    create_leg_visualization()