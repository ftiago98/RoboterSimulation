from pathlib import Path
import re


class CNCInterpreter:
    def __init__(self):
        self.position = {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0
        }

        self.feedrate = None
        self.absolute_mode = True
        self.moves = []

    def load_from_string(self, gcode: str):
        lines = gcode.splitlines()
        self._parse_lines(lines)

    def load_from_path(self, path: str | Path):
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Datei nicht gefunden: {path}")

        with path.open("r", encoding="utf-8") as file:
            lines = file.readlines()

        self._parse_lines(lines)

    def _parse_lines(self, lines):
        for line_number, line in enumerate(lines, start=1):
            line = self._clean_line(line)

            if not line:
                continue

            self._parse_line(line, line_number)

    def _clean_line(self, line: str) -> str:
        line = line.split(";")[0]
        line = re.sub(r"\(.*?\)", "", line)
        return line.strip().upper()

    def _parse_line(self, line: str, line_number: int):
        tokens = re.findall(r"([A-Z])([-+]?\d*\.?\d+)", line)

        command = None
        values = {}

        for letter, value in tokens:
            if letter == "G":
                command = f"G{int(float(value))}"
            else:
                values[letter] = float(value)

        if command == "G90":
            self.absolute_mode = True
            return

        if command == "G91":
            self.absolute_mode = False
            return

        if "F" in values:
            self.feedrate = values["F"]

        if command in ["G0", "G1"]:
            self._linear_move(command, values, line_number)

        elif command in ["G2", "G3"]:
            self._arc_move(command, values, line_number)

        elif command is not None:
            print(f"Warnung Zeile {line_number}: Befehl {command} wird noch nicht unterstützt")

    def _linear_move(self, command, values, line_number):
        start = self.position.copy()
        end = self.position.copy()

        for axis in ["X", "Y", "Z"]:
            if axis in values:
                if self.absolute_mode:
                    end[axis] = values[axis]
                else:
                    end[axis] += values[axis]

        self.position = end.copy()

        self.moves.append({
            "line": line_number,
            "type": "rapid" if command == "G0" else "linear",
            "start": start,
            "end": end,
            "feedrate": self.feedrate
        })

    def _arc_move(self, command, values, line_number):
        start = self.position.copy()
        end = self.position.copy()

        for axis in ["X", "Y", "Z"]:
            if axis in values:
                if self.absolute_mode:
                    end[axis] = values[axis]
                else:
                    end[axis] += values[axis]

        center_offset = {
            "I": values.get("I", 0.0),
            "J": values.get("J", 0.0),
            "K": values.get("K", 0.0)
        }

        self.position = end.copy()

        self.moves.append({
            "line": line_number,
            "type": "arc_cw" if command == "G2" else "arc_ccw",
            "start": start,
            "end": end,
            "center_offset": center_offset,
            "feedrate": self.feedrate
        })

    def get_moves(self):
        return self.moves


# -------------------------
# TEST 1: G-Code als String
# -------------------------

gcode_string = """
G90
G0 X0 Y0 Z5
G1 X10 Y0 F1000
G1 X10 Y10
G1 X0 Y10
G1 X0 Y0
"""

cnc = CNCInterpreter()
cnc.load_from_string(gcode_string)

print("Bewegungen aus String:")
for move in cnc.get_moves():
    print(move)


# -------------------------
# TEST 2: G-Code aus Datei
# -------------------------

print("\nBewegungen aus Datei:")

cnc2 = CNCInterpreter()
cnc2.load_from_path("programm.nc")

for move in cnc2.get_moves():
    print(move)