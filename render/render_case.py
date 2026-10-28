# Product renders of the assembled case on an oak desk, for the README.
# Run: /Applications/Blender.app/Contents/MacOS/Blender -b -P render/render_case.py [-- shot ...]   (PREVIEW=1: quick low-res pass)
# Parts come from the viewer meshes in docs/mesh/ (assembly coordinates, mm, flat triangle lists), default variants.
# Assets (CC0, Poly Haven): artist_workshop HDRI, oak_veneer_01 texture, in render/assets/.
import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(HERE, "assets")
MESH = os.path.join(ROOT, "docs", "mesh")
OUT = os.path.join(ROOT, "docs")
RES = (1800, 1350) if "PREVIEW" not in os.environ else (600, 450)
SAMPLES = 256 if "PREVIEW" not in os.environ else 32
CENTER = Vector((86.0, 105.5, -14.2))   # footprint centre, underside of the feet (mm)

# viewer palettes: body, panels, feet
PALETTES = {"graphite": ("#2b2e33", "#1c1d20", "#1a1b1e"), "bone": ("#e4dfd3", "#1c1d20", "#1a1b1e")}
# file, colour group (or a fixed hardware colour), roughness
PARTS = [("lid", 0, 0.42), ("body_upper", 0, 0.42), ("body_lower", 0, 0.42), ("side_upper", 0, 0.42),
         ("side_lower", 0, 0.42), ("psu_support", 0, 0.42), ("strip__controls", 1, 0.45), ("faceplate__mesh", 1, 0.5),
         ("front_lower__screen", 1, 0.35), ("foot", 2, 0.6),
         ("ref_board", "#16291d", 0.5), ("ref_gpu", "#23262b", 0.5), ("ref_bracket", "#b8bcc2", 0.3),
         ("ref_cooler", "#8a8f96", 0.35), ("ref_psu", "#202226", 0.5), ("ref_ssd", "#5b6066", 0.5),
         ("ref_fan_top", "#1e2024", 0.5), ("ref_fan_bottom", "#1e2024", 0.5), ("rotor_top", "#1e2024", 0.5),
         ("rotor_bottom", "#1e2024", 0.5), ("rotor_cpu", "#1e2024", 0.5), ("rotor_gpu", "#1e2024", 0.5),
         ("rotor_psu", "#1e2024", 0.5), ("ref_lcd", "#050506", 0.05)]
FEET = [(0, 0), (151, 0), (0, 176), (151, 176)]   # viewer copies of the one foot mesh (mm)
LAYERED = ("body_upper", "body_lower")           # printed upright: 0.2 mm layer lines show on the walls


def linear(hexcol):
    c = [int(hexcol[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    for dev in ("OPTIX", "CUDA", "METAL"):
        try:
            prefs.compute_device_type = dev
        except TypeError:   # not in this build
            continue
        if any(d.type == dev for d in prefs.get_devices_for_type(dev)):
            break
    prefs.get_devices()
    for d in prefs.devices:
        d.use = True
    sc.cycles.device = "GPU"
    sc.cycles.samples = SAMPLES
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    sc.view_settings.exposure = 0.6


def world(rot=110):
    w = bpy.data.worlds.new("World")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(os.path.join(ASSETS, "artist_workshop_2k.hdr"))
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value[2] = math.radians(rot)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
    bg = next(n for n in nt.nodes if n.type == "BACKGROUND")
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])


def desk():
    bpy.ops.mesh.primitive_plane_add(size=1)
    d = bpy.context.object
    d.scale = (1.6, 1.0, 1)
    m = bpy.data.materials.new("Oak")
    m.use_nodes = True
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1.6, 1.0, 1)   # texture tile = 1 m
    nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])

    def tex(name, colorspace):
        t = nt.nodes.new("ShaderNodeTexImage")
        t.image = bpy.data.images.load(os.path.join(ASSETS, name))
        t.image.colorspace_settings.name = colorspace
        nt.links.new(mp.outputs["Vector"], t.inputs["Vector"])
        return t

    nt.links.new(tex("oak_veneer_01_diff_2k.jpg", "sRGB").outputs["Color"], p.inputs["Base Color"])
    nt.links.new(tex("oak_veneer_01_rough_2k.jpg", "Non-Color").outputs["Color"], p.inputs["Roughness"])
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nt.links.new(tex("oak_veneer_01_nor_gl_2k.jpg", "Non-Color").outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], p.inputs["Normal"])
    d.data.materials.append(m)


def material(name, color, rough, layers):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    p.inputs["Base Color"].default_value = color
    p.inputs["Roughness"].default_value = rough
    if name == "ref_bracket" or name == "ref_cooler":
        p.inputs["Metallic"].default_value = 0.8
    if layers:   # bands along Z in object space (metres): period 0.314 / 1571 = 0.2 mm
        tc = nt.nodes.new("ShaderNodeTexCoord")
        wave = nt.nodes.new("ShaderNodeTexWave")
        wave.wave_type = "BANDS"
        wave.bands_direction = "Z"
        wave.inputs["Scale"].default_value = 1571.0
        bump = nt.nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value = 0.15
        bump.inputs["Distance"].default_value = 0.00004
        nt.links.new(tc.outputs["Object"], wave.inputs["Vector"])
        nt.links.new(wave.outputs["Fac"], bump.inputs["Height"])
        nt.links.new(bump.outputs["Normal"], p.inputs["Normal"])
    return m


def part(file, mat, offsets=((0, 0),)):
    pos = json.load(open(os.path.join(MESH, file + ".json")))
    verts, faces = [], []
    for dx, dy in offsets:
        base = len(verts)
        verts += [((pos[i] + dx - CENTER.x) / 1000, (pos[i + 1] + dy - CENTER.y) / 1000, (pos[i + 2] - CENTER.z) / 1000)
                  for i in range(0, len(pos), 3)]
        faces += [(base + i, base + i + 1, base + i + 2) for i in range(0, len(pos) // 3, 3)]
    me = bpy.data.meshes.new(file)
    me.from_pydata(verts, [], faces)
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)   # the viewer stores unshared triangles
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(file, me)
    bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(30))
    o.select_set(False)
    me.materials.append(mat)
    return o


def case(palette):
    cols = [linear(c) for c in PALETTES[palette]]
    for file, group, rough in PARTS:
        color = cols[group] if isinstance(group, int) else linear(group)
        mat = material(file, color, rough, file in LAYERED)
        part(file, mat, FEET if file == "foot" else ((0, 0),))


def camera(target, dist, az, el, lens, fstop, focus=None):
    """Orbit camera: az 0 looks at the front (-Y side), positive towards the left side (-X), el above the desk, degrees."""
    a, e = math.radians(az), math.radians(el)
    loc = Vector(target) + dist * Vector((-math.cos(e) * math.sin(a), -math.cos(e) * math.cos(a), math.sin(e)))
    c = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
    bpy.context.scene.collection.objects.link(c)
    c.location = loc
    c.rotation_euler = (Vector(target) - loc).to_track_quat("-Z", "Y").to_euler()
    c.data.lens = lens
    c.data.dof.use_dof = True
    c.data.dof.aperture_fstop = fstop
    c.data.dof.focus_distance = (Vector(focus or target) - loc).length
    bpy.context.scene.camera = c


def shot(name, palette, cam, world_rot=110):
    reset()
    world(world_rot)
    desk()
    case(palette)
    camera(**cam)
    bpy.context.scene.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)
    print("wrote", bpy.context.scene.render.filepath)


MID = (0.0, 0.0, 0.135)   # case centre, metres above the desk
SHOTS = {
    "hero":  lambda: shot("render-01-hero.png", "graphite", dict(target=MID, dist=1.15, az=-35, el=14, lens=70, fstop=5.6)),
    "front": lambda: shot("render-02-front.png", "graphite", dict(target=MID, dist=1.2, az=0, el=5, lens=85, fstop=4.0)),
    "rear":  lambda: shot("render-03-rear.png", "graphite", dict(target=MID, dist=1.15, az=145, el=16, lens=70, fstop=5.6)),
    "bone":  lambda: shot("render-04-bone.png", "bone", dict(target=MID, dist=1.15, az=35, el=14, lens=70, fstop=5.6)),
}
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else list(SHOTS)
for s in args:
    SHOTS[s]()
