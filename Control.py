#!/usr/bin/ python
# Control
#
# Author: Omar García
# Date: January 17, 2024
# mail: omar.garcia.alcant@gmail.com
# git: @OmarGAlcantara
#
# Description: This script interfaces with the Control_utlis.py file to use the information provided by XPlane to program a Control Law and
#              send the Control Signal to the motors. Control Law programmed here is just an example PD controller

import socket
import Control_utlis as utlis

UDP_PORT = 49005                      # Definition of communication port with XPlane

error_q = 0
error_p = 0
error_r = 0
q_des = 0
p_des = 0
r_des = 0
pitch_des = 0
roll_des = 0
altura_des = -30
velz_des = 0
p = 0

########### - Definition of coordinate planes (Double check) ######################
#     for XPLANE is  /   for our common NED conception is
#            x       /                 y
#            y       /                 z
#            z       /                 x

###################################################################################

def main():

  UDP_IP = "127.0.0.1"                     #Definition of IP address
  sock = socket.socket(socket.AF_INET,     # Internet
                       socket.SOCK_DGRAM)  # UDP
  sock.bind((UDP_IP, UDP_PORT))


 # Definition of flags for the controller
  yaw_init = None  
  is_yaw_set = False
  z_init = None  
  is_z_set = False
  time_init = None  
  is_time_set = False

  while True:
    # Receive a packet
    data, addr = sock.recvfrom(1024)              # buffer size is 1024 bytes
    
    # Decode the packet. Result is a python dict (like a map in C) with values from X-Plane.
    # Example:
    # {'latitude': 47.72798156738281, 'longitude': 12.434000015258789, 
    #   'altitude MSL': 1822.67, 'altitude AGL': 0.17, 'speed': 4.11, 
    #   'roll': 1.05, 'pitch': -4.38, 'heading': 275.43, 'heading2': 271.84}
    values = utlis.DecodePacket(data)             # Calling the Control_utlis output, which is the aircraft states

    #Definition of Control Gains
    k_p = 0.03
    k_d = 0.07
    k_pp = 0.03
    k_dp = 0.09
    k_rp = 0.07
    k_rd = 0.66
    kp_z = 0.01
    kd_z = 0.05

# Angular velocities in the body frame    #[rad/s]
    p = values["P"]
    q = values["Q"]
    r = values["R"]

    pitch2 = values["pitch"]*(3.14/180)   #Euler angles and converted to radians
    roll2 = values["roll"]*(3.14/180)
    yaw2 = values["heading"]*(3.14/180)

    vz = -values["vy"]                    # XPlane uses a strange definition of coordinates, which are reported in the git repo
                                          # Since we want NED we will try to use common convention, z being the earth pointing axes

#   Initialization of flags for saving inital values
    if not is_yaw_set:
        yaw_init = values["heading"]*(3.14/180)
        is_yaw_set = True
    if not is_z_set:
        z_init = values["yy"]
        is_z_set = True
    if not is_time_set:
        time_init = values["times"]
        is_time_set = True  

#   Error definition
    z = z_init - values["yy"]
    error_pitch = pitch2 - pitch_des
    error_roll = roll2 - roll_des 
    error_yaw = yaw2 - yaw_init
    error_z = z - altura_des
    error_velz = vz - velz_des
    error_q = q - q_des
    error_p = p - p_des 
    error_r = r - r_des

#   PD Controller (Might need to implement Rotation for the angular velocities)
    PDRoll =  error_roll*k_p + error_p*k_d
    PDPitch =  error_pitch*k_pp + error_q*k_dp
    PDYaw = error_yaw*k_rp + error_r*k_rd
    PDz = (error_z*kp_z + error_velz*kd_z)

#   Mixer
    Throttle1 = PDz + PDRoll - PDPitch - PDYaw
    Throttle2 = PDz + PDRoll + PDPitch + PDYaw
    Throttle3 = PDz - PDRoll + PDPitch - PDYaw
    Throttle4 = PDz - PDRoll - PDPitch + PDYaw

    with utlis.XPlaneConnect() as client:
        # Structuring Motor Data in the necessary format to be packed by Control_utlis and sent back to XPlane
        data = [\
                [25,Throttle1, Throttle2, Throttle3, Throttle4, -998, -998, -998, -998],\
                [8, -998,  -998, -998,  -998, -998, -998, -998, -998]
               ]
        client.sendDATA(data)

if __name__ == '__main__':
  print("Executing controller")
  main()
