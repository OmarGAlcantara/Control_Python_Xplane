# Control_Python_Xplane
This repo is a sample script that interfaces with the XPlane Flight simulator to program in "in the Loop" Controllers using Python


Follow the next configuration to be able to interface with the XPlane Flight Sim
1. Install XPlane 11
2. -Download from the git files inside the XPC plugin folder the "XPlaneCOnnect" folder and paste it in the XPlane plugins instalation route
      for example: /home/omarg/.local/share/Steam/steamapps/common/X-Plane 11/Resources/plugins
   -Download the "My custom Aircraft" folder and paste it in the /home/omarg/.local/share/Steam/steamapps/common/X-Plane 11/Aircraft folder
   -Download the "Airfoils" folder and paste it in the /home/omarg/.local/share/Steam/steamapps/common/X-Plane 11/, replacing the current folder 
4. Verify the plugin is working by opening an XPlane Simulation and click on the plugins tab. Make sure XPlaneConnect is there.
5. If so, open XPlane and chenge the following:

      -On the Settings / Network tab
            Port we receive on
            Port we receive on (legacy)
            Port we send from (legaU)
      -On the Settings / Data Output
            Increase "UDP Rate" to the maximum
            Select "Send network data output"
            IP Address: 127.0.0.1
            Port: 49005
      -Select the "Network Via UDP" case on the required aircraft states
            -...
To start a Simulation
      Select New Flight
      Select the Intel_AeroRTF_2 aircraft
      Start simulation
      Execute the Control.py file to start the simulation

XPlane quickkeys:
      Throttle increase: F2
      Switch aircraft views : Shift + 1,2,3...
      Restart sim without aircraft crashing: Click on the top right plane symbol + New Location + Start Flight
   

