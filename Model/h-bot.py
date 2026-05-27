import os

class HBot:
    def __init__(self):
        self.X = 0
        self.Y = 0
        self.MotorA = 0
        self.MotorB = 0

    def inverse(self, target_x, target_y):

        a = target_x + target_y
        b = target_x - target_y
        return a, b

    def forward(self, pos_a, pos_b):

            x = (pos_a + pos_b) / 2.0
            y = (pos_a - pos_b) / 2.0
            return x, y

    def move_to(self, target_x, target_y):
            print(f"Command: Move to X={target_x}, Y={target_y}")
            
            self.motor_a, self.motor_b = self.inverse(target_x, target_y)
            self.x = target_x
            self.y = target_y

    def get_actual_position(self):
            """Calculates current XY position based strictly on motor state."""
            return self.forward(self.motor_a, self.motor_b)

# --- Test the Transformation ---
bot = HBot()

# Move the bot to X=10, Y=5
bot.move_to(int(input("Enter a value for X: ")),int(input("Enter a value for Y: ")))

print(f"Motor Positions -> A: {bot.motor_a}, B: {bot.motor_b}")
print(f"Calculated XY   -> {bot.get_actual_position()}")

