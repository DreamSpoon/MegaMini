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
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View 3D -> Tools -> MegaMini",
    "category": "Other",
}

import bpy
from bpy.props import PointerProperty

from .panels import (OBJ_PROP_SCALE, MEGAMINI_CreateObserverPair, MEGAMINI_CreateProxyPair, MEGAMINI_AttachProxyPair)

if bpy.app.version < (2,80,0):
#    from .imp_v27 import *
    Region = "TOOLS"
else:
#    from .imp_v28 import *
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
        box.operator("mega_mini.create_observer_pair")
        box.prop(scn, "MegaMini_NewObserverScale")

class MEGAMINI_PT_Proxy(bpy.types.Panel):
    bl_label = "Proxy"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "MegaMini"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        box = layout.box()
        box.prop(scn, "MegaMini_SelMegaObserver")
        box.prop(scn, "MegaMini_SelMiniObserver")
        box = layout.box()
        box.label(text="Create Proxy Pair")
        box.operator("mega_mini.create_proxy_pair")
        box = layout.box()
        box.label(text="Attach Proxy Pair")
        box.operator("mega_mini.attach_proxy_pair")

classes = [
    MEGAMINI_PT_Observer,
    MEGAMINI_PT_Proxy,
    MEGAMINI_CreateObserverPair,
    MEGAMINI_CreateProxyPair,
    MEGAMINI_AttachProxyPair,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_props()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

def filter_callback(self, ob):
#    return ob.get(OBJ_PROP_SCALE) != None
    return True

def register_props():
    bts = bpy.types.Scene
    bp = bpy.props
    bts.MegaMini_NewObserverScale = bp.FloatProperty(name="Observer Scale",
        description="Scale to assign to new Mega Observer", default=1000.0, min=0.0)
    bts.MegaMini_SelMegaObserver = PointerProperty(name="Mega Observer",
        description="Mega Observer object to use when creating/attaching Proxy Pairs", type=bpy.types.Object,
        poll=filter_callback)
    bts.MegaMini_SelMiniObserver = PointerProperty(name="Mini Observer",
        description="Mini Observer object to use when creating/attaching Proxy Pairs", type=bpy.types.Object,
        poll=filter_callback)

if __name__ == "__main__":
    register()
