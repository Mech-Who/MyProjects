import gltflib
import json

# get model info
model_info = {}
with open("models.json", "r", encoding="utf-8") as f:
    content = json.load(f)
    model_info = content.get("woman_demon")

# Load the model
loader = gltflib.GLTF()
model_root = model_info.get("model_root")
asset_name = model_info.get("asset_name")
model = loader.load_glb(model_root + asset_name)
# model.export_glb("./export_models/"+asset_name)
for node in model.model.nodes:
    print(node)
