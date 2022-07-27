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

# TODO: show current MegaMini rig stats, including bones by way of list box

bl_info = {
    "name": "Mega Mini",
    "description": "Use 'forced perspective' optical illusion to 'condense space' between objects. Display far away objects at a smaller scale and closer distance than would be realistic.",
    "author": "Dave",
    "version": (0, 3, 0),
    "blender": (2, 80, 0),
    "location": "View 3D -> Tools -> MegaMini",
    "category": "Other",
    "wiki_url": "https://github.com/DreamSpoon/MegaMini#readme",
}

import bpy
from bpy.props import PointerProperty

from .panels import (MEGAMINI_CreateMegaMiniRig, MEGAMINI_CreateRigProxyPair, MEGAMINI_AttachRigProxyPair,
                     MEGAMINI_AddGeoNodes)

if bpy.app.version < (2,80,0):
    Region = "TOOLS"
else:
    Region = "UI"

class MEGAMINI_PT_Observer(bpy.types.Panel):
    bl_label = "Rig"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "MegaMini"

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        box = layout.box()
        box.label(text="Create Rig")
        box.operator("mega_mini.create_mega_mini_rig")
        box.prop(scn, "MegaMini_NewObserverScale")
        box.prop(scn, "MegaMini_NewObserverFP_Power")
        box.prop(scn, "MegaMini_NewObserverFP_MinDist")
        box.prop(scn, "MegaMini_NewObserverFP_MinScale")

class MEGAMINI_PT_Proxy(bpy.types.Panel):
    bl_label = "Proxy"
    bl_space_type = "VIEW_3D"
    bl_region_type = Region
    bl_category = "MegaMini"

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        box = layout.box()
        box.label(text="Create Proxy")
        box.operator("mega_mini.create_proxy_pair")
        box.label(text="Attach to Rig")
        box.operator("mega_mini.attach_proxy_pair")
        # geometry node support is only for Blender v2.9+ (or maybe v3.0+ ... TODO: check this)
        if bpy.app.version >= (2,90,0):
            box.operator("mega_mini.add_geo_nodes")
            box.prop(scn, "MegaMini_GeoNodesOverrideCreate")
            box.prop(scn, "MegaMini_GeoNodesCreateUseAltGroup")
            col = box.column()
            col.active = scn.MegaMini_GeoNodesCreateUseAltGroup
            col.prop(scn, "MegaMini_GeoNodesCreateAltGroup")

classes = [
    MEGAMINI_PT_Observer,
    MEGAMINI_PT_Proxy,
    MEGAMINI_CreateMegaMiniRig,
    MEGAMINI_CreateRigProxyPair,
    MEGAMINI_AttachRigProxyPair,
    MEGAMINI_AddGeoNodes,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_props()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bts.MegaMini_GeoNodesCreateAltGroup
    del bts.MegaMini_GeoNodesCreateUseAltGroup
    del bts.MegaMini_GeoNodesOverrideCreate
    del bts.MegaMini_NewObserverFP_MinScale
    del bts.MegaMini_NewObserverFP_MinDist
    del bts.MegaMini_NewObserverFP_Power
    del bts.MegaMini_NewObserverScale

def only_geo_node_group_poll(self, object):
    return object.type == 'GEOMETRY'

def register_props():
    bts = bpy.types.Scene
    bp = bpy.props
    bts.MegaMini_NewObserverScale = bp.FloatProperty(name="Observer Scale",
        description="Scaling factor to assign to MegaMini rig", default=1000.0, min=0.0)
    bts.MegaMini_NewObserverFP_Power = bp.FloatProperty(name="FP Power",
        description="Forced Perspective distance Power value, for generating scales of objects attached to MegaMini " +
        "rig based on distance. Value is usually between zero and one. Setting this value to zero will remove the " +
        "'forced perspective effect'", default=0.5)
    bts.MegaMini_NewObserverFP_MinDist = bp.FloatProperty(name="FP Min Dist",
        description="Forced Perspective Minimum Distance value, for generating scales of objects attached to MegaMini " +
        "rig", default=0.0)
    bts.MegaMini_NewObserverFP_MinScale = bp.FloatProperty(name="FP Min Scale",
        description="Forced Perspective Minimum Scale value, which is the minimum scale to apply with the " +
        "'Forced Perspective' effect", default=0.0)
    bts.MegaMini_GeoNodesOverrideCreate = bp.BoolProperty(name="Override Create", description="MegaMini Geometry " +
        "Nodes custom node group is re-created when geometry nodes are added to object(s), and any previous custom " +
        "group with the same name is deprecated", default=False)
    bts.MegaMini_GeoNodesCreateUseAltGroup = bp.BoolProperty(name="Use Alt Group", description="Add MegaMini Geo " +
        "node group to alternate geometry node group", default=False)
    bts.MegaMini_GeoNodesCreateAltGroup = bp.PointerProperty(name="Group Name", type=bpy.types.NodeTree,
        poll=only_geo_node_group_poll)

if __name__ == "__main__":
    register()
