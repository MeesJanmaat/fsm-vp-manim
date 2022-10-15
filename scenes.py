from manim import *
import numpy as np

BACKGROUND_COLOR = GRAY_E
TEXT_COLOR = WHITE
TEXT_OUTLINE_COLOR = BLACK
TEXT_OUTLINE_WIDTH = 4
GRADIENT_RGBA_MAX = [1.0, 0.3, 0.3, 1.0]
GRADIENT_RGMA_MIN = [0.0, 0.3, 0.3, 1.0]

Tex.set_default(color=TEXT_COLOR, background_stroke_width = TEXT_OUTLINE_WIDTH, background_stroke_color = TEXT_OUTLINE_COLOR)
MathTex.set_default(color=TEXT_COLOR, background_stroke_width = TEXT_OUTLINE_WIDTH, background_stroke_color = TEXT_OUTLINE_COLOR)
config.background_color = BACKGROUND_COLOR

class FlowVelocityDefine(Scene):
    def construct(self):
        eq = Tex(r"$\mathbf{u}(\vec{x}) = u(r) \hat{\theta}$")
        self.play(Write(eq[0][:5]))
        self.wait()
        self.play(Write(eq[0][5:]))
        self.wait()

class FlowVelocityRigidbody(Scene):
    def construct(self):
        eq = Tex(r"$u(r) = C r$")
        self.play(Write(eq))
        self.wait()

class FlowVelocityFree(Scene):
    def construct(self):
        eq = Tex(r"$u(r) = \frac{C}{r}$")
        self.play(Write(eq))
        self.wait()

class FlowFieldRigidbody(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=0, theta=0)

        func = lambda pos: pos[0] * DOWN + pos[1] * RIGHT if np.sqrt(pos[0]**2 + pos[1]**2) < 4 else 0 * RIGHT
        vf = ArrowVectorField(func, x_range=[-5, 5, 0.5], y_range=[-5, 5, 0.5], min_color_scheme_value=0, max_color_scheme_value=4, colors=[BLUE_C, RED_C], length_func=lambda x: x/5)
        self.play(Create(vf))
        self.wait()
        self.move_camera(phi=60*DEGREES, theta=45*DEGREES)
        self.wait()

class FlowFieldRigidbodyLines(ThreeDScene):
    def construct(self):
        radii = np.linspace(0.3, 3.5, 12)
        loops = VGroup(
            *[
                VGroup(
                    Circle(radius=r),
                    Triangle().scale(0.1).set_fill(RED, 1.0).move_to(Circle(radius=r).point_at_angle(0)).shift(0.05 * UP)
                ).set_color(rgba_to_color([r / 3.5 * (GRADIENT_RGBA_MAX[i] - GRADIENT_RGMA_MIN[i]) + GRADIENT_RGMA_MIN[i] for i in range(4)]))
            for r in radii]
        )
        self.play(Create(loops))
        self.play(*[Rotate(loops[i][1], radii[i] * 5 * PI, about_point=[0, 0, 0], rate_func=linear, run_time=10) for i in range(len(radii))])
        self.wait()

class FlowFieldRigidbodyLinesAngled(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        radii = np.linspace(0.3, 3.5, 12)
        loops = VGroup(
            *[
                VGroup(
                    Circle(radius=r),
                    Triangle().scale(0.1).set_fill(RED, 1.0).move_to(Circle(radius=r).point_at_angle(0)).shift(0.05 * UP)
                ).set_color(rgba_to_color([r / 3.5 * (GRADIENT_RGBA_MAX[i] - GRADIENT_RGMA_MIN[i]) + GRADIENT_RGMA_MIN[i] for i in range(4)]))
            for r in radii]
        )
        self.play(Create(loops))
        self.play(*[Rotate(loops[i][1], radii[i] * 5 * PI, about_point=[0, 0, 0], rate_func=linear, run_time=10) for i in range(len(radii))])
        self.wait()


class FlowFieldRigidbodyLinesWithVorticity(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)

        vorticity_func = lambda pos: OUT if np.sqrt(pos[0]**2 + pos[1]**2) < 3.5 else 0 * OUT
        vorticity_vf = ArrowVectorField(vorticity_func, color=YELLOW, x_range=[-5, 5, 0.5], y_range=[-5, 5, 0.5])
        vorticity_label = MathTex(r"\boldsymbol{\omega}").shift(3*LEFT + 2 * UP)

        radii = np.linspace(0.3, 3.5, 12)
        loops = VGroup(
            *[
                VGroup(
                    Circle(radius=r),
                    Triangle().scale(0.1).set_fill(RED, 1.0).move_to(Circle(radius=r).point_at_angle(0)).shift(0.05 * UP)
                ).set_color(rgba_to_color([r / 3.5 * (GRADIENT_RGBA_MAX[i] - GRADIENT_RGMA_MIN[i]) + GRADIENT_RGMA_MIN[i] for i in range(4)]))
            for r in radii]
        )
        self.play(Create(loops))
        self.add_fixed_in_frame_mobjects(vorticity_label)
        self.play(Create(vorticity_vf), Write(vorticity_label), *[Rotate(loops[i][1], radii[i] * 5 * PI, about_point=[0, 0, 0], rate_func=linear, run_time=10) for i in range(len(radii))])
        self.wait()

class FlowFieldFree(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=0, theta=0)

        func = lambda pos: (pos[0] * DOWN + pos[1] * RIGHT) / (pos[0]**2 + pos[1]**2) if 0.1 < np.sqrt(pos[0]**2 + pos[1]**2) < 4 else 0 * RIGHT
        vf = ArrowVectorField(func, x_range=[-5, 5, 0.5], y_range=[-5, 5, 0.5], min_color_scheme_value=0, max_color_scheme_value=1, colors=[BLUE_C, RED_C], length_func=lambda x: x/3)
        self.play(Create(vf))
        self.wait()
        self.move_camera(phi=60*DEGREES, theta=45*DEGREES)
        self.wait()

class FlowFieldFreeLines(ThreeDScene):
    def construct(self):
        radii = np.linspace(0.3, 3.5, 12)
        loops = VGroup(
            *[
                VGroup(
                    Circle(radius=r),
                    Triangle().scale(0.1).set_fill(RED, 1.0).move_to(Circle(radius=r).point_at_angle(0)).shift(0.05 * UP)
                ).set_color(rgba_to_color([0.3 / r * (GRADIENT_RGBA_MAX[i] - GRADIENT_RGMA_MIN[i]) + GRADIENT_RGMA_MIN[i] for i in range(4)]))
            for r in radii]
        )
        self.play(Create(loops))
        self.play(*[Rotate(loops[i][1], 1/radii[i] * 20 * PI, about_point=[0, 0, 0], rate_func=linear, run_time=10) for i in range(len(radii))])
        self.wait()

class FlowFieldFreeLinesAngled(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)

        radii = np.linspace(0.3, 3.5, 12)
        loops = VGroup(
            *[
                VGroup(
                    Circle(radius=r),
                    Triangle().scale(0.1).set_fill(RED, 1.0).move_to(Circle(radius=r).point_at_angle(0)).shift(0.05 * UP)
                ).set_color(rgba_to_color([0.3 / r * (GRADIENT_RGBA_MAX[i] - GRADIENT_RGMA_MIN[i]) + GRADIENT_RGMA_MIN[i] for i in range(4)]))
            for r in radii]
        )
        self.play(Create(loops))
        self.play(*[Rotate(loops[i][1], 1/radii[i] * 20 * PI, about_point=[0, 0, 0], rate_func=linear, run_time=10) for i in range(len(radii))])
        self.wait()

class FlowFieldFreeLinesAngledWithVorticity(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)

        vorticity_vf = Vector(5 * OUT, color=YELLOW)
        vorticity_label = MathTex(r"\boldsymbol{\omega}").to_edge(UP).shift(0.3 * RIGHT)

        radii = np.linspace(0.3, 3.5, 12)
        loops = VGroup(
            *[
                VGroup(
                    Circle(radius=r),
                    Triangle().scale(0.1).set_fill(RED, 1.0).move_to(Circle(radius=r).point_at_angle(0)).shift(0.05 * UP)
                ).set_color(rgba_to_color([0.3 / r * (GRADIENT_RGBA_MAX[i] - GRADIENT_RGMA_MIN[i]) + GRADIENT_RGMA_MIN[i] for i in range(4)]))
            for r in radii]
        )
        self.play(Create(loops))
        self.add_fixed_in_frame_mobjects(vorticity_label)
        self.play(Create(vorticity_vf), Write(vorticity_label), *[Rotate(loops[i][1], 1/radii[i] * 20 * PI, about_point=[0, 0, 0], rate_func=linear, run_time=10) for i in range(len(radii))])
        self.wait()

class FlowFieldFreeBecomeNonideal(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)

        vorticity_vf_ideal = Vector(5 * OUT, color=YELLOW)
        vorticity_func_nonideal = lambda pos: OUT if np.sqrt(pos[0]**2 + pos[1]**2) < 0.5 else 0 * OUT
        vorticity_vf_nonideal = ArrowVectorField(vorticity_func_nonideal, color=YELLOW, x_range=[-0.6, 0.6, 0.2], y_range=[-0.6, 0.6, 0.2], length_func=lambda x: x)
        vorticity_label = MathTex(r"\boldsymbol{\omega}").to_edge(UP).shift(0.3 * RIGHT)

        radii = np.linspace(0.3, 3.5, 12)
        loops = VGroup(
            *[
                VGroup(
                    Circle(radius=r),
                    Triangle().scale(0.1).set_fill(RED, 1.0).move_to(Circle(radius=r).point_at_angle(0)).shift(0.05 * UP)
                ).set_color(rgba_to_color([0.3 / r * (GRADIENT_RGBA_MAX[i] - GRADIENT_RGMA_MIN[i]) + GRADIENT_RGMA_MIN[i] for i in range(4)]))
            for r in radii]
        )
        self.play(Create(loops))
        self.add_fixed_in_frame_mobjects(vorticity_label)
        self.play(Create(vorticity_vf_ideal), Write(vorticity_label), *[Rotate(loops[i][1], 1/radii[i] * 20 * PI, about_point=[0, 0, 0], rate_func=linear, run_time=10) for i in range(len(radii))])
        self.play(vorticity_vf_ideal.animate.become(vorticity_vf_nonideal), *[Rotate(loops[i][1], 1/radii[i] * 20 * PI, about_point=[0, 0, 0], rate_func=linear, run_time=10) for i in range(len(radii))])
        self.wait()

class VorticityDefine(Scene):
    def construct(self):
        eq = Tex(r"$\boldsymbol{\omega} = \nabla \times \mathbf{u}$")
        self.play(Write(eq))
        self.wait()

class VorticityIsUniform(Scene):
    def construct(self):
        eq = MathTex(r"\boldsymbol{\omega} = C \hat{z}")
        self.play(Write(eq))
        self.wait()

class VorticityIsZero(Scene):
    def construct(self):
        eq = MathTex(r"\boldsymbol{\omega} = 0")
        self.play(Write(eq))
        self.wait()

class KelvinsTheorem(Scene):
    def construct(self):
        text = Tex(r"Kelvin's circulation theorem")
        self.play(Write(text))
        self.wait()

class BottleNoVortex(Scene):
    def construct(self):
        slider = Line(0.5 * LEFT, RIGHT)

        liquid_fill = Polygon(
            [-0.5, 0, 0], [-0.5, 1, 0], [-2, 2, 0], [-2, 4, 0],
            [2, 4, 0], [2, 2, 0], [0.5, 1, 0], [0.5, 0, 0]
        ).set_fill(BLUE, 1.0).set_z_index(-1)

        bottle_poly = Polygon(
            [-0.5, 0, 0], [-0.5, 1, 0], [-2, 2, 0], [-2, 5, 0],
            [2, 5, 0], [2, 2, 0], [0.5, 1, 0], [0.5, -1, 0],
            [2, -2, 0], [2, -5, 0], [-2, -5, 0], [-2, -2, 0],
            [-0.5, -1, 0], color=WHITE
        )

        self.play(Create(slider))
        self.play(Create(bottle_poly))
        self.play(FadeIn(liquid_fill))

        self.wait()

        self.play(slider.animate.shift(RIGHT))

        liquid_flowing = Polygon(
            [-0.5, 0, 0], [-0.5, 4, 0], [0.5, 4, 0], [0.5, 0, 0]
        ).set_fill(BLUE, 1.0).set_z_index(-1)
        self.add(liquid_flowing)

        self.play(liquid_flowing.animate.shift(4*DOWN), FadeOut(slider), rate_func=rate_functions.ease_in_quad)

        water_arrow = Arrow(start=2.5 * UP, end=0.5 * UP)
        water_label = Tex("Water").shift(3 * UP)
        self.play(Write(water_label), Create(water_arrow))

        air_arrow1 = Arrow(start=2.5 * DOWN + 1 * LEFT, end=0.8 * DOWN + 0.2 * LEFT)
        air_arrow2 = Arrow(start=2.5 * DOWN + 1 * RIGHT, end=0.8 * DOWN + 0.2 * RIGHT)
        air_label = Tex("Air").shift(3 * DOWN)
        self.play(Write(air_label), Create(air_arrow1), Create(air_arrow2))
        self.wait()
        self.play(FadeOut(air_label, air_arrow1, air_arrow2, water_label, water_arrow))

        bubble1 = Circle(color=WHITE, radius=0.35).set_fill(WHITE, 0.5)
        bubble2 = Circle(color=WHITE, radius=0.25).set_fill(WHITE, 0.5).shift(0.8 * UP, 0.2 * LEFT)
        bubble3 = Circle(color=WHITE, radius=0.1).set_fill(WHITE, 0.5).shift(1.2 * UP, 0.1 * RIGHT)

        self.play(FadeIn(bubble1, bubble2, bubble3), bubble1.animate.shift(UP), bubble2.animate.shift(1.3 * UP), bubble3.animate.shift(1.6 * UP), run_time=4, rate_func=linear)
        self.play(FadeOut(bubble1, bubble2, bubble3, shift=0.3*UP, rate_func=linear))

class BottleWithVortex(Scene):
    def construct(self):
        liquid_fill1 = Polygon(
            [-0.5, 0, 0], [-0.5, 1, 0], [-2, 2, 0], [-2, 4, 0],
            [-1, 4, 0], [-0.75, 3.5, 0], [-0.5, 2.5, 0], [-0.4, 1, 0], [-0.35, -4, 0], [-0.45, -4, 0]
        ).set_fill(BLUE, 1.0).set_z_index(-1)

        liquid_fill2 = Polygon(
            [0.45, -4, 0], [0.35, -4, 0], [0.4, 1, 0], [0.5, 2, 0], [0.75, 3.25, 0], [1, 4, 0],
            [2, 4, 0], [2, 2, 0], [0.5, 1, 0], [0.5, 0, 0]
        ).set_fill(BLUE, 1.0).set_z_index(-1)

        bottle_poly = Polygon(
            [-0.5, 0, 0], [-0.5, 1, 0], [-2, 2, 0], [-2, 5, 0],
            [2, 5, 0], [2, 2, 0], [0.5, 1, 0], [0.5, -1, 0],
            [2, -2, 0], [2, -5, 0], [-2, -5, 0], [-2, -2, 0],
            [-0.5, -1, 0], color=WHITE
        )

        self.play(Create(bottle_poly))
        self.play(FadeIn(liquid_fill1), FadeIn(liquid_fill2))
        self.wait()

        water_arrow1 = Arrow(start=2.5 * UP + 0.5 * LEFT, end=0.5 * UP + 0.4 * LEFT)
        water_arrow2 = Arrow(start=2.5 * UP + 0.5 * RIGHT, end=0.5 * UP + 0.4 * RIGHT)
        water_label = Tex("Water").shift(3 * UP)
        self.play(Write(water_label), Create(water_arrow1), Create(water_arrow2))

        air_arrow = Arrow(start=2.5 * DOWN, end=0.8 * DOWN)
        air_label = Tex("Air").shift(3 * DOWN)
        self.play(Write(air_label), Create(air_arrow))
        self.wait()