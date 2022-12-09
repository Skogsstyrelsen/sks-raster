import json
import os
import shutil

import requests

USERNAME = ""
PASSWORD = ""
SERVICE_URL = """https://geodata.skogsstyrelsen.se/arcgis/rest/services/Publikt/Markfuktighet_SLU_2_0/ImageServer"""


def sample_markfuktighet_rasterfunction_1():
    """Hämtar en bild från den angivna bildtjänsten i png format, lämpligt för visning.
    Här används en rendering rule med en raster funktion för att maska bort alla
    klasser som ligger utanför spannet 44-55.
     """
    # folder och filnamn för att spara bilden
    folder = "output"
    file_name = "masked_markfuktighet.png"
    # Tjänstens url
    url = f"{SERVICE_URL}/exportimage"
    # Anger bildens storlek i pixlar
    pixels = 400
    # Anger bildens utsträckning (minx, miny, maxx, maxy)
    extent = (467709, 6338995, 469858, 6341200)
    # Renderingrule, inkludera endast klasserna 44 till 45, sätter övriga klasser till nodata
    rendering_rule = {
        "rasterFunction": "SKS_SLUMarkfuktighetMask",
        "rasterfunctionArguments":
            {
                "IncludedRanges": [44, 55]
            }
    }
    # Konvertera rendering rule till en json sträng för att skicka som parameter till servern
    rendering_rule_json = json.dumps(rendering_rule)
    params = {
        "bbox": f"{extent[0]},{extent[1]},{extent[2]},{extent[3]}",
        "size": f"{str(pixels)},{str(pixels)}",
        "format": "png",
        "f": "image",
        "renderingRule": rendering_rule_json
    }
    resp = requests.get(url, params, stream=True, auth=(USERNAME, PASSWORD))
    resp.raise_for_status()
    save_image(folder=folder, image_name=file_name, image_data=resp)


def sample_markfuktighet_rasterfunction_2():
    """Hämtar en bild från den angivna bildtjänsten i png format, lämpligt för visning.
    Här används en rendering rule med en raster funktion för att få en klassad bild.
     """
    # folder och filnamn för att spara bilden
    folder = "output"
    file_name = "classed_markfuktighet.png"
    # Tjänstens url
    url = f"{SERVICE_URL}/exportimage"
    # Anger bildens storlek i pixlar
    pixels = 400
    # Anger bildens utsträckning (minx, miny, maxx, maxy)
    extent = (467709, 6338995, 469858, 6341200)
    # Renderingrule, inkludera endast klasserna 44 till 45, sätter övriga klasser till nodata
    rendering_rule = {
        "rasterFunction": "SKS_SLUMarkfuktighetKlassad"
    }
    # Konvertera rendering rule till en json sträng för att skicka som parameter till servern
    rendering_rule_json = json.dumps(rendering_rule)
    params = {
        "bbox": f"{extent[0]},{extent[1]},{extent[2]},{extent[3]}",
        "size": f"{str(pixels)},{str(pixels)}",
        "format": "png",
        "f": "image",
        "renderingRule": rendering_rule_json
    }
    resp = requests.get(url, params, stream=True, auth=(USERNAME, PASSWORD))
    resp.raise_for_status()
    save_image(folder=folder, image_name=file_name, image_data=resp)


def save_image(folder, image_name, image_data):
    """Sparar bilddata i angiven folder med angivet namn (inklusive filformat)"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    image_path = os.path.join(folder, image_name)
    with open(image_path, 'wb') as f:
        image_data.raw.decode_content = True
        shutil.copyfileobj(image_data.raw, f)
        print(f"Bilden sparades som {image_path}")


if __name__ == '__main__':
    sample_markfuktighet_rasterfunction_1()
    sample_markfuktighet_rasterfunction_2()