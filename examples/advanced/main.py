import io
import json
import image_rest_apis as image_rest_api
from tifffile import imread

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
    outdata = driver.Create(out_image_filepath, cols, rows, len(list_of_numpy_arr), gdal.GDT_Float32,
                            options=['COMPRESS=LZW'])
    outdata.SetGeoTransform(ds.GetGeoTransform())  ##sets same geotransform as input
    for i in range(len(list_of_numpy_arr)):
        outdata.GetRasterBand(i + 1).WriteArray(list_of_numpy_arr[i])
        outdata.GetRasterBand(i + 1).SetNoDataValue(10000)  ##if you want these values transparent
    outdata.FlushCache()  ##saves to disk!!
    outdata = None
    band = None
    ds = None


def main():
    with open('configurations.json', encoding='utf-8') as f:
        json_data = json.load(f)

    selected_apis = []

    selected_configuration = "example_1"
    for api in json_data[selected_configuration]['apis']:
        print("api: {}".format(api))
        selected_apis.append(api)

    # koordinater i SWEREF_99
    x = 428000
    y = 6470000
    offset = 256
    image_coordinates = [x, y, x + offset, y + offset]
    # Hämta hem bilder för varje vald rest-API
    raw_images = []
    for rest_api in selected_apis:
        params = image_rest_api.apis[rest_api]['params'](image_coordinates, image_size=256)
        image_url = image_rest_api.apis[rest_api]['post'](params)
        image_name = 'images/{}.tiff'.format(rest_api)

        resp = image_rest_api.get_image_data_from_url(image_url)
        raw_images.append({"name": image_name, "data": io.BytesIO(resp.content)})

    # Kombinera ihop bilder till en gemensam för att kunna användas som indata till en AI-modell
    imgs = []
    for image in raw_images:
        im = imread(image["data"])
        # normalisera bilder med hjälp av tillhörande normaliseringsfunktion för varje rest-API:
        rest_api = image["name"].split('/')[-1].split('.')[0]
        im = image_rest_api.apis[rest_api]['normalization'](im)

        if len(im.shape) > 2:
            im = im.transpose(2, 0, 1)
            for chan in im:
                imgs.append(chan)
        else:
            imgs.append(im)
        write_geotif_at_location(raw_images[0]["name"], 'combined.tiff', imgs)


if __name__ == '__main__':
    main()
