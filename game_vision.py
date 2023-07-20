import cv2

base_res_x = 1280
base_res_y = 800
base_aspect_ratio = 1.6

template_x = 135
template_y = 42

resolutions = [
    [1024, 768],
    [1280, 1024],
    [1280, 800],
    [1440, 900],
    [1024, 700],
    [1680, 1050],
]


def choose_resolution():
    print("Choose your game resolution:")
    for idx, res in enumerate(resolutions):
        print(idx, res, res[0]/res[1])
    user_res = input()

    return resolutions[int(user_res)]


def calculate_aspect_ratio(resolution):
    return resolution[0] / resolution[1]


def resize_template(user_resolution, template):
    user_aspect_ratio = calculate_aspect_ratio(user_resolution)
    aspect_ratio_ratio = user_aspect_ratio / base_aspect_ratio

    new_x_scale = user_resolution[0]/base_res_x
    new_y_scale = user_resolution[1]/base_res_y

    if user_aspect_ratio != base_aspect_ratio:
        new_x = template_x * new_x_scale
        new_y = template_y * new_y_scale
        new_x_scale2 = new_x_scale / aspect_ratio_ratio
        new_y_scale2 = new_y_scale * aspect_ratio_ratio
        new_x2 = template_x * new_x_scale2
        new_y2 = template_y * new_y_scale2
        new_x = (new_x + new_x2)/2
        new_y = (new_y + new_y2)/2
    else:
        new_x = template_x * new_x_scale
        new_y = template_y * new_y_scale
    new_dim = [int(new_x), int(new_y)]
    print(new_dim)
    resized_template = cv2.resize(template, new_dim)

    return resized_template


def is_animation_present(template, screenshot, threshold):
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        return True, max_loc
    else:
        return False, None
