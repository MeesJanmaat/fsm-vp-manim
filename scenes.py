from manim import *
import numpy as np

# Aesthetic defaults
BACKGROUND_COLOR = BLACK
TEXT_COLOR = WHITE
TEXT_OUTLINE_COLOR = BLACK
TEXT_OUTLINE_WIDTH = 0
GRADIENT_RGBA_MAX = [1.0, 0.2, 0.2, 1.0]
GRADIENT_RGBA_MIN = [0.0, 0.2, 0.5, 1.0]

Tex.set_default(color=TEXT_COLOR, background_stroke_width = TEXT_OUTLINE_WIDTH, background_stroke_color = TEXT_OUTLINE_COLOR)
MathTex.set_default(color=TEXT_COLOR, background_stroke_width = TEXT_OUTLINE_WIDTH, background_stroke_color = TEXT_OUTLINE_COLOR)
Line.set_default(background_stroke_width = TEXT_OUTLINE_WIDTH, background_stroke_color = TEXT_OUTLINE_COLOR)
config.background_color = BACKGROUND_COLOR

# Functional defaults
R_MIN = 0.3
R_MAX = 3.5
N_CIRCLES = 12
ROT_RIGIDBODY = 8 * PI
ROT_FREE = 10 * PI

class FlowFieldRigidbodyLines(ThreeDScene):
    def construct(self):
        # Create circles
        radii = np.linspace(R_MIN, R_MAX, N_CIRCLES)
        loops = VGroup(
            *[
                VGroup(
                    Circle(radius=r),
                    Triangle().scale(0.1).set_fill(RED, 1.0).move_to(Circle(radius=r).point_at_angle(0)).shift(0.05 * UP)
                ).set_color(rgba_to_color([r / R_MAX * (GRADIENT_RGBA_MAX[i] - GRADIENT_RGBA_MIN[i]) + GRADIENT_RGBA_MIN[i] for i in range(4)]))
            for r in radii]
        )

        # Animations
        self.play(Create(loops))
        self.play(*[Rotate(loops[i][1], ROT_RIGIDBODY, about_point=[0, 0, 0], rate_func=linear, run_time=25) for i in range(len(radii))])
        self.wait()

class FlowFieldRigidbodyLinesWithVorticity(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)

        # Prepare vorticity vector field
        vorticity_func = lambda pos: OUT if np.sqrt(pos[0]**2 + pos[1]**2) < 3.5 else 0 * OUT
        vorticity_vf = ArrowVectorField(vorticity_func, color=YELLOW, x_range=[-5, 5, 0.8], y_range=[-5, 5, 0.8], length_func=lambda x: x, opacity=0.5)
        vorticity_label = MathTex(r"\boldsymbol{\omega}").shift(2.5 * UP)
        vorticity_label[0][0].set_color(YELLOW)

        # Create circles
        radii = np.linspace(R_MIN, R_MAX, N_CIRCLES)
        loops = VGroup(
            *[
                VGroup(
                    Circle(radius=r),
                    Triangle().scale(0.1).set_fill(RED, 1.0).move_to(Circle(radius=r).point_at_angle(0)).shift(0.05 * UP)
                ).set_color(rgba_to_color([r / R_MAX * (GRADIENT_RGBA_MAX[i] - GRADIENT_RGBA_MIN[i]) + GRADIENT_RGBA_MIN[i] for i in range(4)]))
            for r in radii]
        )

        # Animations
        self.play(Create(loops))
        self.add_fixed_in_frame_mobjects(vorticity_label)
        self.play(Create(vorticity_vf), Write(vorticity_label), *[Rotate(loops[i][1], ROT_RIGIDBODY, about_point=[0, 0, 0], rate_func=linear, run_time=25) for i in range(len(radii))])
        self.wait()

class FlowFieldFreeLines(ThreeDScene):
    def construct(self):
        # Create circles
        radii = np.linspace(R_MIN, R_MAX, N_CIRCLES)
        loops = VGroup(
            *[
                VGroup(
                    Circle(radius=r),
                    Triangle().scale(0.1).set_fill(RED, 1.0).move_to(Circle(radius=r).point_at_angle(0)).shift(0.05 * UP)
                ).set_color(rgba_to_color([min(R_MIN * 2 / r, 1.0) * (GRADIENT_RGBA_MAX[i] - GRADIENT_RGBA_MIN[i]) + GRADIENT_RGBA_MIN[i] for i in range(4)]))
            for r in radii]
        )

        # Animations
        self.play(Create(loops))
        self.play(*[Rotate(loops[i][1], 1/(radii[i])**2 * ROT_FREE, about_point=[0, 0, 0], rate_func=linear, run_time=10) for i in range(len(radii))])
        self.wait()

class FlowFieldFreeBecomeNonideal(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)

        # Prepare vorticity vector fields
        #Delta function
        vorticity_vf_ideal = Line(start=0 * OUT, end=3.35 * OUT, color=YELLOW).set_opacity(0.5)
        vorticity_vf_ideal2 = DashedLine(start=3.35 * OUT, end = 5 * OUT, color=YELLOW).set_opacity(0.5)
        vorticity_vf_ideal_group = VGroup(vorticity_vf_ideal, vorticity_vf_ideal2)
        #Concentrated uniform
        vorticity_func_nonideal = lambda pos: 3 * OUT if np.sqrt(pos[0]**2 + pos[1]**2) < 0.5 else 0 * OUT
        vorticity_vf_nonideal = ArrowVectorField(vorticity_func_nonideal, color=YELLOW, x_range=[-0.6, 0.6, 0.2], y_range=[-0.6, 0.6, 0.2], length_func=lambda x: x, opacity=0.5)
        vorticity_label = MathTex(r"\boldsymbol{\omega}").to_edge(UP).shift(0.3 * RIGHT)
        vorticity_label[0][0].set_color(YELLOW)

        # Create circles
        radii = np.linspace(R_MIN, R_MAX, N_CIRCLES)
        loops = VGroup(
            *[
                VGroup(
                    Circle(radius=r),
                    Triangle().scale(0.1).set_fill(RED, 1.0).move_to(Circle(radius=r).point_at_angle(0)).shift(0.05 * UP)
                ).set_color(rgba_to_color([min(R_MIN * 2 / r, 1.0) * (GRADIENT_RGBA_MAX[i] - GRADIENT_RGBA_MIN[i]) + GRADIENT_RGBA_MIN[i] for i in range(4)]))
            for r in radii]
        )

        # Animations
        self.play(Create(loops))
        self.add_fixed_in_frame_mobjects(vorticity_label)
        self.play(FadeIn(vorticity_vf_ideal_group), Write(vorticity_label), *[Rotate(loops[i][1], 1/(radii[i])**2 * ROT_FREE, about_point=[0, 0, 0], rate_func=linear, run_time=10) for i in range(len(radii))])
        #Update circles colour mapping
        for i in range(len(radii)):
            loops[i].set_color(rgba_to_color([min(0.6 / radii[i], 1.0) * (GRADIENT_RGBA_MAX[j] - GRADIENT_RGBA_MIN[j]) + GRADIENT_RGBA_MIN[j] if radii[i] > 0.8 else radii[i] / 3.5 * (GRADIENT_RGBA_MAX[j] - GRADIENT_RGBA_MIN[j]) + GRADIENT_RGBA_MIN[j] for j in range(4)]))
        self.play(vorticity_vf_ideal_group.animate.become(vorticity_vf_nonideal), *[Rotate(loops[i][1], 1/(radii[i])**2 * ROT_FREE if radii[i] > 0.8 else ROT_RIGIDBODY, about_point=[0, 0, 0], rate_func=linear, run_time=20) for i in range(len(radii))])
        self.wait()

class KelvinsTheorem(Scene):
    def construct(self):
        # Prepare texts
        subtitle1 = Tex(r"Without any external forces acting on it,")
        title = Tex(r"\textbf{Kelvin's circulation theorem}", font_size=72).set_color(RED_B).next_to(subtitle1, UP)
        subtitle2 = Tex(r"an irrotational vortex remains irrotational.").next_to(subtitle1, DOWN)

        # Animations
        self.play(Write(subtitle1))
        self.play(Write(subtitle2))
        self.play(Write(title))
        self.wait()

class BottleNoVortex(Scene):
    def construct(self):
        # Prepare shapes
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

        # Construct bottle
        self.play(Create(slider))
        self.play(Create(bottle_poly))
        self.play(FadeIn(liquid_fill))

        self.wait()

        self.play(slider.animate.shift(RIGHT))

        # Liquid flow animation
        liquid_flowing = Polygon(
            [-0.5, 0, 0], [-0.5, 4, 0], [0.5, 4, 0], [0.5, 0, 0]
        ).set_fill(BLUE, 1.0).set_z_index(-1)
        self.add(liquid_flowing)

        self.play(liquid_flowing.animate.shift(4*DOWN), FadeOut(slider), rate_func=rate_functions.ease_in_quad)

        # Water/air direction anims
        water_arrow = Arrow(start=2.5 * UP, end=0.5 * UP)
        water_label = Tex("Water").shift(3 * UP)
        self.play(Write(water_label), Create(water_arrow))

        air_arrow1 = Arrow(start=2.5 * DOWN + 1 * LEFT, end=0.8 * DOWN + 0.2 * LEFT)
        air_arrow2 = Arrow(start=2.5 * DOWN + 1 * RIGHT, end=0.8 * DOWN + 0.2 * RIGHT)
        air_label = Tex("Air").shift(3 * DOWN)
        self.play(Write(air_label), Create(air_arrow1), Create(air_arrow2))
        self.wait()
        self.play(FadeOut(air_label, air_arrow1, air_arrow2, water_label, water_arrow))

        # Bubble anims
        bubble1 = Circle(color=WHITE, radius=0.35).set_fill(WHITE, 0.5)
        bubble2 = Circle(color=WHITE, radius=0.25).set_fill(WHITE, 0.5).shift(0.8 * UP, 0.2 * LEFT)
        bubble3 = Circle(color=WHITE, radius=0.1).set_fill(WHITE, 0.5).shift(1.2 * UP, 0.1 * RIGHT)

        self.play(FadeIn(bubble1, bubble2, bubble3), bubble1.animate.shift(UP), bubble2.animate.shift(1.3 * UP), bubble3.animate.shift(1.6 * UP), run_time=4, rate_func=linear)
        self.play(FadeOut(bubble1, bubble2, bubble3, shift=0.3*UP, rate_func=linear))

class BottleWithVortex(Scene):
    def construct(self):
        # Prepare shapes
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

        # Construct bottle
        self.play(Create(bottle_poly))
        self.play(FadeIn(liquid_fill1), FadeIn(liquid_fill2))
        self.wait()

        # Water/air direction anims
        water_arrow1 = Arrow(start=2.5 * UP + 0.5 * LEFT, end=0.5 * UP + 0.4 * LEFT)
        water_arrow2 = Arrow(start=2.5 * UP + 0.5 * RIGHT, end=0.5 * UP + 0.4 * RIGHT)
        water_label = Tex("Water").shift(3 * UP)
        self.play(Write(water_label), Create(water_arrow1), Create(water_arrow2))

        air_arrow = Arrow(start=2.5 * DOWN, end=0.8 * DOWN)
        air_label = Tex("Air").shift(3 * DOWN)
        self.play(Write(air_label), Create(air_arrow))
        self.wait()

class FlowVelocityFunctions(Scene):
    def construct(self):
        # Introduce formula
        title = Tex("Flow velocity").to_edge(UP, buff=1.0)
        eq = MathTex(r"\mathbf{u}(\vec{x})").next_to(title, DOWN)
        eq[0][0].set_color(BLUE)
        eq2 = MathTex(r"{{ \mathbf{u}(\vec{x}) }} = {{ u(r) }} \; \hat{\theta}").next_to(title, DOWN)
        eq2[0][0].set_color(BLUE)
        eq2[2][0].set_color(GREEN)

        self.play(Write(title))
        self.play(Write(eq))
        self.play(eq.animate.move_to(eq2.get_part_by_tex(r"\mathbf{u}(\vec{x})")))
        self.play(FadeIn(eq2), FadeOut(eq))

        tex_part = eq2.get_part_by_tex(r"u(r)")
        
        rect = SurroundingRectangle(tex_part)

        self.play(Create(rect))
        self.wait()

        # Rigid-body
        func1 = MathTex(r"{{ u(r) }} \propto r").shift(3 * LEFT)
        func1[0][0].set_color(GREEN)
        label1 = Tex(r"Rigid-body").next_to(func1, DOWN)

        arrow1 = Arrow(LEFT, RIGHT).set_color(YELLOW).put_start_and_end_on(rect.get_bottom(), func1.get_part_by_tex(r"u(r)").get_top() + 0.3 * UP + RIGHT)

        self.play(Create(arrow1, shift=0.3 * DOWN))

        self.play(Write(func1))
        self.play(Write(label1))

        self.play(FadeOut(func1, label1, arrow1))

        # Free
        func2 = MathTex(r"{{ u(r) }} \propto \frac{1}{r}").shift(3 * RIGHT)
        func2[0][0].set_color(GREEN)
        label2 = Tex(r"Free").next_to(func2, DOWN)

        arrow2 = Arrow(LEFT, RIGHT).set_color(YELLOW).put_start_and_end_on(rect.get_bottom(), func2.get_part_by_tex(r"u(r)").get_top() + 0.3 * UP + 0.3 * LEFT)

        self.play(Create(arrow2, shift=0.3 * DOWN))

        self.play(Write(func2))
        self.play(Write(label2))

class Vorticity(Scene):
    def construct(self):
        # Introduce formula
        title = Tex("Vorticity").to_edge(UP, buff=1.0)
        eq = MathTex(r"\boldsymbol{\omega} = \nabla \times \mathbf{u}").next_to(title, DOWN)
        eq[0][0].set_color(YELLOW)
        eq[0][-1].set_color(BLUE)

        self.play(Write(title))
        self.play(Write(eq))

        # Rigid-body
        subtitle1 = Tex("Rigid-body").shift(3 * LEFT)
        func1 = MathTex(r"\boldsymbol{\omega} = C \hat{z}").next_to(subtitle1, DOWN)
        func1[0][0].set_color(YELLOW)

        self.play(Write(subtitle1))
        self.play(Write(func1))

        self.play(FadeOut(func1, subtitle1))

        # Free
        subtitle2 = Tex("Free").shift(3 * RIGHT)
        func2 = MathTex(r"\boldsymbol{\omega} = \delta(r)").next_to(subtitle2, DOWN)
        func2[0][0].set_color(YELLOW)

        self.play(Write(subtitle2))
        self.play(Write(func2))

        # Non-ideal free
        subtitle3 = Tex("Free (non-ideal)").shift(3 * RIGHT)
        func3 = MathTex(r"\boldsymbol{\omega}(r) = \begin{cases} C \hat{z}, & \text{if } r < R \\ \mathbf{0}, & \text{if } r > R \end{cases}").next_to(subtitle3, DOWN)
        func3[0][0].set_color(YELLOW)

        self.play(FadeOut(subtitle2, func2))
        self.play(Write(subtitle3))
        self.play(Write(func3))