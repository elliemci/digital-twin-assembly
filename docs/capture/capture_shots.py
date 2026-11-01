"""Render the static stills of DigitalTwin.usd inside Kit.

Run from the repo root (path to the built Kit app may differ):
  SHOT_DIR=docs/media kit-app-template/_build/linux-x86_64/release/ellie.usd_composer.kit.sh \
      --exec docs/capture/capture_shots.py
Needs an RTX GPU. The temporary camera lives on the session layer only; nothing is saved.
"""
import asyncio, os, sys
import omni.usd, omni.kit.app
from pxr import Gf, UsdGeom
from omni.kit.viewport.utility import get_active_viewport, capture_viewport_to_file

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from shots import SHOTS  # noqa: E402

ROOT = os.path.join(REPO, "scenes", "assemblies", "DigitalTwin.usd")
OUT = os.path.abspath(os.environ.get("SHOT_DIR", os.path.join(REPO, "docs", "media")))


async def upd(n):
    for _ in range(n):
        await omni.kit.app.get_app().next_update_async()


async def main():
    await upd(300)
    await omni.usd.get_context().open_stage_async(ROOT)
    await upd(900)  # let materials and textures stream in
    stage = omni.usd.get_context().get_stage()
    stage.SetEditTarget(stage.GetSessionLayer())
    vp = get_active_viewport()
    for name, eye, tgt in SHOTS:
        cam = UsdGeom.Camera.Define(stage, "/ShotCam")
        cam.GetFocalLengthAttr().Set(24)
        cam.GetClippingRangeAttr().Set(Gf.Vec2f(5, 100000))
        m = Gf.Matrix4d().SetLookAt(Gf.Vec3d(*eye), Gf.Vec3d(*tgt), Gf.Vec3d(0, 0, 1)).GetInverse()
        x = UsdGeom.Xformable(cam)
        x.ClearXformOpOrder()
        x.AddTransformOp().Set(m)
        vp.camera_path = "/ShotCam"
        await upd(400)  # RTX convergence
        cap = capture_viewport_to_file(vp, os.path.join(OUT, name + ".png"))
        await cap.wait_for_result(completion_frames=30)
        print("SHOT", name, flush=True)
    os._exit(0)


asyncio.ensure_future(main())
