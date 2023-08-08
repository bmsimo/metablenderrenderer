import os
import subprocess

blender_url_dict = {'3.2.2': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender3.2/blender-3.2.2-linux-x64.tar.xz",
                    '3.6.1': "https://download.blender.org/release/Blender3.6/blender-3.6.1-linux-x64.tar.xz"
                    }


def setup(blenderVersionOrPath, isBlenderPath):
    blender_path = None
    blenderVersion = None
    if (isBlenderPath == True):
        blender_path = blenderVersionOrPath
        blenderVersion = os.path.basename(blender_path)
    else:
        blender_path = os.path.join(
            '/gdrive/My Drive/blender/', blenderVersionOrPath)
        blenderVersion = blenderVersionOrPath

    try:
        print("Installing blender = " + blenderVersion)
        subprocess.run(["tar", "xf", blender_path], encoding="utf-8",
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Blender installed..." + blenderVersion)
        return os.path.splitext(blenderVersion)[0]
    except subprocess.CalledProcessError as e:
        print("Something went wrong..... Blender library installation failed.....")
        print(e.output)


def enable_rendering(gpu_enabled, cpu_enabled):
    data = "import re\n" +\
        "import bpy\n" +\
        "scene = bpy.context.scene\n" +\
        "scene.cycles.device = 'GPU'\n" +\
        "prefs = bpy.context.preferences\n" +\
        "prefs.addons['cycles'].preferences.get_devices()\n" +\
        "cprefs = prefs.addons['cycles'].preferences\n" +\
        "print(cprefs)\n" +\
        "for compute_device_type in ('CUDA', 'OPENCL', 'NONE'):\n" +\
        "    try:\n" +\
        "        cprefs.compute_device_type = compute_device_type\n" +\
        "        print('Device found:',compute_device_type)\n" +\
        "        break\n" +\
        "    except TypeError:\n" +\
        "        pass\n" +\
        "for device in cprefs.devices:\n" +\
        "    if not re.match('intel', device.name, re.I):\n" +\
        "        print('Activating',device)\n" +\
        "        device.use = "+str(gpu_enabled)+"\n" +\
        "    else:\n" +\
        "        device.use = "+str(cpu_enabled)+"\n"
    with open('setgpu.py', 'w') as f:
        f.write(data)
