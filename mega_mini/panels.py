# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import mathutils

import math

if bpy.app.version < (2,80,0):
    from .imp_v27 import create_mesh_obj_from_pydata
else:
    from .imp_v28 import create_mesh_obj_from_pydata

RIG_BASENAME = "MegaMini"
PROXY_FIELD_BNAME = "ProxyField"
PROXY_OBSERVER_BNAME = "ProxyObserver"
OBSERVER_BNAME = "Observer"
PROXY_PLACE_BNAME = "ProxyPlace"
PROXY_PLACE_FOCUS_BNAME = "ProxyPlaceFocus"
PLACE_BNAME = "Place"

OBJ_PROP_SCALE = "mega_mini_scale"
OBJ_PROP_FP_POWER = "mega_mini_fp_power"
OBJ_PROP_BONE_SCL_MULT = "mega_mini_bone_scl_mult"

PROXY_FIELD_BONEHEAD = (0, 0, 0)
PROXY_FIELD_BONETAIL = (0, 6.854101911, 0)
PROXY_OBSERVER_BONEHEAD = (0, 0, 0)
PROXY_OBSERVER_BONETAIL = (0, 0.034441854, 0)
OBSERVER_BONEHEAD = (0, 0, 0)
OBSERVER_BONETAIL = (0, 0.61803399, 0)
PROXY_PLACE_BONEHEAD = (0, 0, 0)
PROXY_PLACE_BONETAIL = (0, 0.090169945, 0)
PROXY_PLACE_FOCUS_BONEHEAD = (0, 0, 0)
PROXY_PLACE_FOCUS_BONETAIL = (0, 0.034441854, 0)
PLACE_BONEHEAD = (0, 0, 0)
PLACE_BONETAIL = (0, 4.236067952, 0)

PROXY_FIELD_BONELAYERS = [(x==0) for x in range(32)]
PROXY_OBSERVER_BONELAYERS = [(x==1) for x in range(32)]
PROXY_PLACE_BONELAYERS = [(x==2) for x in range(32)]
PROXY_PLACE_FOCUS_BONELAYERS = PROXY_PLACE_BONELAYERS
OBSERVER_BONELAYERS = [(x==17) for x in range(32)]
PLACE_BONELAYERS = [(x==18) for x in range(32)]

RIG_BONEVIS_LAYERS = [(x in [0, 1, 2, 17, 18]) for x in range(32)]

WIDGET_TRIANGLE_OBJNAME = "WGT_Tri"
WIDGET_PINCH_TRIANGLE_OBJNAME = "WGT_PinchTri"
WIDGET_QUAD_OBJNAME = "WGT_Quad"
WIDGET_PINCH_QUAD_OBJNAME = "WGT_PinchQuad"
WIDGET_CIRCLE_OBJNAME = "WGT_Circle"
WIDGET_CARDIOD_OBJNAME = "WGT_Cardiod"

TRI_WIDGET_NAME = "WidgetTriangle"
TRI_PINCH_WIDGET_NAME = "WidgetPinchTriangle"
QUAD_WIDGET_NAME = "WidgetQuad"
PINCH_QUAD_WIDGET_NAME = "WidgetPinchQuad"
CIRCLE_WIDGET_NAME = "WidgetCircle"
CARDIOD_WIDGET_NAME = "WidgetCardiod"

WIDGET_CIRCLE_VERT_COUNT = 32
WIDGET_CARDIOD_VERT_COUNT = 32

MEGA_MINI_CUSTOM_NODE_GROUP_NAME = "MegaMiniGeoNodeGroup"

def get_collection_by_name(root_collection, collection_name):
    if root_collection.name == collection_name:
        return root_collection

    for c in root_collection.children:
        coll = get_collection_by_name(c, collection_name)
        if coll != None:
            return coll

def collection_hide_in_viewport(context, collection_name):
    for v_layer in context.scene.view_layers:
        coll = get_collection_by_name(v_layer.layer_collection, collection_name)
        if coll is None:
            continue
        coll.hide_viewport = True

def create_widget_triangle(collection_name=None):
    verts = [(math.sin(math.radians(deg)), math.cos(math.radians(deg)), 0) for deg in [0, 120, 240]]
    edges = [ ( x, (x+1)*(x+1!=len(verts)) ) for x in range(len(verts)) ]
    if collection_name is None:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_TRIANGLE_OBJNAME)
    else:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_TRIANGLE_OBJNAME,
                                           collection_name=collection_name)

def create_widget_pinch_triangle(collection_name=None):
    verts = [(r * math.sin(math.radians(deg)), r * math.cos(math.radians(deg)), 0) for (deg, r) in
             [(0, 1), (60, 0.35), (120, 1), (180, 0.35), (240, 1), (300, 0.35)]]
    edges = [ ( x, (x+1)*(x+1!=len(verts)) ) for x in range(len(verts)) ]
    if collection_name is None:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_PINCH_TRIANGLE_OBJNAME)
    else:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_PINCH_TRIANGLE_OBJNAME,
                                           collection_name=collection_name)

def create_widget_square(collection_name=None):
    verts = [(-0.5, -0.5, 0),
             (0.5, -0.5, 0),
             (0.5, 0.5, 0),
             (-0.5, 0.5, 0), ]
    edges = [ ( x, (x+1)*(x+1!=len(verts)) ) for x in range(len(verts)) ]
    if collection_name is None:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_QUAD_OBJNAME)
    else:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_QUAD_OBJNAME,
                                           collection_name=collection_name)

def create_widget_pinch_square(collection_name=None):
    verts = [(-0.5, -0.5, 0),
             (0.0, -0.4, 0),
             (0.5, -0.5, 0),
             (0.4, 0.0, 0),
             (0.5, 0.5, 0),
             (0.0, 0.4, 0),
             (-0.5, 0.5, 0),
             (-0.4, 0.0, 0),]
    edges = [ ( x, (x+1)*(x+1!=len(verts)) ) for x in range(len(verts)) ]
    if collection_name is None:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_PINCH_QUAD_OBJNAME)
    else:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_PINCH_QUAD_OBJNAME,
                                           collection_name=collection_name)

def create_widget_circle(collection_name=None):
    verts = [(math.sin(rads), math.cos(rads), 0) for rads in \
             [index/WIDGET_CIRCLE_VERT_COUNT*2*math.pi for index in range(WIDGET_CIRCLE_VERT_COUNT)]]
    edges = [ ( x, (x+1)*(x+1!=len(verts)) ) for x in range(len(verts)) ]
    if collection_name is None:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_CIRCLE_OBJNAME)
    else:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_CIRCLE_OBJNAME,
                                           collection_name=collection_name)

def create_widget_cardiod(collection_name=None):
    verts = [((1-math.cos(rads))*math.sin(rads), (1-math.cos(rads))*math.cos(rads), 0) for rads in \
             [index/WIDGET_CARDIOD_VERT_COUNT*2*math.pi for index in range(WIDGET_CARDIOD_VERT_COUNT)]]
    edges = [ ( x, (x+1)*(x+1!=len(verts)) ) for x in range(len(verts)) ]
    if collection_name is None:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_CARDIOD_OBJNAME)
    else:
        return create_mesh_obj_from_pydata(verts, edges=edges, obj_name=WIDGET_CARDIOD_OBJNAME,
                                           collection_name=collection_name)

def create_mege_mini_widgets(context):
    # if v2.7 or earlier
    if bpy.app.version < (2,80,0):
        tri_obj = create_widget_triangle()
        tri_pinch_obj = create_widget_pinch_triangle()
        quad_obj = create_widget_square()
        pinch_quad_obj = create_widget_pinch_square()
        circle_obj = create_widget_circle()
        cardiod_obj = create_widget_cardiod()

        # widgets are only in final layer
        tri_obj.layers[19] = True
        tri_pinch_obj.layers[19] = True
        quad_obj.layers[19] = True
        pinch_quad_obj.layers[19] = True
        circle_obj.layers[19] = True
        cardiod_obj.layers[19] = True
        for i in range(19):
            tri_obj.layers[i] = False
            tri_pinch_obj.layers[i] = False
            quad_obj.layers[i] = False
            pinch_quad_obj.layers[i] = False
            circle_obj.layers[i] = False
            cardiod_obj.layers[i] = False
    # else v2.8 or later
    else:
        new_collection = bpy.data.collections.new("MegaMiniHidden")
        new_collection.hide_render = True
        # link new collection to currently active collection
        context.view_layer.active_layer_collection.collection.children.link(new_collection)
        collection_hide_in_viewport(context, new_collection.name)

        # widgets are in MegaMiniHidden collection
        tri_obj = create_widget_triangle(collection_name=new_collection.name)
        tri_pinch_obj = create_widget_pinch_triangle(collection_name=new_collection.name)
        quad_obj = create_widget_square(collection_name=new_collection.name)
        pinch_quad_obj = create_widget_pinch_square(collection_name=new_collection.name)
        circle_obj = create_widget_circle(collection_name=new_collection.name)
        cardiod_obj = create_widget_cardiod(collection_name=new_collection.name)

    widget_ob_dict = { TRI_WIDGET_NAME : tri_obj,
                      TRI_PINCH_WIDGET_NAME : tri_pinch_obj,
                      QUAD_WIDGET_NAME : quad_obj,
                      PINCH_QUAD_WIDGET_NAME : pinch_quad_obj,
                      CIRCLE_WIDGET_NAME: circle_obj,
                      CARDIOD_WIDGET_NAME: cardiod_obj,
                     }
    return widget_ob_dict

def add_bconst_scl_influence_driver(mega_mini_rig, proxy_obs_bconst):
    drv_copy_loc = proxy_obs_bconst.driver_add('influence').driver

    v_mega_mini_scale = drv_copy_loc.variables.new()
    v_mega_mini_scale.type = 'SINGLE_PROP'
    v_mega_mini_scale.name                 = "mega_mini_scl"
    v_mega_mini_scale.targets[0].id        = mega_mini_rig
    v_mega_mini_scale.targets[0].data_path = "[\""+OBJ_PROP_SCALE+"\"]"

    drv_copy_loc.expression = "1 / " + v_mega_mini_scale.name

# Notes:
#     - 'Field' is the mega_mini_rig itself, 'ProxyField' is intended to be like a 'TV remote controller',
#       easy to pick up and move around in the scene, without modifying the positions of objects in the rig
#     - 'ProxyField' is a Scaled Remote Controller for an Actual World of objects
def create_mega_mini_armature(context, mega_mini_scale, mega_mini_fp_power):
    widget_objs = create_mege_mini_widgets(context)

    old_3dview_mode = context.mode

    # create MegaMini mega_mini_rig and enter EDIT mode
    bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
    mega_mini_rig = context.active_object
    # the mega_mini_rig represents the "actual space", the ProxyField bone represents the "scaled space"
    mega_mini_rig.name = RIG_BASENAME
    mega_mini_rig[OBJ_PROP_SCALE] = mega_mini_scale
    mega_mini_rig[OBJ_PROP_FP_POWER] = mega_mini_fp_power
    # ensure mega_mini_rig will display custom bone shapes
    mega_mini_rig.data.show_bone_custom_shapes = True
    # modify default bone to make ProxyField bone, to hold proxies for observer(s) and actual place(s)
    b_proxy_field = mega_mini_rig.data.edit_bones[0]
    b_proxy_field.head = mathutils.Vector(PROXY_FIELD_BONEHEAD)
    b_proxy_field.tail = mathutils.Vector(PROXY_FIELD_BONETAIL)
    b_proxy_field.name = PROXY_FIELD_BNAME
    proxy_field_bname = b_proxy_field.name
    b_proxy_field.show_wire = True
    b_proxy_field.layers = PROXY_FIELD_BONELAYERS

    b_proxy_observer = mega_mini_rig.data.edit_bones.new(name=PROXY_OBSERVER_BNAME)
    # save bone name for later use (in Pose bones mode, where the edit bones name may not be usable - will cause error)
    proxy_observer_bname = b_proxy_observer.name
    # set bone data
    b_proxy_observer.head = mathutils.Vector(PROXY_OBSERVER_BONEHEAD)
    b_proxy_observer.tail = mathutils.Vector(PROXY_OBSERVER_BONETAIL)
    b_proxy_observer.parent = b_proxy_field
    b_proxy_observer.show_wire = True
    b_proxy_observer.layers = PROXY_OBSERVER_BONELAYERS

    b_observer = mega_mini_rig.data.edit_bones.new(name=OBSERVER_BNAME)
    observer_bname = b_observer.name
    b_observer.head = mathutils.Vector(OBSERVER_BONEHEAD)
    b_observer.tail = mathutils.Vector(OBSERVER_BONETAIL)
    b_observer.show_wire = True
    b_observer.layers = OBSERVER_BONELAYERS

    # enter Pose mode to allow adding bone constraints
    bpy.ops.object.mode_set(mode='POSE')
    # apply custom bone shapes to Sun Target, Sensor, and Blinds (apply to Blinds by way of Diff Cube),
    mega_mini_rig.pose.bones[proxy_observer_bname].custom_shape = \
        bpy.data.objects[widget_objs[TRI_PINCH_WIDGET_NAME].name]
    mega_mini_rig.pose.bones[observer_bname].custom_shape = bpy.data.objects[widget_objs[TRI_WIDGET_NAME].name]
    mega_mini_rig.pose.bones[proxy_field_bname].custom_shape = bpy.data.objects[widget_objs[CIRCLE_WIDGET_NAME].name]
    # Add bone constraint 'Copy Location' to ProxyObserver, so ProxyObserver bone can be adjusted (fine-tuned) with
    # Observer bone, e.g. add 'Copy Location' bone constraint to Observer bone to copy scene Camera location,
    # so forced perspective always looks correct to Camera.
    proxy_obs_bconst = mega_mini_rig.pose.bones[proxy_observer_bname].constraints.new(type='COPY_LOCATION')
    proxy_obs_bconst.target = mega_mini_rig
    proxy_obs_bconst.subtarget = observer_bname
    proxy_obs_bconst.use_offset = True
    # change space types to LOCAL, to prevent problems if MegaMini rig is moved
    proxy_obs_bconst.target_space = 'LOCAL'
    proxy_obs_bconst.owner_space = 'LOCAL'
    # add a driver to scale the influence by the mega_mini_rig's mega_mini_scale value
    add_bconst_scl_influence_driver(mega_mini_rig, proxy_obs_bconst)

    bpy.ops.object.mode_set(mode=old_3dview_mode)

    # parent widgets to new MegaMini Rig, first widget is "main parent" widget to other widgets
    if len(widget_objs) > 0:
        main_parent = None
        for w in widget_objs.values():
            if main_parent is None:
                # parent first widget to rig
                main_parent = w
                main_parent.parent = mega_mini_rig
                continue
            # parent remaining widgets to first widget
            w.parent = main_parent

    mega_mini_rig.data.layers = RIG_BONEVIS_LAYERS

    return mega_mini_rig

class MEGAMINI_CreateMegaMiniRig(bpy.types.Operator):
    bl_description = "Create a MegaMini rig, for 'condensed space' - e.g. Solar system simulations, " + \
        "outer-space-to-Earth-surface zoom"
    bl_idname = "mega_mini.create_mega_mini_rig"
    bl_label = "Create MegaMini Rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mega_mini_scale = context.scene.MegaMini_NewObserverScale
        mega_mini_fp_power = context.scene.MegaMini_NewObserverFP_Power
        if mega_mini_scale <= 0:
            self.report({'ERROR'}, "Error in new Observer scale. Must be above zero.")
            return {'CANCELLED'}
        create_mega_mini_armature(context, mega_mini_scale, mega_mini_fp_power)
        return {'FINISHED'}

# "edit bones" must be created at origin (head at origin, ...), so that pose bone locations can be used by drivers
# to perform offsets, distance calculations, etc.
def create_proxy_bone_pair(context, mega_mini_rig, use_obs_loc, widget_objs):
    # save old view3d mode and enter Edit mode, to add bones to mega_mini_rig
    old_3dview_mode = context.mode

    bpy.ops.object.mode_set(mode='EDIT')

    b_place = mega_mini_rig.data.edit_bones.new(name=PLACE_BNAME)
    place_bname = b_place.name
    b_place.head = mathutils.Vector(PLACE_BONEHEAD)
    b_place.tail = mathutils.Vector(PLACE_BONETAIL)
    b_place.parent = mega_mini_rig.data.edit_bones[OBSERVER_BNAME]
    b_place.show_wire = True
    b_place.layers = PLACE_BONELAYERS

    b_proxy_place = mega_mini_rig.data.edit_bones.new(name=PROXY_PLACE_BNAME)
    proxy_place_bname = b_proxy_place.name
    b_proxy_place.head = mathutils.Vector(PROXY_PLACE_BONEHEAD)
    b_proxy_place.tail = mathutils.Vector(PROXY_PLACE_BONETAIL)
    b_proxy_place.parent = mega_mini_rig.data.edit_bones[PROXY_FIELD_BNAME]
    b_proxy_place.show_wire = True
    b_proxy_place.layers = PROXY_PLACE_BONELAYERS

    b_proxy_place_focus = mega_mini_rig.data.edit_bones.new(name=PROXY_PLACE_FOCUS_BNAME)
    proxy_place_focus_bname = b_proxy_place_focus.name
    b_proxy_place_focus.head = mathutils.Vector(PROXY_PLACE_FOCUS_BONEHEAD)
    b_proxy_place_focus.tail = mathutils.Vector(PROXY_PLACE_FOCUS_BONETAIL)
    b_proxy_place_focus.parent = b_proxy_place
    b_proxy_place_focus.show_wire = True
    b_proxy_place_focus.layers = PROXY_PLACE_FOCUS_BONELAYERS

    # switch to Pose mode to allow adding drivers, and to set pose bone location(s)
    bpy.ops.object.mode_set(mode='POSE')

    # custom bone shape, and show as Wireframe
    mega_mini_rig.pose.bones[place_bname].custom_shape = bpy.data.objects[widget_objs[QUAD_WIDGET_NAME].name]
    mega_mini_rig.pose.bones[proxy_place_bname].custom_shape = \
        bpy.data.objects[widget_objs[PINCH_QUAD_WIDGET_NAME].name]
    mega_mini_rig.pose.bones[proxy_place_focus_bname].custom_shape = \
        bpy.data.objects[widget_objs[CARDIOD_WIDGET_NAME].name]

    # add driver to actual bone to make it scale with scaled bone
    add_bone_scl_drivers(mega_mini_rig, place_bname, proxy_place_focus_bname, PROXY_OBSERVER_BNAME)
    add_bone_loc_drivers(mega_mini_rig, place_bname, proxy_place_bname, PROXY_OBSERVER_BNAME)
    add_bone_rot_drivers(mega_mini_rig, place_bname, proxy_place_bname)

    # if new scaled bone should use the scaled observer position, then do it
    if use_obs_loc:
        # get position of Scaled observer, with it's "Copy Location" constraint included, by using "matrix"
        mega_mini_rig.pose.bones[proxy_place_bname].location = (
            mega_mini_rig.pose.bones[PROXY_OBSERVER_BNAME].matrix[0][3],
            mega_mini_rig.pose.bones[PROXY_OBSERVER_BNAME].matrix[1][3],
            mega_mini_rig.pose.bones[PROXY_OBSERVER_BNAME].matrix[2][3])
        # insert keyframe, to prevent data loss, i.e. position erased, if user does menu Pose -> Clear Transform,
        # presses Ctrl-G to reset location, etc.
        mega_mini_rig.pose.bones[proxy_place_bname].keyframe_insert(data_path="location")

    mega_mini_rig.pose.bones[place_bname][OBJ_PROP_BONE_SCL_MULT] = 1.0

    # switch back to previous view3d mode
    bpy.ops.object.mode_set(mode=old_3dview_mode)

    return place_bname, proxy_place_bname

def add_bone_scl_drivers(armature, place_bname, proxy_place_focus_bname, proxy_observer_bname):
    drv_scale_x = armature.pose.bones[place_bname].driver_add("scale", 0).driver

    v_proxy_dist = drv_scale_x.variables.new()
    v_proxy_dist.type = 'LOC_DIFF'
    v_proxy_dist.name                 = "proxy_dist"
    v_proxy_dist.targets[0].id        = armature
    v_proxy_dist.targets[0].bone_target        = proxy_place_focus_bname
    v_proxy_dist.targets[0].transform_space = 'WORLD_SPACE'
    v_proxy_dist.targets[1].id        = armature
    v_proxy_dist.targets[1].bone_target        = proxy_observer_bname
    v_proxy_dist.targets[1].transform_space = 'WORLD_SPACE'

    v_mega_mini_scale = drv_scale_x.variables.new()
    v_mega_mini_scale.type = 'SINGLE_PROP'
    v_mega_mini_scale.name                 = "mega_mini_scl"
    v_mega_mini_scale.targets[0].id        = armature
    v_mega_mini_scale.targets[0].data_path = "[\""+OBJ_PROP_SCALE+"\"]"

    v_mega_mini_fp_power = drv_scale_x.variables.new()
    v_mega_mini_fp_power.type = 'SINGLE_PROP'
    v_mega_mini_fp_power.name                 = "mega_mini_fp_pow"
    v_mega_mini_fp_power.targets[0].id        = armature
    v_mega_mini_fp_power.targets[0].data_path = "[\""+OBJ_PROP_FP_POWER+"\"]"

    v_self_bone_scale = drv_scale_x.variables.new()
    v_self_bone_scale.type = 'SINGLE_PROP'
    v_self_bone_scale.name                 = "self_bone_scale"
    v_self_bone_scale.targets[0].id        = armature
    v_self_bone_scale.targets[0].data_path = "pose.bones[\""+place_bname+"\"][\""+OBJ_PROP_BONE_SCL_MULT+"\"]"

    # Actual's forced perspective scaling value equals
    #     1 over
    #         1 plus distance from ProxyObserver to ProxyPlaceFocus
    #             to the power of "forced perspective power" value (usually 0.5 - meaning: take square root)
    drv_scale_x.expression = v_self_bone_scale.name+" / ( (1 + "+v_mega_mini_scale.name+" * "+v_proxy_dist.name + \
        ") ** "+v_mega_mini_fp_power.name+")"

    # Y scale is copy of X scale value
    drv_scale_y = armature.pose.bones[place_bname].driver_add('scale', 1).driver
    v_scale_y = drv_scale_y.variables.new()
    v_scale_y.type = 'TRANSFORMS'
    v_scale_y.name                 = "self_scl_x"
    v_scale_y.targets[0].id        = armature
    v_scale_y.targets[0].bone_target        = place_bname
    v_scale_y.targets[0].transform_type = 'SCALE_X'
    v_scale_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_scale_y.targets[0].data_path = "scale.x"
    drv_scale_y.expression = v_scale_y.name
    # Z scale is copy of X scale value
    drv_scale_z = armature.pose.bones[place_bname].driver_add('scale', 2).driver
    v_scale_z = drv_scale_z.variables.new()
    v_scale_z.type = 'TRANSFORMS'
    v_scale_z.name                 = "self_scl_x"
    v_scale_z.targets[0].id        = armature
    v_scale_z.targets[0].bone_target        = place_bname
    v_scale_z.targets[0].transform_type = 'SCALE_X'
    v_scale_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_scale_z.targets[0].data_path = "scale.x"
    drv_scale_z.expression = v_scale_z.name

def add_bone_loc_drivers(armature, place_bname, proxy_place_bname, proxy_observer_bname):
    # X
    drv_loc_x = armature.pose.bones[place_bname].driver_add('location', 0).driver
    # proxy place X
    v_proxy_place_x = drv_loc_x.variables.new()
    v_proxy_place_x.type = 'TRANSFORMS'
    v_proxy_place_x.name                 = "proxy_place_x"
    v_proxy_place_x.targets[0].id        = armature
    v_proxy_place_x.targets[0].bone_target        = proxy_place_bname
    v_proxy_place_x.targets[0].transform_type = 'LOC_X'
    v_proxy_place_x.targets[0].transform_space = 'LOCAL_SPACE'
    v_proxy_place_x.targets[0].data_path = "location.x"
    # proxy observer X
    v_proxy_obs_x = drv_loc_x.variables.new()
    v_proxy_obs_x.type = 'TRANSFORMS'
    v_proxy_obs_x.name                 = "proxy_obs_x"
    v_proxy_obs_x.targets[0].id        = armature
    v_proxy_obs_x.targets[0].bone_target        = proxy_observer_bname
    v_proxy_obs_x.targets[0].transform_type = 'LOC_X'
    v_proxy_obs_x.targets[0].transform_space = 'LOCAL_SPACE'
    v_proxy_obs_x.targets[0].data_path = "location.x"
    # bone self scale X
    v_bone_scale_x = drv_loc_x.variables.new()
    v_bone_scale_x.type = 'TRANSFORMS'
    v_bone_scale_x.name                 = "place_x"
    v_bone_scale_x.targets[0].id        = armature
    v_bone_scale_x.targets[0].bone_target        = place_bname
    v_bone_scale_x.targets[0].transform_type = 'SCALE_X'
    v_bone_scale_x.targets[0].transform_space = 'LOCAL_SPACE'
    v_bone_scale_x.targets[0].data_path = "location.x"
    # rig scale
    v_mega_mini_scale_x = drv_loc_x.variables.new()
    v_mega_mini_scale_x.type = 'SINGLE_PROP'
    v_mega_mini_scale_x.name                 = "mega_mini_scl"
    v_mega_mini_scale_x.targets[0].id        = armature
    v_mega_mini_scale_x.targets[0].data_path = "[\""+OBJ_PROP_SCALE+"\"]"
    # driver X
    drv_loc_x.expression = "("+v_proxy_place_x.name+" - "+v_proxy_obs_x.name+") * "+v_mega_mini_scale_x.name+" * "+\
        v_bone_scale_x.name

    # Y
    drv_loc_y = armature.pose.bones[place_bname].driver_add('location', 1).driver
    # proxy place Y
    v_proxy_place_y = drv_loc_y.variables.new()
    v_proxy_place_y.type = 'TRANSFORMS'
    v_proxy_place_y.name                 = "proxy_place_y"
    v_proxy_place_y.targets[0].id        = armature
    v_proxy_place_y.targets[0].bone_target        = proxy_place_bname
    v_proxy_place_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_place_y.targets[0].transform_space = 'LOCAL_SPACE'
    v_proxy_place_y.targets[0].data_path = "location.y"
    # proxy observer Y
    v_proxy_obs_y = drv_loc_y.variables.new()
    v_proxy_obs_y.type = 'TRANSFORMS'
    v_proxy_obs_y.name                 = "proxy_obs_y"
    v_proxy_obs_y.targets[0].id        = armature
    v_proxy_obs_y.targets[0].bone_target        = proxy_observer_bname
    v_proxy_obs_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_obs_y.targets[0].transform_space = 'LOCAL_SPACE'
    v_proxy_obs_y.targets[0].data_path = "location.y"
    # bone self scale Y
    v_bone_scale_y = drv_loc_y.variables.new()
    v_bone_scale_y.type = 'TRANSFORMS'
    v_bone_scale_y.name                 = "place_y"
    v_bone_scale_y.targets[0].id        = armature
    v_bone_scale_y.targets[0].bone_target        = place_bname
    v_bone_scale_y.targets[0].transform_type = 'SCALE_Y'
    v_bone_scale_y.targets[0].transform_space = 'LOCAL_SPACE'
    v_bone_scale_y.targets[0].data_path = "location.y"
    # rig scale
    v_mega_mini_scale_y = drv_loc_y.variables.new()
    v_mega_mini_scale_y.type = 'SINGLE_PROP'
    v_mega_mini_scale_y.name                 = "mega_mini_scl"
    v_mega_mini_scale_y.targets[0].id        = armature
    v_mega_mini_scale_y.targets[0].data_path = "[\""+OBJ_PROP_SCALE+"\"]"
    # driver Y
    drv_loc_y.expression = "("+v_proxy_place_y.name+" - "+v_proxy_obs_y.name+") * "+v_mega_mini_scale_y.name+" * "+\
        v_bone_scale_y.name

    # Z
    drv_loc_z = armature.pose.bones[place_bname].driver_add('location', 2).driver
    # proxy place Z
    v_proxy_place_z = drv_loc_z.variables.new()
    v_proxy_place_z.type = 'TRANSFORMS'
    v_proxy_place_z.name                 = "proxy_place_z"
    v_proxy_place_z.targets[0].id        = armature
    v_proxy_place_z.targets[0].bone_target        = proxy_place_bname
    v_proxy_place_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_place_z.targets[0].transform_space = 'LOCAL_SPACE'
    v_proxy_place_z.targets[0].data_path = "location.z"
    # proxy observer Z
    v_proxy_obs_z = drv_loc_z.variables.new()
    v_proxy_obs_z.type = 'TRANSFORMS'
    v_proxy_obs_z.name                 = "proxy_obs_z"
    v_proxy_obs_z.targets[0].id        = armature
    v_proxy_obs_z.targets[0].bone_target        = proxy_observer_bname
    v_proxy_obs_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_obs_z.targets[0].transform_space = 'LOCAL_SPACE'
    v_proxy_obs_z.targets[0].data_path = "location.z"
    # bone self scale Z
    v_bone_scale_z = drv_loc_z.variables.new()
    v_bone_scale_z.type = 'TRANSFORMS'
    v_bone_scale_z.name                 = "place_z"
    v_bone_scale_z.targets[0].id        = armature
    v_bone_scale_z.targets[0].bone_target        = place_bname
    v_bone_scale_z.targets[0].transform_type = 'SCALE_Z'
    v_bone_scale_z.targets[0].transform_space = 'LOCAL_SPACE'
    v_bone_scale_z.targets[0].data_path = "location.z"
    # rig scale
    v_mega_mini_scale_z = drv_loc_z.variables.new()
    v_mega_mini_scale_z.type = 'SINGLE_PROP'
    v_mega_mini_scale_z.name                 = "mega_mini_scl"
    v_mega_mini_scale_z.targets[0].id        = armature
    v_mega_mini_scale_z.targets[0].data_path = "[\""+OBJ_PROP_SCALE+"\"]"
    # driver Z
    drv_loc_z.expression = "("+v_proxy_place_z.name+" - "+v_proxy_obs_z.name+") * "+v_mega_mini_scale_z.name+" * "+\
        v_bone_scale_z.name

def add_bone_rot_drivers(armature, place_bname, proxy_place_bname):
    # ensure pose bone uses Euler rotation, because Euler is only rotation mode available due to Drivers usage
    armature.pose.bones[place_bname].rotation_mode = 'XYZ'
    # X
    drv_rot_x = armature.pose.bones[place_bname].driver_add('rotation_euler', 0).driver
    v_rot_x = drv_rot_x.variables.new()
    v_rot_x.type = 'TRANSFORMS'
    v_rot_x.name                 = "proxy_rot_x"
    v_rot_x.targets[0].id        = armature
    v_rot_x.targets[0].bone_target        = proxy_place_bname
    v_rot_x.targets[0].transform_type = 'ROT_X'
    v_rot_x.targets[0].transform_space = 'LOCAL_SPACE'
    v_rot_x.targets[0].data_path = "rotation_euler.x"
    drv_rot_x.expression = v_rot_x.name
    # Y
    drv_rot_y = armature.pose.bones[place_bname].driver_add('rotation_euler', 1).driver
    v_rot_y = drv_rot_y.variables.new()
    v_rot_y.type = 'TRANSFORMS'
    v_rot_y.name                 = "proxy_rot_y"
    v_rot_y.targets[0].id        = armature
    v_rot_y.targets[0].bone_target        = proxy_place_bname
    v_rot_y.targets[0].transform_type = 'ROT_Y'
    v_rot_y.targets[0].transform_space = 'LOCAL_SPACE'
    v_rot_y.targets[0].data_path = "rotation_euler.y"
    drv_rot_y.expression = v_rot_y.name
    # Z
    drv_rot_z = armature.pose.bones[place_bname].driver_add('rotation_euler', 2).driver
    v_rot_z = drv_rot_z.variables.new()
    v_rot_z.type = 'TRANSFORMS'
    v_rot_z.name                 = "proxy_rot_z"
    v_rot_z.targets[0].id        = armature
    v_rot_z.targets[0].bone_target        = proxy_place_bname
    v_rot_z.targets[0].transform_type = 'ROT_Z'
    v_rot_z.targets[0].transform_space = 'LOCAL_SPACE'
    v_rot_z.targets[0].data_path = "rotation_euler.z"
    drv_rot_z.expression = v_rot_z.name

def get_widget_objs_from_rig(active_ob):
    widget_objs = {}
    for ob in bpy.data.objects:
        if ob.parent == active_ob or (ob.parent != None and ob.parent.parent == active_ob):
            if WIDGET_TRIANGLE_OBJNAME in ob.name:
                widget_objs[TRI_WIDGET_NAME] = ob
            elif WIDGET_PINCH_TRIANGLE_OBJNAME in ob.name:
                widget_objs[TRI_PINCH_WIDGET_NAME] = ob
            elif WIDGET_QUAD_OBJNAME in ob.name:
                widget_objs[QUAD_WIDGET_NAME] = ob
            elif WIDGET_PINCH_QUAD_OBJNAME in ob.name:
                widget_objs[PINCH_QUAD_WIDGET_NAME] = ob
            elif WIDGET_CIRCLE_OBJNAME in ob.name:
                widget_objs[CIRCLE_WIDGET_NAME] = ob
            elif WIDGET_CARDIOD_OBJNAME in ob.name:
                widget_objs[CARDIOD_WIDGET_NAME] = ob
    return widget_objs

# check if 'ob' is a MegaMini Rig and return False if 'ob' is not a MegaMini Rig, otherwise return True
def is_mega_mini_rig(ob):
    if ob is None or not hasattr(ob, 'type') or ob.type != 'ARMATURE' or \
            ob.data.bones.get(PROXY_OBSERVER_BNAME) is None or ob.data.bones.get(PROXY_FIELD_BNAME) is None:
        return False
    return True

class MEGAMINI_CreateRigProxyPair(bpy.types.Operator):
    bl_description = "Based on the current position of MegaMini rig's ProxyObserver, create an Place-ProxyPlace " + \
        "pair of bones.\nObjects parented to the Place of the pair will be scaled and moved as the ProxyObserver moves"
    bl_idname = "mega_mini.create_proxy_pair"
    bl_label = "Create Proxy"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_ob = context.active_object
        # error checks
        if not is_mega_mini_rig(active_ob):
            self.report({'ERROR'}, "Unable to Create Proxy Pair because Active Object is not a MegaMini Rig.")
            return {'CANCELLED'}
        # get widgets and create
        widget_objs = get_widget_objs_from_rig(active_ob)
        create_proxy_bone_pair(context, active_ob, True, widget_objs)
        return {'FINISHED'}

class MEGAMINI_AttachRigProxyPair(bpy.types.Operator):
    bl_description = "Attach all selected object(s) to MegaMini rig. Rig must be selected last, and all other\n" + \
        "objects will be parented to rig. Note: this uses current position of rig's ProxyObserver"
    bl_idname = "mega_mini.attach_proxy_pair"
    bl_label = "Attach to Rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_ob = context.active_object
        # error checks
        if not is_mega_mini_rig(active_ob):
            self.report({'ERROR'}, "Unable to attach object(s) because Active Object is not a MegaMini Rig.")
            return {'CANCELLED'}
        if len(context.selected_objects) < 1:
            self.report({'ERROR'}, "Unable to attach object(s) to MegaMini Rig because no object(s) selected")
            return {'CANCELLED'}
        widget_objs = get_widget_objs_from_rig(active_ob)
        # expand the rig by creating new bones in the rig
        place_bname, proxy_place_bname = create_proxy_bone_pair(context, active_ob, True, widget_objs)

        # debug: change current frame of animation, to force Blender to update the armature, drivers, etc. in the
        # dependency graph - which Blender isn't automatically doing, for some reason...
        # all of this is done avoid errors with locations of objects/bones when parenting objects to bones
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)

        # make the new Actual bone the active bone, to be used for parenting objects
        active_ob.data.bones.active = active_ob.data.bones[place_bname]
        # parent all the selected object(s) to the new Actual bone
        bpy.ops.object.parent_set(type='BONE')

        return {'FINISHED'}

def create_mega_mini_custom_geo_node_group(node_group_name):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=node_group_name, type='GeometryNodeTree')
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.inputs.new(type='NodeSocketVectorTranslation', name="Observer Loc")
    new_node_group.inputs.new(type='NodeSocketVector', name="ProxyObserver Loc")
    new_node_group.inputs.new(type='NodeSocketFloat', name="MegaMini Scale")
    new_node_group.inputs.new(type='NodeSocketFloat', name="MegaMini FP Power")
    new_node_group.inputs.new(type='NodeSocketVector', name="Place Scale")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    tree_nodes = new_node_group.nodes
    # delete all nodes before adding new nodes
    tree_nodes.clear()

    # material shader nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.name = "Math"
    node.location = (-1020.000, 40.000)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[0].default_value = 1.0
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.name = "Vector Math.002"
    node.location = (-1460.000, 120.000)
    node.operation = "SUBTRACT"
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.name = "Position"
    node.location = (-1680.000, 100.000)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.name = "Vector Math.001"
    node.location = (-300.000, 180.000)
    node.operation = "MULTIPLY"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.name = "Math.001"
    node.location = (-800.000, 20.000)
    node.operation = "POWER"
    node.use_clamp = False
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.name = "Vector Math.005"
    node.location = (-1720.000, -100.000)
    node.operation = "MULTIPLY"
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.name = "Math.002"
    node.location = (-600.000, 100.000)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[0].default_value = 1.0
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.name = "Vector Math"
    node.location = (-1220.000, 60.000)
    node.operation = "DISTANCE"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.name = "Vector Math.003"
    node.location = (-100.000, 20.000)
    node.operation = "DIVIDE"
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.name = "Group Input"
    node.location = (-1920.000, -220.000)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.name = "Vector Math.004"
    node.location = (120.000, -120.000)
    node.operation = "ADD"
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.name = "Vector Math.006"
    node.location = (297.448, -161.419)
    node.operation = "SUBTRACT"
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.name = "Set Position.001"
    node.location = (510.702, -273.721)
    new_nodes["Set Position.001"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.name = "Group Output"
    node.location = (708.626, -316.601)
    new_nodes["Group Output"] = node

    # links between nodes
    new_links = []
    tree_links = new_node_group.links
    link = tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Set Position.001"].inputs[0])
    new_links.append(link)
    link = tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Vector Math.003"].inputs[1])
    new_links.append(link)
    link = tree_links.new(new_nodes["Set Position.001"].outputs[0], new_nodes["Group Output"].inputs[0])
    new_links.append(link)
    link = tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.001"].inputs[1])
    new_links.append(link)
    link = tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Math.005"].inputs[1])
    new_links.append(link)
    link = tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.005"].inputs[0])
    new_links.append(link)
    link = tree_links.new(new_nodes["Vector Math.002"].outputs[1], new_nodes["Vector Math"].inputs[1])
    new_links.append(link)
    link = tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math"].inputs[1])
    new_links.append(link)
    link = tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    new_links.append(link)
    link = tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[1])
    new_links.append(link)
    link = tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Vector Math.001"].inputs[1])
    new_links.append(link)
    link = tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math"].inputs[0])
    new_links.append(link)
    link = tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    new_links.append(link)
    link = tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    new_links.append(link)
    link = tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    new_links.append(link)
    link = tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    new_links.append(link)
    link = tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Set Position.001"].inputs[2])
    new_links.append(link)
    link = tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.002"].inputs[1])
    new_links.append(link)
    link = tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.004"].inputs[1])
    new_links.append(link)
    link = tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.006"].inputs[0])
    new_links.append(link)
    link = tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.006"].inputs[1])
    new_links.append(link)

    return new_node_group

def add_mega_mini_to_geo_node_group(existing_group_name, clear_node_tree, mega_mini_rig, mega_mini_rig_bone):
    existing_node_group = bpy.data.node_groups.get(existing_group_name)
    tree_nodes = existing_node_group.nodes
    # if needed, delete old nodes (clear tree) before adding new nodes
    if clear_node_tree:
        tree_nodes.clear()

    new_nodes = {}

    node = tree_nodes.new(type="NodeGroupInput")
    node.name = "Group Input"
    node.location = (120.000, -140.000)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="FunctionNodeInputVector")
    node.name = "Vector"
    node.label = "Observer Loc"
    node.location = (120.000, -240.000)
    # add drivers to get bone location from MegaMini rig
    # Observer location X
    drv_obs_loc_x = node.driver_add('vector', 0).driver
    v_obs_loc_x = drv_obs_loc_x.variables.new()
    v_obs_loc_x.type = 'TRANSFORMS'
    v_obs_loc_x.name = "var"
    v_obs_loc_x.targets[0].id = mega_mini_rig
    v_obs_loc_x.targets[0].bone_target = OBSERVER_BNAME
    v_obs_loc_x.targets[0].transform_type = 'LOC_X'
    v_obs_loc_x.targets[0].transform_space = 'LOCAL_SPACE'
    v_obs_loc_x.targets[0].data_path = "location.x"
    drv_obs_loc_x.expression = v_obs_loc_x.name
    # Observer location Y
    drv_obs_loc_y = node.driver_add('vector', 1).driver
    v_obs_loc_y = drv_obs_loc_y.variables.new()
    v_obs_loc_y.type = 'TRANSFORMS'
    v_obs_loc_y.name = "var"
    v_obs_loc_y.targets[0].id = mega_mini_rig
    v_obs_loc_y.targets[0].bone_target = OBSERVER_BNAME
    v_obs_loc_y.targets[0].transform_type = 'LOC_Y'
    v_obs_loc_y.targets[0].transform_space = 'LOCAL_SPACE'
    v_obs_loc_y.targets[0].data_path = "location.y"
    drv_obs_loc_y.expression = v_obs_loc_y.name
    # Observer location Z
    drv_obs_loc_z = node.driver_add('vector', 2).driver
    v_obs_loc_z = drv_obs_loc_z.variables.new()
    v_obs_loc_z.type = 'TRANSFORMS'
    v_obs_loc_z.name = "var"
    v_obs_loc_z.targets[0].id = mega_mini_rig
    v_obs_loc_z.targets[0].bone_target = OBSERVER_BNAME
    v_obs_loc_z.targets[0].transform_type = 'LOC_Z'
    v_obs_loc_z.targets[0].transform_space = 'LOCAL_SPACE'
    v_obs_loc_z.targets[0].data_path = "location.z"
    drv_obs_loc_z.expression = v_obs_loc_z.name
    # finished adding drivers for Observer location
    new_nodes["Vector"] = node

    node = tree_nodes.new(type="FunctionNodeInputVector")
    node.name = "Vector.002"
    node.label = "ProxyObserver Loc"
    node.location = (120.000, -380.000)

    # add drivers to get bone location from MegaMini rig
    # Proxy Observer location X
    drv_proxy_obs_loc_x = node.driver_add('vector', 0).driver
    v_proxy_obs_loc_x = drv_proxy_obs_loc_x.variables.new()
    v_proxy_obs_loc_x.type = 'TRANSFORMS'
    v_proxy_obs_loc_x.name = "var"
    v_proxy_obs_loc_x.targets[0].id = mega_mini_rig
    v_proxy_obs_loc_x.targets[0].bone_target = PROXY_OBSERVER_BNAME
    v_proxy_obs_loc_x.targets[0].transform_type = 'LOC_X'
    v_proxy_obs_loc_x.targets[0].transform_space = 'LOCAL_SPACE'
    v_proxy_obs_loc_x.targets[0].data_path = "location.x"
    drv_proxy_obs_loc_x.expression = v_proxy_obs_loc_x.name
    # Observer location Y
    drv_proxy_obs_loc_y = node.driver_add('vector', 1).driver
    v_proxy_obs_loc_y = drv_proxy_obs_loc_y.variables.new()
    v_proxy_obs_loc_y.type = 'TRANSFORMS'
    v_proxy_obs_loc_y.name = "var"
    v_proxy_obs_loc_y.targets[0].id = mega_mini_rig
    v_proxy_obs_loc_y.targets[0].bone_target = PROXY_OBSERVER_BNAME
    v_proxy_obs_loc_y.targets[0].transform_type = 'LOC_Y'
    v_proxy_obs_loc_y.targets[0].transform_space = 'LOCAL_SPACE'
    v_proxy_obs_loc_y.targets[0].data_path = "location.y"
    drv_proxy_obs_loc_y.expression = v_proxy_obs_loc_y.name
    # Observer location Z
    drv_proxy_obs_loc_z = node.driver_add('vector', 2).driver
    v_proxy_obs_loc_z = drv_proxy_obs_loc_z.variables.new()
    v_proxy_obs_loc_z.type = 'TRANSFORMS'
    v_proxy_obs_loc_z.name = "var"
    v_proxy_obs_loc_z.targets[0].id = mega_mini_rig
    v_proxy_obs_loc_z.targets[0].bone_target = PROXY_OBSERVER_BNAME
    v_proxy_obs_loc_z.targets[0].transform_type = 'LOC_Z'
    v_proxy_obs_loc_z.targets[0].transform_space = 'LOCAL_SPACE'
    v_proxy_obs_loc_z.targets[0].data_path = "location.z"
    drv_proxy_obs_loc_z.expression = v_proxy_obs_loc_z.name
    # finished adding drivers for Proxy Observer location
    new_nodes["Vector.002"] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.name = "Value.001"
    node.label = "MegaMini Scale"
    node.location = (120.000, -520.000)
    node.outputs[0].default_value = 1000.0
    # add driver to get MegaMini Scale
    drv_mm_scale = node.outputs[0].driver_add('default_value').driver
    v_mm_scale = drv_mm_scale.variables.new()
    v_mm_scale.type = 'SINGLE_PROP'
    v_mm_scale.name                 = "var"
    v_mm_scale.targets[0].id        = mega_mini_rig
    v_mm_scale.targets[0].data_path = "[\""+OBJ_PROP_SCALE+"\"]"
    drv_mm_scale.expression = v_mm_scale.name
    # finish
    new_nodes["Value.001"] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.name = "Value"
    node.label = "MegaMini FP Power"
    node.location = (120.000, -620.000)
    node.outputs[0].default_value = 0.5
    # add driver to get MegaMini Scale
    drv_mm_fp_power = node.outputs[0].driver_add('default_value').driver
    v_mm_fp_power = drv_mm_fp_power.variables.new()
    v_mm_fp_power.type = 'SINGLE_PROP'
    v_mm_fp_power.name                 = "var"
    v_mm_fp_power.targets[0].id        = mega_mini_rig
    v_mm_fp_power.targets[0].data_path = "[\""+OBJ_PROP_FP_POWER+"\"]"
    drv_mm_fp_power.expression = v_mm_fp_power.name
    # finish
    new_nodes["Value"] = node

    node = tree_nodes.new(type="FunctionNodeInputVector")
    node.name = "Vector.001"
    node.label = "Place Scale"
    node.location = (120.000, -720.000)
    node.vector = (1, 1, 1) # default value of XYZ scale is (1, 1, 1)
    # add drivers to get bone location from MegaMini rig
    # Place scale X
    drv_place_scale_x = node.driver_add('vector', 0).driver
    v_place_scale_x = drv_place_scale_x.variables.new()
    v_place_scale_x.type = 'TRANSFORMS'
    v_place_scale_x.name = "var"
    v_place_scale_x.targets[0].id = mega_mini_rig
    v_place_scale_x.targets[0].bone_target = PLACE_BNAME
    v_place_scale_x.targets[0].transform_type = 'SCALE_X'
    v_place_scale_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_place_scale_x.targets[0].data_path = "scale.x"
    drv_place_scale_x.expression = v_place_scale_x.name
    # Place scale Y
    drv_place_scale_y = node.driver_add('vector', 1).driver
    v_place_scale_y = drv_place_scale_y.variables.new()
    v_place_scale_y.type = 'TRANSFORMS'
    v_place_scale_y.name = "var"
    v_place_scale_y.targets[0].id = mega_mini_rig
    v_place_scale_y.targets[0].bone_target = PLACE_BNAME
    v_place_scale_y.targets[0].transform_type = 'SCALE_Y'
    v_place_scale_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_place_scale_y.targets[0].data_path = "scale.y"
    drv_place_scale_y.expression = v_place_scale_y.name
    # Place scale Z
    drv_place_scale_z = node.driver_add('vector', 2).driver
    v_place_scale_z = drv_place_scale_z.variables.new()
    v_place_scale_z.type = 'TRANSFORMS'
    v_place_scale_z.name = "var"
    v_place_scale_z.targets[0].id = mega_mini_rig
    v_place_scale_z.targets[0].bone_target = PLACE_BNAME
    v_place_scale_z.targets[0].transform_type = 'SCALE_Z'
    v_place_scale_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_place_scale_z.targets[0].data_path = "scale.z"
    drv_place_scale_z.expression = v_place_scale_z.name
    # finished adding drivers for Place location
    new_nodes["Vector.001"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.name = "Group Output"
    node.location = (600.000, -280.000)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.name = "MegaMiniGeoNodeGroup"
    node.label = "MegaMini Geo"
    node.node_tree = bpy.data.node_groups.get(MEGA_MINI_CUSTOM_NODE_GROUP_NAME)
    node.location = (401.944, -255.587)
    new_nodes["Group"] = node

    # links between nodes
    new_links = []
    tree_links = existing_node_group.links
    link = tree_links.new(new_nodes["Vector"].outputs[0], new_nodes["Group"].inputs[1])
    new_links.append(link)
    link = tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group"].inputs[0])
    new_links.append(link)
    link = tree_links.new(new_nodes["Vector.001"].outputs[0], new_nodes["Group"].inputs[5])
    new_links.append(link)
    link = tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Group Output"].inputs[0])
    new_links.append(link)
    link = tree_links.new(new_nodes["Value"].outputs[0], new_nodes["Group"].inputs[4])
    new_links.append(link)
    link = tree_links.new(new_nodes["Value.001"].outputs[0], new_nodes["Group"].inputs[3])
    new_links.append(link)
    link = tree_links.new(new_nodes["Vector.002"].outputs[0], new_nodes["Group"].inputs[2])
    new_links.append(link)

def add_mega_mini_nodes_to_node_group(existing_group_name, override_create, clear_node_tree, mega_mini_rig,
                                      mega_mini_rig_bone):
    # check if custom node group already exists, and create/override if necessary
    node_group = bpy.data.node_groups.get(MEGA_MINI_CUSTOM_NODE_GROUP_NAME)
    if node_group is None or override_create:
        # create the custom node group
        new_node_group = create_mega_mini_custom_geo_node_group(MEGA_MINI_CUSTOM_NODE_GROUP_NAME)
        # if override create is enabled, then ensure new group name will be "first", meaning:
        #     group name does not have suffix like '.001', '.002', etc.
        if override_create:
            new_node_group.name = MEGA_MINI_CUSTOM_NODE_GROUP_NAME

    add_mega_mini_to_geo_node_group(existing_group_name, clear_node_tree, mega_mini_rig, mega_mini_rig_bone)

def add_mega_mini_geo_nodes_to_object(ob, override_create, alt_group_name, mega_mini_rig, mega_mini_rig_bone):
    geo_nodes_mod = ob.modifiers.new(name="MegaMini.GeometryNodes", type='NODES')
    # use alternate group, if needed and if available
    if alt_group_name != None:
        if bpy.data.node_groups.get(alt_group_name) is None:
            return  # TODO return error / throw exception
        # create nodes, but don't clear node tree before creating new nodes
        add_mega_mini_nodes_to_node_group(alt_group_name, override_create, False, mega_mini_rig, mega_mini_rig_bone)
        geo_nodes_mod.node_group = bpy.data.node_groups.get(alt_group_name)
        return  # success, return
    # create nodes, and clear node tree before creating new nodes
    add_mega_mini_nodes_to_node_group(geo_nodes_mod.node_group.name, override_create, True, mega_mini_rig,
                                      mega_mini_rig_bone)

class MEGAMINI_AddGeoNodes(bpy.types.Operator):
    bl_description = "Add Geometry Nodes to selected object(s). Object(s) must already be attached to MegaMini Rig "+\
                     "for this to work"
    bl_idname = "mega_mini.add_geo_nodes"
    bl_label = "Add Geometry Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        for ob in context.selected_objects:
            # skip objects that are not parented to a MegaMini Rig
            if not is_mega_mini_rig(ob.parent) or ob.parent_bone == "":
                continue
            alt_group_name = None
            if scn.MegaMini_GeoNodesCreateUseAltGroup:
                if scn.MegaMini_GeoNodesCreateAltGroup is None:
                    self.report({'ERROR'}, "Unable to create geometry nodes because Alternate Group not found.")
                    return {'CANCELLED'}
                alt_group_name = scn.MegaMini_GeoNodesCreateAltGroup.name
            add_mega_mini_geo_nodes_to_object(ob, scn.MegaMini_GeoNodesOverrideCreate, alt_group_name, ob.parent,
                                              ob.parent_bone)
        return {'FINISHED'}
