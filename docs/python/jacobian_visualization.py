#!/usr/bin/env python3
"""
Generate visualization of Jacobian columns for hexapod leg kinematics.

This script creates plots showing the physical interpretation of Jacobian
columns, which represent the instantaneous velocity directions for each joint.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_jacobian_visualization():
    """Create visualization of Jacobian columns."""
    
    # Parameters from the Go example
    l1 = 0.05  # hip offset to thigh (m)
    l2 = 0.20  # thigh length
    l3 = 0.20  # shank length
    
    # Joint angles from the example
    theta1 = 20 * np.pi / 180  # Hip yaw
    theta2 = -10 * np.pi / 180  # Thigh pitch
    theta3 = 30 * np.pi / 180   # Knee pitch
    
    # Toe position from Go example output
    toe = np.array([0.1879168356409856, 0.06839613469081296, 0.05183064269966951])
    
    # Joint positions
    hip = np.array([0, 0, 0])
    thigh = np.array([l1 * np.cos(theta1), l1 * np.sin(theta1), 0])
    
    # Joint axes
    z_axis = np.array([0, 0, 1])  # Hip yaw axis
    y_axis = np.array([0, 1, 0])  # Thigh and knee pitch axes
    
    # Jacobian columns from Go example output (linear velocity components)
    J1 = np.array([-0.06839613469081296, 0.1879168356409856, 0])
    J2 = np.array([0.05183064269966951, 0, -0.1379168356409856])
    J3 = np.array([0.05183064269966951, 0, 0.0620831643590144])
    
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 12))
    
    # 3D plot showing all Jacobian columns
    ax1 = fig.add_subplot(221, projection='3d')
    
    # Draw leg structure
    ax1.plot([hip[0], thigh[0]], [hip[1], thigh[1]], [hip[2], thigh[2]], 
             'b-', linewidth=4, alpha=0.6, label='Hip Link')
    ax1.plot([thigh[0], toe[0]], [thigh[1], toe[1]], [thigh[2], toe[2]], 
             'g-', linewidth=4, alpha=0.6, label='Thigh+Shank')
    
    # Draw joints
    ax1.scatter(*hip, color='black', s=100, label='Hip')
    ax1.scatter(*thigh, color='blue', s=80)
    ax1.scatter(*toe, color='red', s=120, label='Toe')
    
    # Draw Jacobian vectors
    scale = 2.0
    ax1.quiver(toe[0], toe[1], toe[2], J1[0]*scale, J1[1]*scale, J1[2]*scale, 
               color='red', arrow_length_ratio=0.1, linewidth=3, label='J₁ (Hip)')
    ax1.quiver(toe[0], toe[1], toe[2], J2[0]*scale, J2[1]*scale, J2[2]*scale, 
               color='green', arrow_length_ratio=0.1, linewidth=3, label='J₂ (Thigh)')
    ax1.quiver(toe[0], toe[1], toe[2], J3[0]*scale, J3[1]*scale, J3[2]*scale, 
               color='blue', arrow_length_ratio=0.1, linewidth=3, label='J₃ (Knee)')
    
    ax1.set_xlabel('X [m]')
    ax1.set_ylabel('Y [m]')
    ax1.set_zlabel('Z [m]')
    ax1.set_title('Jacobian Columns: Velocity Directions', fontweight='bold')
    ax1.legend()
    ax1.view_init(elev=20, azim=45)
    
    # Individual Jacobian column plots
    ax2 = fig.add_subplot(222)
    ax2.quiver(0, 0, J1[0], J1[1], color='red', scale=1, scale_units='xy', angles='xy', width=0.005)
    ax2.set_xlim(-0.1, 0.1)
    ax2.set_ylim(-0.05, 0.25)
    ax2.set_xlabel('X velocity [m/s/rad]')
    ax2.set_ylabel('Y velocity [m/s/rad]')
    ax2.set_title('J₁: Hip Yaw Jacobian Column\n(XY plane)', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')
    
    ax3 = fig.add_subplot(223)
    ax3.quiver(0, 0, J2[0], J2[2], color='green', scale=1, scale_units='xy', angles='xy', width=0.005)
    ax3.set_xlim(-0.05, 0.1)
    ax3.set_ylim(-0.2, 0.1)
    ax3.set_xlabel('X velocity [m/s/rad]')
    ax3.set_ylabel('Z velocity [m/s/rad]')
    ax3.set_title('J₂: Thigh Pitch Jacobian Column\n(XZ plane)', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.set_aspect('equal')
    
    ax4 = fig.add_subplot(224)
    ax4.quiver(0, 0, J3[0], J3[2], color='blue', scale=1, scale_units='xy', angles='xy', width=0.005)
    ax4.set_xlim(-0.05, 0.1)
    ax4.set_ylim(-0.05, 0.1)
    ax4.set_xlabel('X velocity [m/s/rad]')
    ax4.set_ylabel('Z velocity [m/s/rad]')
    ax4.set_title('J₃: Knee Pitch Jacobian Column\n(XZ plane)', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    ax4.set_aspect('equal')
    
    # Add text box with explanation
    explanation = """Jacobian Column Interpretation:
    
• Each column represents the instantaneous 
  linear velocity of the toe when the 
  corresponding joint rotates at 1 rad/s
  
• J₁: Hip yaw creates circular motion in XY plane
• J₂: Thigh pitch affects X and Z components  
• J₃: Knee pitch contributes to leg extension
  
• These form the velocity Jacobian matrix:
  J = [J₁ J₂ J₃]
  
• Joint velocities map to toe velocity:
  v_toe = J * [θ̇₁ θ̇₂ θ̇₃]ᵀ"""
    
    fig.text(0.02, 0.02, explanation, fontsize=10, 
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)
    plt.savefig('jacobian_visualization-py.png', dpi=300, bbox_inches='tight')
    print("Generated jacobian_visualization-py.png")

if __name__ == "__main__":
    create_jacobian_visualization()