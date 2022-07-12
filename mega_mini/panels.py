import bpy

OBJ_PROP_SCALE = "mega_mini_scale"

MEGA_OBS_EMPTY_NAME = "MegaObserverEmpty"
MEGA_OBS_EMPTY_TYPE = "PLAIN_AXES"
MINI_OBS_EMPTY_NAME = "MiniObserverEmpty"
MINI_OBS_EMPTY_TYPE = "PLAIN_AXES"
MINI_EMPTY_NAME = "MiniEmpty"
MINI_EMPTY_TYPE = "PLAIN_AXES"
MINI_FOCUS_EMPTY_NAME = "MiniFocusEmpty"
MINI_FOCUS_EMPTY_TYPE = "PLAIN_AXES"
MEGA_EMPTY_NAME = "MegaEmpty"
MEGA_EMPTY_TYPE = "PLAIN_AXES"

def create_empty_object(context, empty_name, empty_type, empty_loc):
    bpy.ops.object.empty_add(type=empty_type, location=empty_loc)
    new_empty = context.active_object
    new_empty.name = empty_name
    return new_empty

def create_observer_empty_pair(context, obs_scale, obs_loc):
    new_mega_obs_empty = create_empty_object(context, MEGA_OBS_EMPTY_NAME, MEGA_OBS_EMPTY_TYPE, obs_loc)
    new_mini_obs_empty = create_empty_object(context, MINI_OBS_EMPTY_NAME, MINI_OBS_EMPTY_TYPE, obs_loc)
    new_mini_obs_empty[OBJ_PROP_SCALE] = obs_scale

    # add object constraint re: Copy Location, so the Mini empty can be adjusted (fine-tuned) with the Mega empty
    copy_loc_const = new_mini_obs_empty.constraints.new('COPY_LOCATION')
    copy_loc_const.use_offset = True
    copy_loc_const.target = new_mega_obs_empty
    drv_copy_loc = copy_loc_const.driver_add('influence').driver
    drv_copy_loc.use_self = True
    drv_copy_loc.expression = "1 / self.id_data[\"mega_mini_scale\"]"

    return new_mega_obs_empty, new_mini_obs_empty

class MEGAMINI_CreateObserverPair(bpy.types.Operator):
    bl_description = "Create placeholder objects that acts as an 'Observer' in the 'Condensed Space' of objects"
    bl_idname = "mega_mini.create_observer_pair"
    bl_label = "Create Observer Pair"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.scene.MegaMini_NewObserverScale <= 0:
            self.report({'ERROR'}, "Error in new Observer scale. Must be above zero.")
            return {'CANCELLED'}
        mega_obs_empty, mini_obs_empty = create_observer_empty_pair(context, context.scene.MegaMini_NewObserverScale,
            (0, 0, 0))
        # update the selected Mega Observer object field in the panels, if it was empty beforehand
        if context.scene.MegaMini_SelMegaObserver is None:
            context.scene.MegaMini_SelMegaObserver = mega_obs_empty
        if context.scene.MegaMini_SelMiniObserver is None:
            context.scene.MegaMini_SelMiniObserver = mini_obs_empty

        return {'FINISHED'}

def create_mini_empty(context, loc):
    new_mini_empty = create_empty_object(context, MINI_EMPTY_NAME, MINI_EMPTY_TYPE, loc)
    return new_mini_empty

def create_mini_focus_empty(context, mini_empty):
    new_mini_focus_empty = create_empty_object(context, MINI_FOCUS_EMPTY_NAME, MINI_FOCUS_EMPTY_TYPE, mini_empty.location)
    new_mini_focus_empty.parent = mini_empty
    return new_mini_focus_empty

def create_mega_empty(context, scale):
    new_mega_empty = create_empty_object(context, MEGA_EMPTY_NAME, MEGA_EMPTY_TYPE, (0, 0, 0))
    new_mega_empty[OBJ_PROP_SCALE] = scale
    return new_mega_empty

def add_mega_drivers_scl(obs_empty, focus_empty, mega_empty):
    drv_scale_x = mega_empty.driver_add('scale', 0).driver
    drv_scale_x.use_self = True

    v_focus_x = drv_scale_x.variables.new()
    v_focus_x.type = 'TRANSFORMS'
    v_focus_x.name                 = "focus_x"
    v_focus_x.targets[0].id        = focus_empty
    v_focus_x.targets[0].transform_type = 'LOC_X'
    v_focus_x.targets[0].data_path = "location.x"
    v_focus_y = drv_scale_x.variables.new()
    v_focus_y.type = 'TRANSFORMS'
    v_focus_y.name                 = "focus_y"
    v_focus_y.targets[0].id        = focus_empty
    v_focus_y.targets[0].transform_type = 'LOC_Y'
    v_focus_y.targets[0].data_path = "location.y"
    v_focus_z = drv_scale_x.variables.new()
    v_focus_z.type = 'TRANSFORMS'
    v_focus_z.name                 = "focus_z"
    v_focus_z.targets[0].id        = focus_empty
    v_focus_z.targets[0].transform_type = 'LOC_Z'
    v_focus_z.targets[0].data_path = "location.z"

    v_obs_x = drv_scale_x.variables.new()
    v_obs_x.type = 'TRANSFORMS'
    v_obs_x.name                 = "obs_x"
    v_obs_x.targets[0].id        = obs_empty
    v_obs_x.targets[0].transform_type = 'LOC_X'
    v_obs_x.targets[0].data_path = "location.x"
    v_obs_y = drv_scale_x.variables.new()
    v_obs_y.type = 'TRANSFORMS'
    v_obs_y.name                 = "obs_y"
    v_obs_y.targets[0].id        = obs_empty
    v_obs_y.targets[0].transform_type = 'LOC_Y'
    v_obs_y.targets[0].data_path = "location.y"
    v_obs_z = drv_scale_x.variables.new()
    v_obs_z.type = 'TRANSFORMS'
    v_obs_z.name                 = "obs_z"
    v_obs_z.targets[0].id        = obs_empty
    v_obs_z.targets[0].transform_type = 'LOC_Z'
    v_obs_z.targets[0].data_path = "location.z"

    # Mega scale equals
    #     1 over square root of
    #         1 plus actual distance from Observer empty to Mini Focus empty
    drv_scale_x.expression = "1 / sqrt(1 + self[\"mega_mini_scale\"] * sqrt( " + \
        "("+v_focus_x.name+" - "+v_obs_x.name+") * ("+v_focus_x.name+" - "+v_obs_x.name+") + " + \
        "("+v_focus_y.name+" - "+v_obs_y.name+") * ("+v_focus_y.name+" - "+v_obs_y.name+") + " + \
        "("+v_focus_z.name+" - "+v_obs_z.name+") * ("+v_focus_z.name+" - "+v_obs_z.name+") ) )"

    # Y and Z scale are copies of X scale value
    drv_scale_y = mega_empty.driver_add('scale', 1).driver
    drv_scale_y.use_self = True
    drv_scale_z = mega_empty.driver_add('scale', 2).driver
    drv_scale_z.use_self = True
    drv_scale_y.expression = drv_scale_z.expression = "self.scale.x"

def add_mega_drivers_loc(obs_empty, mega_empty, mini_empty):
    # X
    drv_loc_x = mega_empty.driver_add('location', 0).driver
    drv_loc_x.use_self = True
    # mini X
    v_mini_x = drv_loc_x.variables.new()
    v_mini_x.type = 'TRANSFORMS'
    v_mini_x.name                 = "mini_x"
    v_mini_x.targets[0].id        = mini_empty
    v_mini_x.targets[0].transform_type = 'LOC_X'
    v_mini_x.targets[0].data_path = "location.x"
    # observer X
    v_obs_x = drv_loc_x.variables.new()
    v_obs_x.type = 'TRANSFORMS'
    v_obs_x.name                 = "obs_x"
    v_obs_x.targets[0].id        = obs_empty
    v_obs_x.targets[0].transform_type = 'LOC_X'
    v_obs_x.targets[0].data_path = "location.x"
    # driver X
    drv_loc_x.expression = "("+v_mini_x.name+" - "+v_obs_x.name+") * self[\"mega_mini_scale\"] * sqrt(self.scale.x)"

    # Y
    drv_loc_y = mega_empty.driver_add('location', 1).driver
    drv_loc_y.use_self = True
    # mini Y
    v_mini_y = drv_loc_y.variables.new()
    v_mini_y.type = 'TRANSFORMS'
    v_mini_y.name                 = "mini_y"
    v_mini_y.targets[0].id        = mini_empty
    v_mini_y.targets[0].transform_type = 'LOC_Y'
    v_mini_y.targets[0].data_path = "location.y"
    # observer Y
    v_obs_y = drv_loc_y.variables.new()
    v_obs_y.type = 'TRANSFORMS'
    v_obs_y.name                 = "mini_obs_y"
    v_obs_y.targets[0].id        = obs_empty
    v_obs_y.targets[0].transform_type = 'LOC_Y'
    v_obs_y.targets[0].data_path = "location.y"
    # driver Y
    drv_loc_y.expression = "("+v_mini_y.name+" - "+v_obs_y.name+") * self[\"mega_mini_scale\"] * sqrt(self.scale.y)"

    # Z
    drv_loc_z = mega_empty.driver_add('location', 2).driver
    drv_loc_z.use_self = True
    # mini Z
    v_mini_z = drv_loc_z.variables.new()
    v_mini_z.type = 'TRANSFORMS'
    v_mini_z.name                 = "mini_z"
    v_mini_z.targets[0].id        = mini_empty
    v_mini_z.targets[0].transform_type = 'LOC_Z'
    v_mini_z.targets[0].data_path = "location.z"
    # observer Z
    v_obs_z = drv_loc_z.variables.new()
    v_obs_z.type = 'TRANSFORMS'
    v_obs_z.name                 = "obs_z"
    v_obs_z.targets[0].id        = obs_empty
    v_obs_z.targets[0].transform_type = 'LOC_Z'
    v_obs_z.targets[0].data_path = "location.z"
    # driver Z
    drv_loc_z.expression = "("+v_mini_z.name+" - "+v_obs_z.name+") * self[\"mega_mini_scale\"] * sqrt(self.scale.z)"

# TODO check if this works with rotation types other than Euler
def add_mega_drivers_rot(mega_empty, mini_empty):
    # X
    drv_rot_x = mega_empty.driver_add('rotation_euler', 0).driver
    v_mini_x = drv_rot_x.variables.new()
    v_mini_x.type = 'TRANSFORMS'
    v_mini_x.name                 = "mini_rot_x"
    v_mini_x.targets[0].id        = mini_empty
    v_mini_x.targets[0].transform_type = 'ROT_X'
    v_mini_x.targets[0].data_path = "rotation.x"
    drv_rot_x.expression = v_mini_x.name
    # Y
    drv_rot_y = mega_empty.driver_add('rotation_euler', 1).driver
    v_mini_y = drv_rot_y.variables.new()
    v_mini_y.type = 'TRANSFORMS'
    v_mini_y.name                 = "mini_rot_y"
    v_mini_y.targets[0].id        = mini_empty
    v_mini_y.targets[0].transform_type = 'ROT_Y'
    v_mini_y.targets[0].data_path = "rotation.y"
    drv_rot_y.expression = v_mini_y.name
    # Z
    drv_rot_z = mega_empty.driver_add('rotation_euler', 2).driver
    v_mini_z = drv_rot_z.variables.new()
    v_mini_z.type = 'TRANSFORMS'
    v_mini_z.name                 = "mini_rot_z"
    v_mini_z.targets[0].id        = mini_empty
    v_mini_z.targets[0].transform_type = 'ROT_Z'
    v_mini_z.targets[0].data_path = "rotation.z"
    drv_rot_z.expression = v_mini_z.name

def create_proxy_empty_pair(context, mini_obs_empty):
    mega_empty = create_mega_empty(context, mini_obs_empty.get(OBJ_PROP_SCALE))
    mini_empty = create_mini_empty(context, mini_obs_empty.location)
    mini_focus_empty = create_mini_focus_empty(context, mini_empty)
    # to calculate scale, use Mini Focus empty instead of Mini empty, to allow changing object's 'scale focus'
    add_mega_drivers_scl(mini_obs_empty, mini_focus_empty, mega_empty)
    add_mega_drivers_loc(mini_obs_empty, mega_empty, mini_empty)
    add_mega_drivers_rot(mega_empty, mini_empty)
    return mega_empty, mini_empty

class MEGAMINI_CreateProxyPair(bpy.types.Operator):
    bl_description = "Based on the current position of current Mini Observer, create a Mega-Mini pair of empties.\n" + \
        "Objects parented to the MegaEmpty of the pair will be scaled and moved as the Mini Observer moves"
    bl_idname = "mega_mini.create_proxy_pair"
    bl_label = "Create Pair"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        observer_empty = scn.MegaMini_SelMiniObserver
        if observer_empty is None:
            self.report({'ERROR'}, "Unable to Create Proxy Pair because Mini Observer is None.")
            return {'CANCELLED'}
        if observer_empty.get(OBJ_PROP_SCALE) is None:
            self.report({'ERROR'}, "Unable to Create Proxy Pair because Mini Observer's custom property Scale is missing.")
            return {'CANCELLED'}
        mega_empty, mini_empty = create_proxy_empty_pair(context, observer_empty)
        # if Mega Observer exists then parent the new Mega Empty to the Mega Observer
        if scn.MegaMini_SelMegaObserver is not None:
            mega_empty.parent = scn.MegaMini_SelMegaObserver

        return {'FINISHED'}

class MEGAMINI_AttachProxyPair(bpy.types.Operator):
    bl_description = "Create a Mega-Mini pair of empties, and parent the selected object(s) to the Mini of the" + \
        " pair.\nNote: this uses current position of given Mega Observer"
    bl_idname = "mega_mini.attach_proxy_pair"
    bl_label = "Attach Pair"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        # error checks
        observer_empty = scn.MegaMini_SelMiniObserver
        if observer_empty is None:
            self.report({'ERROR'}, "Unable to Attach Proxy Pair because Mini Observer is None.")
            return {'CANCELLED'}
        if observer_empty.get(OBJ_PROP_SCALE) is None:
            self.report({'ERROR'}, "Unable to Attach Proxy Pair because Mini Observer's custom property Scale is missing.")
            return {'CANCELLED'}
        if len(context.selected_objects) < 1:
            self.report({'ERROR'}, "Unable to Attach Proxy Pair because no object(s) selected")
            return {'CANCELLED'}
        # store the original copy of the list of selected objects, since this list will be modified when empties are created
        sel_obj_list = []
        for ob in context.selected_objects:
            sel_obj_list.append(ob)
        # create the empties
        mega_empty, mini_empty = create_proxy_empty_pair(context, observer_empty)
        # parent the previously selected object(s) to the mega_empty that was just created
        for ob in sel_obj_list:
            ob.parent = mega_empty
        return {'FINISHED'}
