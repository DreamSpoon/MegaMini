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

from .rig import (PROXY_FIELD_BNAME, OBSERVER_BNAME, PROXY_OBSERVER_BNAME, PLACE_BNAME, PROXY_PLACE_BNAME,
    PROXY_PLACE_FOCUS_BNAME, PLACE_BONEHEAD, PLACE_BONETAIL, PROXY_PLACE_BONEHEAD, PROXY_PLACE_BONETAIL,
    PROXY_PLACE_FOCUS_BONEHEAD, PROXY_PLACE_FOCUS_BONETAIL, PLACE_BONELAYERS, PROXY_PLACE_BONELAYERS,
    PROXY_PLACE_FOCUS_BONELAYERS)
from .rig import (TRI_WIDGET_NAME, TRI_PINCH_WIDGET_NAME, QUAD_WIDGET_NAME, PINCH_QUAD_WIDGET_NAME, CIRCLE_WIDGET_NAME,
    CARDIOD_WIDGET_NAME, WIDGET_TRIANGLE_OBJNAME, WIDGET_PINCH_TRIANGLE_OBJNAME, WIDGET_QUAD_OBJNAME,
    WIDGET_PINCH_QUAD_OBJNAME, WIDGET_CIRCLE_OBJNAME, WIDGET_CARDIOD_OBJNAME)
from .rig import (OBJ_PROP_BONE_SCL_MULT, OBJ_PROP_SCALE, OBJ_PROP_FP_POWER, OBJ_PROP_FP_MIN_DIST,
    OBJ_PROP_FP_MIN_SCALE, MEGA_MINI_CUSTOM_NODE_GROUP_NAME, create_mega_mini_armature, is_mega_mini_rig)

if bpy.app.version < (2,80,0):
    from .imp_v27 import (select_object, get_cursor_location)
else:
    from .imp_v28 import (select_object, get_cursor_location)

# "edit bones" must be created at origin (head at origin, ...), so that pose bone locations can be used by drivers
# to perform offsets, distance calculations, etc.
def create_proxy_bone_pair(context, mega_mini_rig, widget_objs, use_obs_loc, place_loc=None):
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

    # add driver to place bone to make it scale with scaled bone
    add_bone_scl_drivers(mega_mini_rig, place_bname, proxy_place_focus_bname, PROXY_OBSERVER_BNAME)
    add_bone_loc_drivers(mega_mini_rig, place_bname, proxy_place_bname, PROXY_OBSERVER_BNAME)
    add_bone_rot_drivers(mega_mini_rig, place_bname, proxy_place_bname)

    # if a place location is given then convert the location to Proxy coordinates
    if place_loc != None:
        mega_mini_rig.pose.bones[proxy_place_bname].location = (place_loc[0] / mega_mini_rig[OBJ_PROP_SCALE],
                                                                place_loc[1] / mega_mini_rig[OBJ_PROP_SCALE],
                                                                place_loc[2] / mega_mini_rig[OBJ_PROP_SCALE])
    # else if new proxy bone should use the proxy observer position, then do it
    elif use_obs_loc:
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

    v_mega_mini_fp_min_dist = drv_scale_x.variables.new()
    v_mega_mini_fp_min_dist.type = 'SINGLE_PROP'
    v_mega_mini_fp_min_dist.name                 = "mega_mini_fp_min_dist"
    v_mega_mini_fp_min_dist.targets[0].id        = armature
    v_mega_mini_fp_min_dist.targets[0].data_path = "[\""+OBJ_PROP_FP_MIN_DIST+"\"]"

    v_mega_mini_fp_min_scale = drv_scale_x.variables.new()
    v_mega_mini_fp_min_scale.type = 'SINGLE_PROP'
    v_mega_mini_fp_min_scale.name                 = "mega_mini_fp_min_scale"
    v_mega_mini_fp_min_scale.targets[0].id        = armature
    v_mega_mini_fp_min_scale.targets[0].data_path = "[\""+OBJ_PROP_FP_MIN_SCALE+"\"]"

    v_self_bone_scale = drv_scale_x.variables.new()
    v_self_bone_scale.type = 'SINGLE_PROP'
    v_self_bone_scale.name                 = "self_bone_scale"
    v_self_bone_scale.targets[0].id        = armature
    v_self_bone_scale.targets[0].data_path = "pose.bones[\""+place_bname+"\"][\""+OBJ_PROP_BONE_SCL_MULT+"\"]"

    # MegaMini distance scaling formula:
    drv_scale_x.expression = "max("+v_mega_mini_fp_min_scale.name+", "+v_self_bone_scale.name+" / ( (1 + max(0, " + \
        v_mega_mini_scale.name+" * "+v_proxy_dist.name+" - "+v_mega_mini_fp_min_dist.name+") ) ** " + \
        v_mega_mini_fp_power.name+") )"

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

class MEGAMINI_AttachCreatePlace(bpy.types.Operator):
    bl_description = "Based on current position of MegaMini rig's ProxyObserver, create Place-ProxyPlace " + \
        "pair. Objects parented to Place will be scaled and moved as ProxyObserver moves. Note: Observer " + \
        "location must be (0, 0, 0) for this to work correctly"
    bl_idname = "mega_mini.create_proxy_place"
    bl_label = "Create Place"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_ob = context.active_object
        # error checks
        if not is_mega_mini_rig(active_ob):
            # create a rig if needed
            if context.scene.MegaMini_AttachPreCreateRig:
                mega_mini_scale = context.scene.MegaMini_NewObserverScale
                mega_mini_fp_power = context.scene.MegaMini_NewObserverFP_Power
                mega_mini_fp_min_dist = context.scene.MegaMini_NewObserverFP_MinDist
                mega_mini_fp_min_scale = context.scene.MegaMini_NewObserverFP_MinScale
                if mega_mini_scale <= 0:
                    self.report({'ERROR'}, "Cannot PreCreate MegaMini Rig, error is Observer scale. Must be greater than zero.")
                    return {'CANCELLED'}
                create_mega_mini_armature(context, mega_mini_scale, mega_mini_fp_power, mega_mini_fp_min_dist,
                                          mega_mini_fp_min_scale)
                # new active object
                active_ob = context.active_object
            else:
                self.report({'ERROR'}, "Unable to Create Place because Active Object is not a MegaMini Rig.")
                return {'CANCELLED'}
        # get widgets and create
        widget_objs = get_widget_objs_from_rig(active_ob)
        create_proxy_bone_pair(context, active_ob, widget_objs, True)
        return {'FINISHED'}

class MEGAMINI_AttachSinglePlace(bpy.types.Operator):
    bl_description = "Attach all selected object(s) to MegaMini rig. Rig must be selected last, and all other\n" + \
        "objects will be parented to rig. Note: this uses current position of rig's ProxyObserver"
    bl_idname = "mega_mini.attach_single_place"
    bl_label = "Single Place"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_ob = context.active_object
        # get list of objects, a separate copy of context's list - because context's list may change
        selected_obs = [ob for ob in context.selected_objects]
        # error checks
        if not is_mega_mini_rig(active_ob):
            # create a rig if needed
            if context.scene.MegaMini_AttachPreCreateRig:
                mega_mini_scale = context.scene.MegaMini_NewObserverScale
                mega_mini_fp_power = context.scene.MegaMini_NewObserverFP_Power
                mega_mini_fp_min_dist = context.scene.MegaMini_NewObserverFP_MinDist
                mega_mini_fp_min_scale = context.scene.MegaMini_NewObserverFP_MinScale
                if mega_mini_scale <= 0:
                    self.report({'ERROR'}, "Cannot PreCreate MegaMini Rig, error is Observer scale. Must be greater than zero.")
                    return {'CANCELLED'}
                create_mega_mini_armature(context, mega_mini_scale, mega_mini_fp_power, mega_mini_fp_min_dist,
                                          mega_mini_fp_min_scale)
                # new active object
                active_ob = context.active_object
            else:
                self.report({'ERROR'}, "Unable to attach object(s) because Active Object is not a MegaMini Rig.")
                return {'CANCELLED'}
        if len(context.selected_objects) < 1:
            self.report({'ERROR'}, "Unable to attach object(s) to MegaMini Rig because no object(s) selected")
            return {'CANCELLED'}
        widget_objs = get_widget_objs_from_rig(active_ob)
        # expand the rig by creating new bones in the rig
        place_bname, proxy_place_bname = create_proxy_bone_pair(context, active_ob, widget_objs, True)

        # debug: change current frame of animation, to force Blender to update the armature, drivers, etc. in the
        # dependency graph - which Blender isn't automatically doing, for some reason...
        # all of this is done avoid errors with locations of objects/bones when parenting objects to bones
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)

        # select only the objects that were selected before the function was called, and the
        # MegaMini Rig (which may have been 'pre-created')
        bpy.ops.object.select_all(action='DESELECT')
        select_object(active_ob, True)
        for ob in selected_obs:
            # do not select objects that have a parent, if 'no re-parent' option is enabled
            if ob.parent != None and context.scene.MegaMini_AttachNoReParent:
                continue
            select_object(ob, True)

        # make the new Place bone the active bone, to be used for parenting objects
        active_ob.data.bones.active = active_ob.data.bones[place_bname]
        # parent all the selected object(s) to the new Place bone
        bpy.ops.object.parent_set(type='BONE')

        return {'FINISHED'}

class MEGAMINI_AttachMultiPlace(bpy.types.Operator):
    bl_description = "Attach selected objects to active MegaMini Rig, creating a separate Place for each attached " + \
        "object. Select Rig last. This uses current position of objects relative to MegaMini Rig, and zeroes " + \
        "those objects' locations (may not work with location-keyframed objects)"
    bl_idname = "mega_mini.attach_multi_place"
    bl_label = "Multi Place"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_ob = context.active_object
        # get list of objects, a separate copy of context's list - because context's list may change
        selected_obs = [ob for ob in context.selected_objects]
        # error checks
        if not is_mega_mini_rig(active_ob):
            # create a rig if needed
            if context.scene.MegaMini_AttachPreCreateRig:
                mega_mini_scale = context.scene.MegaMini_NewObserverScale
                mega_mini_fp_power = context.scene.MegaMini_NewObserverFP_Power
                mega_mini_fp_min_dist = context.scene.MegaMini_NewObserverFP_MinDist
                mega_mini_fp_min_scale = context.scene.MegaMini_NewObserverFP_MinScale
                if mega_mini_scale <= 0:
                    self.report({'ERROR'}, "Cannot PreCreate MegaMini Rig, error is Observer scale. Must be greater than zero.")
                    return {'CANCELLED'}
                create_mega_mini_armature(context, mega_mini_scale, mega_mini_fp_power, mega_mini_fp_min_dist,
                                          mega_mini_fp_min_scale)
                # new active object
                active_ob = context.active_object
            else:
                self.report({'ERROR'}, "Unable to attach object(s) because Active Object is not a MegaMini Rig.")
                return {'CANCELLED'}
        if len(context.selected_objects) < 1:
            self.report({'ERROR'}, "Unable to attach object(s) to MegaMini Rig because no object(s) selected")
            return {'CANCELLED'}
        widget_objs = get_widget_objs_from_rig(active_ob)

        # select only the objects that were selected before the function was called, and the
        # MegaMini Rig (which may have been 'pre-created')
        bpy.ops.object.select_all(action='DESELECT')
        select_object(active_ob, True)
        for ob in selected_obs:
            # skip the MegaMini Rig for this part (it's already been selected)
            if ob == active_ob:
                continue
            # do not select objects that have a parent, if 'no re-parent' option is enabled
            if ob.parent != None and context.scene.MegaMini_AttachNoReParent:
                continue
            select_object(ob, True)

            place_loc = ob.matrix_world.translation - get_cursor_location(context)
            # expand the rig by creating new bones in the rig
            place_bname, proxy_place_bname = create_proxy_bone_pair(context, active_ob, widget_objs, True, place_loc)

            # object's location was converted to MegaMini Proxy coordinates, so zero object's location values
            ob.location.zero()
            # parent the object to the new Place,
            ob.parent = active_ob
            ob.parent_type = 'BONE'
            ob.parent_bone = place_bname
            ob.matrix_parent_inverse.identity()
            # undo translation due to bone length
            ob.matrix_parent_inverse[1][3] = -PLACE_BONETAIL[1]

        # debug: change current frame of animation, to force Blender to update the armature, drivers, etc. in the
        # dependency graph - which Blender isn't automatically updating, for some reason...
        # all of this is done to avoid errors with locations of objects/bones when parenting objects to bones
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)
        return {'FINISHED'}
