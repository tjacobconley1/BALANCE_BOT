# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 22:38:14 2021

@author: TCadmin
"""

import odrive

odrv0 = odrive()

# Current Limit [10amps]
odrv0.axis0.motor.config.current_lim = 10
odrv0.axis1.motor.config.current_lim = 10



# the largest value you feel comfortable leaving 
# running through the motor continuously when 
# the motor is stationary
odrv0.axis0.motor.config.calibration_current = 5
odrv0.axis1.motor.config.calibration_current = 5

# Set this to True if using a brake resistor. 
# You need to save the ODrive configuration 
# and reboot the ODrive for this to take effect.
odrv0.config.enable_brake_resistor = False

# This is the resistance of the brake 
# resistor. You can leave this at the 
# default setting if you are not using 
# a brake resistor.
odrv0.config.brake_resistance

# the amount of current allowed to 
# flow back into the power supply
odrv0.config.dc_max_negative_current




# VELOCITY MODE=============================================

# for the hoverboard motors I believe this should
# be set to 15 
odrv0.axis0.motor.config.pole_pairs = 15
odrv0.axis1.motor.config.pole_pairs = 15

# type of motor being used, there are only 2 types
# 1-> MOTOR_TYPE_HIGH_CURRENT
# 2-> MOTOR_TYPE_GIMBAL (does not have built in encoders)
odrv0.axis0.motor.config.motor_type = odrive.MOTOR_TYPE_HIGH_CURRENT
odrv0.axis1.motor.config.motor_type = odrive.MOTOR_TYPE_HIGH_CURRENT







# THESE WERE EXECUTED IN THE FOLLOWING ORDER 

# FIRST
# resistance calibration max voltage 
odrv0.axis0.motor.config.resistance_calib_max_voltage = 4
odrv0.axis1.motor.config.resistance_calib_max_voltage = 4

# SECOND
# REQUIRES A config SAVE AND REBOOT
# requested current range 
odrv0.axis0.motor.config.requested_current_range = 25 #Requires config save and reboot
odrv0.axis1.motor.config.requested_current_range = 25 #Requires config save and reboot

# can atleast save the config before executing 
# the rest of the config 
odrv0.save_configuration()


# THIRD
# reduced bandwidth for hoverboard motors
odrv0.axis0.motor.config.current_control_bandwidth = 100
odrv0.axis1.motor.config.current_control_bandwidth = 100

# FOURTH
# This is the ratio of torque produced by the 
# motor per Amp of current delivered to the motor. 
# This should be set to 8.27 / (motor KV(usually 16 with hoverboard motors)) 
# this is the weight of the internals of the motor
# If you decide that you would rather command torque 
# in units of Amps, you could simply set the torque constant to 1.
odrv0.axis0.motor.config.torque_constant = 1 
odrv0.axis1.motor.config.torque_constant = 1

# FIFTH 
# can be set to HALL or INCREMENTAL
# HALL feedback has 6 states for every pole pair
# in the motor 
odrv0.axis0.encoder.config.mode = odrive.ENCODER_MODE_HALL
odrv0.axis1.encoder.config.mode = odrive.ENCODER_MODE_HALL

# SIXTH
# if using an encoder set equal to 
# Encoder Count Per Revolution 
# this should be 4x the pulse per 
# revolution value
# usually indicated in the datasheet of the encoder 
odrv0.axis0.encoder.config.cpr = 90
odrv0.axis1.encoder.config.cpr = 90

# SEVENTH
# increased offset calibration displacement because
# the HALL sensors are low resolution feedback 
# like an analog signal 
odrv0.axis0.encoder.config.calib_scan_distance = 150
odrv0.axis1.encoder.config.calib_scan_distance = 150

# EIGHTH 
# set the states of some GPIOs for some reason 
odrv0.config.gpio9_mode = odrive.GPIO_MODE_DIGITAL
odrv0.config.gpio10_mode = odrive.GPIO_MODE_DIGITAL
odrv0.config.gpio11_mode = odrive.GPIO_MODE_DIGITAL

# NINETH 
# setting the size of the encoder bandwidth  
odrv0.axis0.encoder.config.bandwidth = 100
odrv0.axis1.encoder.config.bandwidth = 100

# TENTH 
# position control mode not used but set to 
# default value 
odrv0.axis0.controller.config.pos_gain = 1
odrv0.axis1.controller.config.pos_gain = 1

# ELEVENTH
# set velocity gain 
odrv0.axis0.controller.config.vel_gain = 0.02 * odrv0.axis0.motor.config.torque_constant * odrv0.axis0.encoder.config.cpr
odrv0.axis1.controller.config.vel_gain = 0.02 * odrv0.axis1.motor.config.torque_constant * odrv0.axis1.encoder.config.cpr

# TWELVETH 
# set velocity integrator gain? 
# is just scaled differently than above 
# velocity gain 
odrv0.axis0.controller.config.vel_integrator_gain = 0.1 * odrv0.axis0.motor.config.torque_constant * odrv0.axis0.encoder.config.cpr
odrv0.axis1.controller.config.vel_integrator_gain = 0.1 * odrv0.axis1.motor.config.torque_constant * odrv0.axis1.encoder.config.cpr

# THIRTEENTH
# Velocity Limit [turns/s]
odrv0.axis0.controller.config.vel_limit = 10
odrv0.axis1.controller.config.vel_limit = 10

# FOURTEENTH 
# set the motorcontroller config for each to
# velocity control 
odrv0.axis0.controller.config.control_mode = odrive.CONTROL_MODE_VELOCITY_CONTROL
odrv0.axis1.controller.config.control_mode = odrive.CONTROL_MODE_VELOCITY_CONTROL


# (need to figure out a way to do the odrv0.reboot() here and then
#   continue to execute the rest of the code in this file)
odrv0.save_configuration()
odrv0.reboot()



# after reboot this motor calibration should be 
# activated 
odrv0.axis0.requested_state = odrive.AXIS_STATE_MOTOR_CALIBRATION
odrv0.axis1.requested_state = odrive.AXIS_STATE_MOTOR_CALIBRATION

# read out both motor data
# to check that there is no error and that
# the phase resistance and inductance are reasonable
odrv0.axis0.motor
odrv0.axis1.motor

# Should be similar to this 
#  error = 0x0000 (int)
# phase_inductance = 0.00033594953129068017 (float)
# phase_resistance = 0.1793474406003952 (float) 

# if everthing looks good and there are no errors 
# or missing values here we can tell the odrive that 
# saving this calibration to persistent memory is OK
odrv0.axis0.motor.config.pre_calibrated = True
odrv0.axis1.motor.config.pre_calibrated = True

# this checks the alignment between the motor and the hall sensor
# because of this step we can plug the motor phases in random order 
# and also the hall signals can be random
# just dont change it after calibration  
odrv0.axis0.requested_state = odrive.AXIS_STATE_ENCODER_HALL_POLARITY_CALIBRATION
odrv0.axis1.requested_state = odrive.AXIS_STATE_ENCODER_HALL_POLARITY_CALIBRATION


# check the status of the encoder objects
# check that there are no errors 
# error = 0x0000 (int)
odrv0.axis0.encoder
odrv0.axis1.encoder

# if the hall encoder polarity was successful
# run the encoder offset calibration
odrv0.axis0.requested_state = odrive.AXIS_STATE_ENCODER_OFFSET_CALIBRATION
odrv0.axis1.requested_state = odrive.AXIS_STATE_ENCODER_OFFSET_CALIBRATION

# check encoder status for errors 
# phase_offset_float should be close to 0.5 mod 1
# values (-1.5, -0.5, 0.5, 1.5) are all good 
odrv0.axis0.encoder
odrv0.axis1.encoder

# should look like this 
#  error = 0x0000 (int)
#  config:
#    phase_offset_float = 0.5126956701278687 (float)

# if everything looks good then you can tell the ODrive that saving
# this calibration to persistent is OK
odrv0.axis0.encoder.config.pre_calibrated = True
odrv0.axis1.encoder.config.pre_calibrated = True

# need to save config and do a reboot right here somehow 
odrv0.save_configuration()
#odrv0.reboot()

# enable the closed loop control state 
odrv0.axis0.requested_state = odrive.AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis1.requested_state = odrive.AXIS_STATE_CLOSED_LOOP_CONTROL

# this sets the initial velocity 
odrv0.axis0.controller.input_vel = 2
odrv0.axis1.controller.input_vel = 2

# Your motor should spin here
odrv0.axis0.controller.input_vel = 0
odrv0.axis1.controller.input_vel = 0

# set the control state back to idle 
odrv0.axis0.requested_state = AXIS_STATE_IDLE
odrv0.axis0.requested_state = AXIS_STATE_IDLE




