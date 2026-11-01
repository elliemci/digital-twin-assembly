"""Open DigitalTwin.usd (which sublayers FactoryWaypoints.usd), recall each waypoint and capture it.

  SHOT_DIR=docs/media kit-app-template/_build/linux-x86_64/release/ellie.usd_composer.kit.sh \
      --enable omni.kit.waypoint.core --enable omni.kit.viewport.menubar.waypoint \
      --exec docs/capture/capture_waypoints.py
"""
import asyncio, os
import omni.usd, omni.kit.app
from omni.kit.viewport.utility import get_active_viewport, capture_viewport_to_file

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
ROOT = os.path.join(REPO, "scenes", "assemblies", "DigitalTwin.usd")
OUT = os.path.abspath(os.environ.get("SHOT_DIR", os.path.join(REPO, "docs", "media")))


async def upd(n):
    for _ in range(n):
        await omni.kit.app.get_app().next_update_async()


async def main():
    import omni.kit.waypoint.core as wp
    await upd(300)
    await omni.usd.get_context().open_stage_async(ROOT)
    await upd(900)
    inst = wp.get_instance()
    vp = get_active_viewport()
    waypoints = list(inst.get_waypoints())
    print("FOUND", [w.name for w in waypoints], flush=True)
    for w in waypoints:
        w.recall()
        await upd(400)  # RTX convergence
        cap = capture_viewport_to_file(vp, os.path.join(OUT, f"waypoint_{w.name}.png"))
        await cap.wait_for_result(completion_frames=30)
        print("SHOT", w.name, "|", w.comment, flush=True)
    os._exit(0)


asyncio.ensure_future(main())
