from PIL import Image
import math
from urllib.request import urlretrieve
from os.path import isfile

source_file = "world_map.jpg"
if not isfile(source_file):
    urlretrieve("https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73776/world.topo.bathy.200408.3x5400x2700.jpg", source_file)
world_map = Image.open(source_file)
input_pixels = world_map.load()

output_size = 768
output = Image.new("RGBA", (output_size, output_size))
output_pixels = output.load()

for i in range(output.size[0]):
    for j in range(output.size[1]):
        x = (2.0 * i / output.size[0] - 1.0)
        y = (2.0 * j / output.size[1] - 1.0)
        if x**2 + y**2 < 1.0:
            z = math.sqrt(1.0 - x**2 - y**2)
            theta = math.atan2(y, x) % (2 * math.pi)
            phi = math.acos(z)
            x = int(theta / (2 * math.pi) * world_map.size[0])
            y = int(phi / math.pi * world_map.size[1])
            r, g, b = input_pixels[x, y]
            output_pixels[i, j] = (r, g, b, 255)
        else:
            output_pixels[i, j] = (0, 0, 0, 0)

output.save("output.png")
output.show()
