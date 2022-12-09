import os
import shutil

import requests

USERNAME = ""
PASSWORD = ""
SERVICE_URL = """https://geodata.skogsstyrelsen.se/arcgis/rest/services/Publikt/Markfuktighet_SLU_2_0/ImageServer"""


def sample_markfuktighet_png():
    """Hämtar en bild från den angivna bildtjänsten med default parametrar i png format, lämpligt för visning"""
    # folder och filnamn
    folder = "output"
    file_name = "markfuktighet.png"
    url = f"{SERVICE_URL}/exportimage"
    # Anger bildens storlek i pixlar
    pixels = 400
    # Anger bildens utsträckning (minx, miny, maxx, maxy)
    extent = (467709, 6338995, 469858, 6341200)
    params = {
        "bbox": f"{extent[0]},{extent[1]},{extent[2]},{extent[3]}",
        "size": f"{str(pixels)},{str(pixels)}",
        "format": "png",
        "f": "image"
    }
    resp = requests.get(url, params, stream=True, auth=(USERNAME, PASSWORD))
    resp.raise_for_status()
    save_image(folder=folder, image_name=file_name, image_data=resp)


def sample_markfuktighet_tif():
    """Hämtar en bild från den angivna bildtjänsten med default parametrar i tif format. Lämpligt för vidare data-analys"""
    # folder och filnamn
    folder = "output"
    file_name = "markfuktighet.tiff"
    # url till tjänsten
    url = f"{SERVICE_URL}/exportimage"
    pixels = 400
    extent = (467709, 6338995, 469858, 6341200)
    params = {
        "bbox": f"{extent[0]},{extent[1]},{extent[2]},{extent[3]}",
        "size": f"{str(pixels)},{str(pixels)}",
        "format": "tiff",
        "f": "image"
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


if __name__ == "__main__":
    sample_markfuktighet_png()
    sample_markfuktighet_tif()
