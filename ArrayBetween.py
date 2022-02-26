"""

select 2 objects to do an array between. 
objects (instances or full copy) between will be dupplicates of the first selected object ("head") 
or the last one ("tail")

or select 3 objects
objects between the two first selected will be dupplicates of the last selected ("third")


"""

#TODO keep modifiers or not, animation copy fix? 
 
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
    
    instances: bpy.props.BoolProperty(default=True)
    
#    copy_modifiers: bpy.props.BoolProperty(default=True)
#    copy_animations: bpy.props.BoolProperty(default=False)

    count: bpy.props.IntProperty(
        name="Count",
        description = "Amount of copies",        
        default = 1,
        min = 0,
    )        

    From: bpy.props.EnumProperty(
        name="From",
        description="",
        items= [
        ("0", "head", ""),
        ("1", "tail", ""),
        ]
    )

    def duplicate(self, obj, linked=False, actions=False, collection=None):
        obj_copy = obj.copy()
        if not linked:
            obj_copy.data = obj_copy.data.copy()
# not working
#        if actions and obj_copy.animation_data:
#            obj_copy.animation_data.action = obj_copy.animation_data.action.copy()
# https://blender.stackexchange.com/questions/220926/python-copy-animation-from-armature-to-another-armature-different-rest-pose
        if not actions and obj_copy.animation_data:
            obj_copy.animation_data.action = None #don't copy animation
        collection.objects.link(obj_copy)
        return obj_copy
        
    def execute(self, context):
        global sel, activ
        sel = context.selected_objects.copy()
        sel2=[]
        activ = context.active_object       

        if len(sel) not in {2, 3}:
           self.report({"ERROR"}, "Must select 2 or 3 objects")
           return {"CANCELLED"}
        
        sel1 = sel if len(sel) == 2 else [s for s in sel if s != context.object] #sel without active
        
#        loc0 = sel1[0].matrix_world.to_translation() #not solving pb when copy animation
        loc0 = sel1[0].location
        loc1 = sel1[1].location
        diff = loc1 - loc0
        diff /= self.count+1

        def multiply():
            instances = True if self.instances else False
            obj=context.object
            for i in range(1, self.count+1):
                obj = self.duplicate(obj=obj, linked=instances, collection=context.collection)
                context.view_layer.objects.active = obj
                obj.location = loc0 +i*diff
                sel2.append(obj)

        if len(sel) == 3:
            sel1[1].select_set(False)
            sel1[0].select_set(False)
#            multiply()         
        if self.From == "0" and not len(sel) == 3:
            context.view_layer.objects.active = sel1[0]
            sel1[1].select_set(False)
            sel1[0].select_set(True)
#            multiply() 
        if self.From == "1" and not len(sel) == 3:
            context.view_layer.objects.active = sel1[1]
            sel1[1].select_set(True)
            sel1[0].select_set(False)
#            multiply()
        multiply()
           
        for obj in (set(sel) | set(sel2)):
            obj.select_set(True)
      
        if self.From == "2" and len(set(sel)) == 3:
            activ.select_set(False) 
        return {'FINISHED'}
    
    def draw(self, context):   
        layout=self.layout
        layout.prop(self,"count")
#        layout.prop(self,"copy_animations")
        if len(sel) == 2:
            layout.prop(self,"From")
        else:
            layout.label(text="From: "+activ.name)
        
def draw(self, context):
    self.layout.operator(
        "object.instbetween")

from bpy.utils import register_class, unregister_class

def register():
    register_class(OBJECT_OT_instance_between)
    bpy.types.VIEW3D_MT_object.append(draw)


def unregister():
    unregister_class(OBJECT_OT_instance_between)
    bpy.types.VIEW3D_MT_object.remove(draw)
