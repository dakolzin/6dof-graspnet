#!/usr/bin/env python3
# visualize_grasps.py
#
#   pip install trimesh pyrender pyglet imageio
#
#   python visualize_grasps.py tmp.json            # интерактивное окно
#   python visualize_grasps.py tmp.json --save img.png   # ещё и PNG

import argparse, json, pathlib, numpy as np, trimesh, pyrender, imageio

def load_data(json_path):
    data = json.load(open(json_path))
    mesh_file = pathlib.Path(data["object"]).expanduser()
    if not mesh_file.exists():
        raise FileNotFoundError(mesh_file)
    T = np.asarray(data["transforms"])          # (N,4,4)
    scores = np.asarray(data.get("quality_number_of_contacts", []))
    return mesh_file, T, scores

def trimesh_axis(length=0.05, thickness=0.002):
    """RGB XYZ-ось для наглядности."""
    return trimesh.creation.axis(
        origin_size=thickness,
        axis_length=length,
        axis_radius=thickness / 4.0,
    )

def build_scene(mesh_path, transforms, scores):
    base_mesh = trimesh.load_mesh(mesh_path, force='mesh')
    scene = pyrender.Scene(bg_color=[1,1,1,0])
    scene.add(pyrender.Mesh.from_trimesh(base_mesh, smooth=False))

    axis = trimesh_axis()
    score_norm = (scores - scores.min()) / (scores.ptp() + 1e-9)

    for T, s in zip(transforms, score_norm):
        # градиент  красный (плохо) → зелёный (хорошо)
        color = pyrender.material.MetallicRoughnessMaterial(
            baseColorFactor=[1-s, s, 0, 1]
        )
        scene.add(
            pyrender.Mesh.from_trimesh(axis, smooth=False),
            pose=T
        )
    return scene

def main():
    parser = argparse.ArgumentParser(description="Visualize 6-DoF grasps")
    parser.add_argument("json", help="output from sample.py")
    parser.add_argument("--save", metavar="IMG.png", help="also save PNG")
    args = parser.parse_args()

    mesh_path, T, scores = load_data(args.json)
    print(f"loaded {len(T)} grasps   mesh: {mesh_path}")

    scene = build_scene(mesh_path, T, scores)

    if args.save:
        r = pyrender.OffscreenRenderer(800,600)
        color,_ = r.render(scene)
        imageio.imwrite(args.save, color)
        print("saved", args.save)

    pyrender.Viewer(scene, use_raymond_lighting=True)

if __name__ == "__main__":
    main()
