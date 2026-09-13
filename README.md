# Optimization Techniques Assignment 1 - CS2105

Author: Aditya Kumar (Roll: 2501CS19)

This repository contains Python implementations for solving optimization problems using the Big-M Method, Vogel's Approximation Method (VAM), and the Modified Distribution (MODI) Method.

## 1. Big-M Method
The bigM.py script solves the following constrained Linear Programming Problem (LPP):

Problem Statement:
Minimize z = -3x1 + x2 + x3

Subject to:
* x1 - 2x2 + x3 <= 11
* -4x1 + x2 + 2x3 >= 3
* 2x1 - x3 = -1
* x1, x2 >= 0, for i=1,2,3

Results:
* The script converts the problem into standard form and iterates through the Simplex tableau.
* The optimal objective value (Minimize z) is successfully calculated as 2.0.

## 2. Transportation Problem (VAM and MODI Method)
The vam_modi.py script solves a balanced transportation optimization problem to determine the optimal shipment plan and minimum total cost. 

Problem Details:
* The problem includes three origins (O1, O2, O3) and three destinations (D1, D2, D3).
* The total supply (10 + 15 + 40) equals the total demand (20 + 15 + 30), both totaling 65, making it a balanced problem.

Results:
* VAM: Vogel's Approximation Method calculates the initial basic feasible solution with a total initial cost of 75.0.
* MODI: The Modified Distribution method tests for optimality and confirms that all opportunity costs are >= 0, meaning the current solution is optimal.
* The final optimal transportation cost remains 75.0.

## Attached Files
* bigM.py: Python code for the Big-M method.
* vam_modi.py: Python code for the VAM and MODI methods.
* Assignment1_OT.pdf: Contains the problem formulations, code snapshots, and terminal output screenshots.
