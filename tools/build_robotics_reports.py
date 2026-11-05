"""Build four illustrated, reproducible robotics portfolio PDFs.

Run from the repository root with a Python environment containing reportlab
and Pillow. Figures are generated here; no lab measurements are used.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from projects.cleaning_bot.simulator import DEFAULT_MAP, simulate as simulate_cleaning
from projects.dc_motor_pid.dc_motor_pid import simulate as simulate_motor
from projects.me3202_labs.two_link_pid.simulate import simulate as simulate_arm


NAVY = "#19324D"
TEAL = "#087E8B"
ORANGE = "#E18A40"
INK = "#25374A"
MUTED = "#60738A"
PALE = "#F3F7FA"
GREEN = "#27855B"
FONT = Path("C:/Windows/Fonts/arial.ttf")
BOLD = Path("C:/Windows/Fonts/arialbd.ttf")


def font(size: int, bold: bool = False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)


def canvas(width: int = 1500, height: int = 570):
    im = PILImage.new("RGB", (width, height), "white")
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle((2, 2, width - 3, height - 3), radius=22, outline="#D9E3EB", width=3)
    return im, dr


def centered(dr, box, text: str, size: int = 28, fill: str = INK, bold: bool = False):
    x1, y1, x2, y2 = box
    f = font(size, bold)
    bounds = dr.textbbox((0, 0), text, font=f)
    tw, th = bounds[2] - bounds[0], bounds[3] - bounds[1]
    dr.text(((x1 + x2 - tw) / 2, (y1 + y2 - th) / 2 - bounds[1]), text, font=f, fill=fill)


def box(dr, xy, label: str, *, fill: str = PALE, outline: str = TEAL, size: int = 27):
    dr.rounded_rectangle(xy, radius=17, fill=fill, outline=outline, width=4)
    centered(dr, xy, label, size=size, bold=True)


def arrow(dr, start, end, *, fill: str = TEAL, width: int = 6):
    dr.line((*start, *end), fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 20
    for offset in (-0.55, 0.55):
        p = (end[0] - length * math.cos(angle + offset), end[1] - length * math.sin(angle + offset))
        dr.line((*end, *p), fill=fill, width=width)


def save(im, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, optimize=True)
    return path


def cleaning_architecture(path: Path):
    im, dr = canvas()
    centered(dr, (40, 20, 1460, 75), "Proposed cleaning robot architecture", 34, NAVY, True)
    box(dr, (60, 125, 340, 240), "Obstacle sensors")
    box(dr, (470, 125, 760, 240), "Arduino / Pi")
    box(dr, (890, 125, 1170, 240), "Motor driver")
    box(dr, (1210, 125, 1450, 240), "Wheel motors")
    arrow(dr, (340, 182), (470, 182))
    arrow(dr, (760, 182), (890, 182))
    arrow(dr, (1170, 182), (1210, 182))
    box(dr, (470, 340, 760, 455), "Battery / power", fill="#FFF5EB", outline=ORANGE)
    box(dr, (890, 340, 1450, 455), "Brush  |  Vacuum  |  Mop", fill="#FFF5EB", outline=ORANGE)
    arrow(dr, (615, 340), (615, 240), fill=ORANGE)
    arrow(dr, (760, 398), (890, 398), fill=ORANGE)
    centered(dr, (55, 490, 1450, 545), "Concept from ATOMQUEST 2025 proposal - hardware modules were not validated in this repository", 25, MUTED)
    return save(im, path)


def cleaning_route(path: Path, report):
    im, dr = canvas()
    centered(dr, (40, 15, 1460, 65), "Default grid route: reachable floor and obstacles", 32, NAVY, True)
    x0, y0, cell = 180, 95, 60
    for y, row in enumerate(DEFAULT_MAP):
        for x, char in enumerate(row):
            xy = (x0 + x * cell, y0 + y * cell, x0 + (x + 1) * cell - 3, y0 + (y + 1) * cell - 3)
            dr.rectangle(xy, fill="#DDEEF0" if char == "." else "#506178", outline="white", width=2)
    points = [(x0 + x * cell + cell / 2, y0 + y * cell + cell / 2) for x, y in report.path]
    dr.line(points, fill=ORANGE, width=7, joint="curve")
    for px, py in (points[0], points[-1]):
        dr.ellipse((px - 13, py - 13, px + 13, py + 13), fill=GREEN if (px, py) == points[0] else NAVY)
    dr.text((1020, 150), "Green: start", font=font(29, True), fill=GREEN)
    dr.text((1020, 205), "Navy: finish", font=font(29, True), fill=NAVY)
    dr.text((1020, 260), "Orange: path", font=font(29, True), fill=ORANGE)
    dr.text((1020, 330), f"{report.reachable_count} cells reached", font=font(29, True), fill=INK)
    dr.text((1020, 385), f"{len(report.path)-1} moves", font=font(29, True), fill=INK)
    centered(dr, (45, 495, 1455, 550), "The route revisits some cells; coverage is 100% of reachable cells, not an optimal-distance claim", 24, MUTED)
    return save(im, path)


def motor_control_diagram(path: Path):
    im, dr = canvas()
    centered(dr, (40, 20, 1460, 75), "Closed-loop DC motor speed control", 34, NAVY, True)
    box(dr, (40, 190, 265, 305), "Target speed")
    box(dr, (355, 190, 580, 305), "PID")
    box(dr, (670, 190, 925, 305), "PWM 0 to 1")
    box(dr, (1015, 190, 1255, 305), "Motor model")
    box(dr, (1315, 190, 1470, 305), "Speed")
    for a, b in [((265, 247), (355, 247)), ((580, 247), (670, 247)), ((925, 247), (1015, 247)), ((1255, 247), (1315, 247))]:
        arrow(dr, a, b)
    dr.line((1390, 305, 1390, 420, 460, 420, 460, 305), fill=TEAL, width=5)
    arrow(dr, (460, 340), (460, 305))
    centered(dr, (500, 425, 1250, 485), "Measured-speed feedback in concept; modeled speed in this simulation", 24, MUTED)
    centered(dr, (60, 505, 1450, 555), "Plant is a normalized first-order model; no encoder or physical motor data is used", 24, MUTED)
    return save(im, path)


def chart(path: Path, title: str, series: list[tuple[str, list[float], str]], x: list[float],
          ylabel: str, ymin: float, ymax: float):
    im, dr = canvas()
    w, h = im.size
    centered(dr, (40, 18, w - 40, 75), title, 34, NAVY, True)
    left, right, top, bottom = 165, w - 70, 115, h - 110
    for i in range(5):
        y = top + i * (bottom - top) / 4
        value = ymax - i * (ymax - ymin) / 4
        dr.line((left, y, right, y), fill="#DEE7ED", width=2)
        dr.text((75, y - 14), f"{value:.2f}", font=font(23), fill=MUTED)
    dr.line((left, top, left, bottom, right, bottom), fill=NAVY, width=4)
    xmin, xmax = min(x), max(x)
    for i in range(5):
        xp = left + i * (right - left) / 4
        value = xmin + i * (xmax - xmin) / 4
        dr.text((xp - 25, bottom + 10), f"{value:.1f}", font=font(22), fill=MUTED)
    for name, values, color in series:
        points = [(left + (xx - xmin) / (xmax - xmin) * (right - left),
                   bottom - (yy - ymin) / (ymax - ymin) * (bottom - top)) for xx, yy in zip(x, values)]
        dr.line(points, fill=color, width=6, joint="curve")
    lx = left
    for name, _, color in series:
        dr.line((lx, h - 50, lx + 42, h - 50), fill=color, width=7)
        dr.text((lx + 52, h - 66), name, font=font(25), fill=INK)
        lx += max(240, len(name) * 17 + 100)
    dr.text((right - 190, bottom + 45), "Time (s)", font=font(24, True), fill=INK)
    dr.text((left, 80), ylabel, font=font(23, True), fill=INK)
    return save(im, path)


def arm_diagram(path: Path):
    im, dr = canvas()
    centered(dr, (40, 15, 1460, 70), "Two-link planar arm: joint positions and control", 34, NAVY, True)
    base = (220, 425)
    joint = (470, 250)
    tip = (755, 335)
    dr.line((*base, *joint), fill=TEAL, width=32)
    dr.line((*joint, *tip), fill=ORANGE, width=32)
    for p in (base, joint, tip):
        dr.ellipse((p[0]-22, p[1]-22, p[0]+22, p[1]+22), fill=NAVY, outline="white", width=5)
    dr.text((90, 448), "Base / q1", font=font(28, True), fill=NAVY)
    dr.text((400, 178), "Elbow / q2", font=font(28, True), fill=NAVY)
    dr.text((720, 365), "End effector", font=font(27, True), fill=NAVY)
    dr.text((300, 300), "Link 1: 0.5 m", font=font(25), fill=TEAL)
    dr.text((540, 260), "Link 2: 0.5 m", font=font(25), fill=ORANGE)
    box(dr, (895, 135, 1400, 235), "Joint targets + PID", size=28)
    box(dr, (895, 340, 1400, 440), "Dynamics M, C, G", size=28)
    arrow(dr, (1148, 235), (1148, 340))
    centered(dr, (60, 493, 1450, 550), "Illustrative parameters; target step is q1 = 0.40 rad and q2 = -0.25 rad", 24, MUTED)
    return save(im, path)


def arduino_wiring(path: Path):
    im, dr = canvas()
    centered(dr, (40, 15, 1460, 70), "Arduino Uno - keypad - I2C LCD wiring study", 34, NAVY, True)
    box(dr, (75, 130, 390, 425), "4x4 keypad", size=34)
    box(dr, (595, 110, 930, 445), "Arduino Uno", size=36)
    box(dr, (1140, 130, 1430, 425), "16x2 I2C LCD", size=33)
    for y, label in [(205, "Rows 1-4 -> D2-D5"), (285, "Cols 1-4 -> D6-D9")]:
        arrow(dr, (390, y), (595, y))
        centered(dr, (370, y-52, 615, y-7), label, 22, INK)
    for y, label in [(205, "A4 / SDA"), (285, "A5 / SCL"), (365, "5V / GND")]:
        arrow(dr, (930, y), (1140, y))
        centered(dr, (925, y-50, 1140, y-9), label, 23, INK)
    centered(dr, (45, 485, 1455, 550), "Schematic only: verify LCD I2C address, pin order and common ground on the actual parts", 24, MUTED)
    return save(im, path)


def arduino_flow(path: Path):
    im, dr = canvas()
    centered(dr, (40, 20, 1460, 75), "Keypress handling in the repository sketch", 34, NAVY, True)
    labels = ["Scan 4x4 matrix", "Decode key", "Print to LCD", "Print to Serial"]
    xs = [(55, 360), (430, 735), (805, 1110), (1180, 1460)]
    for (x1, x2), label in zip(xs, labels):
        box(dr, (x1, 205, x2, 345), label, size=27)
    for (_, x2), (nx1, _) in zip(xs, xs[1:]):
        arrow(dr, (x2, 275), (nx1, 275))
    centered(dr, (60, 425, 1450, 510), "Expected behavior: one pressed key appears on the display and in the 9600-baud Serial Monitor", 25, MUTED)
    return save(im, path)


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ReportTitle", fontName="Helvetica-Bold", fontSize=17, leading=21,
                          textColor=colors.HexColor(NAVY), spaceAfter=7))
styles.add(ParagraphStyle(name="Meta", fontName="Helvetica", fontSize=9, leading=13,
                          textColor=colors.HexColor(MUTED), spaceAfter=13))
styles.add(ParagraphStyle(name="ReportHead", fontName="Helvetica-Bold", fontSize=11.2, leading=14,
                          textColor=colors.HexColor(NAVY), spaceBefore=11, spaceAfter=5))
styles.add(ParagraphStyle(name="ReportBody", fontName="Helvetica", fontSize=9.4, leading=13.5,
                          textColor=colors.HexColor(INK), spaceAfter=6))
styles.add(ParagraphStyle(name="Caption", fontName="Helvetica-Oblique", fontSize=8.2, leading=11,
                          textColor=colors.HexColor(MUTED), spaceBefore=4, spaceAfter=7))
styles.add(ParagraphStyle(name="Small", fontName="Helvetica", fontSize=8.3, leading=11.5,
                          textColor=colors.HexColor(INK), spaceAfter=4))


def p(text: str, style: str = "ReportBody"):
    return Paragraph(text, styles[style])


def section(title: str, body: str):
    return [p(title, "ReportHead"), p(body)]


def bullets(items: list[str]):
    return [p("&#8226; " + item) for item in items]


def fig(path: Path, caption: str):
    with PILImage.open(path) as im:
        width, height = im.size
    display_width = 510
    return [Image(str(path), width=display_width, height=display_width * height / width), p(caption, "Caption")]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D5E0E8"))
    canvas.line(48, 43, 564, 43)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor(MUTED))
    canvas.drawString(48, 29, "Gajendra | 2301ME18 | IIT Patna | Robotics portfolio")
    canvas.drawRightString(564, 29, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(destination: Path, title: str, subtitle: str, abstract: str,
              context: str, first_figure: Path, first_caption: str,
              methods: list[str], second_figure: Path, second_caption: str,
              completed: list[str], result: str, limits: str, run: str, source_url: str):
    destination.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(destination), pagesize=letter, leftMargin=48, rightMargin=48,
                            topMargin=43, bottomMargin=58, title=title, author="Gajendra")
    story = [p(title, "ReportTitle"), p(subtitle, "Meta")]
    story += section("Abstract - short summary", abstract)
    story += section("Purpose and background", context)
    story += fig(first_figure, first_caption)
    story += [p("Methods - how the study was carried out", "ReportHead")]
    story += bullets(methods)
    story += [PageBreak(), p(title + " | Work and results", "ReportTitle")]
    story += section("What was done", "The items below describe the work represented by this repository and the course context.")
    story += bullets(completed)
    story += fig(second_figure, second_caption)
    story += section("Result and interpretation", result)
    story += section("Limits and next validation step", limits)
    story += [p("Reproduce it", "ReportHead"), p(run, "Small"),
              p(f'<link href="{source_url}" color="#087E8B">Open project code on GitHub</link>', "Small")]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return destination


def main():
    clean = simulate_cleaning(DEFAULT_MAP)
    motor = simulate_motor()
    arm = simulate_arm()
    base = "https://github.com/GajendraLodhi1/robotics-engineering-portfolio/tree/main/projects/"

    clean_dir = ROOT / "projects/cleaning_bot/reports"
    build_pdf(clean_dir / "cleaning_robot_route_study.pdf",
              "Cleaning robot: proposal and route study", "ATOMQUEST 2025 | Team Super Kings | Gajendra, 2301ME18",
              "This report explains Team Super Kings' proposed cleaning robot and a later grid-based software study. The team was Harsh Raj, Rakesh Hembram and Gajendra. The proposal combines brush, vacuum and mop modules. The runnable program explores obstacle-aware route coverage; it does not demonstrate a constructed robot or cleaning performance.",
              "The proposed system aimed to clean a floor in quadrants using onboard sensing and locomotion. The diagram separates the proposed hardware idea from the Python route simulation documented here.",
              cleaning_architecture(clean_dir / "figures/concept_architecture.png"),
              "Figure 1. Concept diagram derived from the team proposal; component selection and integration remain unvalidated.",
              ["Represent floor cells as open (.) or blocked (#); start at the first open cell in the default map.",
               "Use breadth-first search to find a shortest obstacle-free route to the nearest uncleaned reachable cell.",
               "Repeat until every cell connected to the start has been visited; count moves and report unreachable cells separately."],
              cleaning_route(clean_dir / "figures/default_route.png", clean),
              "Figure 2. Generated route on the default map. The orange line shows travel, not a physical robot trace.",
              ["The team prepared the ATOMQUEST proposal; the original proposal PDF remains in this project folder.",
               "A Python simulator and tests were prepared for this portfolio to demonstrate grid coverage."],
              f"On the default {len(DEFAULT_MAP[0])} by {len(DEFAULT_MAP)} map, the software reaches {clean.reachable_count} of {clean.open_count} open cells in {len(clean.path)-1} moves. Coverage of reachable floor is {clean.coverage_percent:.0f}%. The route may revisit cells, so this is a coverage result and not a shortest-overall-route result.",
              "The map assumes known static obstacles and four-direction movement. No localization, wheel slip, dynamic obstacle, battery, suction, mopping or hardware measurements are modeled. A physical build would require wiring checks, sensor calibration, collision tests and measured coverage.",
              "Run: python projects/cleaning_bot/simulator.py", base + "cleaning_bot")

    motor_dir = ROOT / "projects/dc_motor_pid/reports"
    build_pdf(motor_dir / "dc_motor_pid_study.pdf",
              "DC motor: PWM and PID speed study", "ME3202 control lab concept | Gajendra, 2301ME18",
              "This independent Python study compares a fixed PWM command with PID speed control on a normalized first-order motor model. It makes the control loop and its output visible for interview preparation. The plotted speeds are simulated values, not measurements from the IIT Patna lab motor.",
              "The ME3202 course covered DC motor PWM and closed-loop PID with Arduino, a driver and Simulink. This repository model isolates the control principle so target tracking can be reproduced without hardware.",
              motor_control_diagram(motor_dir / "figures/control_loop.png"),
              "Figure 1. Simulated closed-loop structure. The diagram does not imply an encoder was used in this Python study.",
              ["Use d(speed)/dt = (gain * PWM - speed) / time_constant with unitless speed and PWM.",
               "Apply fixed PWM = 0.45 to one copy and a PID command to another; clamp PID PWM to 0 through 1.",
               "Integrate with 0.02 s steps for 4.0 s using the documented default gains; compare against target 0.70."],
              chart(motor_dir / "figures/speed_response.png", "Simulated speed response",
                    [("Target", [s.target for s in motor], NAVY),
                     ("Fixed PWM", [s.open_loop_speed for s in motor], ORANGE),
                     ("PID", [s.closed_loop_speed for s in motor], TEAL)],
                    [s.time_s for s in motor], "Norm. speed", 0, 0.85),
              "Figure 2. Speed trajectories generated by the repository code with default parameters.",
              ["Gajendra reports completing the corresponding motor control lab at IIT Patna.",
               "This repository adds an independent Python model, CSV output and tests for fixed-PWM versus PID behavior."],
              f"At 4.0 s, fixed PWM gives normalized speed {motor[-1].open_loop_speed:.3f}; PID gives {motor[-1].closed_loop_speed:.3f} against target {motor[-1].target:.3f}. With these parameters, integral action removes the persistent error present under the fixed command.",
              "The model has no measured motor constant, encoder noise, load disturbance, dead zone or direction reversal. For hardware validation, log commanded duty, measured RPM and load changes, then retune gains while checking saturation and safety.",
              "Run: python projects/dc_motor_pid/dc_motor_pid.py", base + "dc_motor_pid")

    arm_dir = ROOT / "projects/me3202_labs/two_link_pid/reports"
    build_pdf(arm_dir / "two_link_arm_pid_study.pdf",
              "Two-link robot arm: PID simulation", "ME3202 Lab 7 study | Gajendra, 2301ME18",
              "This report presents an independent two-degree-of-freedom planar arm simulation inspired by the course manipulator lab. A gravity-compensated PID controller tracks two step joint targets. Link dimensions and the resulting angles are illustrative simulation outputs, not physical robot measurements.",
              "The course lab studies M(q) qdd + C(q, qd) qd + G(q) = torque and PID tracking. The portfolio code implements that structure in Python for a reproducible step-response study.",
              arm_diagram(arm_dir / "figures/two_link_model.png"),
              "Figure 1. Two-link geometry and controller relationship. Link lengths are model parameters.",
              ["Set link lengths to 0.5 m and masses to 1.0 kg each; form symmetric inertia, velocity coupling and gravity terms.",
               "Apply joint PID with gravity compensation, integral clamp and +/-15 N m torque limits.",
               "Integrate dynamics at 0.002 s steps for 3.0 s; compare q1 and q2 with 0.40 and -0.25 rad targets."],
              chart(arm_dir / "figures/joint_tracking.png", "Simulated joint tracking",
                    [("q1 target", [r[3] for r in arm], NAVY),
                     ("q1", [r[1] for r in arm], TEAL),
                     ("q2 target", [r[4] for r in arm], "#9A69B1"),
                     ("q2", [r[2] for r in arm], ORANGE)],
                    [r[0] for r in arm], "Angle (rad)", -0.4, 0.55),
              "Figure 2. Joint trajectories generated by the Python model with default gains.",
              ["Gajendra reports completing the corresponding manipulator lab at IIT Patna.",
               "The portfolio adds a separate Python simulation, CSV response and tests of inertia and tracking."],
              f"At 3.0 s, q1 = {arm[-1][1]:.4f} rad and q2 = {arm[-1][2]:.4f} rad. Absolute step errors are {abs(arm[-1][3]-arm[-1][1]):.4f} and {abs(arm[-1][4]-arm[-1][2]):.4f} rad. The response illustrates model-based tracking under the chosen parameters.",
              "This is a step-reference study only; the original lab also included ramp and sinusoidal inputs. Joint friction, backlash, encoder quantization and payload changes are not validated. Hardware work would require parameter identification, torque calibration and safe travel limits.",
              "Run: python projects/me3202_labs/two_link_pid/simulate.py", base + "me3202_labs/two_link_pid")

    arduino_dir = ROOT / "projects/me3202_labs/arduino_keypad_lcd/reports"
    build_pdf(arduino_dir / "arduino_keypad_lcd_study.pdf",
              "Arduino Uno: keypad and LCD interface", "ME3202 Lab 6 study | Gajendra, 2301ME18",
              "This report documents the course keypad/LCD interface and a fresh Arduino sketch in the portfolio. A key press is intended to appear on a 16x2 I2C display and Serial Monitor. The diagrams show the wiring and logic to check; this repository copy has not been compiled or retested on hardware.",
              "A 4x4 matrix keypad reduces the number of required signal pins by sharing four rows and four columns. The I2C LCD uses SDA and SCL for display communication.",
              arduino_wiring(arduino_dir / "figures/wiring_study.png"),
              "Figure 1. Pin mapping used by the fresh sketch. Confirm the particular keypad and LCD module pin order before wiring.",
              ["Map keypad rows to D2-D5 and columns to D6-D9; connect LCD SDA to A4 and SCL to A5.",
               "Use the Keypad library to scan for a pressed key and LiquidCrystal_I2C to update the 16x2 display.",
               "Send the same key to Serial at 9600 baud for debugging; check all 16 keys on a physical setup."],
              arduino_flow(arduino_dir / "figures/key_flow.png"),
              "Figure 2. Intended software path from keypress to LCD and serial output.",
              ["Gajendra reports completing the institute keypad/LCD lab.",
               "The repository includes a newly written .ino sketch and a documented pin table for practice."],
              "The expected behavior is that each press appears as one character on the LCD and in Serial Monitor. No physical output or compile log for this fresh sketch is included, so this report does not claim a verified new hardware demonstration.",
              "Install compatible Keypad and LiquidCrystal_I2C libraries, confirm address (often 0x27), power, ground and LCD contrast, then test all keys. Wrong characters usually point to row/column order; a blank display may indicate address or power trouble.",
              "Open projects/me3202_labs/arduino_keypad_lcd/keypad_lcd.ino in Arduino IDE.",
              base + "me3202_labs/arduino_keypad_lcd")

    print("Generated four illustrated PDF reports")


if __name__ == "__main__":
    main()
