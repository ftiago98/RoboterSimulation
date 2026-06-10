# Task: Implement a Generic Axis Limit Management System for All SCARA Robots

The spindle synchronization with the gripper has been successfully implemented, and Z-axis movement is functioning correctly. However, the system currently lacks a robust mechanism to prevent axes from moving beyond their allowed mechanical or operational limits.

We now need to design and implement a standardized axis limit management concept that can be applied consistently across all SCARA robot variants and all controlled axes.

## Objective

Create a generic, maintainable, and scalable axis limit framework that prevents any robot axis from exceeding its defined motion boundaries.

The solution must not be limited to the spindle or Z-axis. It should establish a common approach that applies to all robot axes, including future robot variants.

## Scope

Analyze all motion-controlled axes, including but not limited to:

- SCARA Axis 1 (Rotation)
- SCARA Axis 2 (Rotation)
- Z-Axis
- Spindle Axis
- Gripper-related axes
- Any additional linear or rotary axes present in the system

## Requirements

### 1. Current State Analysis

Investigate the current implementation and determine:

- Which limits already exist.
- Which limits are enforced by hardware.
- Which limits are enforced by the robot controller.
- Which limits are enforced by PLC software.
- Which limits are missing entirely.
- Where motion commands originate from.

Consider all command sources:

- Automatic sequences
- HMI commands
- Manual jogging
- Service functions
- Maintenance functions
- Recovery procedures
- API or software interfaces

### 2. Unified Axis Limit Concept

Design a generic architecture that ensures every axis follows the same validation process.

The concept should define:

- Minimum position limit
- Maximum position limit
- Soft limits
- Hard limits
- Safety margins
- Emergency stop behavior
- Error reporting behavior

The implementation should avoid axis-specific custom logic whenever possible.

### 3. Single Source of Truth

Determine where axis limits should be maintained.

Examples:

- Robot configuration
- PLC configuration
- Axis parameter database
- Dedicated configuration file

The goal is that each axis has one authoritative definition of its allowed movement range.

No limits should be duplicated across multiple locations unless absolutely necessary.

### 4. Command Validation Layer

Design a mechanism that validates all movement requests before execution.

Every movement command should pass through the same validation process regardless of whether it originates from:

- Automatic operation
- HMI operation
- Jogging
- Maintenance mode
- Service mode

The validation layer should:

- Reject invalid movements
- Clamp movements if appropriate
- Generate clear error messages
- Log violations for diagnostics

### 5. Scalability

The solution must support:

- Existing SCARA robots
- Future SCARA variants
- Additional axes
- Different robot configurations

Adding a new axis should require only configuration changes whenever possible.

### 6. Safety Considerations

Analyze:

- Mechanical collision risks
- Overtravel risks
- Cable strain risks
- End-stop impacts
- Sensor failures
- Encoder failures
- Communication failures

Determine how the limit system should behave in each case.

### 7. Testing Strategy

Create a comprehensive validation plan including:

#### Functional Tests

- Move exactly to minimum limit
- Move exactly to maximum limit
- Move just inside limits
- Move just outside limits

#### HMI Tests

- Manual positioning
- Jogging
- Override operation

#### Automatic Operation Tests

- Recipe execution
- Pick-and-place operations
- Recovery sequences

#### Fault Injection Tests

- Invalid commands
- Missing configuration values
- Sensor failures
- Unexpected axis positions

## Deliverables

### 1. Architecture Proposal

Provide a detailed architecture for a generic axis limit management system.

### 2. Gap Analysis

Document all currently missing protections and inconsistencies.

### 3. Implementation Plan

Provide a step-by-step implementation plan.

### 4. Configuration Strategy

Define how limits should be configured and maintained across all robot types.

### 5. Test Plan

Provide a complete validation and acceptance test plan.

### 6. Acceptance Criteria

Define measurable criteria that must be met before the solution is considered complete.

## Planning Instructions

Do not immediately propose code changes.

First perform a full architectural analysis and identify all existing motion paths and control layers.

Think systematically about how axis limits can be enforced consistently across the entire robot platform rather than solving the issue only for the spindle or Z-axis.

The final proposal should result in a reusable, platform-wide axis limit framework that guarantees no axis can move beyond its defined operating range regardless of how the movement command is initiated.
