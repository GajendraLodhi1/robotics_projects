# Robotics learning tracks

These are **study references**, not projects claimed as Gajendra's own work. Each `upstream_*` folder is a Git submodule pinned to an original author's commit. The two study guides and diagrams in the neighboring `reports/` folders were prepared for learning. No ROS 2 simulation, camera, or physical robot was run during guide preparation on this Windows machine.

| Order | Skill to learn | Original project | Study guide |
| --- | --- | --- | --- |
| 1 | ROS 2 graph, simulation, browser teleoperation, odometry, lidar, command safety | [weepwood/RoboPilot](https://github.com/weepwood/RoboPilot) | [DOCX](01_ros2_web_teleoperation/reports/ros2_web_teleoperation_study_guide.docx) · [PDF](01_ros2_web_teleoperation/reports/ros2_web_teleoperation_study_guide.pdf) |
| 2 | Camera intrinsics, ArUco detection, pose transforms, ROS 2 services, calibration checks | [Hydran00/aruco_camera_pose_estimator](https://github.com/Hydran00/aruco_camera_pose_estimator) | [DOCX](02_aruco_camera_pose/reports/aruco_camera_pose_study_guide.docx) · [PDF](02_aruco_camera_pose/reports/aruco_camera_pose_study_guide.pdf) |

## Download the reference code

Clone this portfolio with submodules:

```bash
git clone --recurse-submodules https://github.com/GajendraLodhi1/robotics-engineering-portfolio.git
```

If the portfolio is already cloned:

```bash
git submodule update --init --recursive
```

The upstream directories remain separate from Gajendra's work and retain their original MIT licenses. A GitHub ZIP of this portfolio will not include submodule contents; use `git clone --recurse-submodules` or the original links above.

## What to do next

Read the first guide, map its ROS topics, and run the simulation on Ubuntu 24.04 with ROS 2 Jazzy and Gazebo Harmonic when available. Record actual commands, screenshots, failures and fixes in its `progress_log.md`. Then study camera calibration and transforms with the second guide. Only after reproducing an upstream baseline, create a **new project with a distinct problem, your own code, tests and measured evidence**. The guides include concrete extension briefs.

For comparison, [pocket-teleop](https://github.com/chngyicheng/pocket-teleop) is an additional online reference for phone control, video and a server-side watchdog. It is linked for reading; its source is not included in this portfolio.

Official references: [ROS 2 Jazzy documentation](https://docs.ros.org/en/jazzy/), [Gazebo and ROS compatibility](https://gazebosim.org/docs/jetty/ros_installation/), [rosbag2](https://github.com/ros2/rosbag2), [OpenCV ArUco guide](https://docs.opencv.org/5.0/tutorials/objdetect/aruco_detection/aruco_detection.html).
