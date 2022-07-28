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
OBJ_PROP_FP_MIN_DIST = "mega_mini_fp_min_dist"
OBJ_PROP_FP_MIN_SCALE = "mega_mini_fp_min_scale"
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
PLACE_BONETAIL = (0, 4, 0)

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

# check if 'ob' is a MegaMini Rig and return False if 'ob' is not a MegaMini Rig, otherwise return True
def is_mega_mini_rig(ob):
    if ob is None or not hasattr(ob, 'type') or ob.type != 'ARMATURE' or \
            ob.data.bones.get(PROXY_OBSERVER_BNAME) is None or ob.data.bones.get(PROXY_FIELD_BNAME) is None:
        return False
    return True

# if a MegaMini Rig is found in the parent-hierarchy of ob, then return the rig and the associated 'Place' bone,
# otherwise return None
def get_parent_mega_mini_rig(ob):
    if ob.parent is None:
        return None, None
    if is_mega_mini_rig(ob.parent):
        # return MegaMiniRig, MegaMiniRigPlaceBoneName
        return ob.parent, ob.parent_bone
    # recursively search parent(s) for MegaMini Rig
    return get_parent_mega_mini_rig(ob.parent)

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
def create_mega_mini_armature(context, mega_mini_scale, mega_mini_fp_power, mega_mini_fp_min_dist,
                              mega_mini_fp_min_scale):
    widget_objs = create_mege_mini_widgets(context)

    old_3dview_mode = context.mode

    # create MegaMini mega_mini_rig and enter EDIT mode
    bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
    mega_mini_rig = context.active_object
    # the mega_mini_rig represents the "actual space", the ProxyField bone represents the "scaled space"
    mega_mini_rig.name = RIG_BASENAME
    mega_mini_rig[OBJ_PROP_SCALE] = mega_mini_scale
    mega_mini_rig[OBJ_PROP_FP_POWER] = mega_mini_fp_power
    mega_mini_rig[OBJ_PROP_FP_MIN_DIST] = mega_mini_fp_min_dist
    mega_mini_rig[OBJ_PROP_FP_MIN_SCALE] = mega_mini_fp_min_scale
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

    # move mega-mini rig to cursor location
    if bpy.app.version < (2,80,0):
        mega_mini_rig.location = context.scene.cursor_location
    else:
        mega_mini_rig.location = context.scene.cursor.location

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
        mega_mini_fp_min_dist = context.scene.MegaMini_NewObserverFP_MinDist
        mega_mini_fp_min_scale = context.scene.MegaMini_NewObserverFP_MinScale
        if mega_mini_scale <= 0:
            self.report({'ERROR'}, "Error in new Observer scale. Must be greater than zero.")
            return {'CANCELLED'}
        create_mega_mini_armature(context, mega_mini_scale, mega_mini_fp_power, mega_mini_fp_min_dist,
                                  mega_mini_fp_min_scale)
        return {'FINISHED'}
