"""Build two illustrated DOCX study guides for pinned upstream robotics references.

This script writes only the editable DOCX files and locally generated diagrams.
Use the bundled render_docx.py workflow to make and inspect the matching PDFs.
"""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
BLACK = RGBColor(0, 0, 0)
BLUE = RGBColor(22, 76, 120)
GRAY = RGBColor(85, 92, 100)
FONT = Path("C:/Windows/Fonts/arial.ttf")
BOLD = Path("C:/Windows/Fonts/arialbd.ttf")


def font(size: int, bold: bool = False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)


def center(draw, bounds, label: str, size: int = 29, bold: bool = True):
    x1, y1, x2, y2 = bounds
    f = font(size, bold)
    bb = draw.textbbox((0, 0), label, font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    draw.text(((x1 + x2 - w) / 2, (y1 + y2 - h) / 2 - bb[1]), label, font=f, fill="#17334D")


def box(draw, bounds, label, fill="#F2F7FA"):
    draw.rounded_rectangle(bounds, radius=18, fill=fill, outline="#3E8293", width=4)
    center(draw, bounds, label)


def arrow(draw, a, b, color="#168099"):
    draw.line((*a, *b), fill=color, width=6)
    import math
    theta = math.atan2(b[1] - a[1], b[0] - a[0])
    for d in (-0.55, 0.55):
        p = (b[0] - 22 * math.cos(theta + d), b[1] - 22 * math.sin(theta + d))
        draw.line((*b, *p), fill=color, width=6)


def new_canvas(title):
    im = Image.new("RGB", (1600, 570), "white")
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle((2, 2, 1597, 567), radius=22, outline="#CBD8E3", width=3)
    center(dr, (40, 18, 1560, 72), title, 35)
    return im, dr


def draw_teleop_arch(path):
    im, d = new_canvas("RoboPilot message path")
    boxes = [((48, 148, 320, 275), "Browser dashboard"),
             ((390, 148, 650, 275), "rosbridge"),
             ((720, 148, 980, 275), "ROS 2 topics"),
             ((1050, 148, 1300, 275), "ros_gz_bridge"),
             ((1360, 148, 1555, 275), "Gazebo")]
    for xy, label in boxes:
        box(d, xy, label, fill="#EEF7FA")
    for a, b in [((320, 212), (390, 212)), ((650, 212), (720, 212)),
                 ((980, 212), (1050, 212)), ((1300, 212), (1360, 212))]:
        arrow(d, a, b)
    center(d, (50, 312, 1545, 358), "Commands travel right: /cmd_vel. Telemetry returns left: /odom and /scan.", 27, False)
    d.line((1450, 375, 1450, 447, 180, 447, 180, 375), fill="#DC8840", width=6)
    arrow(d, (180, 400), (180, 375), "#DC8840")
    center(d, (80, 465, 1520, 530), "Simulation only. Browser stop logic is not a substitute for a robot-side watchdog.", 25, False)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)


def draw_teleop_validation(path):
    im, d = new_canvas("Teleoperation validation ladder")
    labels = ["Build and launch", "Inspect ROS topics", "Drive and release", "Record a bag", "Drop the link"]
    coords = [(45, 170, 325, 315), (365, 170, 645, 315), (685, 170, 965, 315),
              (1005, 170, 1285, 315), (1325, 170, 1560, 315)]
    for xy, label in zip(coords, labels):
        box(d, xy, label, fill="#F4F6F8")
    for a, b in zip(coords, coords[1:]):
        arrow(d, (a[2], 242), (b[0], 242))
    center(d, (50, 355, 1550, 425), "Save evidence at each step before adding new features.", 30, False)
    center(d, (50, 430, 1550, 515), "The last step measures failure behavior, not normal driving performance.", 25, False)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)


def draw_aruco_arch(path):
    im, d = new_canvas("ArUco camera pose pipeline")
    labels = ["Camera image", "Marker corners", "Marker pose", "N observations", "Camera pose"]
    coords = [(40, 158, 318, 292), (360, 158, 638, 292), (680, 158, 958, 292),
              (1000, 158, 1278, 292), (1320, 158, 1560, 292)]
    for xy, label in zip(coords, labels):
        box(d, xy, label)
    for a, b in zip(coords, coords[1:]):
        arrow(d, (a[2], 225), (b[0], 225))
    center(d, (75, 345, 1525, 405), "Image topic -> OpenCV detection -> pose estimate -> average -> ROS 2 service response", 27, False)
    center(d, (75, 432, 1525, 500), "Inputs that must match reality: intrinsics, distortion, marker ID and physical marker side length", 24, False)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)


def draw_aruco_frames(path):
    im, d = new_canvas("Camera and marker coordinate frames")
    box(d, (100, 185, 450, 345), "World / base")
    box(d, (625, 185, 975, 345), "ArUco marker")
    box(d, (1150, 185, 1500, 345), "Camera")
    arrow(d, (450, 265), (625, 265))
    arrow(d, (975, 265), (1150, 265))
    center(d, (455, 340, 650, 390), "T world marker", 22, False)
    center(d, (980, 340, 1175, 390), "inverse T camera marker", 20, False)
    center(d, (80, 425, 1520, 505), "T world camera = T world marker x inverse(T camera marker)", 30, False)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)


def set_repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def borders(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    bd = OxmlElement("w:tcBorders")
    for name in ("top", "left", "bottom", "right"):
        edge = OxmlElement("w:" + name)
        edge.set(qn("w:val"), "single")
        edge.set(qn("w:color"), "D9D9D9")
        edge.set(qn("w:sz"), "4")
        bd.append(edge)
    tcPr.append(bd)


def add_hyperlink(paragraph, text, url):
    part = paragraph.part
    rel = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), rel)
    run = OxmlElement("w:r")
    props = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "164C78")
    props.append(color)
    run.append(props)
    t = OxmlElement("w:t")
    t.text = text
    run.append(t)
    link.append(run)
    paragraph._p.append(link)


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.autofit = False
    if widths:
        for i, width in enumerate(widths):
            table.columns[i].width = Inches(width)
    for i, label in enumerate(headers):
        c = table.rows[0].cells[i]
        c.text = label
        shade(c, "E8EEF3")
        borders(c)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for run in c.paragraphs[0].runs:
            run.bold = True
            run.font.size = Pt(9)
    set_repeat_header(table.rows[0])
    for j, row in enumerate(rows):
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)
            borders(cells[i])
            cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if j % 2:
                shade(cells[i], "F7FAFC")
            for par in cells[i].paragraphs:
                par.paragraph_format.space_after = Pt(1)
                for run in par.runs:
                    run.font.size = Pt(8.8)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return table


def para(doc, text, style=None):
    p = doc.add_paragraph(style=style)
    p.add_run(text)
    return p


def bullet(doc, text):
    return para(doc, text, "List Bullet")


def heading(doc, text, level=1):
    return doc.add_heading(text, level=level)


def code(doc, lines):
    for line in lines:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.22)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(line)
        r.font.name = "Consolas"
        r.font.size = Pt(8.7)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def figure(doc, path, caption):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(path), width=Inches(6.85))
    c = doc.add_paragraph(caption, style="Caption")
    c.paragraph_format.keep_together = True


def setup_doc(title, subtitle, upstream_url, commit, license_name):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.top_margin = Inches(0.7)
    sec.bottom_margin = Inches(0.62)
    sec.left_margin = Inches(0.78)
    sec.right_margin = Inches(0.78)
    sec.header_distance = Inches(0.35)
    sec.footer_distance = Inches(0.34)

    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10.3)
    normal.font.color.rgb = BLACK
    normal.paragraph_format.line_spacing = 1.16
    normal.paragraph_format.space_after = Pt(6)
    for name, size, before, after in [("Title", 20, 0, 7), ("Heading 1", 13, 15, 6), ("Heading 2", 11, 11, 4)]:
        st = doc.styles[name]
        st.font.name = "Arial"
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = BLACK
        st.paragraph_format.space_before = Pt(before)
        st.paragraph_format.space_after = Pt(after)
        st.paragraph_format.keep_with_next = True
    doc.styles["Caption"].font.name = "Arial"
    doc.styles["Caption"].font.size = Pt(8.8)
    doc.styles["Caption"].font.italic = True
    doc.styles["Caption"].font.color.rgb = GRAY
    doc.styles["Caption"].paragraph_format.space_after = Pt(9)
    doc.styles["List Bullet"].font.name = "Arial"
    doc.styles["List Bullet"].font.size = Pt(10.2)
    doc.styles["List Bullet"].paragraph_format.space_after = Pt(3)

    tp = doc.add_paragraph(style="Title")
    tp.add_run(title)
    s = doc.add_paragraph(subtitle)
    s.paragraph_format.space_after = Pt(6)
    for run in s.runs:
        run.font.size = Pt(11)
        run.font.color.rgb = GRAY
    meta = doc.add_paragraph()
    meta.paragraph_format.space_after = Pt(11)
    meta.add_run("Prepared for Gajendra  |  IIT Patna  |  5 November 2026\n")
    meta.add_run("Reference status  |  Original upstream code pinned at " + commit[:12] + "  |  " + license_name + " license\n")
    add_hyperlink(meta, "Original repository", upstream_url)
    for run in meta.runs:
        run.font.size = Pt(8.8)
        run.font.color.rgb = GRAY
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    footer.add_run("Learning guide  |  Gajendra 2301ME18  |  Page ")
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    footer._p.append(field)
    for run in footer.runs:
        run.font.size = Pt(8)
        run.font.color.rgb = GRAY
    return doc


def sources(doc, items):
    heading(doc, "Sources and attribution")
    for label, url in items:
        p = doc.add_paragraph()
        p.add_run(label + "  ")
        add_hyperlink(p, url, url)


def teleop_guide():
    folder = ROOT / "01_ros2_web_teleoperation"
    fig1 = folder / "figures/message_path.png"
    fig2 = folder / "figures/validation_ladder.png"
    draw_teleop_arch(fig1)
    draw_teleop_validation(fig2)
    doc = setup_doc("ROS 2 Web Teleoperation Study Guide", "A practical learning path from simulation to reliable robot control",
                    "https://github.com/weepwood/RoboPilot", "011692aeed3f5438aa9ed4a93d6670902d3b112c", "MIT")

    heading(doc, "Purpose and status")
    para(doc, "This guide explains how to learn from RoboPilot, a small browser-controlled differential-drive simulation. The aim is to understand the full command and telemetry path, then design an original reliability and logging extension. The upstream project belongs to weepwood. Its code is included as a pinned reference submodule; the guide does not present it as Gajendra's work. The ROS stack was reviewed from source but was not run on this Windows machine.")
    heading(doc, "Abstract")
    para(doc, "RoboPilot combines a ROS 2 Jazzy robot description, Gazebo Harmonic world, a ROS to Gazebo bridge, rosbridge and a Vue dashboard. The browser publishes velocity commands and displays odometry and lidar data. The learning sequence begins with reading the message graph, proceeds to a controlled simulation run, and ends with failure testing and a separate robot-side command timeout design. These skills transfer to robot bring-up, teleoperation, diagnostics and data collection work.")
    heading(doc, "Why this reference is useful")
    para(doc, "The repository is focused enough to trace end to end. It uses the current documented ROS 2 Jazzy and Gazebo Harmonic pairing on Ubuntu 24.04. It exposes standard topics that appear in many mobile robots. Its browser controls also create concrete questions about stale commands, network loss and operator feedback. The project has only a small public footprint, so assess it by reading and testing the code rather than assuming it is production ready.")
    figure(doc, fig1, "Figure 1  Command and telemetry path inferred from the pinned upstream files")

    heading(doc, "Concepts to learn before running")
    add_table(doc, ["Concept", "Meaning in this project", "Check in a run"], [
        ("ROS 2 topic", "Named stream between publishers and subscribers", "ros2 topic list and ros2 topic info"),
        ("Twist command", "Linear x and angular z velocity request on /cmd_vel", "Echo commands while pressing and releasing controls"),
        ("Odometry", "Estimated position and velocity on /odom", "Check sign and units while moving"),
        ("LaserScan", "Ranges around the robot on /scan", "Inspect valid ranges and frame ID"),
        ("TF", "Transforms between robot coordinate frames", "Inspect frame tree and timestamps"),
        ("rosbridge", "WebSocket bridge between browser and ROS graph", "Confirm URL and connection state"),
    ], [1.15, 3.25, 2.45])
    para(doc, "For a differential drive robot, forward speed is half the sum of wheel linear speeds. Turning rate depends on their difference divided by wheel separation. You do not need to derive the full controller at first; you should understand why a Twist command can make the wheels turn at different rates.")

    heading(doc, "Read the upstream files in this order")
    add_table(doc, ["File", "Question to answer"], [
        ("README.md and docs/ARCHITECTURE.md", "What components start and which ports or topics connect them?"),
        ("src/robopilot_sim/urdf/robopilot.urdf.xacro", "Which links, joints and sensor frames make up the robot?"),
        ("src/robopilot_sim/config/bridge.yaml", "Which topics move from ROS to Gazebo and back?"),
        ("src/robopilot_sim/launch/simulation.launch.py", "Which processes start, and what happens when a launch option is disabled?"),
        ("dashboard/src/App.vue", "Where are commands published, stopped and displayed?"),
        ("scripts/build_ros.sh and scripts/run_sim.sh", "What environment do the helper scripts assume?"),
    ], [3.3, 3.55])
    para(doc, "In App.vue, find startMotion, publishActiveMotion, stopMotion and emergencyStop. The browser publishes commands repeatedly while an input is active. The code calls stopMotion on key release, blur and visibility change. A lost connection can prevent the last zero command from reaching a robot. Treat the displayed E-STOP as a software state in this simulation, not as a physical safety circuit.")

    heading(doc, "Environment and first run")
    para(doc, "Use Ubuntu 24.04 with ROS 2 Jazzy and Gazebo Harmonic, either natively or through Windows 11 WSL2 with WSLg. The upstream Windows guide recommends keeping a runnable workspace inside the Linux filesystem rather than under /mnt/d. Installations and package versions should follow the upstream README and official ROS documentation at run time.")
    code(doc, ["# In an Ubuntu 24.04 shell after installing ROS 2 Jazzy", "mkdir -p ~/projects && cd ~/projects", "git clone https://github.com/weepwood/RoboPilot.git", "cd RoboPilot", "# Review scripts/bootstrap_ubuntu.sh before running it", "./scripts/build_ros.sh", "./scripts/run_sim.sh", "# In a second shell: ./scripts/run_dashboard.sh"])
    para(doc, "These commands are a planned procedure, not a completed run. The bootstrap script installs software, so read it and confirm the package list first. A successful baseline requires Gazebo and RViz to open, a browser dashboard to connect, and /cmd_vel, /odom and /scan to appear with expected message types.")

    heading(doc, "Experiments and evidence")
    figure(doc, fig2, "Figure 2  Study sequence with an evidence checkpoint after each stage")
    add_table(doc, ["Experiment", "Action", "Evidence to save"], [
        ("Graph inventory", "List nodes, topics, topic types and frame IDs", "Command output with date and ROS version"),
        ("Drive and release", "Hold forward, turn, release and press Stop", "Short /cmd_vel log and /odom plot"),
        ("Input loss", "Blur tab, close browser, interrupt WebSocket", "Last command and time until motion stops"),
        ("Record and replay", "Record /cmd_vel /odom /scan with ros2 bag", "Bag metadata and replay notes"),
        ("Parameter change", "Change velocity limits and compare", "Before and after values, run conditions"),
    ], [1.3, 3.1, 2.45])
    para(doc, "Use ros2 bag record /cmd_vel /odom /scan for a short reproducible session and ros2 bag info on the saved directory. Do not upload a large bag or anything containing private camera/audio data without review. Write measured results only after you run the experiment.")

    heading(doc, "What failure testing should reveal")
    para(doc, "A browser can request zero speed when the operator releases a key, but it cannot guarantee delivery after a link or process failure. Inspect the Gazebo diff-drive command timeout, if any, and measure it rather than assuming one exists. A stronger independent design places a timeout near the actuator or simulation controller and publishes or applies zero speed when commands become stale. Record the time from last valid command to stop under repeated disconnects. This is the main engineering distinction between a demo interface and a dependable teleoperation path.")

    heading(doc, "Original follow-on project brief")
    para(doc, "Build a separate Teleoperation Reliability Logger after reproducing the baseline. Keep the upstream project as a cited reference. Your project can use a fresh ROS 2 node that accepts operator Twist commands, stamps them, checks age and speed limits, forwards safe commands, and records command, odometry and fault events. Add a small test harness that injects delayed commands and link loss. Do not present this design as completed until code and measurements exist.")
    add_table(doc, ["Deliverable", "Minimum acceptance check"], [
        ("Robot-side timeout", "A stale command leads to zero within a documented target time in repeated tests"),
        ("Command limits", "Linear and angular outputs never exceed configured caps"),
        ("Episode log", "Bag or structured log contains command, state, stop reason and timestamps"),
        ("Test evidence", "At least normal drive, release, disconnect and delayed-message cases"),
        ("Project report", "Architecture, actual plots, failure table, reproducible instructions and limits"),
    ], [2.0, 4.85])
    para(doc, "A candidate target is a 250 ms command-age limit, but choose the final value from controller frequency, network measurements and safe stopping behavior. The number is a design goal, not a claimed result.")

    heading(doc, "Four week learning plan")
    add_table(doc, ["Week", "Output you should personally produce"], [
        ("1", "ROS 2 and Gazebo installation notes, package build, topic and frame map"),
        ("2", "Recorded baseline drive, odometry and scan; explanation of every path in Figure 1"),
        ("3", "Failure experiments and a written timeout design with test cases"),
        ("4", "A small independent node or simulator extension, tests and measured report"),
    ], [0.7, 6.15])
    heading(doc, "Interview questions to practise")
    for question in [
        "What is the difference between /cmd_vel and /odom, and why can they disagree?",
        "What does ros_gz_bridge do, and how is it different from rosbridge?",
        "What happens if the browser disappears after sending a nonzero command?",
        "How would you measure the delay from operator action to robot motion?",
        "What would you record in a teleoperation episode for debugging and later learning?",
    ]:
        bullet(doc, question)
    heading(doc, "What can honestly appear on a resume")
    para(doc, "After a verified run, describe the specific package you built, topics you inspected, faults you reproduced and code you personally changed. Until then, list this only as a learning reference. A strong original entry includes measured latency or stop time, a test method and a link to your own repository.")
    sources(doc, [
        ("Pinned upstream project", "https://github.com/weepwood/RoboPilot"),
        ("Upstream Windows setup", "https://github.com/weepwood/RoboPilot/blob/main/docs/WINDOWS_WSL2.md"),
        ("Gazebo and ROS pairing", "https://gazebosim.org/docs/jetty/ros_installation/"),
        ("ROS 2 Jazzy documentation", "https://docs.ros.org/en/jazzy/"),
        ("rosbag2 recording and playback", "https://github.com/ros2/rosbag2"),
    ])
    path = folder / "reports/ros2_web_teleoperation_study_guide.docx"
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)
    return path


def aruco_guide():
    folder = ROOT / "02_aruco_camera_pose"
    fig1 = folder / "figures/pose_pipeline.png"
    fig2 = folder / "figures/coordinate_frames.png"
    draw_aruco_arch(fig1)
    draw_aruco_frames(fig2)
    doc = setup_doc("ArUco Camera Pose Estimation Study Guide", "A practical learning path for camera geometry and robot frames",
                    "https://github.com/Hydran00/aruco_camera_pose_estimator", "236c420d3470ebc65d3429abf7e8597045fa00ac", "MIT")

    heading(doc, "Purpose and status")
    para(doc, "This guide explains a compact ROS 2 project that estimates a camera pose from a known ArUco marker. The goal is to learn camera intrinsics, marker detection, coordinate transforms, service calls and validation. The upstream repository belongs to Davide Nardi. It is included as a pinned reference submodule. The package was reviewed from source but not built or run with a camera during preparation of this guide.")
    heading(doc, "Abstract")
    para(doc, "The upstream node subscribes to a camera image topic, detects a requested marker ID, estimates the marker pose in the camera frame, collects several observations, and returns a camera pose through a ROS 2 service. The learner should first trace frames and units, then supply real camera calibration values and measure stability. The proposed independent extension adds quality checks and a clear diagnostic report. These skills matter whenever a robot must relate image measurements to physical workspace coordinates.")
    heading(doc, "Why this reference is useful")
    para(doc, "The project is small enough to read its C++ image processor and service callback in one sitting. It exposes the practical difference between intrinsic camera calibration and extrinsic camera pose. It also shows a service-based workflow rather than a continuous output topic. The repository has a small public footprint and includes build workflows for Humble and Jazzy; its runtime behavior still needs independent validation on the learner's hardware.")
    figure(doc, fig1, "Figure 1  Data path inferred from the pinned upstream image processor and service code")

    heading(doc, "The geometry in plain language")
    para(doc, "Camera intrinsics describe how a 3D point maps to pixels. The focal lengths fx and fy and principal point cx and cy form a 3 by 3 camera matrix. Distortion coefficients describe how the lens bends straight image rays. Extrinsics describe where the camera sits relative to a marker, robot base or world frame. Correct intrinsics and a measured marker side length are prerequisites for a meaningful metric pose.")
    figure(doc, fig2, "Figure 2  Coordinate chain used to express camera pose in a chosen world or base frame")
    para(doc, "The marker detector estimates a transform from marker coordinates into camera coordinates. To express the camera in a world frame, invert that detected transform and combine it with the known world-to-marker transform. In compact notation: T_world_camera = T_world_marker x inverse(T_camera_marker). A transform is a 4 by 4 matrix carrying rotation and translation. Always state the source and target frames before multiplying transforms.")

    heading(doc, "Read the upstream files in this order")
    add_table(doc, ["File", "Question to answer"], [
        ("README.md", "What does the service return and what hardware is assumed?"),
        ("calibration_srv/srv/Calibration.srv", "What enters the service and what pose message comes back?"),
        ("aruco_camera_pose_estimator_cpp/config/config.yaml", "What image topic, marker ID context, sample count, timeout and frame are configured?"),
        ("aruco_camera_pose_estimator_cpp/config/calibration_params.yaml", "Which intrinsics and distortion values are example values?"),
        ("aruco_camera_pose_estimator_cpp/src/image_processor.cpp", "How are markers matched, pose vectors computed and observations averaged?"),
        ("aruco_camera_pose_estimator_cpp/src/pose_service.cpp", "How is the service called, timed out and transformed into the response frame?"),
    ], [3.5, 3.35])

    heading(doc, "Parameters that must be checked")
    add_table(doc, ["Parameter", "Why it matters", "Action before a real run"], [
        ("input_topic_name", "Names the incoming image stream", "Confirm with ros2 topic list and echo"),
        ("aruco_size", "Sets metric scale of translation", "Measure printed marker side and use metres as the code/config expect"),
        ("fx fy cx cy", "Camera matrix at chosen image resolution", "Calibrate your own camera or load verified values"),
        ("k1 k2 k3 p1 p2", "Lens distortion model", "Use measured coefficients, not copied defaults"),
        ("n_observation", "Number of detections averaged", "Compare latency and pose variation"),
        ("timeout_ms", "Maximum wait for sufficient detections", "Check actual camera frame rate and visibility"),
        ("frame_id and marker offset", "Defines output coordinate frame", "Measure marker pose relative to the chosen base"),
    ], [1.3, 2.7, 2.85])
    para(doc, "At the pinned commit, the example calibration file contains values for an RS435 at 1280 by 720 and zero distortion coefficients. Treat those as sample values. The README describes marker size in centimetres, while config.yaml and pose_service.cpp label aruco_size as metres. Follow the code's unit convention and verify scale with a known distance before trusting a pose.")

    heading(doc, "Environment and first run")
    para(doc, "Use a supported Ubuntu and ROS 2 environment with a camera driver that publishes a ROS image topic. The upstream README lists OpenCV development files and cv_bridge, then builds the C++ package and custom service with colcon. A printed DICT_4X4_50 marker of measured side length is needed. The repository does not supply a camera driver or intrinsics for every webcam. Windows WSL2 can build ROS code, but passing a physical camera into the Linux environment may require extra setup; native Ubuntu is often simpler for the first camera run.")
    code(doc, ["# In a sourced Ubuntu ROS 2 shell", "mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src", "git clone https://github.com/Hydran00/aruco_camera_pose_estimator.git", "cd ..", "rosdep install --from-paths src --ignore-src -r -y", "colcon build --symlink-install", "source install/setup.bash", "ros2 launch aruco_camera_pose_estimator_cpp aruco_camera_pose_estimator.launch.py", "# In another shell, call /calibration/get_camera_pose with marker_id"])
    para(doc, "These are study instructions and were not executed here. Before service calls, check that the image topic is live, marker ID and dictionary match the printed marker, the camera intrinsics match the stream resolution, and the marker has a measured world or base pose. Capture the exact service response and verify its header frame and units.")

    heading(doc, "Validation experiments and evidence")
    add_table(doc, ["Experiment", "Action", "Evidence to save"], [
        ("Single marker", "Hold one marker at a measured distance", "Image, marker size, pose, distance error"),
        ("Repeated calls", "Request pose at a fixed camera position", "Translation and rotation variation across runs"),
        ("Different views", "Tilt and move the marker within the image", "Pose changes and detection failures"),
        ("Wrong configuration", "Change marker ID or image topic deliberately", "Timeout and error response"),
        ("Two markers", "Show requested and unrelated IDs together", "Which marker drives the response"),
        ("Resolution change", "Switch image size without recalibration", "Scale or bias change; then correct intrinsics"),
    ], [1.15, 3.05, 2.65])
    para(doc, "Use a table with date, camera, resolution, calibrated matrix, distortion values, marker ID, measured side length, number of detections, output frame, measured reference distance and computed error. Save sample images only when allowed. Do not invent accuracy numbers from a single screenshot.")

    heading(doc, "Code review question for multiple markers")
    para(doc, "At the pinned commit, image_processor.cpp loops over detected marker IDs, but after calling estimatePoseSingleMarkers for the full corners list it reads tvec[0] and rvec[0]. Inspect whether the selected ID can be at another index and design a test with two visible markers. This is a testable review finding, not a confirmed field failure. A later independent patch should choose the pose matching the requested marker and include a regression test.")

    heading(doc, "Original follow-on project brief")
    para(doc, "Build a separate Camera Pose Quality Monitor after reproducing the upstream baseline. The new tool can accept frames and a calibrated camera model, select a specified marker ID, estimate pose, calculate corner reprojection error, reject low-quality frames, and export a CSV with timestamps and pose variation. Give it a small visualization that marks detected corners and axes. Keep the upstream project credited and implement your own tested code in a new repository.")
    add_table(doc, ["Deliverable", "Minimum acceptance check"], [
        ("Marker selection", "Requested ID is used when multiple IDs are visible"),
        ("Unit verification", "Known marker side and distance yield a documented scale error"),
        ("Quality metric", "Every accepted pose has a reprojection error and threshold"),
        ("Repeatability", "Report mean and spread of pose over a stationary capture"),
        ("Failure cases", "No marker, blurred marker, wrong calibration and timeout are logged"),
    ], [2.0, 4.85])
    para(doc, "Start with a recorded image set or a webcam before integrating a robot arm. The goal is a reproducible calibration check, not a claim of universal accuracy. Later, connect the pose to a robot frame tree and test a pick-point mapping with a measured target.")

    heading(doc, "Four week learning plan")
    add_table(doc, ["Week", "Output you should personally produce"], [
        ("1", "Frame diagram, source-code map and camera calibration plan"),
        ("2", "Working image topic, marker detection and first service response"),
        ("3", "Repeated pose measurements, multi-marker test and error analysis"),
        ("4", "Independent quality checker with tests, plots and a measured report"),
    ], [0.7, 6.15])
    heading(doc, "Interview questions to practise")
    for question in [
        "What is the difference between camera intrinsics and camera extrinsics?",
        "Why does a wrong printed marker size distort translation scale?",
        "Which transform must be inverted to express camera pose in the world frame?",
        "How would you know whether an estimated pose is trustworthy?",
        "Why might a service request time out even when a camera topic is visible?",
    ]:
        bullet(doc, question)
    heading(doc, "What can honestly appear on a resume")
    para(doc, "After a verified run, state the camera and calibration process, frame convention, measured repeatability or error, and code or tests you personally wrote. Until then, label this as a studied upstream reference. A strong original entry links to your own dataset, validation plots and implementation changes.")
    sources(doc, [
        ("Pinned upstream project", "https://github.com/Hydran00/aruco_camera_pose_estimator"),
        ("OpenCV ArUco detection", "https://docs.opencv.org/5.0/tutorials/objdetect/aruco_detection/aruco_detection.html"),
        ("OpenCV camera calibration", "https://docs.opencv.org/5.0/tutorials/calib3d/camera_calibration/camera_calibration.html"),
        ("ROS 2 Jazzy documentation", "https://docs.ros.org/en/jazzy/"),
    ])
    path = folder / "reports/aruco_camera_pose_study_guide.docx"
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)
    return path


if __name__ == "__main__":
    for output in (teleop_guide(), aruco_guide()):
        print(output)
