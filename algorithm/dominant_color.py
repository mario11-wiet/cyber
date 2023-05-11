from sklearn.cluster import KMeans
import cv2 as cv
from collections import Counter
from colormath.color_objects import LabColor
import numpy as np
from colormath.color_conversions import convert_color

from algorithm.const import N_CLUSTERS, SHADE, BRIGHTNESS, COLORS, UNDEFINED


def calculate_color_difference(color1_rgb, color2_rgb):
    """
    Calculates the color difference between two RGB colors in the CIE 1976 (CIELAB) color space
    using the Euclidean distance formula.

    :param color1_rgb: The RGB value of the first color as a tuple (R, G, B)
    :param color2_rgb: The RGB value of the second color as a tuple (R, G, B)

    :return: The color difference between the two colors in the CIE 1976 color space.
    """
    lab_color1 = convert_color(LabColor(*color1_rgb), LabColor)
    lab_color2 = convert_color(LabColor(*color2_rgb), LabColor)
    delta_e = np.sqrt((lab_color1.lab_l - lab_color2.lab_l) ** 2 +
                      (lab_color1.lab_a - lab_color2.lab_a) ** 2 +
                      (lab_color1.lab_b - lab_color2.lab_b) ** 2)
    return delta_e


def brightness(r, g, b):
    """
    Calculates the brightness of an RGB color using the Y'UV color space formula.

    :param r: The red component of the color.
    :param g: The green component of the color.
    :param b: The blue component of the color.

    :return: The brightness value of the color.
    """
    brightness_value = (299 * r + 587 * g + 114 * b) / 1000

    return BRIGHTNESS < brightness_value < 255 - BRIGHTNESS


def shades_color(r, g, b, shade_threshold=SHADE):
    """
    Determines whether an RGB color is considered a shade of gray.

    :param r: The red component of the color.
    :param g: The green component of the color.
    :param b: The blue component of the color.
    :param shade_threshold: The threshold value for determining whether a color is a shade of gray. Colors with a
                            difference between the maximum and minimum RGB component values less than or equal to
                            this threshold are considered shades of gray. Default value is 40.
    :return: True if the color is a shade of gray, False otherwise.
    """
    return max(r, g, b) - min(r, g, b) > shade_threshold


def choice_color(color_array):
    calculate_color = {}

    for weight, color in color_array:
        for key, value in COLORS.items():
            calculate = calculate_color_difference(value, color)
            if key in calculate_color:
                calculate_color[key] += calculate_color[key] + weight / calculate
            else:
                calculate_color[key] = weight / calculate

    return max(calculate_color, key=calculate_color.get)


def calculate_dominant_color(k_cluster):
    n_pixels = len(k_cluster.labels_)
    counter = Counter(k_cluster.labels_)
    color = []
    for i in counter:
        cluster_color = [int(x) for x in k_cluster.cluster_centers_[i]]
        if shades_color(*cluster_color) and brightness(*cluster_color):
            percent = np.round(counter[i] / n_pixels, 2)
            color.append((max(percent, 0.01), cluster_color))


    if color:
        total_weight = sum([percent for percent, _ in color])
        normalized_color_array = [(weight / total_weight, color) for weight, color in color]
        return choice_color(normalized_color_array)

    return UNDEFINED


def dominant_color(path):
    try:
        cluster_website = KMeans(n_clusters=N_CLUSTERS, n_init='auto')
        website = cv.imread(path)
        website = cv.cvtColor(website, cv.COLOR_BGR2RGB)
        cluster_website_fit = cluster_website.fit(website.reshape(-1, 3))
    except ValueError:
        return UNDEFINED
    return calculate_dominant_color(cluster_website_fit)
