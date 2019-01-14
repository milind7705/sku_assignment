'''schema validator file'''
import os

absPath = "file://" + os.path.dirname(__file__)

sku = {
    "type": "object",
    "$ref": absPath + "/sku.json"
}