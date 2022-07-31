bl_info = {
    "name": "Braille Generator",
    "author": "Pedro Lemos",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Create a new Braille Tag",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy

class OBJECT_PT_BrailleGenerator(bpy.types.Panel):
    bl_label = "Braille Generator"
    bl_idname = "OBJECT_PT_BrailleGenerator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Braille Generator"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("wm.generator")
        
        
class WM_OT_generatorOP(bpy.types.Operator):
    bl_label = "Braille Generator Operator"
    bl_idname = "wm.generator"
    
    text: bpy.props.StringProperty(name= "Enter Name", default= "text")
    scale: bpy.props.FloatProperty(name= "Scale", default= 0.3)
    
    cubeX: bpy.props.FloatProperty(name= "Board Width (mm)", default= 150)
    cubeY: bpy.props.FloatProperty(name= "Board Length (mm)", default= 100)
    cubeZ: bpy.props.FloatProperty(name= "Board Height (mm)", default= 5)
    
    def execute(self, context):
        t = self.text
        cX = self.cubeX
        cY = self.cubeY
        cZ = self.cubeZ
        cScale = 2000
        tScale = self.scale
        bScale = 0.2 #Escala da fonte em Braille
        locationArr = []
        
        #deletar todos os itens anteriores
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:
            print(obj)
            obj.hide_set(False)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False, confirm=False)
        
        #Text 02 - Braille
        bpy.ops.object.text_add(enter_editmode=True, align='WORLD', location=(0, -0.015, 0.0025), scale=(1, 1, 1))
        txt2 = bpy.context.object
        bpy.ops.font.delete(type='PREVIOUS_WORD')
        bpy.ops.font.text_insert(text = t)
        bpy.context.object.data.align_x = 'CENTER'
        #bpy.context.object.data.extrude = 1
        bpy.ops.object.editmode_toggle()
        fnt2 = bpy.data.fonts.load("//braille_type\\Braille Type.ttf")
        txt2.data.font = fnt2
        bpy.ops.object.convert(target='MESH')  
        
        bpy.ops.transform.resize(value=(bScale*cX/cScale, bScale*cX/cScale, bScale*cZ/cScale), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        
        # Separando os pontos da fonte Braille
        txt2.select_set(True)
        if txt2.type == 'MESH':
            print("Splitting mesh")
            bpy.ops.mesh.separate(type='LOOSE')
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        txt2.select_set(False)
        
        for collection in bpy.data.collections:
            if collection.name == "Collection":
                for object in collection.objects:
                    locationArr.append(object.location)
                    object.hide_set(True)

        
        for i in range(len(locationArr)):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0005, enter_editmode=False, align='WORLD', location=locationArr[i], scale=(1, 1, 1))
        #radius = raio da esfera, dos pontos da escrita em braille
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.join()
        
        braille = bpy.context.object
        
        bpy.context.object.hide_set(True)
        
         #Text 01 - Regular Font
        bpy.ops.object.text_add(enter_editmode=True, align='WORLD', location=(0, 0.015, 0.0025), scale=(tScale*cX/cScale, tScale*cX/cScale, cZ/cScale))
        txt = bpy.context.object
        bpy.ops.font.delete(type='PREVIOUS_WORD')
        bpy.ops.font.text_insert(text = t)
        bpy.context.object.data.align_x = 'CENTER'
        bpy.context.object.data.extrude = 1
        bpy.ops.object.editmode_toggle()
        fnt = bpy.data.fonts.load("C:\\WINDOWS\\Fonts\\arial.ttf")
        txt.data.font = fnt
        bpy.ops.object.convert(target='MESH')          
        
        bpy.ops.transform.resize(value=(tScale*cX/cScale, tScale*cX/cScale, cZ/cScale), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        
        bpy.context.object.hide_set(True)
        
        #Create Board
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(cX/cScale, cY/cScale, cZ/cScale))
        
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].object = txt
        
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean.001"].operation = 'UNION'
        bpy.context.object.modifiers["Boolean.001"].object = braille
        
        

        
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(OBJECT_PT_BrailleGenerator)
    bpy.utils.register_class(WM_OT_generatorOP)


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_BrailleGenerator)
    bpy.utils.unregister_class(WM_OT_generatorOP)

def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")

if __name__ == "__main__":
    register()

