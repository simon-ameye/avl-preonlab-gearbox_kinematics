"""
Script written by Simon Ameye, AVL France, for RENAULT
This will set transform groups rotation speed to help setting of gearbox kinematics
Just drag and drop to your PreonLab window!
Please contact simon.ameye@avl.com for help
For PreonLab V4.3.0

---MANUAL---
IN PreonLab:
0) Create a PreonLab scene, import geometries.
Create as much transform groups as you have "lines"
Lines are “transform groups” that are aligned with shafts.
Ex, in 2 shafts manual gearboxes, create 2 transform groups aligned (co axial) with shafts.
Give nice names to lines and gears to make following steps easier

IN THIS SCRIPT: 
1) Enter gear names
It will only be used to define gear contacts.
No need to set name according to PreonLab objects or geometry.
Just give arbitrary names, but remind it to be able to define gear contacts
ex: gears_names = ["l1_g1", "l2_g1", "l2_g2", "l2_g3", "l5_g1", "l6_g1", "l4_g1", "l3_g1"]
2) Set gears number of teeth.
Of course, it has to be the same order as gear names.
ex: nb_of_teeth = [15, 55, 12, 88, 24, 32, 12, 12]
3) Set lines names.
The line is the name given in PreonLab to the TransformGroup that will be used to set gear rotation.
Transform group name from PreonLab has to be set here.
In most gearboxes, some gears are in the same kinematic sub-system.
It means that they are fixed between each other.
Thus, they share the same line.
ex: lines = ["l1", "l2", "l2", "l2", "l5", "l6", "l4", "l3"]
Here, 3 gears share the same "l2" transform group
4) Set gear contacts
Set the couples of gears that are engaged with each other.
ex: 
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
ex: 
input_gear = "l1_g1"
input_rotation_speeds = [200, 500] #RPS
input_rotation_timings = [0, 2] #s
rotation_direction = [0, 0, 1]

IN PREONLAB: 
6) Drag and drop this file in PL.
Your lines transform groups will be keyframed so that rotation speed is defined!
You can use it to transform your gears in the connection tab.
"""

#gearbox data
gears_names = ["diff", "intermsmall", "intermbig", "input"] #[-] names of the grars
nb_of_teeth = [70, 18, 55, 20] #[-] nb of teeth
lines = ["TransformGroup_diff", "TransformGroup_interm", "TransformGroup_interm", "TransformGroup_input"] #[-] lines names
gears_contacts = [
    ["diff", "intermsmall"],
    ["intermbig", "input"]] #[-] gears names in contact

input_gear = "input" #[-] name of the input gear
input_rotation_speeds = [0, -100, -100, 300] #[RPS]
input_rotation_timings = [0, 1, 2, 3] #[s]
rotation_direction = [1, 0, 0] #[-]

#code
import preonpy
#s = preonpy.Scene('C:/Users/u22p37/Downloads/gears.prscene')
s = preonpy.current_scene

#reset keyframes
for gear_name in gears_names:
    gear_index = gears_names.index(gear_name)
    tg = s.find_object(lines[gear_index])
    tg['orientation control mode'] = 'revolutions_PerSecond'
    tg['revolution axis'] = rotation_direction
    tg.set_keyframes("revolutions per second", [])
    

nb_gears = len(nb_of_teeth)

for input_rotation_timing in input_rotation_timings:
    input_rotation_speed = input_rotation_speeds[input_rotation_timings.index(input_rotation_timing)]
    rotation_speeds = [0] * nb_gears
    rotation_speeds_is_defined = [False] * nb_gears
    rotation_speeds[gears_names.index(input_gear)] = input_rotation_speed
    rotation_speeds_is_defined[gears_names.index(input_gear)] = True

    while False in rotation_speeds_is_defined:
        #set rotation speed accorsing to teeth ratio
        for gear_name in gears_names:
            gear_index = gears_names.index(gear_name)
            if not(rotation_speeds_is_defined[gear_index]):
                for gears_contact in gears_contacts:
                    if gear_name in gears_contact:
                        gear_neighbor = gears_contact[gears_contact.index(gear_name)-1]
                        gear_neighbor_index = gears_names.index(gears_contact[gears_contact.index(gear_name)-1])
                        if rotation_speeds_is_defined[gear_neighbor_index]:
                            rotation_speeds_is_defined[gear_index] = True
                            rotation_speeds[gear_index] = -rotation_speeds[gear_neighbor_index] * nb_of_teeth[gear_neighbor_index] / nb_of_teeth[gear_index]
            
        #set rotation speed according to lines sub systems
        for gear_name in gears_names:
            gear_index = gears_names.index(gear_name)
            if rotation_speeds_is_defined[gear_index]:
                for gear_2_name in gears_names:
                    gear_2_index = gears_names.index(gear_2_name)
                    if not(rotation_speeds_is_defined[gear_2_index]):
                        if lines[gear_index] == lines[gear_2_index]:
                            rotation_speeds_is_defined[gear_2_index] = True
                            rotation_speeds[gear_2_index] = rotation_speeds[gear_index]

    lines_names = []
    for gear_name in gears_names:
        gear_index = gears_names.index(gear_name)
        if not(lines[gear_index] in lines_names):
            lines_names.append(lines[gear_index])
            tg = s.find_object(lines[gear_index])
            key = [(input_rotation_timing, rotation_speeds[gear_index], "Linear")]
            temp_key = tg.get_keyframes("revolutions per second")
            tg.set_keyframes("revolutions per second", temp_key + key)
            print(lines[gear_index] + " line set to " + str(rotation_speeds[gear_index]) + " RPS at t = " + str(input_rotation_timing) + "s")

print("Done!")
