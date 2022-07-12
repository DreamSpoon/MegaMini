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

OBJ_PROP_SCALE = "mega_mini_scale"

SCALED_WINDOW_BNAME = "ScaledWindow"

# Notes:
#     - 'Actual Window' is the armature itself, 'Scaled Window' is intended to be like a 'TV remote controller',
#       easy to pick up and move around in the scene, without modifying the positions of objects
#     - 'Scaled Window' is a Scaled Remote Controller for an Actual World of objects
#     - 'Scaled Window' can be scaled up (object scale values, not MegaMini scale) to make it 1:1 scale factor,
#       to test how things would appear without the 'forced perspective' object scaling effect - and compare with
#       'forced perspective' effect in real-time
def create_mega_mini_armature(context, mega_mini_scale):
    old_3dview_mode = context.object.mode
    # create MegaMini armature and enter EDIT mode
    bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
    armature = context.active_object
    armature.name = "ActualWindow"
    armature[OBJ_PROP_SCALE] = mega_mini_scale

    # modify default bone to make 'Scaled Window' bone, to hold Scaled empties (this is the 'TV remote controller' part)
    scaled_window = armature.data.edit_bones[0]
    scaled_window.name = SCALED_WINDOW_BNAME

    bpy.ops.object.mode_set(mode=old_3dview_mode)

class MEGAMINI_CreateMegaMiniRig(bpy.types.Operator):
    bl_description = "Create a MegaMini rig, for 'condensed space'"
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
