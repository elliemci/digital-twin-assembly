import asyncio, omni.usd, omni.kit.app
from pxr import Usd, UsdGeom
ROOT="/home/elliemcintosh/Documents/digital-twin-assembly/scenes/assemblies/DigitalTwin.usd"
async def main():
    for _ in range(300): await omni.kit.app.get_app().next_update_async()
    r=await omni.usd.get_context().open_stage_async(ROOT)
    print('OPENRESULT',r)
    for _ in range(600): await omni.kit.app.get_app().next_update_async()
    st=omni.usd.get_context().get_stage()
    cache=UsdGeom.BBoxCache(Usd.TimeCode.Default(),["default","render"])
    def walk(p,d):
        if d>4: return
        for c in p.GetChildren():
            b=cache.ComputeWorldBound(c).ComputeAlignedRange()
            print("  "*d+str(c.GetPath()),c.GetTypeName(),(tuple(round(x) for x in b.GetMin()),tuple(round(x) for x in b.GetMax())) if not b.IsEmpty() else "")
            walk(c,d+1)
    walk(st.GetPseudoRoot(),0)
    print("UPAXIS",UsdGeom.GetStageUpAxis(st),UsdGeom.GetStageMetersPerUnit(st))
    import os,sys; sys.stdout.flush(); os._exit(0)
asyncio.ensure_future(main())
