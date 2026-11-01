"""Create the factory navigation waypoints with the Waypoint Core API.

Follows NVIDIA's "Setup Navigation Waypoints" lesson, but scripted: position the camera, add a
waypoint, write a note. Waypoints are authored into scenes/assemblies/FactoryWaypoints.usd, which is
added as a sublayer of DigitalTwin.usd (muting that layer removes them).

  kit-app-template/_build/linux-x86_64/release/ellie.usd_composer.kit.sh \
      --enable omni.kit.waypoint.core --enable omni.kit.viewport.menubar.waypoint \
      --exec docs/capture/setup_waypoints.py
"""
import asyncio, os, sys
import omni.usd, omni.kit.app
from pxr import Gf, Sdf, UsdGeom
from omni.kit.viewport.utility import get_active_viewport

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from shots import WAYPOINTS  # noqa: E402

ROOT = os.path.join(REPO, "scenes", "assemblies", "DigitalTwin.usd")
WP_LAYER = os.path.join(REPO, "scenes", "assemblies", "FactoryWaypoints.usd")


async def upd(n):
    for _ in range(n):
        await omni.kit.app.get_app().next_update_async()


async def main():
    import omni.kit.waypoint.core as wp
    await upd(300)
    await omni.usd.get_context().open_stage_async(ROOT)
    await upd(600)
    stage = omni.usd.get_context().get_stage()
    layer = Sdf.Layer.FindOrOpen(WP_LAYER) or Sdf.Layer.CreateNew(WP_LAYER)
    # Waypoints are authored in their own layer, which must be in the stage's local layer stack.
    stage.GetRootLayer().subLayerPaths.append("./FactoryWaypoints.usd")
    await upd(30)

    inst = wp.get_instance()
    inst.edit_target = layer
    vp = get_active_viewport()

    # Waypoints store a copy of the active camera, so aim the perspective camera (session layer only).
    for name, note, eye, tgt in WAYPOINTS:
        stage.SetEditTarget(stage.GetSessionLayer())
        cam = UsdGeom.Camera.Get(stage, "/OmniverseKit_Persp")
        m = Gf.Matrix4d().SetLookAt(Gf.Vec3d(*eye), Gf.Vec3d(*tgt), Gf.Vec3d(0, 0, 1)).GetInverse()
        x = UsdGeom.Xformable(cam)
        x.ClearXformOpOrder()
        x.AddTransformOp().Set(m)
        vp.camera_path = "/OmniverseKit_Persp"
        await upd(200)
        await inst.create_waypoint_async(f"/Viewport_Waypoints/{name}")
        await upd(60)
        w = inst.get_waypoint(name)
        print("CREATED", name, bool(w), flush=True)
        if w is not None:
            w.comment = note
        await upd(30)

    layer.Save()
    # Save the root layer only (its sublayer list gained FactoryWaypoints.usd); session-layer
    # cameras are not part of it.
    stage.GetRootLayer().Save()
    print("SAVED", layer.identifier, flush=True)
    os._exit(0)


asyncio.ensure_future(main())
