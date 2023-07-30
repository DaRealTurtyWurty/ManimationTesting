import math

from manim import *
from numpy import interp


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

            widthArrow = DoubleArrow(
                start=LEFT * 3 + UP * 2 + UP * 0.15,
                end=RIGHT * 3 + UP * 2 + UP * 0.15,
                color=BLUE,
                stroke_width=2,
                tip_length=0.25
            )

            widthText = Text(
                text="1028",
                font="Consolas",
                color=BLUE
            ).scale(0.5).next_to(widthArrow, UP * 0.15)

            self.play(Create(widthArrow), Write(widthText), run_time=0.5)
            self.wait(1)

            heightArrow = DoubleArrow(
                start=LEFT * 3 + UP * 2 + LEFT * 0.15,
                end=LEFT * 3 + DOWN * 2 + LEFT * 0.15,
                color=GREEN,
                stroke_width=2,
                tip_length=0.25
            )

            heightText = Text(
                text="768",
                font="Consolas",
                color=GREEN
            ).scale(0.5).next_to(heightArrow, LEFT * 0.05).rotate(PI / 2)

            self.play(Create(heightArrow), Write(heightText), run_time=0.5)

        window = create_window()
        self.wait(0.5)
        show_window_size()
        self.wait(0.5)
        demonstrate_blit()
        self.wait(0.5)

