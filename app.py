"""
bake smart
"""

import bpy

# texture resolution
max_image_size = 1024
# texels per unit
texel_density = 20

def Vector2dMultiple(A, B, C):
	return abs((B[0]- A[0])*(C[1]- A[1])-(B[1]- A[1])*(C[0]- A[0]))

def Vector3dMultiple(A, B, C):
	result = 0
	vectorX = 0
	vectorY = 0
	vectorZ = 0
	
	vectorX = (B[1]- A[1])*(C[2]- A[2])-(B[2]- A[2])*(C[1]- A[1])
	vectorY = -1*((B[0]- A[0])*(C[2]- A[2])-(B[2]- A[2])*(C[0]- A[0]))
	vectorZ = (B[0]- A[0])*(C[1]- A[1])-(B[1]- A[1])*(C[0]- A[0])
	
	result = math.sqrt(math.pow(vectorX, 2) + math.pow(vectorY, 2) + math.pow(vectorZ, 2))
	return result


def get_geo():
    """
     get all the geos
    """
    geos = bpy.context.selected_objects
    return [geo for geo in geos if geo.type == 'MESH' and len(actObj.data.uv_layers) > 0]


def calculate_surface_area():
    """
    set the texel density
    """
    geos = get_geo()
    for geo in geos:


def triangulate_selected():
    """
    triangulate the object
    """
    bpy.ops.object.mode_set(mode='EDIT')
    # not sure why is this is needed 
    bpy.ops.mesh.reveal()
    # FIXME: noticed by admin @ 2017-10-26 14:34:18
    # need to improve the logic
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_all(action='SELECT')
    # tiangulate... 
    bpy.ops.mesh.quads_convert_to_tris( quad_method='BEAUTY', ngon_method='BEAUTY')
    bpy.ops.object.mode_set(mode='OBJECT')


def smart_bake():
    """
    bake 
    """
    actObj = bpy.context.scene.objects.active
    bpy.ops.object.duplicate()
    bpy.ops.object.transform_apply( location=False, rotation=True, scale=True)
    triangulate_selected()

    # get bmesh from active object
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    bm.faces.ensure_lookup_table()
    face_count = len(bm.faces)

    for faceid in range (0, face_count):
        #set default values for multiplication of vectors (uv and physical area of object)
        multiVector = 0
        gmmultiVector = 0
        #UV Area calculating
        #get uv-coordinates of vertexes of current triangle
        loopA = bm.faces[faceid].loops[0][bm.loops.layers.uv.active].uv
        loopB = bm.faces[faceid].loops[1][bm.loops.layers.uv.active].uv
        loopC = bm.faces[faceid].loops[2][bm.loops.layers.uv.active].uv
        #get multiplication of vectors of current triangle
        multiVector = Vector2dMultiple(loopA, loopB, loopC)
        #Increment area of current tri to total uv area
        Area+=0.5*multiVector

        #Phisical Area calculating
        #get world coordinates of vertexes of current triangle
        gmloopA = bm.faces[faceid].loops[0].vert.co
        gmloopB = bm.faces[faceid].loops[1].vert.co
        gmloopC = bm.faces[faceid].loops[2].vert.co
        #get multiplication of vectors of current triangle
        gmmultiVector = Vector3dMultiple(gmloopA, gmloopB, gmloopC)
        #Increment area of current tri to total phisical area
        gmArea += 0.5*gmmultiVector

# get all the selected objects
# get the scale up the 
# set the texel density to average
#


def calc_texel_density():
    """ calculate texel density
    """
    # make the given object as active
    actObj = bpy.data.objects['Cube']
    bpy.ops.object.select_all(action='DESELECT')
    actObj.select = True
    bpy.ops.object.duplicate()
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.reveal() # not sure 
    for v in bpy.context.active_object.data.vertices:
        v.select = True
    # bpy.ops.mesh.select_all(action='DESELECT')
    # bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')

    Area=0
    gmArea = 0
    textureSizeCurX = 1024
    textureSizeCurY = 1024
    
    
    #get bmesh from active object
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    # update the internal face table
    bm.faces.ensure_lookup_table()

    #get faces and round this
    face_count = len(bm.faces)
    for faceid in range (0, face_count):
        #set default values for multiplication of vectors (uv and physical area of object)
        multiVector = 0
        gmmultiVector = 0
        #UV Area calculating
        #get uv-coordinates of vertexes of current triangle
        loopA = bm.faces[faceid].loops[0][bm.loops.layers.uv.active].uv
        loopB = bm.faces[faceid].loops[1][bm.loops.layers.uv.active].uv
        loopC = bm.faces[faceid].loops[2][bm.loops.layers.uv.active].uv
        #get multiplication of vectors of current triangle
        multiVector = Vector2dMultiple(loopA, loopB, loopC)
        #Increment area of current tri to total uv area
        Area+=0.5*multiVector

        #Phisical Area calculating
        #get world coordinates of vertexes of current triangle
        gmloopA = bm.faces[faceid].loops[0].vert.co
        gmloopB = bm.faces[faceid].loops[1].vert.co
        gmloopC = bm.faces[faceid].loops[2].vert.co
        #get multiplication of vectors of current triangle
        gmmultiVector = Vector3dMultiple(gmloopA, gmloopB, gmloopC)
        #Increment area of current tri to total phisical area
        gmArea += 0.5*gmmultiVector
        
    #UV Area in percents
    UVspace = Area * 100

    aspectRatio = textureSizeCurX / textureSizeCurY
    if aspectRatio < 1:
        aspectRatio = 1 / aspectRatio
    largestSide = textureSizeCurX if textureSizeCurX > textureSizeCurY else textureSizeCurY
    #TexelDensity calculating from selected in panel texture size
    TexelDensity = ((largestSide / math.sqrt(aspectRatio)) * math.sqrt(Area))/(math.sqrt(gmArea)*100) / bpy.context.scene.unit_settings.scale_length

    # #show calculated values on panel
    UVspace = '%.3f' % round(UVspace, 3) + ' %'
    texel_density = '%.3f' % round(TexelDensity, 3)

    print (UVspace, texel_density)

    return (UVspace, texel_density)
