import time
from viewModel_Tiago import RobotViewer

def main():
    print("Initialisiere den Roboter...")
    

    robot = RobotViewer()
    

    robot.show()
    
    print("Starte externe Steuerung...")
    
    # 3. Externe Animationsschleife
    for step in range(5000):
        robot.update_joints(inner_angle=0, outer_angle=0, spindle_angle=step)
        
        print(f"Schritt: {step} | Innerer Arm Winkel: {step}")
        
        time.sleep(0.2)
        
    print("Animation beendet.")
    robot.close()

# Startpunkt des Skripts
if __name__ == "__main__":
    main()