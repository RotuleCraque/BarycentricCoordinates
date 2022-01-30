bl_info = {
    "name": "Barycentric Coordinates to Vertex Colour",
    "category": "Object",
    "blender": (3, 0, 0),
    "author": "Alo",
}




import bpy
import mathutils
from random import uniform



class BaryCoordsToVertexColour(bpy.types.Operator):
    """Bake data for barycentric coordinates computation in vertex colour rgb and a random numder in alpha"""
    bl_idname = 'object.barycentric_coords_to_vertex_colour'
    bl_label = 'Barycentric Coordinates to Vertex Colour'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        barycentric_coordinates_to_vertex_colour()
        return {'FINISHED'}


def barycentric_coordinates_to_vertex_colour():
    # triangulation is done in edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    bpy.ops.mesh.quads_convert_to_tris()

    # vertex colour layer creation is done in object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # selected object
    obj = bpy.context.active_object
    mesh = obj.data

    # objects needs a vertex color layer
    vertex_colours = mesh.vertex_colors
    if len(vertex_colours) == 0:
        vertex_colours.new()
        
    # get colour layer
    colour_layer = vertex_colours.active


    coloursArray = [
                    mathutils.Vector([1.0, 0.0, 0.0]),
                    mathutils.Vector([0.0, 1.0, 0.0]),
                    mathutils.Vector([0.0, 0.0, 1.0])
                    ]

    i = 0
    # in each triangle, vertex weights are stored in vertex colour
    for face in mesh.polygons:
        
        # compute random in [0,1] range to store in alpha
        rand = uniform(0.0, 1.0)
        
        j = 0
        for idx in face.loop_indices:
            finalColour = mathutils.Vector([coloursArray[j].x, coloursArray[j].y, coloursArray[j].z, rand])
            colour_layer.data[i].color = finalColour
            i += 1
            j += 1
        

            
            
            
def menu_func(self, context):
    self.layout.operator(BaryCoordsToVertexColour.bl_idname)
            
def register():
    bpy.utils.register_class(BaryCoordsToVertexColour)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unregister():
    bpy.utils.unregister_class(BaryCoordsToVertexColour)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    
    
if __name__ == "__main__":
    register()