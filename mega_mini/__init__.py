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

bl_info = {
    "name": "Mega Mini",
    "description": "Use 'forced perspective' optical illusion to 'condense space' between objects. Display far away objects at a smaller scale and closer distance than would be realistic.",
    "author": "Dave",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "View 3D -> Tools -> MegaMini",
    "category": "Other",
}

import bpy
from bpy.props import PointerProperty

from .panels import (MEGAMINI_CreateMegaMiniRig, MEGAMINI_CreateRigProxyPair, MEGAMINI_AttachRigProxyPair)

if bpy.app.version < (2,80,0):
    Region = "TOOLS"
else:
    Region = "UI"

class MEGAMINI_PT_Observer(bpy.types.Panel):
    bl_label = "Observer"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "MegaMini"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        box = layout.box()
        box.label(text="Create Observer")
        box.operator("mega_mini.create_mega_mini_rig")
        box.prop(scn, "MegaMini_NewObserverScale")

class MEGAMINI_PT_Proxy(bpy.types.Panel):
    bl_label = "Proxy"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "MegaMini"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Create Proxy Pair")
        box.operator("mega_mini.create_proxy_pair")
        box.operator("mega_mini.attach_proxy_pair")

classes = [
    MEGAMINI_PT_Observer,
    MEGAMINI_PT_Proxy,
    MEGAMINI_CreateMegaMiniRig,
    MEGAMINI_CreateRigProxyPair,
    MEGAMINI_AttachRigProxyPair,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_props()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

def register_props():
    bts = bpy.types.Scene
    bp = bpy.props
    bts.MegaMini_NewObserverScale = bp.FloatProperty(name="Observer Scale",
        description="Scaling factor to assign to MegaMini rig", default=1000.0, min=0.0)

if __name__ == "__main__":
    register()
