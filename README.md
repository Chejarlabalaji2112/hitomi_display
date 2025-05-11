# hitomi_display

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

*   [Description](#description)
*   [Installation](#installation)
*   [Usage](#usage)
*   [Configuration](#configuration)
*   [Contributing](#contributing)
*   [License](#license)

## Description

The `hitomi_display` package is a comprehensive ROS2-based GUI application meticulously crafted for the seamless control and monitoring of the Hitomi robot. This versatile package boasts an array of functionalities, including:

*   **Speech Recognition:** Empowering users to interact with the robot through voice commands.
*   **Stopwatch:** Facilitating precise timekeeping for task execution and performance analysis.
*   **Timer:** Enabling automated task scheduling and execution.

Designed with the Gazebo simulation environment in mind, `hitomi_display` provides an intuitive and efficient interface for robotics enthusiasts and researchers alike.

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/user/hitomi_display.git
    ```
2.  Navigate to the package directory:

    ```bash
    cd hitomi_display
    ```
3.  Install the dependencies using `rosdep`:

    ```bash
    rosdep install --from-paths src --ignore-src -r -y
    ```
4.  Build the package using `colcon`:

    ```bash
    colcon build
    ```
5.  Source the setup file:

    ```bash
    . install/setup.bash
    ```

## Usage

1.  Launch the Hitomi robot simulation in Gazebo.
2.  Run the `hitomi_display` package:

    ```bash
    ros2 launch hitomi_display gzx.launch.py
    ```
3.  Use the GUI to control and monitor the Hitomi robot.

## Configuration

The `hitomi_display` package can be configured using the following parameters:

*   `robot_name`: The name of the robot to control. Default: `hitomi`.
*   `use_speech_recognition`: Whether to use speech recognition. Default: `True`.
*   `timer_duration`: The duration of the timer in seconds. Default: `60`.

These parameters can be set in the `config/gz_bridge.yaml` file.

## Contributing

We welcome contributions to the `hitomi_display` package! If you would like to contribute, please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with clear, concise messages.
4.  Submit a pull request.

## License

This project is released under the MIT License.
