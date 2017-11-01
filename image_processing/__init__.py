from PIL import Image


def levels(data: Image, all_same: int = 0, clip: int = 0) -> Image:

    if data.mode not in ['RGB', 'CMYK']:
        return data

    lut = __make_lut(data, all_same, clip)

    data = data.point(lut)

    return data


def __find_hi_lo(lut, clip):

    min_value = None
    max_value = None

    for i in range(len(lut)):
        if lut[i] > clip:
            min_value = i
            break

    lut.reverse()

    for i in range(len(lut)):
        if lut[i] > clip:
            max_value = 255 - i
            break

    return min_value, max_value


def __scale(channels, min_value, max_value):

    lut = []

    for i in range(channels):
        for j in range(256):
            value = int((j - min_value) * (255.0 / float(max_value - min_value)))
            if value < 0:
                value = 0
            if value > 255:
                value = 255
            lut.append(value)

    return lut


def __make_lut(data, all_same, clip):

    histogram = data.histogram()

    r, g, b, k = [], [], [], []

    channels = len(histogram)/256

    for i in range(256):
        r.append(histogram[i])
        g.append(histogram[256+i])
        b.append(histogram[512+i])
    if channels == 4:
        for i in range(256):
            k.append(histogram[768+i])

    r_min, r_max = __find_hi_lo(r, clip)
    g_min, g_max = __find_hi_lo(g, clip)
    b_min, b_max = __find_hi_lo(b, clip)

    if channels == 4:
        k_min, k_max = __find_hi_lo(k)
    else:
        k_min, k_max = 128, 128

    if all_same == 1:

        min_max = [r_min, g_min, b_min, k_min, r_max, g_max, b_max, k_max]
        min_max.sort()
        lut = __scale(channels, min_max[0], min_max[-1])

    else:

        lut = []

        r_lut = __scale(1, r_min, r_max)
        g_lut = __scale(1, g_min, g_max)
        b_lut = __scale(1, b_min, b_max)
        if channels == 4:
            k_lut = __scale(1, k_min, k_max)

        for i in range(256):
            lut.append(r_lut[i])
        for i in range(256):
            lut.append(g_lut[i])
        for i in range(256):
            lut.append(b_lut[i])
        if channels == 4:
            for i in range(256):
                lut.append(k_lut[i])

    return lut
