from metalabblender import blender, tokenhandler, ldpreload, setupblender, datalog, filedownload
import subprocess
import sys
import os


class Blender:

    token = None
    blenderFilePath = None
    isFileUrl = None
    outputPath = None
    blenderVersion = None
    isBlenderUrl = None
    fileFormat = None
    renderEngine = None
    startFrame = None
    endFrame = None
    renderer = None
    animation = None
    audio = None
    logEnable = None
    blenderInstallPath = None
    pythonExpression = None

    def __init__(self, blenderFilePath, isFileUrl, outputPath, blenderVersion, isBlenderUrl, fileFormat,
                 renderEngine, startFrame, endFrame, renderer, animation, audio, logEnable, token, pythonExpression):
        self.token = token
        self.blenderFilePath = blenderFilePath
        self.isFileUrl = isFileUrl
        self.outputPath = outputPath
        self.blenderVersion = blenderVersion
        self.isBlenderUrl = isBlenderUrl
        self.fileFormat = fileFormat
        self.renderEngine = renderEngine
        self.startFrame = startFrame
        self.endFrame = endFrame
        self.renderer = renderer
        self.animation = animation
        self.audio = audio
        self.logEnable = logEnable
        self.pythonExpression = pythonExpression

    def gpu_setup():
        gpu = subprocess.run(["nvidia-smi", "--query-gpu=gpu_name", "--format=csv,noheader"],
                             encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        gpu = gpu.stdout
        print("Current GPU: " + gpu)

    def set_renderer(self):
        if self.optixEnabled:
            self.renderer = "OPTIX"

    def setup(self):
        # tokenhandler.TokenHandler.validate(self.token)
        # Blender.set_renderer(self)
        Blender.gpu_setup()
        ldpreload.preload()
        self.blenderInstallPath = '/gdrive/My Drive/blender-3.6.1-linux-x64/'
        if (self.isFileUrl == True):
            self.blenderFilePath = filedownload.download_from_url(
                self.blenderFilePath)
        # setupblender.enable_rendering(self.gpuEnabled, self.cpuEnabled)
        print("Setup completed")

    def render(self):
        print("starting to process blender...")
        blender_binary = './'+self.blenderInstallPath+"/blender"
        if (self.animation):
            if self.startFrame == self.endFrame:
                args = [blender_binary,
                        "-b", self.blenderFilePath,
                        "-E", self.renderEngine,
                        "-o", self.outputPath,
                        "-F", self.fileFormat,
                        "-a", "--", "--cycles-device", self.renderer
                        ]
            else:
                args = [blender_binary,
                        "-b", self.blenderFilePath,
                        "-E", self.renderEngine,
                        "-o", self.outputPath,
                        "-s", str(self.startFrame),
                        "-e", str(self.endFrame),
                        "-F", self.fileFormat,
                        "-a", "--", "--cycles-device", self.renderer
                        ]
        else:
            args = [blender_binary,
                    "-b", self.blenderFilePath,
                    "-E", self.renderEngine,
                    "-o", self.outputPath,
                    "-F", self.fileFormat,
                    "-f", str(self.startFrame),
                    "--", "--cycles-device", self.renderer
                    ]

        if (self.audio == False):
            args.insert(3, "-noaudio")
            if (self.logEnable == True):
                args.insert(6, "--log-level")
                args.insert(7, "1")
        else:
            if (self.logEnable == True):
                args.insert(5, "--log-level")
                args.insert(6, "1")

        if self.pythonExpression:
            python_expr = "--python-expr \"import bpy; bpy.context.scene.render.resolution_x = 720; bpy.context.scene.render.resolution_y = 1280;bpy.context.scene.render.image_settings.color_mode = 'RGBA';bpy.context.scene.render.image_settings.color_depth = '8';bpy.context.scene.render.image_settings.compression = 0\""
            args.extend([python_expr])

        try:
            print(' '.join(args))
            process = subprocess.Popen(args, stdout=subprocess.PIPE)
            while process.poll() is None:
                l = process.stdout.readline()
                if (self.logEnable == True):
                    print(l)
            print(process.stdout.read())
            print("Blender Completed...............................................")
        except subprocess.CalledProcessError as e:
            print("Something went wrong..... Blender file did not executed.....")
            print(e.output)
