from PIL import Image, ImageDraw

file_name = "./results/"

im = Image.new( 'RGB', (500,500), "white") # create a new black image
draw = ImageDraw.Draw(im)
color = (0, 0, 0)
for i, route in enumerate(routes):
    r_c = (i*i)%255
    g_c = (i*r_c)%255
    b_c = (i*g_c)%255
    nodes = route.route
    norm = lambda x, y: (2*x + 250, 2*y + 250)
    draw.line([norm(*self.coords[n]) for n in nodes], fill=(r_c, g_c, b_c), width=2)
