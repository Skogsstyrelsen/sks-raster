import requests
import pixel_normalization as PN

USERNAME = ""
PASSWORD = ""


def params_marktackedata_2_0(coordinates_list, image_year='', rendering_rule='', image_size=512):
    print('{},+{},+{},+{}'.format(coordinates_list[0], coordinates_list[1], coordinates_list[2], coordinates_list[3]))
    params = dict(
        bbox='{},+{},+{},+{}'.format(coordinates_list[0], coordinates_list[1], coordinates_list[2],
                                     coordinates_list[3]),
        bboxSR='3006',
        size='{},{}'.format(image_size, image_size),
        imageSR='',
        time='',
        format='tiff',
        pixelType='UNKNOWN',
        noData='',
        noDataInterpretation='esriNoDataMatchAny',
        interpolation='+RSP_BilinearInterpolation',
        compression='LZ77',
        compressionQuality='',
        bandIds='',
        sliceId='',
        adjustAspectRatio='true',
        validateExtent='false',
        lercVersion='1',
        compressionTolerance='',
        f='pjson',
    )
    return params


def post_marktackedata_2_0(params):
    url = 'https://geodata.skogsstyrelsen.se/arcgis/rest/services/Publikt//Marktackedata_2_0/ImageServer/exportImage'
    resp = requests.get(url=url, params=params, auth=(USERNAME, PASSWORD))
    resp.raise_for_status()
    data = resp.json()
    return data['href']


def params_markfuktighet_slu_2_0(coordinates_list, image_year='', rendering_rule='', image_size=512):
    params = dict(
        bbox='{},+{},+{},+{}'.format(coordinates_list[0], coordinates_list[1], coordinates_list[2],
                                     coordinates_list[3]),
        bboxSR='3006',
        size='{},{}'.format(image_size, image_size),
        imageSR='',
        time='',
        format='tiff',
        pixelType='UNKNOWN',
        noData='',
        noDataInterpretation='esriNoDataMatchAny',
        interpolation='+RSP_BilinearInterpolation',
        compression='LZ77',
        compressionQuality='',
        bandIds='',
        sliceId='',
        adjustAspectRatio='true',
        validateExtent='false',
        lercVersion='1',
        compressionTolerance='',
        f='pjson',
    )
    return params


def post_markfuktighet_slu_2_0(params):
    url = 'https://geodata.skogsstyrelsen.se/arcgis/rest/services/Publikt//Markfuktighet_SLU_2_0/ImageServer/exportImage'
    resp = requests.get(url=url, params=params, auth=(USERNAME, PASSWORD))
    resp.raise_for_status()
    data = resp.json()
    return data['href']


def params_sentinel_2_2_0(coordinates_list, date='2021-03-25', image_size=512, rendering_rule='ndvi'):
    renderingRule = ''
    if rendering_rule == 'ndvi':
        renderingRule = '{"rasterFunction": "BandArithmetic", "rasterFunctionArguments": {"Method": 0, "BandIndexes": "(b3*0+b2-b1-500)/(b1+b2+500)",\
                "Raster": {"rasterFunction": "Mask", "rasterFunctionArguments": {"NoDataValues": ["0", "0", "0 1 2 3 7 8 9 10 11"], "NoDataInterpretation": 0,\
                "Raster": {"rasterFunction": "ExtractBand", "rasterFunctionArguments": {"BandIDs": [2, 3, 6]}}}}}}',

    params = dict(
        bbox='{},+{},+{},+{}'.format(coordinates_list[0], coordinates_list[1], coordinates_list[2],
                                     coordinates_list[3]),
        bboxSR='3006',
        size='{},{}'.format(image_size, image_size),
        imageSR='',
        format='tiff',
        pixelType='UNKNOWN',
        noData='',
        noDataInterpretation='esriNoDataMatchAny',
        interpolation='+RSP_BilinearInterpolation',
        compressionQuality='',
        bandIds='',
        sliceId='',
        renderingRule=renderingRule,
        mosaicRule='{"where":"ImageDate=date' + "'" + str(date) + "'" + '"}',
        validateExtent='false',
        lercVersion='1',
        compressionTolerance='',
        f='pjson',
    )
    return params


def post_sentinel_2_2_0(params):
    url = 'https://geodata.skogsstyrelsen.se/arcgis/rest/services/Swea/Sentinel2_2_0/ImageServer/exportImage'
    resp = requests.post(url=url, params=params, auth=(USERNAME, PASSWORD))
    resp.raise_for_status()
    data = resp.json()
    # print(data)
    return data['href']


def get_image_data_from_url(url):
    resp = requests.get(url, stream=True, auth=(USERNAME, PASSWORD))
    resp.raise_for_status()
    return resp


# Storing all functions in an object
apis = {
    'marktackedata_2_0': {'params': params_marktackedata_2_0, 'post': post_marktackedata_2_0,
                          'normalization': PN.normalization_marktackedata_2_0},
    'markfuktighet_slu_2_0_KAT': {'params': params_markfuktighet_slu_2_0, 'post': post_markfuktighet_slu_2_0,
                                  'normalization': PN.normalization_markfuktighet_slu_2_0_kat},
    'markfuktighet_slu_2_0_KON': {'params': params_markfuktighet_slu_2_0, 'post': post_markfuktighet_slu_2_0,
                                  'normalization': PN.normalization_markfuktighet_slu_2_0_kon},
    'sentinel_2_2_0': {'params': params_sentinel_2_2_0, 'post': post_sentinel_2_2_0,
                       'normalization': PN.normalization_sentinel_2_2_0},
}
