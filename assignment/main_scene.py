""" Week 03, functions in a scene"""
import maya.cmds as cmds
import math
import scene_functions as sf

# ---------------------------------------------------------------------------
# Scene Setup
# ---------------------------------------------------------------------------
cmds.file(new=True, force=True)
# ---------------------------------------------------------------------------
"""Creating a function to add color to objects within another function"""
def apply_color(nodes, r,g,b, shader_name = "colorShader"):
    """Apply Lambert shader to apply a color to an object using rgb values """
    shader = cmds.shadingNode("lambert", asShader=True, name = shader_name)
    cmds.setAttr(shader + ".color", r, g, b, type="double3")
    cmds.select(nodes)
    cmds.hyperShade(assign=shader)
    return shader[0]

"""function to create a ground plane with the color green"""
def create_ground(width, depth):
    ground = cmds.polyPlane(name="ground", width=width, height=depth, subdivisionsX=1, subdivisionsY=1)
    shader = apply_color(ground, 0.35, 0.45, 0.3, shader_name="groundShader")
    return ground[0]

"""Function that creates a full tree, a canopy on top of a trunk"""
def create_tree(x, z, trunk_height=3, trunk_radius=0.4, canopy_radius=2):
    # making a trunk to the tree
    trunk = cmds.polyCylinder(name="trunk_01", radius=trunk_radius, height=trunk_height)[0]
    cmds.move(x, trunk_height / 2, z, trunk)
    # adding a canopy for the tree
    canopy = cmds.polySphere(name="canopy_01", radius=canopy_radius)[0]
    canopy_y = trunk_height + canopy_radius * 0.6
    cmds.move(x, canopy_y, z, canopy)

    # adding green and brown to the trees to color
    shader = apply_color(trunk, 0.15, 0.1, 0.02, shader_name="trunkShader")
    shader = apply_color(canopy, 0.18, 0.23, 0.06, shader_name="canopyShader")

    return trunk, canopy [0]

"""Creating a function that puts an object in a circle"""
def place_in_circle(create_func, count, radius, center_x=0, center_z=0):
    """Call create_func repeatedly, placing results in a circle."""
    results = []
    for i in range(count):
        angle = (2 * math.pi / count) * i
        x = center_x + math.cos(angle) * radius
        z = center_z + math.sin(angle) * radius
        result = create_func(x, z)
        results.append(result)
    return results[0]

"""Function to create a gray road"""
def create_road(x, z, road_width, road_depth):
    road = cmds.polyPlane(name="road_01", width=road_width, height=road_depth, subdivisionsX=1, subdivisionsY=1)
    cmds.move(x, 0.01 , z, road)

    shader = apply_color(road, .04, .04, .04, shader_name="roadShader")
    return road[0]
"""Creating a lamppost with a glowing lamp"""
def create_lamppost(x, z, height=3.0):
    #creation of the pole
    pole = cmds.polyCylinder(name = "pole", radius=0.1, height=height)[0]
    apply_color(pole, 0.06, 0.06, 0.05, shader_name="poleShader")
    cmds.move(x, height / 2.0, z, pole)

    #creating the lamp
    lamp = cmds.polySphere(name = "lamp", radius=0.25)[0]
    apply_color(lamp, 1, 0.95, 0.6, shader_name="lampShader")
    cmds.move(x, height + 0.25, z, lamp)
    return pole, lamp [0]

"""All the call commands"""
create_ground(width=60, depth=60)
create_tree (10, 14)
create_tree (-26, 14)
create_tree (10, -25)
place_in_circle(create_tree, 10, 12, -4 ,-4)
create_road(17, 0, 5, 60)
create_road(0, 20, 60, 5)
place_in_circle(create_lamppost, 9, 9, -4 ,-4)
create_lamppost(21,16)
create_lamppost(21,23)
create_lamppost(14,23)
create_lamppost(14,16)
# ---------------------------------------------------------------------------
# Final viewport framing (do not remove).
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cmds.viewFit(allObjects=True)
    print("Main scene built successfully!")
