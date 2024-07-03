"""Example script for running HaMeR via the HamerHelper."""
from pathlib import Path

import imageio.v3 as iio
import numpy as np
import tyro

from hamer_helper import HamerHelper


def main(
    input_images: list[Path],
    render_output_dir: Path = Path("./hamer_test_script_outputs"),
) -> None:
    # Set up HaMeR.
    # This should magically work as long as the HaMeR repo is set up.
    hamer_helper = HamerHelper()

    for input_image in input_images:
        # Read an image.
        image = iio.imread(input_image)

        # RGB => RGBA.
        if image.shape[-1] == 4:
            image = image / 255.0
            image = image[:, :, :3] * image[:, :, 3:4] + 1.0 * (1.0 - image[:, :, 3:4])
            image = (image * 255).astype(np.uint8)

        # Run HaMeR.
        det_left, det_right = hamer_helper.look_for_hands(
            image=image,
            focal_length=(1137.0 / 1280) * image.shape[1],
            # For most real-world applications, this should probably set to None.
            render_output_dir_for_testing=render_output_dir,
            render_output_prefix_for_testing=input_image.stem,
        )

        # if det_left is not None:
        #     rgb, depth, mask = hamer_helper.render_detection(
        #         det_left, 0, 1280, 720, 1137.0
        #     )
        # if det_right is not None:
        #     rgb, depth, mask = hamer_helper.render_detection(
        #         det_right, 0, 1280, 720, 1137.0
        #     )
        # import matplotlib.pyplot as plt
        #
        # fig, axs = plt.subplots(1, 3)
        # axs[0].imshow(rgb)
        # axs[1].imshow(depth)
        # axs[2].imshow(mask)
        # plt.show()


if __name__ == "__main__":
    tyro.cli(main)
