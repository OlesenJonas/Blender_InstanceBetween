bl_info = {
    "name": "Instance Between",
    "author": "Jonas Olesen",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Object Mode -> Object -> Instance Between",
    "description": "Instance one Object between two others",
    "category": "Object Mode",
}


import bpy
import math
from bpy.props import *


class OBJECT_OT_instance_between(bpy.types.Operator):
    """Instance one Object between two others"""
    bl_idname = "object.instbetween"
    bl_label = "Instance Between"
    bl_options = {'REGISTER', 'UNDO'}

    num: IntProperty(
        name="Amount",
        description = "Amount of copies",
        default = 3,
        min = 0,
    )

    @classmethod
    def poll(cls, context):
        #return len(bpy.context.selected_objects) == 2
        #cant do this in poll because then the IntProperty wont work
        return True

    def execute(self, context):
        
        old_selection = context.selected_objects
        old_active = context.active_object

        if len(old_selection) != 2:
            self.report({"ERROR"}, "Must select two objects")
            return {"CANCELLED"}
        
        bpy.ops.object.select_all(action="DESELECT")
        
        old_active.select_set(True)
        
        loc0 = old_selection[0].location
        loc1 = old_selection[1].location
        diff = loc1 - loc0
        diff /= self.num+1
        
        for i in range(1,self.num+1):
            bpy.ops.object.duplicate(linked=True)
            context.active_object.location = loc0 + i*diff
            old_selection.append(context.active_object)
            
        for obj in old_selection:
            obj.select_set(True)
           

        return {'FINISHED'}
    

def inst_between_button(self, context):
    self.layout.operator(
        "object.instbetween",
        text="Instance Between")

from bpy.utils import register_class
from bpy.utils import unregister_class

def register():
    register_class(OBJECT_OT_instance_between)
    bpy.types.VIEW3D_MT_object.append(inst_between_button)


def unregister():
    unregister_class(OBJECT_OT_instance_between)
    bpy.types.VIEW3D_MT_object.remove(inst_between_button)


if __name__ == "__main__":
    register()
