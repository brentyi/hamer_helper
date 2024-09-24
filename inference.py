"""Example script for running HaMeR. For each image in some directory, detect
hands and render them."""

from pathlib import Path

import cv2
import imageio.v3 as iio
import numpy as np
import tyro

from hamer_helper import HamerHelper


def main(
    input_dir: Path,
    output_dir: Path,
    search_ext: tuple[str, ...] = (".jpg", ".jpeg", ".png"),
) -> None:
    """For each image in the input directory, run HaMeR and composite the detections.

    Args:
        input_dir: The directory to search for images.
        output_dir: The directory to write the composited images.
        search_ext: Image extensions to search for in the input directory.
    """
    # Find images.
    image_paths = tuple(
        filter(
            lambda p: not p.is_dir() and p.suffix.lower() in search_ext,
            input_dir.glob("**/*"),
        )
    )
    print(f"Found {len(image_paths)} images!")

    # Set up HaMeR.
    # This should magically work as long as the HaMeR repo is set up.
    hamer_helper = HamerHelper()

    for image_path in image_paths:
        # Read an image.
        image = iio.imread(image_path)

        # Convert grayscale to RGB.
        if len(image.shape) == 2:
            image = np.stack([image] * 3, axis=-1)

        # RGB => RGBA.
        if image.shape[-1] == 4:
            image = image / 255.0
            image = image[:, :, :3] * image[:, :, 3:4] + 1.0 * (1.0 - image[:, :, 3:4])
            image = (image * 255).astype(np.uint8)

        # Get HaMeR detections as dictionaries.
        det_left, det_right = hamer_helper.look_for_hands(image)

        # Render detections on top of image.
        composited = image
        composited = hamer_helper.composite_detections(
            composited, det_left, border_color=(255, 100, 100)
        )
        composited = hamer_helper.composite_detections(
            composited, det_right, border_color=(100, 100, 255)
        )
        composited = put_text(
            composited,
            "L detections: "
            + ("0" if det_left is None else str(det_left["verts"].shape[0])),
            0,
            color=(255, 100, 100),
            font_scale=10.0 / 2880.0 * image.shape[0],
        )
        composited = put_text(
            composited,
            "R detections: "
            + ("0" if det_right is None else str(det_right["verts"].shape[0])),
            1,
            color=(100, 100, 255),
            font_scale=10.0 / 2880.0 * image.shape[0],
        )

        # Write out the input image next to the composited image.
        output_path = output_dir / image_path.absolute().relative_to(input_dir)
        output_path.parent.mkdir(exist_ok=True, parents=True)
        iio.imwrite(output_path, np.concatenate([image, composited], axis=1))


def put_text(
    image: np.ndarray,
    text: str,
    line_number: int,
    color: tuple[int, int, int],
    font_scale: float,
) -> np.ndarray:
    """Put some text on the top-left corner of an image."""
    image = image.copy()
    font = cv2.FONT_HERSHEY_PLAIN  # type: ignore
    cv2.putText(  # type: ignore
        image,
        text=text,
        org=(2, 1 + int(15 * font_scale * (line_number + 1))),
        fontFace=font,
        fontScale=font_scale,
        color=(0, 0, 0),
        thickness=max(int(font_scale), 1),
        lineType=cv2.LINE_AA,  # type: ignore
    )
    cv2.putText(  # type: ignore
        image,
        text=text,
        org=(2, 1 + int(15 * font_scale * (line_number + 1))),
        fontFace=font,
        fontScale=font_scale,
        color=color,
        thickness=max(int(font_scale), 1),
        lineType=cv2.LINE_AA,  # type: ignore
    )
    return image


if __name__ == "__main__":
    tyro.cli(main)
