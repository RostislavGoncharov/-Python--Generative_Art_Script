import colorsys
import random

from PIL import Image, ImageDraw, ImageChops, ImageFilter


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def interpolate_color(start_color, end_color, factor: float):
    recip = 1 - factor
    return (
        int(start_color[0] * recip + end_color[0] * factor),
        int(start_color[1] * recip + end_color[1] * factor),
        int(start_color[2] * recip + end_color[2] * factor)
    )


def generate_art(path: str):
    print("Generating art")
    # Generate background image
    target_image_size = 2048
    scale_factor = 2
    image_size_px = target_image_size * scale_factor
    image_bg_color = (0, 0, 0)
    padding_px = 100 * scale_factor
    start_color = random_color()
    end_color = random_color()
    image = Image.new("RGB",
                      size=(image_size_px, image_size_px),
                      color=image_bg_color)
    # Making a background gradient which fades to black on the sides
    bg_gradient = ImageDraw.Draw(image)
    bg_gradient_color = random_color()
    for y in range(image_size_px):
        for x in range(image_size_px // 2):
            bg_color_factor = x / (image_size_px - 1)
            interpolated_color = interpolate_color((0, 0, 0), bg_gradient_color, bg_color_factor)
            bg_gradient.point((x, y), fill=interpolated_color)
        for x in range(image_size_px // 2, image_size_px):
            bg_color_factor = x / (image_size_px - 1)
            interpolated_color = interpolate_color(bg_gradient_color, (0, 0, 0), bg_color_factor)
            bg_gradient.point((x, y), fill=interpolated_color)

    # Draw lines
    points = []

    # Generate the points
    for _ in range(40):
        random_point = (random.randint(padding_px, image_size_px - padding_px),
                        random.randint(padding_px, image_size_px - padding_px))
        points.append(random_point)

    # Make a bounding box
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    # Center the image
    delta_x = (image_size_px - max_x) - min_x
    delta_y = (image_size_px - max_y) - min_y

    for i, point in enumerate(points):
        points[i] = (point[0] + delta_x // 2, point[1] + delta_y // 2)

    # Connect the points
    line_thickness = 0
    n_points = len(points) - 1
    for i, point in enumerate(points):

        # Overlay canvas
        overlay_image = Image.new("RGB",
                                  size=(image_size_px, image_size_px),
                                  color=image_bg_color)

        overlay_draw = ImageDraw.Draw(overlay_image)

        p1 = point

        if i == n_points:
            p2 = points[0]
        else:
            p2 = points[i + 1]
        line_xy = (p1, p2)
        color_factor = i / n_points
        line_color = interpolate_color(start_color, end_color, color_factor)

        # set probability however you wish
        probability = random.randint(0, 9)
        if probability > 6:
            line_thickness += scale_factor
        overlay_draw.line(line_xy, line_color, line_thickness, None)
        image = ImageChops.add(image, overlay_image)

    # Filtering and downsampling the image (optional)
    image = image.filter(ImageFilter.SMOOTH)
    image = image.resize((target_image_size, target_image_size), resample=Image.ANTIALIAS)
    image.save(path)


if __name__ == "__main__":
    # generating a batch of images
    for i in range(10):
        generate_art(f"test_image_{i}.png")
