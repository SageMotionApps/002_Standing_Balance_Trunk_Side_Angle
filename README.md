# 002 Standing Balance Trunk Side Angle
Measure and train trunk side angles during standing trials.

### Nodes Required: 3 
 - Sensing (1): trunk (middle of back, switch pointing up) 
 - Feedback (2): 
    - left feedback: Node used to provide haptic feedback when the participant exceeds the threshold set in the app configuration panel.
    - right feedback: Node used to provide haptic feedback when the participant exceeds the threshold set in the app configuration panel.    


## Algorithm & Calibration
### Algorithm Information
The raw quaternions from the IMU are converted to Euler angles, and the roll angle is extracted using well established mathematical principles. If you'd like to learn more about quaternion to Euler angles calculations, we suggest starting with this Wikipedia page: [Conversion between quaternions and Euler angles](https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles)

### Calibration Process:
The angle calculated is the global roll angle for the IMU. This must be aligned with the segment. No initial static calibration is performed to compensate for misalignment with the segment.

## Description of Data in Downloaded File
- time (sec): time since trial start
- TSA (deg): trunk side angle (medial-lateral), positive is to the right
- max_lean_right (deg): The feedback threshold of max right lean set by the user in the app configuration panel.
- max_lean_left (deg): The feedback threshold of max left lean set by the user in the app configuration panel.
- right_feedback_state: feedback status for if the sensor has crossed the max right lean threshold. 
  - 0 is “feedback off”
  - 1 is “feedback on”
- left_feedback_state: feedback status for if the sensor has crossed the max left lean threshold. 
  - 0 is “feedback off”
  - 1 is “feedback on”
- SensorIndex: index of raw sensor data
- AccelX/Y/Z (m/s^2): raw acceleration data
- GyroX/Y/Z (deg/s): raw gyroscope data
- MagX/Y/Z (μT): raw magnetometer data
- Quat1/2/3/4: quaternion data (Scaler first order)
- Sampletime: timestamp of the sensor value
- Package: package number of the sensor value

# Development and App Processing Loop
The best place to start with developing an or modifying an app, is the [SageMotion Documentation](http://docs.sagemotion.com/index.html) page.
