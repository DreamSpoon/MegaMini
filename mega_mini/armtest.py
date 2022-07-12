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

OBJ_PROP_SCALE = "mega_mini_scale"

SCALED_WINDOW_BNAME = "ScaledWindow"
SCALED_OBSERVER_BNAME = "ScaledObserver"
ACTUAL_OBSERVER_BNAME = "ActualObserver"
TEMP_BONE_HEAD = (0, 0, 0)
TEMP_BONE_TAIL = (0, 0, 1)

PROXY_ACTUAL_BNAME = "ActualProxy"
PROXY_SCALED_BNAME = "ScaledProxy"
PROXY_SCALED_FOCUS_BNAME = "ScaledFocusProxy"

def add_bconst_scl_inf_driver(scaled_obs_bconst):
    drv_copy_loc = scaled_obs_bconst.driver_add('influence').driver
    drv_copy_loc.use_self = True
    drv_copy_loc.expression = "1 / self.id_data[\"mega_mini_scale\"]"

# Notes:
#     - 'Actual Window' is the armature itself, 'Scaled Window' is intended to be like a 'TV remote controller',
#       easy to pick up and move around in the scene, without modifying the positions of objects
#     - 'Scaled Window' is a Scaled Remote Controller for an Actual World of objects
#     - 'Scaled Window' can be scaled up (scaled up object scale values, not MegaMini scale) to get 1:1 scale factor,
#       and see how things appear without the 'forced perspective' object scaling effect - and compare with
#       'forced perspective' effect in real-time
def create_mega_mini_armature(context, mega_mini_scale):
    old_3dview_mode = context.mode
    # create MegaMini armature and enter EDIT mode
    bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
    armature = context.active_object
    # the armature represents the "actual space", the ScaledWindow bone represents the "scaled space"
    armature.name = "ActualWindow"
    armature[OBJ_PROP_SCALE] = mega_mini_scale

    # modify default bone to make 'Scaled Window' bone, to hold Scaled empties (this is the 'TV remote controller' part)
    scaled_window = armature.data.edit_bones[0]
    scaled_window.name = SCALED_WINDOW_BNAME

    scaled_obs = armature.data.edit_bones.new(name=SCALED_OBSERVER_BNAME)
    # save bone name for later use (in Pose bones mode, where the edit bones name may not be usable - will cause error)
    scaled_obs_name = scaled_obs.name
    # set bone data
    scaled_obs.head = mathutils.Vector(TEMP_BONE_HEAD)
    scaled_obs.tail = mathutils.Vector(TEMP_BONE_TAIL)
    scaled_obs.parent = scaled_window

    actual_obs = armature.data.edit_bones.new(name=ACTUAL_OBSERVER_BNAME)
    actual_obs_name = actual_obs.name
    actual_obs.head = mathutils.Vector(TEMP_BONE_HEAD)
    actual_obs.tail = mathutils.Vector(TEMP_BONE_TAIL)

    # enter Pose mode to allow adding bone constraints
    bpy.ops.object.mode_set(mode='POSE')

    # add bone constraint 'Copy Location' to Scaled Observer, so the Scaled Observer bone can be adjusted (fine-tuned)
    # with the Actual Observer bone (e.g. the Actual Observer bone can be parented to a scene Camera)
    scaled_obs_bconst = armature.pose.bones[scaled_obs_name].constraints.new(type='COPY_LOCATION')
    scaled_obs_bconst.target = armature
    scaled_obs_bconst.subtarget = actual_obs_name
    scaled_obs_bconst.use_offset = True
    # add a driver to scale the influence by the armature's mega_mini_scale value
    add_bconst_scl_inf_driver(scaled_obs_bconst)

    bpy.ops.object.mode_set(mode=old_3dview_mode)

class MEGAMINI_CreateMegaMiniRig(bpy.types.Operator):
    bl_description = "Create a MegaMini rig, for 'condensed space' - e.g. Solar system simulations, outer-space-to-Earth-surface zoom"
    bl_idname = "mega_mini.create_mega_mini_rig"
    bl_label = "Create MegaMini Rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mega_mini_scale = context.scene.MegaMini_NewObserverScale
        if mega_mini_scale <= 0:
            self.report({'ERROR'}, "Error in new Observer scale. Must be above zero.")
            return {'CANCELLED'}
        create_mega_mini_armature(context, mega_mini_scale)
        return {'FINISHED'}

def create_proxy_empty_pair(context, armature):
    # save old view3d mode and enter Edit mode, to add bones to armature
    old_3dview_mode = context.mode
    bpy.ops.object.mode_set(mode='EDIT')

    proxy_actual_bone = armature.data.edit_bones.new(name=PROXY_ACTUAL_BNAME)
    proxy_actual_bname = proxy_actual_bone.name
    proxy_actual_bone.head = mathutils.Vector(TEMP_BONE_HEAD)
    proxy_actual_bone.tail = mathutils.Vector(TEMP_BONE_TAIL)

    proxy_scaled_bone = armature.data.edit_bones.new(name=PROXY_SCALED_BNAME)
    proxy_scaled_bone_bname = proxy_scaled_bone.name
    proxy_scaled_bone.head = mathutils.Vector(TEMP_BONE_HEAD)
    proxy_scaled_bone.tail = mathutils.Vector(TEMP_BONE_TAIL)
    proxy_scaled_bone.parent = armature.data.edit_bones[SCALED_WINDOW_BNAME]

    proxy_scaled_focus_bone = armature.data.edit_bones.new(name=PROXY_SCALED_FOCUS_BNAME)
    proxy_scaled_focus_bname = proxy_scaled_focus_bone.name
    proxy_scaled_focus_bone.head = mathutils.Vector(TEMP_BONE_HEAD)
    proxy_scaled_focus_bone.tail = mathutils.Vector(TEMP_BONE_TAIL)
    proxy_scaled_focus_bone.parent = proxy_scaled_bone
    # switch back to previous view3d mode
    bpy.ops.object.mode_set(mode=old_3dview_mode)

    # add driver to actual bone to make it scale with scaled bone
    add_bone_scl_driver(armature, proxy_actual_bname, proxy_scaled_focus_bname, SCALED_OBSERVER_BNAME)

def add_bone_scl_driver(armature, proxy_actual_bname, proxy_scaled_focus_bname, s_obs_bname):
    drv_scale_x = armature.pose.bones[proxy_actual_bname].driver_add("scale", 0).driver
    drv_scale_x.use_self = True

    obs_x = drv_scale_x.variables.new()
    obs_x.type = 'TRANSFORMS'
    obs_x.name                 = "obs_x"
    obs_x.targets[0].id        = armature
    obs_x.targets[0].bone_target        = s_obs_bname
    obs_x.targets[0].transform_type = 'LOC_X'
    obs_x.targets[0].data_path = "location.x"

    obs_y = drv_scale_x.variables.new()
    obs_y.type = 'TRANSFORMS'
    obs_y.name                 = "obs_y"
    obs_y.targets[0].id        = armature
    obs_y.targets[0].bone_target        = s_obs_bname
    obs_y.targets[0].transform_type = 'LOC_Y'
    obs_y.targets[0].data_path = "location.y"

    obs_z = drv_scale_x.variables.new()
    obs_z.type = 'TRANSFORMS'
    obs_z.name                 = "obs_z"
    obs_z.targets[0].id        = armature
    obs_z.targets[0].bone_target        = s_obs_bname
    obs_z.targets[0].transform_type = 'LOC_Z'
    obs_z.targets[0].data_path = "location.z"

    focus_x = drv_scale_x.variables.new()
    focus_x.type = 'TRANSFORMS'
    focus_x.name                 = "focus_x"
    focus_x.targets[0].id        = armature
    focus_x.targets[0].bone_target        = proxy_scaled_focus_bname
    focus_x.targets[0].transform_type = 'LOC_X'
    focus_x.targets[0].data_path = "location.x"

    focus_y = drv_scale_x.variables.new()
    focus_y.type = 'TRANSFORMS'
    focus_y.name                 = "focus_y"
    focus_y.targets[0].id        = armature
    focus_y.targets[0].bone_target        = proxy_scaled_focus_bname
    focus_y.targets[0].transform_type = 'LOC_Y'
    focus_y.targets[0].data_path = "location.y"

    focus_z = drv_scale_x.variables.new()
    focus_z.type = 'TRANSFORMS'
    focus_z.name                 = "focus_z"
    focus_z.targets[0].id        = armature
    focus_z.targets[0].bone_target        = proxy_scaled_focus_bname
    focus_z.targets[0].transform_type = 'LOC_Z'
    focus_z.targets[0].data_path = "location.z"

    # Actual's forced perspective scaling value equals
    #     1 over square root of
    #         1 plus actual distance (un-scaled distance) from Scaled Observer to Scaled Focus
    drv_scale_x.expression = "1 / sqrt(1 + self.id_data[\"mega_mini_scale\"] * sqrt( " + \
        "("+focus_x.name+" - "+obs_x.name+") * ("+focus_x.name+" - "+obs_x.name+") + " + \
        "("+focus_y.name+" - "+obs_y.name+") * ("+focus_y.name+" - "+obs_y.name+") + " + \
        "("+focus_z.name+" - "+obs_z.name+") * ("+focus_z.name+" - "+obs_z.name+") ) )"

    # Y and Z scale are copies of X scale value
    drv_scale_y = armature.pose.bones[proxy_actual_bname].driver_add('scale', 1).driver
    drv_scale_y.use_self = True
    drv_scale_z = armature.pose.bones[proxy_actual_bname].driver_add('scale', 2).driver
    drv_scale_z.use_self = True
    drv_scale_y.expression = drv_scale_z.expression = "self.scale.x"

class MEGAMINI_CreateRigProxyPair(bpy.types.Operator):
    bl_description = "Based on the current position of current Scaled Observer, create an Actual-Scaled pair of " + \
        "bones.\nObjects parented to the Actual of the pair will be scaled and moved as the Scaled Observer moves"
    bl_idname = "mega_mini.create_proxy_pair"
    bl_label = "Create Pair"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        arm_ob = context.active_object
        if arm_ob is None:
            self.report({'ERROR'}, "Unable to Create Proxy Pair because no MegaMini rig object selected.")
            return {'CANCELLED'}
        if arm_ob.data.bones.get(SCALED_OBSERVER_BNAME) is None:
            self.report({'ERROR'}, "Unable to Create Proxy Pair because because Scaled Observer bone not found " +
                "in MegaMini rig active object.")
            return {'CANCELLED'}
        if arm_ob.data.bones.get(SCALED_WINDOW_BNAME) is None:
            self.report({'ERROR'}, "Unable to Create Proxy Pair because because Scaled Window bone not found " +
                "in MegaMini rig active object.")
            return {'CANCELLED'}

        create_proxy_empty_pair(context, arm_ob)
        return {'FINISHED'}
