from manim import *
from numpy import interp
from PIL import Image
import os


def crop_image_array(original_image_array, x, y, width, height):
    cropped_image_array = original_image_array[y:y+height, x:x+width]
    padded_cropped_image_array = np.zeros_like(original_image_array)
    padded_cropped_image_array[y:y+cropped_image_array.shape[0], x:x+cropped_image_array.shape[1]] = cropped_image_array
    return padded_cropped_image_array


def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))


def get_or_create(texture_path, output_folder, target_u, target_v):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Define the cropping size
    crop_size = 256

    # Define the filename for the cropped image
    output_filename = f"cropped_{target_u}_{target_v}.png"
    output_filepath = os.path.join(output_folder, output_filename)

    if os.path.exists(output_filepath):
        # If the cropped image already exists, return its filepath
        return output_filepath
    else:
        # If the cropped image does not exist, prepare it
        # Load the texture image using Pillow
        texture = Image.open(texture_path)

        # Calculate the cropping box
        # Ensure target_u and target_v are within valid bounds
        target_u = max(0, min(target_u, texture.width - crop_size))
        target_v = max(0, min(target_v, texture.height - crop_size))
        crop_box = (target_u, texture.height - target_v - crop_size, target_u + crop_size, texture.height - target_v)

        # Crop the texture image
        cropped_texture = texture.crop(crop_box)

        # Save the cropped image to the output folder
        cropped_texture.save(output_filepath)

        # Return the filepath to the newly created cropped image
        return output_filepath


class BlitDemonstration(Scene):
    def construct(self):
        def create_window():
            dotTL = Dot(color=WHITE).shift(UP * 2 + LEFT * 3)
            dotTR = Dot(color=WHITE).shift(UP * 2 + RIGHT * 3)
            dotBR = Dot(color=WHITE).shift(DOWN * 2 + RIGHT * 3)
            dotBL = Dot(color=WHITE).shift(DOWN * 2 + LEFT * 3)

            self.play(Create(dotTL), run_time=0.1)
            self.play(Create(dotTR), run_time=0.1)
            self.play(Create(dotBR), run_time=0.1)
            self.play(Create(dotBL), run_time=0.1)

            topLine = Line(dotTL.get_center(), dotTR.get_center(), color=WHITE)
            rightLine = Line(dotTR.get_center(), dotBR.get_center(), color=WHITE)
            bottomLine = Line(dotBR.get_center(), dotBL.get_center(), color=WHITE)
            leftLine = Line(dotBL.get_center(), dotTL.get_center(), color=WHITE)

            self.play(Create(topLine), run_time=0.5)
            self.play(Create(rightLine), run_time=0.5)
            self.play(Create(bottomLine), run_time=0.5)
            self.play(Create(leftLine), run_time=0.5)

            window = VGroup(dotTL, dotTR, dotBL, dotBR, topLine, rightLine, bottomLine, leftLine)
            return window

        def show_window_size():
            topLeftDot = Dot(color=RED).shift(UP * 2 + LEFT * 3)
            self.play(Create(topLeftDot), run_time=0.1)
            self.play(topLeftDot.animate.scale(1.5), run_time=0.5)
            topLeftText = Text("(0, 0)", color=RED).next_to(topLeftDot, UP)
            self.play(Write(topLeftText))
            self.play(topLeftText.animate.shift(DOWN * 0.25).scale(0.5), run_time=0.5)

            xPos = ValueTracker(0)
            yPos = ValueTracker(0)

            topRightDot = always_redraw(
                lambda: Dot(color=RED)
                .shift(
                    UP * 2 +
                    LEFT * 3 +
                    RIGHT * interp(xPos.get_value(), [0, 1028], [0, 6]))
            )

            topRightText = always_redraw(lambda: Text(
                f"({int(xPos.get_value())}, 0.0)",
                color=RED
            ).shift(
                UP * 2.5 +
                LEFT * 3 +
                RIGHT * interp(xPos.get_value(), [0, 1028], [0, 6])
            ).scale(0.5))

            self.play(Create(topRightDot), Create(topRightText), run_time=0.1)
            self.play(xPos.animate.set_value(1028), run_time=2.5, rate_func=linear)
            self.play(topRightDot.animate.scale(1.5), run_time=0.5)

            newTopRightDot = Dot(color=RED).shift(UP * 2 + RIGHT * 3).scale(1.5)
            newTopRightText = Text("(1028, 0)", color=RED).next_to(newTopRightDot, UP * 0.5).scale(0.5)
            self.play(
                ReplacementTransform(topRightDot, newTopRightDot),
                ReplacementTransform(topRightText, newTopRightText),
                run_time=0
            )

            self.wait(1)

            bottomRightDot = always_redraw(
                lambda: Dot(color=RED)
                .shift(
                    UP * 2 +
                    LEFT * 3 +
                    RIGHT * interp(xPos.get_value(), [0, 1028], [0, 6]) +
                    DOWN * interp(yPos.get_value(), [0, 768], [0, 4]))
            )

            bottomRightText = always_redraw(lambda: Text(
                f"({int(xPos.get_value())}, {int(yPos.get_value())})",
                color=RED
            ).shift(
                UP * 2.5 +
                LEFT * 3 +
                RIGHT * interp(xPos.get_value(), [0, 1028], [0, 6]) +
                DOWN * interp(yPos.get_value(), [0, 768], [0, 4])
            ).scale(0.5))

            self.play(Create(bottomRightDot), Create(bottomRightText), run_time=0.1)
            self.play(yPos.animate.set_value(768), run_time=2.5, rate_func=linear)
            self.play(bottomRightDot.animate.scale(1.5), run_time=0.5)

            newBottomRightDot = Dot(color=RED).shift(DOWN * 2 + RIGHT * 3).scale(1.5)
            newBottomRightText = Text("(1028, 768)", color=RED).next_to(newBottomRightDot, DOWN).scale(0.5)
            self.play(
                ReplacementTransform(bottomRightDot, newBottomRightDot),
                ReplacementTransform(bottomRightText, newBottomRightText),
                newBottomRightText.animate.shift(UP * 0.25 + RIGHT * 0.25),
                run_time=0
            )

        def demonstrate_blit():
            blitCode = Text(
                text="blit(location, x, y, u, v, width, height)",
                font="Consolas"
            ).scale(0.5).to_corner(UL)

            self.play(Write(blitCode), run_time=1.5)
            self.wait(1)
            self.play(blitCode.animate.shift(DOWN * 0.5), run_time=0.5)

            textureLocation = Text(
                text="private static final ResourceLocation TEXTURE = new ResourceLocation(TutorialMod.MODID, \"textures/gui.png\");",
                font="Consolas"
            ).scale(0.325).to_corner(UL)

            self.play(Write(textureLocation), run_time=2)
            self.wait(1)

            textureReplacedBlitCode = Text(
                text="blit(TEXTURE, x, y, u, v, width, height)",
                font="Consolas"
            ).scale(0.5).to_corner(UL).shift(DOWN * 0.5)

            self.play(ReplacementTransform(blitCode, textureReplacedBlitCode), run_time=0.5)

            valueReplacedBlitCode = Text(
                text="blit(TEXTURE, 0, 0, 0, 0, 256, 256)",
                font="Consolas"
            ).scale(0.5).to_corner(UL).shift(DOWN * 0.5)

            self.play(ReplacementTransform(textureReplacedBlitCode, valueReplacedBlitCode), run_time=0.5)

            self.wait(2)

            guiImage = ImageMobject("assets/images/sample_gui.png")
            guiImage.shift(UP * 2 + LEFT * 3 + RIGHT * guiImage.get_width() / 2 + DOWN * guiImage.get_height() / 2)
            self.play(FadeIn(guiImage), run_time=0.5)
            self.wait(1)

            xValue = ValueTracker(0)
            yValue = ValueTracker(0)

            blitImage = always_redraw(
                lambda: ImageMobject("assets/images/sample_gui.png")
                .shift(
                    UP * 2 + DOWN * guiImage.get_height() / 2 +
                    LEFT * 3 + RIGHT * guiImage.get_width() / 2 +
                    RIGHT * interp(
                        xValue.get_value(),
                        [0, 1028],
                        [0, 5.5 - guiImage.get_width()]
                    ) +
                    DOWN * interp(
                        yValue.get_value(),
                        [0, 768],
                        [0, 4 - guiImage.get_height()]
                    )
                )
            )

            updatingPositionBlitCode = always_redraw(lambda: Text(
                f"blit(TEXTURE, {int(xValue.get_value())}, {int(yValue.get_value())}, 0, 0, 256, 256)",
                font="Consolas"
            ).scale(0.5).to_corner(UL).shift(DOWN * 0.5))
            self.play(ReplacementTransform(valueReplacedBlitCode, updatingPositionBlitCode), run_time=0.01)

            self.play(ReplacementTransform(guiImage, blitImage), run_time=0.5)
            self.wait(1)
            self.play(xValue.animate.set_value(1028), run_time=2.5, rate_func=linear)
            self.play(yValue.animate.set_value(768), run_time=2.5, rate_func=linear)
            self.wait(1)
            self.play(xValue.animate.set_value(0), yValue.animate.set_value(0), run_time=0.75, rate_func=smooth)
            self.wait(1)

            uValue = ValueTracker(0)
            vValue = ValueTracker(0)

            updatingUVBlitCode = always_redraw(lambda: Text(
                f"blit(TEXTURE, {int(xValue.get_value())}, {int(yValue.get_value())}, {int(uValue.get_value())}, {int(vValue.get_value())}, 256, 256)",
                font="Consolas"
            ).scale(0.5).to_corner(UL).shift(DOWN * 0.5))

            self.play(ReplacementTransform(updatingPositionBlitCode, updatingUVBlitCode), run_time=0.01)
            self.wait(1)

            def update_uv_blit_image(mob):
                # Calculate the target u and v values from the trackers
                target_u = clamp(int(uValue.get_value()), 0, 256)
                target_v = clamp(int(vValue.get_value()), 0, 256)

                # Crop the image to the target u and v values
                cropped_image_array = crop_image_array(uvBlitImage.get_pixel_array(), target_u, target_v, 256, 256)

                # Update the ImageMobject with the new texture
                mob.become(ImageMobject(np.uint8(cropped_image_array)))

                # Calculate the position using xValue and yValue (assuming these trackers are defined elsewhere)
                mob.shift(
                    UP * 2 + DOWN * guiImage.get_height() / 2 +
                    LEFT * 3 + RIGHT * guiImage.get_width() / 2 +
                    RIGHT * interp(
                        xValue.get_value(),
                        [0, 1028],
                        [0, 5.5 - guiImage.get_width()]
                    ) +
                    DOWN * interp(
                        yValue.get_value(),
                        [0, 768],
                        [0, 4 - guiImage.get_height()]
                    ))

            uvBlitImage = ImageMobject("assets/images/sample_gui.png")
            uvBlitImage.add_updater(update_uv_blit_image)
            self.play(ReplacementTransform(blitImage, uvBlitImage), run_time=0.01)

            self.play(uValue.animate.set_value(256), run_time=2.5, rate_func=linear)
            self.play(uValue.animate.set_value(0), run_time=0.75, rate_func=smooth)
            self.wait(1)
            self.play(vValue.animate.set_value(256), run_time=2.5, rate_func=linear)
            self.play(vValue.animate.set_value(0), run_time=0.75, rate_func=smooth)
            self.wait(1)

            self.wait(5)

        window = create_window()
        self.wait(0.5)
        show_window_size()
        self.wait(0.5)
        demonstrate_blit()
        self.wait(0.5)
