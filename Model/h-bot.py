from Axis import Axis


class CoreXY:

    def __init__(self):

        # Motor axes
        self.acsAxis_a = Axis()
        self.acsAxis_b = Axis()

        # Cartesian coordinates
        self.mcsAxisX = Axis()
        self.mcsAxisY = Axis()

    # --------------------------------
    # XY -> Motor coordinates
    # --------------------------------
    def inverse(self, mcsAxisX, mcsAxisY):

        motor_a = mcsAxisX + mcsAxisY
        motor_b = mcsAxisX - mcsAxisY

        return motor_a, motor_b

    # --------------------------------
    # Motor coordinates -> XY
    # --------------------------------
    def forward(self, motor_a, motor_b):

        mcsAxisX = (motor_a + motor_b) / 2.0
        mcsAxisY = (motor_a - motor_b) / 2.0

        return mcsAxisX, mcsAxisY

    # --------------------------------
    # Move command
    # --------------------------------
    def move_to(self, mcsAxisX, mcsAxisY):

        print(f"\nMove command -> X:{mcsAxisX} Y:{mcsAxisY}")

        # Convert XY to motor coordinates
        motor_a, motor_b = self.inverse(mcsAxisX, mcsAxisY)

        # Write target positions
        self.acsAxis_a.Sollposition = motor_a
        self.acsAxis_b.Sollposition = motor_b

        # Simulate movement
        self.acsAxis_a.ActualPosition = motor_a
        self.acsAxis_b.ActualPosition = motor_b

        # Update Cartesian coordinates
        self.mcsAxisX = mcsAxisX
        self.mcsAxisY = mcsAxisY

    # --------------------------------
    # Get actual XY position
    # --------------------------------
    def get_actual_position(self):

        motor_a = self.acsAxis_a.getActualPosition()
        motor_b = self.acsAxis_b.getActualPosition()

        return self.forward(motor_a, motor_b)

    # --------------------------------
    # Status output
    # --------------------------------
    def status(self):

        print("\n--- COREXY STATUS ---")

        print(f"Motor A Actual: {self.acsAxis_a.ActualPosition}")
        print(f"Motor B Actual: {self.acsAxis_b.ActualPosition}")

        mcsAxisX, mcsAxisY = self.get_actual_position()

        print(f"Calculated X: {mcsAxisX}")
        print(f"Calculated Y: {mcsAxisY}")


# --------------------------------
# TEST
# --------------------------------

bot = CoreXY()

target_x = int(input("Enter X: "))
target_y = int(input("Enter Y: "))

bot.move_to(target_x, target_y)

bot.status()