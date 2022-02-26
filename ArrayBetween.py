bl_info = {
    "name": "Array Between",
    "author": "Jonas Olesen/1COD review",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Object Mode -> Object -> Array Between",
    "description": "Instance one Object between two others",
    "category": "Object",
}

import bpy

class OBJECT_OT_instance_between(bpy.types.Operator):
    """Array between 2 selected objects"""
    bl_idname = "object.instbetween"
    bl_label = "Array Between"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    count: bpy.props.IntProperty(
        name="count",
        description = "Amount of copies",
        default = 3,
        min = 0,
    )

    def execute(self, context):
        sel = context.selected_objects

        if len(sel) != 2:
           self.report({"ERROR"}, "Must select 2 objects")
           return {"CANCELLED"}

        loc0 = sel[0].location
        loc1 = sel[1].location
        diff = loc1 - loc0
        diff /= self.count+1
        
        # bpy.ops.object.select_all(action="DESELECT")
        
        sel[1].select_set(True)

        for i in range(self.count):
           bpy.ops.object.duplicate(linked=True)
           context.active_object.location = loc0 + i*diff
           old_selection.append(context.active_object)
           
        for obj in old_selection:
           obj.select_set(True)
           

        return {'FINISHED'}
    

def draw(self, context):
    self.layout.operator(
        "object.instbetween")#,        text="Array Between")

from bpy.utils import register_class
from bpy.utils import unregister_class

def register():
    register_class(OBJECT_OT_instance_between)
    bpy.types.VIEW3D_MT_object.append(draw)


def unregister():
    unregister_class(OBJECT_OT_instance_between)
    bpy.types.VIEW3D_MT_object.remove(draw)
