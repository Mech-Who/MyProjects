import random
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Shader, RenderState, ShaderAttrib, LVecBase4f, PNMImage, loadPrcFileData, CardMaker

loadPrcFileData(
    "",
    """
    textures-power-2 none
    show-buffers #t
    show-frame-rate-meter #t
    frame-rate-meter-milliseconds #t
    """)

base = ShowBase()

shaderVert = """
#version 150
// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
// Vertex inputs
in vec4 p3d_Vertex;
void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}
"""

shaderFrag = """
#version 150
// Our models color
uniform vec4 objectColor;
// Output to the screen
out vec4 p3d_FragColor;
void main() {
    // convert colors from 0-255 range to 0-1 range
    float r = objectColor.x / 255;
    float g = objectColor.y / 255;
    float b = objectColor.z / 255;
    // Now set the color of the model
    // we currently ignore alpha. If this is important, just add it.
    p3d_FragColor = vec4(r,g,b,1);
}
"""


# this map will contain colors and their respective models
pick_map = {}

used_color_list = []
def get_random_color():
    global used_color_list
    # get the maximum color value (usually will be 255)
    maxVal = PNMImage().get_maxval()
    # search for an unused color value
    while True:
        r = random.randrange(0, maxVal)
        g = random.randrange(0, maxVal)
        b = random.randrange(0, maxVal)
        color = LVecBase4f(r, g, b, maxVal)
        if color not in used_color_list:
            # found a good color, store and return it
            used_color_list.append(color)
            return color

def arrange():
    # add some pickable models
    for i in range(5):
        # The color for the model. Must be integer values between 0 and 255 to
        # be able to accurately pick the color again later on
        pick_col = get_random_color()
        model = loader.loadModel("panda")
        model.name = f"Panda{i}"
        model.reparent_to(base.render)
        model.set_x(random.randrange(-15, 15))
        model.set_y(random.randint(50, 150))
        model.set_z(random.randrange(-20, 5))
        model.set_shader_input("objectColor", pick_col)
        pick_map[pick_col] = model

def rearrange():
    for panda in list(render.find_all_matches("**/Panda*")):
        panda.remove_node()

    arrange()

# load our shader
shader = Shader.make(Shader.SL_GLSL, shaderVert, shaderFrag)

picker_buffer = None

def pick():
    x = 0
    y = 0
    if base.mouseWatcherNode.hasMouse():
        # get the current mousepointer location
        x = int(base.win.get_pointer(0).get_x())
        y = int(base.win.get_pointer(0).get_y())
    else:
        # we don't have a mousepointer location, hence we can't pick anything
        return

    # create the buffer we render in
    picker_buffer = base.win.makeTextureBuffer("picking Buffer", base.win.getSize()[0], base.win.getSize()[1], to_ram=True)
    picker_buffer.setSort(-100)

    # set up a camera which we use to fill the buffer
    picker_cam = base.makeCamera(picker_buffer)
    # "render" should be the root node that contains the pickable objects. It
    # may not always be "render"
    picker_cam.reparentTo(render)
    # copy our main cameras position and rotation
    picker_cam.set_pos(camera.get_pos())
    picker_cam.set_hpr(camera.get_hpr())

    # load the shader on the camera
    picker_cam.node().setInitialState(RenderState.make(ShaderAttrib.make(shader, 100000)))

    # render two frames to get the buffer actually filled and usable
    base.graphicsEngine.renderFrame()
    base.graphicsEngine.renderFrame()

    # convert the rendered texture into a PNM Image
    picker_img = PNMImage(base.win.getSize()[0], base.win.getSize()[1])
    picker_texture = picker_buffer.getTexture()
    picker_texture.store(picker_img)

    # get the color at the mouse position
    col = LVecBase4f(
        picker_img.getRedVal(x,y),
        picker_img.getGreenVal(x,y),
        picker_img.getBlueVal(x,y),
        picker_img.getAlphaVal(x,y))

    # deselect all models
    for mapCol, model in pick_map.items():
        model.clear_color_scale()

    # select the model with the picked color
    if col in pick_map.keys():
        pick_map[col].setColorScale(1, 1, 0, 1)

    # clear up our buffer window
    base.graphicsEngine.removeWindow(picker_buffer)


base.accept("mouse1-up", pick)
base.accept("r", rearrange)

#initial random arrangement of pandas
arrange()

base.run()