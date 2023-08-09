import shutil
import os
import subprocess

blender_url_dict = {'2.70': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.70/blender-2.70-linux-glibc211-x86_64.tar.bz2",
                    '2.70a': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.70/blender-2.70a-linux-glibc211-x86_64.tar.bz2",
                    '2.71': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.71/blender-2.71-linux-glibc211-x86_64.tar.bz2",
                    '2.72': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.72/blender-2.72-linux-glibc211-x86_64.tar.bz2",
                    '2.72a': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.72/blender-2.72a-linux-glibc211-x86_64.tar.bz2",
                    '2.72b': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.72/blender-2.72b-linux-glibc211-x86_64.tar.bz2",
                    '2.73': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.73/blender-2.73-linux-glibc211-x86_64.tar.bz2",
                    '2.74': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.74/blender-2.74-linux-glibc211-x86_64.tar.bz2",
                    '2.75': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.75/blender-2.75-linux-glibc211-x86_64.tar.bz2",
                    '2.75a': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.75/blender-2.75a-linux-glibc211-x86_64.tar.bz2",
                    '2.76': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.76/blender-2.76-linux-glibc211-x86_64.tar.bz2",
                    '2.76b': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.76/blender-2.76b-linux-glibc211-x86_64.tar.bz2",
                    '2.77': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.77/blender-2.77-linux-glibc211-x86_64.tar.bz2",
                    '2.78': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.78/blender-2.78-linux-glibc211-x86_64.tar.bz2",
                    '2.78c': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.78/blender-2.78c-linux-glibc219-x86_64.tar.bz2",
                    '2.79': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.79/blender-2.79-linux-glibc219-x86_64.tar.bz2",
                    '2.79b': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.79/blender-2.79b-linux-glibc219-x86_64.tar.bz2",
                    '2.80rc3': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.80/blender-2.80rc3-linux-glibc217-x86_64.tar.bz2",
                    '2.81a': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.81/blender-2.81a-linux-glibc217-x86_64.tar.bz2",
                    '2.82a': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.82/blender-2.82a-linux64.tar.xz",
                    '2.83.19': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.83/blender-2.83.19-linux-x64.tar.xz",
                    '2.90.1': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.90/blender-2.90.1-linux64.tar.xz",
                    '2.91.2': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.91/blender-2.91.2-linux64.tar.xz",
                    '2.92.0': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.92/blender-2.92.0-linux64.tar.xz",
                    '2.93.8': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender2.93/blender-2.93.8-linux-x64.tar.xz",
                    '3.0.1': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender3.0/blender-3.0.1-linux-x64.tar.xz",
                    '3.1.0': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender3.1/blender-3.1.0-linux-x64.tar.xz",
                    '3.1.1': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender3.1/blender-3.1.1-linux-x64.tar.xz",
                    '3.1.2': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender3.1/blender-3.1.2-linux-x64.tar.xz",
                    '3.2.0': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender3.2/blender-3.2.0-linux-x64.tar.xz",
                    '3.2.1': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender3.2/blender-3.2.1-linux-x64.tar.xz",
                    '3.2.2': "https://ftp.nluug.nl/pub/graphics/blender/release/Blender3.2/blender-3.2.2-linux-x64.tar.xz",
                    '3.3.0': "https://download.blender.org/release/Blender3.3/blender-3.3.0-linux-x64.tar.xz",
                    '3.6.1': "https://download.blender.org/release/Blender3.6/blender-3.6.1-linux-x64.tar.xz"
                    }


def setup(blenderVersionOrUrl, isBlenderUrl):
    blender_url = None
    blenderVersion = None
    if (isBlenderUrl == True):
        blender_url = blenderVersionOrUrl
        blenderVersion = blenderVersionOrUrl.rsplit('/', 1)[1]
    else:
        blenderVersion = blenderVersionOrUrl
        base_url = f"blender-{blenderVersion}-linux-x64.tar.xz"
        blender_url = os.path.join("/gdrive/My Drive/blender", base_url)

    base_url = os.path.basename(blender_url)

    try:
        # Check if the binary file already exists
        if os.path.exists(os.path.join("/content", base_url.replace(".tar.xz", ""))):
            print("Blender binary already exists...")
            return base_url.replace(".tar.xz", "")

        print("Installing blender = " + blenderVersion)
        print("blender_url = " + blender_url)
        print("base_url = " + base_url)

        # Copy the binary file to the content folder
        subprocess.run(['cp', blender_url, '/content/'], encoding="utf-8",
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print("Copied blender to content folder")

        # Extract the binary file
        subprocess.run(["tar", "xf", base_url], encoding="utf-8",
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print("Blender installed..." + blenderVersion)

        return base_url.replace(".tar.xz", "")
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
