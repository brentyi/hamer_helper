"""Example script for running HaMeR via the HamerHelper."""

from pathlib import Path

import cv2
import imageio.v3 as iio
import numpy as np
import tyro
from scipy.ndimage import binary_dilation

from hamer_helper import HamerHelper, HandOutputsWrtCamera


def composite_detections(
    helper: HamerHelper,
    image: np.ndarray,
    detections: HandOutputsWrtCamera | None,
    border_color: tuple[int, int, int],
) -> np.ndarray:
    if detections is None:
        return image

    h, w = image.shape[:2]

    for index in range(detections["verts"].shape[0]):
        print(index)
        render_rgb, _, render_mask = helper.render_detection(
            detections, hand_index=0, h=h, w=w, focal_length=None
        )
        border_width = 15
        image = np.where(
            binary_dilation(
                render_mask, np.ones((border_width, border_width), dtype=bool)
            )[:, :, None],
            np.zeros_like(render_rgb) + np.array(border_color, dtype=np.uint8),
            image,
        )
        image = np.where(render_mask[:, :, None], render_rgb, image)

    return image


def put_text(
    image: np.ndarray,
    text: str,
    line_number: int,
    color: tuple[int, int, int],
    font_scale: float,
) -> np.ndarray:
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


def main(input_dir: Path, output_dir: Path, ext: str = "jpg") -> None:
    # Set up HaMeR.
    # This should magically work as long as the HaMeR repo is set up.
    hamer_helper = HamerHelper()

    for input_path in input_dir.glob(f"**/*.{ext}"):
        if input_path.is_dir():
            continue

        # Read an image.
        image = iio.imread(input_path)

        # RGB => RGBA.
        if image.shape[-1] == 4:
            image = image / 255.0
            image = image[:, :, :3] * image[:, :, 3:4] + 1.0 * (1.0 - image[:, :, 3:4])
            image = (image * 255).astype(np.uint8)

        # Run HaMeR.
        det_left, det_right = hamer_helper.look_for_hands(image)

        composited = image
        composited = composite_detections(
            hamer_helper, composited, det_left, border_color=(255, 100, 100)
        )
        composited = composite_detections(
            hamer_helper, composited, det_right, border_color=(100, 100, 255)
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

        output_path = output_dir / input_path.absolute().relative_to(input_dir)
        output_path.parent.mkdir(exist_ok=True, parents=True)

        iio.imwrite(output_path, np.concatenate([image, composited], axis=1))


if __name__ == "__main__":
    tyro.cli(main)
