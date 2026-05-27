import os
from Axis import Axis

class CoreXY:
    def __init__(self):
        self.axis_a = Axis()
        self.axis_b = Axis()
        self.x = 0
        self.y = 0

    def inverse(self,x, y):

        motor_a = x + y
        motor_b = x - y

        return motor_a, motor_b

    def forward(self, motor_a, motor_b):

        x = (motor_a + motor_b) / 2.0
        y = (motor_a - motor_b) / 2.0

        return x, y

    def move_to(self, x, y):

        print(f"\nMove command -> X:{x} Y:{y}")

        # Convert XY to motor coordinates
        motor_a, motor_b = self.inverse(x, y)

        # Write target positions into axis objects
        self.axis_a.Sollposition = motor_a
        self.axis_b.Sollposition = motor_b

        # Simulate movement
        self.axis_a.ActualPosition = motor_a
        self.axis_b.ActualPosition = motor_b

        # Update XY position
        self.x = x
        self.y = y

    def get_actual_position(self):

        motor_a = self.axis_a.getActualPosition()
        motor_b = self.axis_b.getActualPosition()

        return self.forward(motor_a, motor_b)
    
    def status(self):

        print("\n--- COREXY STATUS ---")

        print(f"Motor A Actual: {self.axis_a.ActualPosition}")
        print(f"Motor B Actual: {self.axis_b.ActualPosition}")

        x, y = self.get_actual_position()

        print(f"Calculated X: {x}")
        print(f"Calculated Y: {y}")

# --- Test the Transformation ---
bot = CoreXY()

target_x = int(input("Enter X: "))
target_y = int(input("Enter Y: "))

bot.move_to(target_x, target_y)

bot.status()