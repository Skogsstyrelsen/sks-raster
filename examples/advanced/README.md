# Exempelkod för AI tillämpning

## Inledning
I detta avsnitt visas ett exempel på hur man med programmeringsspråket python kan extrahera en kombinerad bild från flera bildtjänster och spara ner den i .tif format. 

### Förkrav

#### Installation
De python paket som behövs för att köra exemplet installeras lättast med conda. För vidare information om conda, se [Condas dokumentation](https://docs.conda.io/en/latest/)

I exemplet finns filen [requirements.txt](./requirements.txt). Denna fil listar samtliga python paket som behövs i conda-miljön för att köra koden. 

För att skapa conda-miljön, öppna Anaconda Prompt och skriv kommandot:
```
conda create --name sks-raster-example-env --file requirements.txt
```

Detta kommando skapar en conda-miljö med namnet 'sks-raster-example-env' med alla nödvändiga paket. 

### Kom igång

När paketen är installerade kan `main.py` köras med:

```
<path-to-conda>\envs\sks-raster-example-env\python.exe main.py
```
där 'path-to-conda>' är sökvägen till conda installationen

Slutresultatet är en sammansatt georefererad tiff-bild `combined.tiff` . Bilden innehåller data från de valda bildtjänsterna.

### Genomgång av kod

------

`configuration.json` innehåller konfigurationer. När en ny sammansättning av data ska användas, skapa en ny konfiguration. Här är ett exempel på en konfiguration:

```
    "example_1": {
        "apis": ["marktackedata_2_0", "markfuktighet_slu_2_0_KON", "sentinel_2_2_0"]
    }
```

------

I konfigurationen finns olika namn på API:er. dessa namn är hårt kopplade till objekt i `image_rest_apis.py`:

```
apis = {
    'marktackedata_2_0':{'params': params_marktackedata_2_0, 'post': post_marktackedata_2_0, 'normalization': PN.normalization_marktackedata_2_0},
    'markfuktighet_slu_2_0_KAT':{ 'params': params_markfuktighet_slu_2_0, 'post': post_markfuktighet_slu_2_0, 'normalization': PN.normalization_markfuktighet_slu_2_0_kat},
    'markfuktighet_slu_2_0_KON':{'params': params_markfuktighet_slu_2_0, 'post': post_markfuktighet_slu_2_0, 'normalization': PN.normalization_markfuktighet_slu_2_0_kon},
    'sentinel_2_2_0':{'params': params_sentinel_2_2_0, 'post': post_sentinel_2_2_0, 'normalization': PN.normalization_sentinel_2_2_0},
}
```

I varje objekt måste det finnas nycklar som heter `params` `post` `normalization`. Dessa nycklar pekar på metoder. Metoderna för `params` och `post` finns i `rest_apis.py`, `normalization` finns i `pixel_normalization.py`.

------

För att använda metoderna baserat på den valda konfigurationen, läs först in konfigurationen och läs ut vilka Rest-API:er som ska användas

```
import json

 with open('configurations.json',encoding='utf-8') as f:
        json_data = json.load(f)

    selected_apis = []

    selected_configuration = "example_1"
    for api in json_data[selected_configuration]['apis']:
        print("api: {}".format(api))
        selected_apis.append(api)
```

------

Bestäm koordinater för en bild i SWEREF99-format

```
    x = 428000
    y = 6470000
    offset = 256
    image_coordinates=[x,y,x+offset,y+offset]
```

------

Hämta hem bilder från varje vald bildtjänst genom att anropa metoderna som är pekade på i `rest_apis.py`

```
import RestAPIs as ra
import requests

raw_images = []
    for rest_api in selected_apis:
        params = ra.apis[rest_api]['params'](image_coordinates, image_size=256)
        image_url = ra.apis[rest_api]['post'](params)
        image_name = 'images/{}.tiff'.format(rest_api)
        urllib.request.urlretrieve(image_url,image_name)
        raw_images.append(image_name)
```

------

Anropa normaliseringsfunktionen för varje hämtad bild. Sammansätt alla bilder i en gemensam array

```
from tifffile import imread
imgs = []
    for image in raw_images:
        im = imread(image)
        #normalisera bilder med hjälp av tillhörande normaliseringsfunktion för varje rest-API:
        rest_api = image.split('/')[-1].split('.')[0]
        im = ra.apis[rest_api]['normalization'](im)

        if(len(im.shape) > 2):
            im = im.transpose(2,0,1)
            for chan in im:
                imgs.append(chan)
        else:
            imgs.append(im)
```

------

Spara den sammansatta bilden. Använd en av de hämtade bilderna som georeferens för att kunna få en georefererad bild

```
try:
    import gdal
except:
    from osgeo import gdal

def write_geotif_at_location(ref_image_filepath, out_image_filepath, list_of_numpy_arr):
    """
    Writes a geotif at the same postion as a reference image. 
    Each band in the geotif is added in the list as np.array 
    
    input:
        ref_image_filepath (string) - path to georeferences image
        out_image_filepath (string) - path to output image
        list_of_numpy_arr (list)  - list of 2d nparrys, shape should be of same size as shape of ref_image_filepath
    output:
        None
    """
    ds = gdal.Open(ref_image_filepath)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()
    [rows, cols] = arr.shape
    
    driver = gdal.GetDriverByName("GTiff")
    outdata = driver.Create(out_image_filepath, cols, rows, len(list_of_numpy_arr), gdal.GDT_Float32, options=['COMPRESS=LZW'])
    outdata.SetGeoTransform(ds.GetGeoTransform())##sets same geotransform as input
    for i in range(len(list_of_numpy_arr)):
        outdata.GetRasterBand(i+1).WriteArray(list_of_numpy_arr[i])
        outdata.GetRasterBand(i+1).SetNoDataValue(10000)##if you want these values transparent
    outdata.FlushCache() ##saves to disk!!
    outdata = None
    band = None
    ds = None
```

```
write_geotif_at_location(raw_images[0],'combined.tiff', imgs)
```

Bilden sparas som `combined.tiff`