# gearbox-kinematics

Script written by Simon Ameye, AVL France, for RENAULT
This will set transform groups rotation speed to help setting of gearbox kinematics
Just drag and drop to your PreonLab window !
Please contact simon.ameye@avl.com for help
For PreonLab V4.3.0

#1) Enter gear names
It will only be used to define gear contacts.
No need to set name according to PreonLab objects or geometry.
Just give arbitrary names, but remind it to be able to define gear contacts
ex : gears_names = ["l1_g1", "l2_g1", "l2_g2", "l2_g3", "l5_g1", "l6_g1", "l4_g1", "l3_g1"]

2) Set gears number of teeth.
Of course, it has to be the same order as gear names.
ex : nb_of_teeth = [15, 55, 12, 88, 24, 32, 12, 12]

3) Set lines names.
The line is the name given in PreonLab to the TransformGroup that will be used to set gear rotation.
Transform group name from PreonLab has to be set here.
In most gearboxes, some gears are in the same kinematic sub-system.
It means that they are fixed between each other.
Thus, they share the same line.
ex : lines = ["l1", "l2", "l2", "l2", "l5", "l6", "l4", "l3"]
Here, 3 gears share the same "l2" transform group

4) Set gear contacts
Set the couples of gears that are engaged with each other.
ex : 
gears_contacts = [
    ["l1_g1", "l2_g1"],
    ["l3_g1", "l2_g2"],
    ["l2_g3", "l4_g1"],
    ["l2_g2", "l5_g1"],
    ["l2_g3", "l6_g1"]]

5) Set input gear + data
This is the gear that is used to set rotation speed
Also set its rotation speed and the associated timing.
Set rotation direction.
ex : 
input_gear = "l1_g1"
input_rotation_speeds = [200, 500] #RPS
input_rotation_timings = [0, 2] #s
rotation_direction = [0, 0, 1]

6) Drag and drop this file in PL.
Your lines transform groups will be keyframed so that rotation speed id defined !
You can use it to transform your gears in the connection tab.
