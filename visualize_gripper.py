#!/usr/bin/env python3
import argparse, json, pathlib, numpy as np, trimesh, pyrender, imageio
from sample import create_gripper                   # ← 1

def load_data(j):
    d = json.load(open(j))
    return (pathlib.Path(d['object']).expanduser(),
            np.asarray(d['transforms']),
            np.asarray(d.get('quality_number_of_contacts', [])))

def build_scene(mesh_path, transforms, alpha=0.7):
    scene = pyrender.Scene(bg_color=[1,1,1,0])
    scene.add(pyrender.Mesh.from_trimesh(trimesh.load_mesh(mesh_path),
                                         smooth=False))

    # 2 ─ меш Panda-грипера
    gmesh = pyrender.Mesh.from_trimesh(create_gripper('panda').hand,
                                       smooth=False)
    gmesh.primitives[0].material.baseColorFactor[3] = alpha   # прозрачность

    for T in transforms:
        scene.add(gmesh, pose=T)          # 3 ─ добавляем во всех позах
    return scene

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('json')
    ap.add_argument('--save', metavar='PNG')
    args = ap.parse_args()

    mesh, T, _ = load_data(args.json)
    scene = build_scene(mesh, T)

    if args.save:
        with pyrender.OffscreenRenderer(800,600) as r:
            img,_ = r.render(scene)
        imageio.imwrite(args.save, img)
        print('saved', args.save)

    pyrender.Viewer(scene, use_raymond_lighting=True)

if __name__ == '__main__':
    main()
