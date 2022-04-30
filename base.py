# coding=utf-8

from asyncio.windows_utils import pipe
import glfw
from OpenGL.GL import *
import numpy as np
import sys, os.path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grafica.gpu_shape import GPUShape
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.scene_graph as sg
from grafica.assets_path import getAssetPath
from controlador import Controller

#Funcion para saber si el cursor esta sobre una textura

def cursor_in(controller, node):
    a = tr.matmul([sg.findTransform(mundo, node.name),
    [[-0.5, 0.5],  
    [-0.5, 0.5],
    [0, 0],
    [1, 1]]])
    (x, y) = (a[0], a[1])
    mousePosX = 2 * (controller.mousePos[0] - width / 2) / width
    mousePosY = 2 * (height / 2 - controller.mousePos[1]) / height
    if x[0] < mousePosX < x[1]:
        if y[0] < mousePosY < y[1]:
            return True
    return False



# Programa

if __name__ == "__main__":

    window = None
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1200
    height = 600

    window = glfw.create_window(width, height, "Desktop", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    controller = Controller()
    glfw.set_key_callback(window, controller.on_key)
    glfw.set_cursor_pos_callback(window, controller.cursor_pos_callback)
    glfw.set_mouse_button_callback(window, controller.mouse_button_callback)

    pipeline = es.SimpleTextureTransformShaderProgram()

    glUseProgram(pipeline.shaderProgram)

    glClearColor(0.75, 0.75, 0.75, 1)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Creamos las texturas y GPU, modelamos jerarquicamente

    wallpaper_node = sg.SceneGraphNode('desktop')
    wallpaper_shape = bs.createTextureQuad(1,1)
    wallpaper_gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(wallpaper_gpu)
    wallpaper_gpu.fillBuffers(wallpaper_shape.vertices, wallpaper_shape.indices, GL_STATIC_DRAW)
    wallpaper_gpu.texture = es.textureSimpleSetup(
        getAssetPath('escritorio.jpg'), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    wallpaper_node.transform = tr.scale(2,2,1)
    wallpaper_node.childs += [wallpaper_gpu]

    folder_icon_node = sg.SceneGraphNode('folder_icon')
    folder_icon_shape = bs.createTextureQuad(1,1)
    folder_icon_gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(folder_icon_gpu)
    folder_icon_gpu.fillBuffers(folder_icon_shape.vertices, folder_icon_shape.indices, GL_STATIC_DRAW)
    folder_icon_gpu.texture = es.textureSimpleSetup(
        getAssetPath('folder.png'), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    folder_icon_node.transform = tr.matmul([tr.translate(-0.8, 0.65, 0), tr.scale(0.25, 0.5, 1)])
    folder_icon_node.childs += [folder_icon_gpu]
    
    app_icon_node = sg.SceneGraphNode('app_icon')
    app_icon_shape = bs.createTextureQuad(1,1)
    app_icon_gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(app_icon_gpu)
    app_icon_gpu.fillBuffers(app_icon_shape.vertices, app_icon_shape.indices, GL_STATIC_DRAW)
    app_icon_gpu.texture = es.textureSimpleSetup(
        getAssetPath('wheel.png'), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    app_icon_node.transform = tr.matmul([tr.translate(-0.8, 0.1, 0), tr.scale(0.25, 0.5, 1)])
    app_icon_node.childs += [app_icon_gpu]
  
    black_back_shape = bs.createTextureQuad(1, 1)
    black_back_gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(black_back_gpu)
    black_back_gpu.fillBuffers(black_back_shape.vertices, black_back_shape.indices, GL_STATIC_DRAW)
    black_back_gpu.texture = es.textureSimpleSetup(
        getAssetPath('black_back.jpg'), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

    black_back_node = sg.SceneGraphNode('black_back')
    black_back_node.transform = tr.matmul([tr.translate(0,-0.875,0),tr.scale(2,0.25,1)])
    black_back_node.childs += [black_back_gpu]

    task_app_icon_node = sg.SceneGraphNode('task_app_icon')
    task_app_icon_node.transform = tr.matmul([tr.translate(0.93, -0.875, 0), tr.scale(0.125, 0.25, 1)])
    task_app_icon_node.childs += [app_icon_gpu]

    task_folder_icon_node = sg.SceneGraphNode('task_folder_icon')
    task_folder_icon_node.transform = tr.matmul([tr.translate(0.81, -0.875, 0), tr.scale(0.1, 0.2, 1)])
    task_folder_icon_node.childs += [folder_icon_gpu]

    # Bike Simulator

    sky_node = sg.SceneGraphNode('sky')
    sky_shape = bs.createTextureQuad(1, 1)
    sky_gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(sky_gpu)
    sky_gpu.fillBuffers(sky_shape.vertices, sky_shape.indices, GL_STATIC_DRAW)
    sky_gpu.texture = es.textureSimpleSetup(
        getAssetPath('sky.png'), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    sky_node.transform = tr.identity()
    sky_node.childs += [sky_gpu]

    road_node = sg.SceneGraphNode('road')
    road_shape = bs.createTextureQuad(1, 1)
    road_gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(road_gpu)
    road_gpu.fillBuffers(road_shape.vertices, road_shape.indices, GL_STATIC_DRAW)
    road_gpu.texture = es.textureSimpleSetup(
        getAssetPath('road.png'), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    road_node.transform = tr.identity()
    road_node.childs += [road_gpu]

    app_background_node = sg.SceneGraphNode('app_background')
    app_background_node.transform = tr.identity()
    app_background_node.childs += [sky_node, road_node]

    bike_node = sg.SceneGraphNode('bike')
    bike_shape = bs.createTextureQuad(1, 1)
    bike_gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(bike_gpu)
    bike_gpu.fillBuffers(bike_shape.vertices, bike_shape.indices, GL_STATIC_DRAW)
    bike_gpu.texture = es.textureSimpleSetup(
        getAssetPath('bike.png'), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    bike_node.transform = tr.matmul([tr.scale(0.3, 0.5, 1)])
    bike_node.childs += [bike_gpu]

    wheel_node = sg.SceneGraphNode('wheel')
    wheel_shape = bs.createTextureQuad(1, 1)
    wheel_gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(wheel_gpu)
    wheel_gpu.fillBuffers(wheel_shape.vertices, wheel_shape.indices, GL_STATIC_DRAW)
    wheel_gpu.texture = es.textureSimpleSetup(
        getAssetPath('wheel.png'), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)
    wheel_node.transform = tr.identity()
    wheel_node.childs += [wheel_gpu]

    Rwheel_node = sg.SceneGraphNode('Rwheel')
    Rwheel_node.childs += [wheel_node]

    Lwheel_node = sg.SceneGraphNode('Lwheel')
    Lwheel_node.childs += [wheel_node]


    Bike_node = sg.SceneGraphNode('Bike')
    Bike_node.transform = tr.identity()
    Bike_node.childs += [Lwheel_node, Rwheel_node, bike_node]

    yellow_shape = bs.createTextureQuad(1, 1)
    yellow_gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(yellow_gpu)
    yellow_gpu.fillBuffers(yellow_shape.vertices, yellow_shape.indices, GL_STATIC_DRAW)
    yellow_gpu.texture = es.textureSimpleSetup(
        getAssetPath('yellow.png'), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

    x_shape = bs.createTextureQuad(1, 1)
    x_gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(x_gpu)
    x_gpu.fillBuffers(x_shape.vertices, x_shape.indices, GL_STATIC_DRAW)
    x_gpu.texture = es.textureSimpleSetup(
        getAssetPath('x.png'), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

    square_shape = bs.createTextureQuad(1, 1)
    square_gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(square_gpu)
    square_gpu.fillBuffers(square_shape.vertices, square_shape.indices, GL_STATIC_DRAW)
    square_gpu.texture = es.textureSimpleSetup(
        getAssetPath('square.png'), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

    x_node = sg.SceneGraphNode('x')
    x_node.transform = tr.matmul([tr.translate(0.47,0,0), tr.scale(0.04,0.08,1)])
    x_node.childs += [x_gpu]

    square_node = sg.SceneGraphNode('square')
    square_node.transform = tr.matmul([tr.translate(0.42,0,0), tr.scale(0.04,0.08,1)])
    square_node.childs += [square_gpu]

    app_taskbar_back_node = sg.SceneGraphNode('app_taskbar_back')
    app_taskbar_back_node.transform = tr.matmul([tr.scale(1,0.1,1)])
    app_taskbar_back_node.childs += [yellow_gpu]

    app_taskbar_node = sg.SceneGraphNode('app_taskbar')
    app_taskbar_node.transform = tr.matmul([tr.translate(0,0.45,0)])
    app_taskbar_node.childs += [app_taskbar_back_node, x_node, square_node]

    left_border_app = sg.SceneGraphNode('left_border_app')
    left_border_app.transform = tr.matmul([tr.translate(-0.49, 0, 0), tr.scale(0.02, 1, 1)])
    left_border_app.childs += [yellow_gpu]

    right_border_app = sg.SceneGraphNode('right_border_app')
    right_border_app.transform = tr.matmul([tr.translate(0.49, 0, 0), tr.scale(0.02, 1, 1)])
    right_border_app.childs += [yellow_gpu]

    under_border_app = sg.SceneGraphNode('under_border_app')
    under_border_app.transform = tr.matmul([tr.translate(0, -0.48, 0), tr.scale(1, 0.04, 1)])
    under_border_app.childs += [yellow_gpu]

    border_app = sg.SceneGraphNode('border_app')
    border_app.childs += [left_border_app, right_border_app, under_border_app]

    # folder

    folder_back_node = sg.SceneGraphNode('folder')
    folder_back_node.transform = tr.identity()
    folder_back_node.childs += [black_back_gpu]

    x2_node = sg.SceneGraphNode('x2')
    x2_node.transform = tr.matmul([tr.translate(0.47,0,0), tr.scale(0.04,0.08,1)])
    x2_node.childs += [x_gpu]

    square2_node = sg.SceneGraphNode('square2')
    square2_node.transform = tr.matmul([tr.translate(0.42,0,0), tr.scale(0.04,0.08,1)])
    square2_node.childs += [square_gpu]

    folder_taskbar_back_node = sg.SceneGraphNode('folder_taskbar_back')
    folder_taskbar_back_node.transform = tr.matmul([tr.scale(1,0.1,1)])
    folder_taskbar_back_node.childs += [yellow_gpu]

    folder_taskbar_node = sg.SceneGraphNode('folder_taskbar')
    folder_taskbar_node.transform = tr.matmul([tr.translate(0,0.45,0)])
    folder_taskbar_node.childs += [folder_taskbar_back_node, x2_node, square2_node]

    left_border_folder = sg.SceneGraphNode('left_border_folder')
    left_border_folder.transform = tr.matmul([tr.translate(-0.49, 0, 0), tr.scale(0.02, 1, 1)])
    left_border_folder.childs += [yellow_gpu]

    right_border_folder = sg.SceneGraphNode('right_border_folder')
    right_border_folder.transform = tr.matmul([tr.translate(0.49, 0, 0), tr.scale(0.02, 1, 1)])
    right_border_folder.childs += [yellow_gpu]

    under_border_folder = sg.SceneGraphNode('under_border_folder')
    under_border_folder.transform = tr.matmul([tr.translate(0, -0.48, 0), tr.scale(1, 0.04, 1)])
    under_border_folder.childs += [yellow_gpu]

    border_folder = sg.SceneGraphNode('border_folder')
    border_folder.childs += [left_border_folder, right_border_folder, under_border_folder]


    # Ensamblamos todo al 'mundo'

    folder_node = sg.SceneGraphNode('folder')
    folder_node.transform = tr.translate(0.4,0.4,0)
    folder_node.childs += [folder_back_node, border_folder, folder_taskbar_node]

    app_node = sg.SceneGraphNode('app')
    app_node.transform = tr.translate(-0.4,-0.2,0)
    app_node.childs += [app_background_node, border_app, Bike_node, app_taskbar_node]

    taskbar = sg.SceneGraphNode('Taskbar')
    taskbar.childs += [black_back_node, task_folder_icon_node, task_app_icon_node]

    desktop = sg.SceneGraphNode('desktop')
    desktop.childs += [
        wallpaper_node,
        folder_icon_node,
        app_icon_node,
        taskbar
    ]

    mundo = sg.SceneGraphNode('mundo')
    mundo.childs += [desktop, folder_node, app_node]

    t0 = glfw.get_time()
    angulo = 0

    mousePosX = 0
    mousePosY = 0

    full_size = tr.matmul([tr.translate(0,0.125,0),tr.scale(2,1.75,1)])
    save_app_tr = full_size
    save_folder_tr = full_size

    while not glfw.window_should_close(window):

        glfw.poll_events()

        if (controller.leftClickOn):
            if cursor_in(controller, app_icon_node):
                if not app_node in mundo.childs:
                    mundo.childs += [app_node]
                    taskbar.childs += [task_app_icon_node]
            if cursor_in(controller, folder_icon_node):
                if not folder_node in mundo.childs:
                    mundo.childs += [folder_node]
                    taskbar.childs += [task_folder_icon_node]

            if app_node in mundo.childs:
                if folder_node in mundo.childs:
                    if cursor_in(controller, app_node) and not cursor_in(controller, folder_node):
                        mundo.childs.remove(app_node)
                        mundo.childs += [app_node]
                    if cursor_in(controller, folder_node) and not cursor_in(controller, app_node):
                        mundo.childs.remove(folder_node)
                        mundo.childs += [folder_node]


            if app_node == mundo.childs[-1]:
                if cursor_in(controller, app_taskbar_back_node):
                    app_node.transform = tr.matmul([tr.translate(dx,dy,0),app_node.transform])
                if cursor_in(controller, square_node):
                    (app_node.transform, save_app_tr) = (save_app_tr, app_node.transform)

                if cursor_in(controller, left_border_app):
                    app_node.transform = tr.matmul([
                        app_node.transform,tr.translate(dx, 0, 0),  tr.translate(-0.5,0,0),
                        tr.scale(1-dx,1,1), tr.translate(0.5,0,0)
                    ])

                if cursor_in(controller, right_border_app):
                    app_node.transform = tr.matmul([
                        app_node.transform,tr.translate(dx, 0, 0),  tr.translate(0.5,0,0),
                        tr.scale(1+dx,1,1), tr.translate(-0.5,0,0)
                    ])

                if cursor_in(controller, under_border_app):
                    app_node.transform = tr.matmul([
                        app_node.transform,tr.translate(0, dy, 0),  tr.translate(0,-0.5,0),
                        tr.scale(1, 1-dy, 1), tr.translate(0,0.5,0)
                    ])

                if cursor_in(controller, x_node):
                    mundo.childs.remove(app_node)
                    taskbar.childs.remove(task_app_icon_node)

            if folder_node == mundo.childs[-1]:
                if cursor_in(controller, folder_taskbar_back_node):
                    folder_node.transform = tr.matmul([tr.translate(dx,dy,0),folder_node.transform])
                if cursor_in(controller, square2_node):
                    (folder_node.transform, save_folder_tr) = (save_folder_tr, folder_node.transform)

                if cursor_in(controller, left_border_folder):
                    folder_node.transform = tr.matmul([
                        folder_node.transform,tr.translate(dx, 0, 0),  tr.translate(-0.5,0,0),
                        tr.scale(1-dx,1,1), tr.translate(0.5,0,0)
                    ])

                if cursor_in(controller, right_border_folder):
                    folder_node.transform = tr.matmul([
                        folder_node.transform,tr.translate(dx, 0, 0),  tr.translate(0.5,0,0),
                        tr.scale(1+dx,1,1), tr.translate(-0.5,0,0)
                    ])

                if cursor_in(controller, under_border_folder):
                    folder_node.transform = tr.matmul([
                        folder_node.transform,tr.translate(0, dy, 0),  tr.translate(0,-0.5,0),
                        tr.scale(1, 1-dy, 1), tr.translate(0,0.5,0)
                    ])

                if cursor_in(controller, x2_node):
                    mundo.childs.remove(folder_node)
                    taskbar.childs.remove(task_folder_icon_node)


        glClear(GL_COLOR_BUFFER_BIT)

        dx = 2 * (controller.mousePos[0] - width / 2) / width - mousePosX
        mousePosX = 2 * (controller.mousePos[0] - width / 2) / width

        dy = 2 * (height / 2 - controller.mousePos[1]) / height - mousePosY
        mousePosY = 2 * (height / 2 - controller.mousePos[1]) / height

        tf = glfw.get_time()
        dt = tf - t0
        t0 += tf

        angulo -= 0.05

        Rwheel_node.transform = tr.matmul([tr.translate(0.145, -0.19, 0) ,tr.scale(0.22, 0.44, 1), tr.rotationZ(angulo)])
        Lwheel_node.transform = tr.matmul([tr.translate(-0.14, -0.19, 0) ,tr.scale(0.22, 0.44, 1), tr.rotationZ(angulo)])


        sg.drawSceneGraphNode(mundo, pipeline, 'transform')

        glfw.swap_buffers(window)

    mundo.clear()
    glfw.terminate()