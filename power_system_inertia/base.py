from manim import *
import numpy as np


class CommaDecimalNumber(DecimalNumber):
    # Keep the animated gauge value in Portuguese decimal format.
    def _get_num_string(self, number):
        return super()._get_num_string(number).replace(".", ",")


from .languages import LANGUAGES


class PowerSystemInertiaBase(Scene):
    def setup_scene(self, language_code="pt"):
        # Configure the common scene style and active language.
        self.language_code = language_code
        self.camera.background_color = "#0b1020"
        self.colors = {
            "text": "#F4F7FB",
            "muted": "#B8C2D6",
            "grid": "#2B3448",
            "blue": "#43B7FF",
            "cyan": "#6FE7E7",
            "red": "#FF5A5F",
            "orange": "#FFB347",
            "yellow": "#FFE066",
            "green": "#70E080",
            "purple": "#B892FF",
        }

    def tr(self, value):
        # Translate exact text fragments when a target language provides them.
        if not isinstance(value, str):
            return value
        return LANGUAGES.get(self.language_code, {}).get(value, value)

    def translated_args(self, args):
        # Translate positional string arguments passed to Manim text objects.
        return tuple(self.tr(arg) if isinstance(arg, str) else arg for arg in args)

    def Text(self, *args, **kwargs):
        # Local wrapper used by slide modules for dictionary-based languages.
        return Text(*self.translated_args(args), **kwargs)

    def Tex(self, *args, **kwargs):
        # Local wrapper used by slide modules for dictionary-based languages.
        return Tex(*self.translated_args(args), **kwargs)

    def MathTex(self, *args, **kwargs):
        # Local wrapper used by slide modules for dictionary-based languages.
        return MathTex(*self.translated_args(args), **kwargs)

    pacing_factor = 2.175
    turbine_nominal_speed = 4.0

    def play(self, *animations, **kwargs):
        # Slow all animations consistently to obtain a lecture-paced video.
        if "run_time" in kwargs:
            kwargs["run_time"] *= self.pacing_factor
        else:
            kwargs["run_time"] = self.pacing_factor
        return super().play(*animations, **kwargs)

    def wait(self, duration=1.0, stop_condition=None, frozen_frame=None):
        # Keep reading pauses proportional to the animation pacing.
        return super().wait(
            duration * self.pacing_factor,
            stop_condition=stop_condition,
            frozen_frame=frozen_frame,
        )

    def make_title(self, text, subtitle=None):
        text = self.tr(text)
        subtitle = self.tr(subtitle) if subtitle else None
        title = self.Text(text, font_size=34, weight=BOLD, color=self.colors["text"])
        title.to_edge(UP, buff=0.35)
        if subtitle:
            subtitle_mob = self.Text(subtitle, font_size=17, color=self.colors["muted"])
            subtitle_mob.next_to(title, DOWN, buff=0.06)
            subtitle_mob.set_width(min(subtitle_mob.width, 10.8))
            title_group = VGroup(title, subtitle_mob)
        else:
            title_group = VGroup(title)
        underline = Line(LEFT, RIGHT, color=self.colors["blue"]).set_width(11.5)
        underline.next_to(title_group, DOWN, buff=0.10)
        return VGroup(title_group, underline)

    def make_caption(self, text, width=10.8, font_size=25):
        text = self.tr(text)
        caption = self.Text(text, font_size=font_size, color=self.colors["text"], line_spacing=0.85)
        if caption.width > width:
            caption.set_width(width)
        return caption

    def equation_box(self, equation, color=None, buff=0.18):
        box_color = color or self.colors["blue"]
        box = RoundedRectangle(
            corner_radius=0.08,
            width=equation.width + 2 * buff,
            height=equation.height + 2 * buff,
            stroke_color=box_color,
            stroke_width=2,
            fill_color="#101A33",
            fill_opacity=0.72,
        )
        box.move_to(equation)
        return VGroup(box, equation)

    def legend_block(self, rows, font_size=24, color=None, buff=0.18, line_buff=0.10):
        # Build a compact technical legend with a subtle background.
        text_color = color or self.colors["text"]
        items = VGroup(
            *[self.MathTex(row, font_size=font_size, color=text_color) for row in rows]
        ).arrange(DOWN, aligned_edge=LEFT, buff=line_buff)
        box = RoundedRectangle(
            corner_radius=0.08,
            width=items.width + 2 * buff,
            height=items.height + 2 * buff,
            stroke_color=self.colors["grid"],
            stroke_width=1.5,
            fill_color="#101A33",
            fill_opacity=0.62,
        )
        box.move_to(items)
        return VGroup(box, items)

    def clear_scene(self):
        if self.mobjects:
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)

    def highlight_terms(self, equation, tex_to_color):
        # Apply consistent colors to selected LaTeX substrings.
        for tex, color in tex_to_color.items():
            equation.set_color_by_tex(tex, color)
        return equation

    def labeled_arrow(self, start, end, label_tex, color):
        arrow = Arrow(start, end, buff=0.12, color=color, stroke_width=5, max_tip_length_to_length_ratio=0.12)
        label = self.MathTex(label_tex, color=color, font_size=34)
        label.next_to(arrow, UP, buff=0.08)
        return VGroup(arrow, label)

    # -------------------------------------------------------------------------
    # Diagram helpers
    # -------------------------------------------------------------------------
    def draw_power_system(self, frequency_value="60,0 Hz", disturbed=False, meter_disturbed=None):
        # Draw a compact generator-grid-load chain with simple technical icons.
        if meter_disturbed is None:
            meter_disturbed = disturbed

        blade = Polygon(
            ORIGIN + LEFT * 0.05 + DOWN * 0.04,
            ORIGIN + RIGHT * 0.33 + UP * 0.11,
            ORIGIN + RIGHT * 0.16 + DOWN * 0.18,
            fill_color=self.colors["cyan"],
            fill_opacity=0.58,
            stroke_color=self.colors["cyan"],
            stroke_width=1.2,
        )
        blades = VGroup(*[blade.copy().rotate(k * TAU / 3, about_point=ORIGIN) for k in range(3)])
        turbine = VGroup(
            Circle(radius=0.48, stroke_color=self.colors["cyan"], stroke_width=3,
                   fill_color="#0F2630", fill_opacity=0.72),
            blades,
            Dot(ORIGIN, radius=0.08, color=self.colors["cyan"]),
            self.Text("Turbina", font_size=22, color=self.colors["text"]).shift(DOWN * 0.82),
        )
        turbine.move_to(LEFT * 4.6 + DOWN * 0.15)

        sine = ParametricFunction(
            lambda t: np.array([t, 0.11 * np.sin(15 * t), 0.0]),
            t_range=[-0.32, 0.32],
            color=self.colors["blue"],
            stroke_width=4,
        )
        generator = VGroup(
            Circle(radius=0.56, stroke_color=self.colors["blue"], stroke_width=3,
                   fill_color="#10243A", fill_opacity=0.78),
            Circle(radius=0.34, stroke_color=self.colors["blue"], stroke_width=1.5,
                   fill_opacity=0),
            sine,
            Dot(ORIGIN, radius=0.045, color=self.colors["cyan"]),
            self.Text("Gerador", font_size=22, color=self.colors["text"]).shift(DOWN * 0.92),
        )
        generator.move_to(LEFT * 2.55 + DOWN * 0.15)

        shaft = Line(turbine[0].get_right(), generator[0].get_left(), color=self.colors["muted"], stroke_width=5)

        connection_y = generator[0].get_center()[1]
        grid_center = np.array([0.05, connection_y, 0.0])
        tower_color = "#D7DEE9"
        arm_color = self.colors["blue"]
        apex = grid_center + UP * 0.68
        base_left = grid_center + LEFT * 0.38 + DOWN * 0.58
        base_right = grid_center + RIGHT * 0.38 + DOWN * 0.58
        mast_bottom = grid_center + DOWN * 0.58
        cross_arms = VGroup(
            Line(grid_center + LEFT * 0.58 + UP * 0.34, grid_center + RIGHT * 0.58 + UP * 0.34,
                 color=arm_color, stroke_width=3.0),
            Line(grid_center + LEFT * 0.45 + UP * 0.06, grid_center + RIGHT * 0.45 + UP * 0.06,
                 color=tower_color, stroke_width=2.6),
            Line(grid_center + LEFT * 0.30 + DOWN * 0.22, grid_center + RIGHT * 0.30 + DOWN * 0.22,
                 color=tower_color, stroke_width=2.2),
        )
        braces = VGroup(
            Line(apex, base_left, color=tower_color, stroke_width=2.6),
            Line(apex, base_right, color=tower_color, stroke_width=2.6),
            Line(apex, mast_bottom, color=tower_color, stroke_width=2.3),
            Line(grid_center + LEFT * 0.45 + UP * 0.34, grid_center + RIGHT * 0.34 + DOWN * 0.22,
                 color=tower_color, stroke_width=1.5),
            Line(grid_center + RIGHT * 0.45 + UP * 0.34, grid_center + LEFT * 0.34 + DOWN * 0.22,
                 color=tower_color, stroke_width=1.5),
            Line(grid_center + LEFT * 0.30 + DOWN * 0.22, grid_center + RIGHT * 0.38 + DOWN * 0.58,
                 color=tower_color, stroke_width=1.5),
            Line(grid_center + RIGHT * 0.30 + DOWN * 0.22, grid_center + LEFT * 0.38 + DOWN * 0.58,
                 color=tower_color, stroke_width=1.5),
        )
        insulators = VGroup()
        for x_offset, y_offset in [(-0.52, 0.30), (0.52, 0.30), (-0.39, 0.02), (0.39, 0.02)]:
            insulators.add(
                Line(
                    grid_center + RIGHT * x_offset + UP * y_offset,
                    grid_center + RIGHT * x_offset + UP * (y_offset - 0.13),
                    color=self.colors["yellow"],
                    stroke_width=2.3,
                )
            )
            insulators.add(Dot(grid_center + RIGHT * x_offset + UP * (y_offset - 0.15),
                               radius=0.025, color=self.colors["yellow"]))
        tower = VGroup(
            Circle(radius=0.72, stroke_color="#22304B", stroke_width=1.4,
                   fill_color="#0D1830", fill_opacity=0.18).move_to(grid_center + UP * 0.02),
            braces,
            cross_arms,
            insulators,
            self.Text("Rede", font_size=22, color=self.colors["text"]).move_to(grid_center + DOWN * 0.98),
        )

        load_box = RoundedRectangle(
            corner_radius=0.08,
            width=1.18,
            height=0.94,
            stroke_color=self.colors["orange"],
            stroke_width=3,
            fill_color="#2B1E10",
            fill_opacity=0.62,
        )
        load_inner = RoundedRectangle(
            corner_radius=0.06,
            width=1.02,
            height=0.78,
            stroke_color="#D98A2D",
            stroke_width=1.0,
            fill_opacity=0,
        )
        load_inner.set_stroke(opacity=0.55)
        load_terminals = VGroup()
        for x_offset in [-0.24, 0.0, 0.24]:
            load_terminals.add(
                VGroup(
                    Line(
                        RIGHT * x_offset + UP * 0.39,
                        RIGHT * x_offset + UP * 0.25,
                        color=self.colors["yellow"],
                        stroke_width=3,
                    ),
                    Dot(RIGHT * x_offset + UP * 0.22, radius=0.018, color=self.colors["yellow"]),
                )
            )
        load_bus = Line(LEFT * 0.38 + UP * 0.14, RIGHT * 0.38 + UP * 0.14,
                        color=self.colors["cyan"], stroke_width=3.0)
        load_bus_drops = VGroup(
            Line(LEFT * 0.26 + UP * 0.14, LEFT * 0.26 + UP * 0.02, color=self.colors["cyan"], stroke_width=2.0),
            Line(ORIGIN + UP * 0.14, ORIGIN + UP * 0.02, color=self.colors["cyan"], stroke_width=2.0),
            Line(RIGHT * 0.26 + UP * 0.14, RIGHT * 0.26 + UP * 0.02, color=self.colors["cyan"], stroke_width=2.0),
        )
        load_lead_left = Line(LEFT * 0.42 + DOWN * 0.11, LEFT * 0.26 + DOWN * 0.11,
                              color=self.colors["orange"], stroke_width=4)
        load_zigzag = VMobject(stroke_color=self.colors["yellow"], stroke_width=4)
        load_zigzag.set_points_as_corners([
            LEFT * 0.26 + DOWN * 0.11,
            LEFT * 0.16 + UP * 0.02,
            LEFT * 0.06 + DOWN * 0.25,
            RIGHT * 0.06 + UP * 0.02,
            RIGHT * 0.16 + DOWN * 0.25,
            RIGHT * 0.28 + DOWN * 0.11,
        ])
        load_lead_right = Line(RIGHT * 0.28 + DOWN * 0.11, RIGHT * 0.42 + DOWN * 0.11,
                               color=self.colors["orange"], stroke_width=4)
        demand_arrow = Arrow(
            DOWN * 0.30,
            DOWN * 0.47,
            color=self.colors["orange"],
            stroke_width=3.0,
            max_tip_length_to_length_ratio=0.45,
            buff=0.0,
        )
        load = VGroup(
            load_box,
            load_inner,
            load_terminals,
            load_bus,
            load_bus_drops,
            load_lead_left,
            load_zigzag,
            load_lead_right,
            demand_arrow,
            self.Text("Carga", font_size=22, color=self.colors["text"]).shift(DOWN * 0.85),
        )
        load.move_to(RIGHT * 2.55 + DOWN * 0.15)

        generator_link = np.array([generator[0].get_right()[0], connection_y, 0.0])
        load_link = np.array([load[0].get_left()[0], connection_y, 0.0])
        link_1 = Line(generator_link, grid_center + LEFT * 0.47, color=self.colors["muted"], stroke_width=4)
        link_2 = Line(grid_center + RIGHT * 0.47, load_link, color=self.colors["muted"], stroke_width=4)

        meter = self.draw_frequency_meter(frequency_value, disturbed=meter_disturbed)
        meter.move_to(RIGHT * 4.75 + UP * 1.35)

        # Keep power arrows perfectly horizontal, even when components have different sizes.
        pm_y = generator[0].get_top()[1] + 0.75
        pm_start = np.array([turbine[0].get_center()[0], pm_y, 0.0])
        pm_end = np.array([generator[0].get_center()[0], pm_y, 0.0])
        pm = self.labeled_arrow(pm_start, pm_end, "P_m", self.colors["cyan"])

        pe_y = min(generator[0].get_bottom()[1], load[0].get_bottom()[1]) - 0.92
        pe_start = np.array([generator[0].get_center()[0], pe_y, 0.0])
        pe_end = np.array([load[0].get_center()[0], pe_y, 0.0])
        pe = self.labeled_arrow(pe_start, pe_end, "P_e", self.colors["orange"])
        pe[1].next_to(pe[0], DOWN, buff=0.06)

        diagram = VGroup(turbine, shaft, generator, link_1, tower, link_2, load, meter, pm, pe)

        if disturbed:
            disturbance_arrow = Arrow(
                load[0].get_top() + UP * 1.08 + LEFT * 0.05,
                load[0].get_top() + UP * 0.18 + LEFT * 0.05,
                color=self.colors["red"],
                stroke_width=6,
                buff=0.0,
            )
            disturbance_label = self.Text(
                "aumento súbito\nde carga",
                font_size=20,
                color=self.colors["red"],
                line_spacing=0.78,
            )
            disturbance_label.next_to(disturbance_arrow, LEFT, buff=0.18)
            disturbance_label.shift(UP * 0.04)
            disturbance = VGroup(
                disturbance_arrow,
                disturbance_label,
            )
            diagram.add(disturbance)

        return diagram

    def make_energy_pulses(self, paths, color=None, speed=0.42, radius=0.045, phases=(0.0, 0.38, 0.76)):
        # Create small moving dots that continuously indicate power flow.
        pulse_color = color or self.colors["yellow"]
        pulses = VGroup()
        for path in paths:
            for phase in phases:
                dot = Dot(radius=radius, color=pulse_color)
                state = {"alpha": phase}

                def update_dot(mob, dt, path=path, state=state):
                    state["alpha"] = (state["alpha"] + speed * dt) % 1.0
                    mob.move_to(path.point_from_proportion(state["alpha"]))

                dot.add_updater(update_dot)
                pulses.add(dot)
        return pulses

    def clear_energy_pulses(self, pulses):
        # Stop all pulse updaters before transitioning to the next slide.
        for pulse in pulses:
            pulse.clear_updaters()

    def start_turbine(self, turbine_rotor, center_point=None, omega_ref=None):
        # Register a rotor updater every time a turbine appears in a new scene.
        if omega_ref is None:
            omega_ref = [self.turbine_nominal_speed]
        else:
            omega_ref[0] = self.turbine_nominal_speed
        rotation_center = center_point if center_point is not None else turbine_rotor.get_center()
        turbine_rotor.add_updater(
            lambda mob, dt: mob.rotate(omega_ref[0] * dt, about_point=rotation_center)
        )
        return omega_ref

    def stop_turbine(self, turbine_rotor):
        # Clear the updater before scene transitions.
        turbine_rotor.clear_updaters()

    def draw_frequency_meter(self, value, disturbed=False):
        # Draw a small analog gauge. Lower frequency moves the needle counterclockwise.
        ring_color = self.colors["red"] if disturbed else self.colors["green"]
        dial = Circle(
            radius=0.56,
            stroke_color=ring_color,
            stroke_width=3.2,
            fill_color="#111827",
            fill_opacity=0.92,
        )
        inner = Circle(radius=0.46, stroke_color="#22304B", stroke_width=1.2, fill_opacity=0)

        scale_arc = Arc(
            radius=0.42,
            start_angle=210 * DEGREES,
            angle=-240 * DEGREES,
            stroke_color=self.colors["muted"],
            stroke_width=2.0,
        )
        low_arc = Arc(
            radius=0.46,
            start_angle=92 * DEGREES,
            angle=58 * DEGREES,
            stroke_color=self.colors["red"],
            stroke_width=3.0,
        )
        normal_arc = Arc(
            radius=0.46,
            start_angle=-28 * DEGREES,
            angle=55 * DEGREES,
            stroke_color=self.colors["green"],
            stroke_width=3.0,
        )

        ticks = VGroup()
        for angle in [-30, 0, 30, 60, 90, 120]:
            direction = np.array([np.cos(angle * DEGREES), np.sin(angle * DEGREES), 0.0])
            tick = Line(0.38 * direction, 0.47 * direction, color=self.colors["muted"], stroke_width=2)
            ticks.add(tick)

        needle_angle = 56 * DEGREES if disturbed else -14 * DEGREES
        needle_end = 0.39 * np.array([np.cos(needle_angle), np.sin(needle_angle), 0.0])
        needle = Line(ORIGIN, needle_end, color=self.colors["yellow"], stroke_width=4.5)
        counter_weight = Line(ORIGIN, -0.12 * needle_end / np.linalg.norm(needle_end),
                              color=self.colors["yellow"], stroke_width=3.0)
        pivot = Dot(ORIGIN, radius=0.055, color=self.colors["yellow"])
        shine = Arc(radius=0.39, start_angle=124 * DEGREES, angle=42 * DEGREES,
                    stroke_color=WHITE, stroke_opacity=0.18, stroke_width=2.2)

        try:
            numeric_value = float(value.replace("Hz", "").strip().replace(",", "."))
        except ValueError:
            numeric_value = 59.7 if disturbed else 60.0
        label = CommaDecimalNumber(
            numeric_value,
            num_decimal_places=1,
            group_with_commas=False,
            unit=r"\,\mathrm{Hz}",
            unit_buff_per_font_unit=0.004,
            font_size=34,
            color=self.colors["text"],
        )
        label.next_to(dial, DOWN, buff=0.12)
        title = self.Text("frequência", font_size=19, color=self.colors["muted"])
        title.next_to(dial, UP, buff=0.10)
        return VGroup(title, dial, inner, scale_arc, low_arc, normal_arc, ticks, counter_weight, needle, pivot, shine, label)

    def play_frequency_meter_drop(self, meter, *initial_animations, omega_ref=None):
        # Rotate the gauge and update the displayed value during the frequency drop.
        rotating_parts = VGroup(meter[7], meter[8])
        pivot = meter[9].get_center()
        first_stage = []
        second_stage = []
        if omega_ref is not None:
            first_stage.append(
                UpdateFromAlphaFunc(
                    Mobject(),
                    lambda mob, alpha: omega_ref.__setitem__(
                        0, self.turbine_nominal_speed * (1 - 0.045 * alpha)
                    ),
                )
            )
            second_stage.append(
                UpdateFromAlphaFunc(
                    Mobject(),
                    lambda mob, alpha: omega_ref.__setitem__(
                        0, self.turbine_nominal_speed * (0.955 - 0.035 * alpha)
                    ),
                )
            )
        self.play(
            Rotate(rotating_parts, angle=35 * DEGREES, about_point=pivot),
            meter[11].animate.set_value(59.9),
            meter[1].animate.set_stroke(color=self.colors["red"]),
            *initial_animations,
            *first_stage,
            run_time=0.9,
            rate_func=linear,
        )
        self.play(
            Rotate(rotating_parts, angle=35 * DEGREES, about_point=pivot),
            meter[11].animate.set_value(59.7),
            *second_stage,
            run_time=0.6,
            rate_func=linear,
        )

    def draw_rotor(self):
        outer_radius = 0.95
        arc_offset = 0.30
        rotor = VGroup(
            Circle(radius=outer_radius, stroke_color=self.colors["blue"], stroke_width=4,
                   fill_color="#10243A", fill_opacity=0.75),
            Circle(radius=0.2, stroke_color=self.colors["cyan"], stroke_width=3,
                   fill_color=self.colors["cyan"], fill_opacity=0.35),
            Line(LEFT * 0.82, RIGHT * 0.82, color=self.colors["blue"], stroke_width=5),
            Line(DOWN * 0.82, UP * 0.82, color=self.colors["blue"], stroke_width=5),
        )
        spin_arrow = Arc(
            radius=outer_radius + arc_offset,
            arc_center=ORIGIN,
            start_angle=40 * DEGREES,
            angle=132 * DEGREES,
            color=self.colors["yellow"],
            stroke_width=6,
        )
        spin_arrow.add_tip(tip_length=0.20, tip_width=0.20)
        omega = self.MathTex(r"\omega", color=self.colors["yellow"], font_size=42)
        omega.move_to(spin_arrow.point_from_proportion(1.0) + UP * 0.30 + LEFT * 0.16)
        return VGroup(rotor, spin_arrow, omega)

    def draw_frequency_plot(self, high_inertia=True, show_tangent=False):
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[58.7, 60.2, 0.5],
            x_length=6.0,
            y_length=3.1,
            axis_config={"color": self.colors["muted"], "stroke_width": 2},
            tips=False,
        )
        x_label = self.Text("tempo", font_size=22, color=self.colors["text"]).next_to(axes.x_axis, DOWN, buff=0.22)
        y_label = self.Text("frequência", font_size=22, color=self.colors["text"]).rotate(90 * DEGREES)
        y_label.next_to(axes.y_axis, LEFT, buff=0.25)

        def high_curve(x):
            return 60 - 0.62 * (1 - np.exp(-0.45 * x)) - 0.035 * np.sin(1.7 * x) * np.exp(-0.25 * x)

        def low_curve(x):
            return 60 - 1.05 * (1 - np.exp(-0.92 * x)) - 0.06 * np.sin(2.0 * x) * np.exp(-0.18 * x)

        def high_slope(x):
            return (
                -0.62 * 0.45 * np.exp(-0.45 * x)
                - 0.035 * np.exp(-0.25 * x) * (1.7 * np.cos(1.7 * x) - 0.25 * np.sin(1.7 * x))
            )

        def low_slope(x):
            return (
                -1.05 * 0.92 * np.exp(-0.92 * x)
                - 0.06 * np.exp(-0.18 * x) * (2.0 * np.cos(2.0 * x) - 0.18 * np.sin(2.0 * x))
            )

        if high_inertia:
            curve = axes.plot(high_curve, x_range=[0, 6], color=self.colors["blue"], stroke_width=5)
            label = self.Text("alta inércia", font_size=22, color=self.colors["blue"]).next_to(curve, UP, buff=0.08)
        else:
            curve = axes.plot(low_curve, x_range=[0, 6], color=self.colors["red"], stroke_width=5)
            label = self.Text("baixa inércia", font_size=22, color=self.colors["red"]).next_to(curve, DOWN, buff=0.08)

        plot = VGroup(axes, x_label, y_label, curve, label)

        if show_tangent:
            x0 = 0.0
            curve_function = high_curve if high_inertia else low_curve
            slope_function = high_slope if high_inertia else low_slope
            y0 = curve_function(x0)
            slope = slope_function(x0)
            dx = 2.25 if high_inertia else 1.08
            tangent = Line(
                axes.c2p(x0, y0),
                axes.c2p(x0 + dx, y0 + slope * dx),
                color=self.colors["yellow"],
                stroke_width=5,
            )
            rocof = self.MathTex(r"RoCoF", color=self.colors["yellow"], font_size=30)
            if high_inertia:
                rocof.move_to(axes.c2p(3.15, 59.22))
            else:
                rocof.move_to(axes.c2p(1.65, 58.92))
            plot.add(tangent, rocof)

        return plot

    def draw_frequency_comparison_plot(self):
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[58.7, 60.2, 0.5],
            x_length=6.5,
            y_length=3.3,
            axis_config={"color": self.colors["muted"], "stroke_width": 2},
            tips=False,
        )
        x_label = self.Text("tempo", font_size=22, color=self.colors["text"]).next_to(axes.x_axis, DOWN, buff=0.22)
        y_label = self.Text("frequência", font_size=22, color=self.colors["text"]).rotate(90 * DEGREES)
        y_label.next_to(axes.y_axis, LEFT, buff=0.25)

        def high_curve(x):
            return 60 - 0.58 * (1 - np.exp(-0.40 * x))

        def low_curve(x):
            return 60 - 1.08 * (1 - np.exp(-0.98 * x))

        def high_slope(x):
            return -0.58 * 0.40 * np.exp(-0.40 * x)

        def low_slope(x):
            return -1.08 * 0.98 * np.exp(-0.98 * x)

        def initial_tangent_to(curve_function, slope_function, dx, color, stroke_width=5):
            # Draw the true initial tangent: same point and derivative as the curve at t = 0.
            x0 = 0.0
            y0 = curve_function(x0)
            slope = slope_function(x0)
            return Line(
                axes.c2p(x0, y0),
                axes.c2p(x0 + dx, y0 + slope * dx),
                color=color,
                stroke_width=stroke_width,
            )

        high = axes.plot(
            high_curve,
            x_range=[0, 6],
            color=self.colors["blue"],
            stroke_width=5,
        )
        low = axes.plot(
            low_curve,
            x_range=[0, 6],
            color=self.colors["red"],
            stroke_width=5,
        )
        high_label = self.Text("alta inércia", font_size=25, color=self.colors["blue"]).next_to(high, UP, buff=0.08)
        high_label.shift(DOWN * 0.40)
        low_label = self.Text("baixa inércia", font_size=25, color=self.colors["red"]).next_to(low, DOWN, buff=0.08)
        tangent_high = initial_tangent_to(high_curve, high_slope, dx=1.35, color=self.colors["cyan"], stroke_width=4)
        tangent_low = initial_tangent_to(low_curve, low_slope, dx=1.12, color=self.colors["yellow"], stroke_width=5)
        tangent_low.set_z_index(4)
        tangent_high.set_z_index(3)

        rocof = self.MathTex(r"RoCoF", color=self.colors["yellow"], font_size=30)
        rocof.move_to(axes.c2p(1.90, 59.52))
        rocof.set_z_index(5)
        return VGroup(
            axes, x_label, y_label, high, low, high_label, low_label,
            tangent_high, tangent_low, rocof,
        )

    def draw_angular_stability_curves(self):
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[-1.4, 1.4, 0.5],
            x_length=6.8,
            y_length=3.2,
            axis_config={"color": self.colors["muted"], "stroke_width": 2},
            tips=False,
        )
        x_label = self.Text("tempo", font_size=22, color=self.colors["text"]).next_to(axes, DOWN, buff=0.22)
        y_label = self.MathTex(r"\Delta\delta", color=self.colors["text"], font_size=32)
        y_label.next_to(axes.y_axis, LEFT, buff=0.22)

        well = axes.plot(lambda x: np.exp(-0.55 * x) * np.cos(2.6 * x), x_range=[0, 8],
                         color=self.colors["green"], stroke_width=4)
        weak = axes.plot(lambda x: np.exp(-0.12 * x) * np.cos(2.7 * x), x_range=[0, 8],
                         color=self.colors["yellow"], stroke_width=4)
        unstable = axes.plot(lambda x: np.clip(np.exp(0.10 * x) * np.cos(2.2 * x), -1.35, 1.35),
                             x_range=[0, 8], color=self.colors["red"], stroke_width=4)

        # Use a compact legend instead of placing labels directly on the curves.
        labels = VGroup(
            VGroup(Line(LEFT * 0.22, RIGHT * 0.22, color=self.colors["green"], stroke_width=4),
                   self.Text("bem amortecido", font_size=23, color=self.colors["green"])).arrange(RIGHT, buff=0.14),
            VGroup(Line(LEFT * 0.22, RIGHT * 0.22, color=self.colors["yellow"], stroke_width=4),
                   self.Text("pouco amortecido", font_size=23, color=self.colors["yellow"])).arrange(RIGHT, buff=0.14),
            VGroup(Line(LEFT * 0.22, RIGHT * 0.22, color=self.colors["red"], stroke_width=4),
                   self.Text("instável", font_size=23, color=self.colors["red"])).arrange(RIGHT, buff=0.14),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        labels.next_to(axes, RIGHT, buff=0.24)
        return VGroup(axes, x_label, y_label, well, weak, unstable, labels)

    def draw_nadir_rocof_plot(self):
        # Draw a frequency trajectory with the initial tangent and the nadir.
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[58.2, 60.2, 0.5],
            x_length=7.2,
            y_length=3.55,
            axis_config={"color": self.colors["muted"], "stroke_width": 2},
            tips=False,
        )
        x_label = self.Text("tempo", font_size=22, color=self.colors["text"]).next_to(axes.x_axis, DOWN, buff=0.20)
        y_label = self.Text("frequência", font_size=22, color=self.colors["text"]).rotate(90 * DEGREES)
        y_label.next_to(axes.y_axis, LEFT, buff=0.24)

        def f_curve(x):
            return 60 - 1.12 * (1 - np.exp(-0.62 * x)) + 0.55 * (1 - np.exp(-0.18 * x))

        def f_slope(x):
            return -1.12 * 0.62 * np.exp(-0.62 * x) + 0.55 * 0.18 * np.exp(-0.18 * x)

        curve = axes.plot(f_curve, x_range=[0, 10], color=self.colors["blue"], stroke_width=5)

        x0 = 0.0
        y0 = f_curve(x0)
        slope = f_slope(x0)
        tangent = Line(
            axes.c2p(x0, y0),
            axes.c2p(1.38, y0 + slope * 1.38),
            color=self.colors["yellow"],
            stroke_width=5,
        )
        rocof_label = self.MathTex(r"RoCoF", font_size=30, color=self.colors["yellow"])
        rocof_label.move_to(axes.c2p(1.95, 59.68))

        sample_x = np.linspace(0, 10, 600)
        sample_y = np.array([f_curve(x) for x in sample_x])
        nadir_index = int(np.argmin(sample_y))
        nadir_x = float(sample_x[nadir_index])
        nadir_y = float(sample_y[nadir_index])
        nadir_dot = Dot(axes.c2p(nadir_x, nadir_y), radius=0.07, color=self.colors["red"])
        nadir_line = DashedLine(
            axes.c2p(nadir_x, 58.2),
            axes.c2p(nadir_x, nadir_y),
            color=self.colors["red"],
            stroke_width=2,
        )
        nadir_label = self.MathTex(r"\text{Nadir}", font_size=30, color=self.colors["red"])
        nadir_label.next_to(nadir_dot, DOWN + RIGHT, buff=0.12)

        ufls_band = Rectangle(
            width=axes.x_axis.get_width(),
            height=axes.c2p(0, 59.5)[1] - axes.c2p(0, 58.5)[1],
            stroke_width=0,
            fill_color=self.colors["red"],
            fill_opacity=0.14,
        )
        ufls_band.move_to((axes.c2p(5, 59.5) + axes.c2p(5, 58.5)) / 2)
        ufls_label = self.MathTex(r"\text{UFLS }59{,}5\text{ a }58{,}5\ \mathrm{Hz}",
                             font_size=24, color=self.colors["red"])
        ufls_label.move_to(axes.c2p(7.0, 58.82))

        return VGroup(
            ufls_band, axes, x_label, y_label, curve, tangent, rocof_label,
            nadir_line, nadir_dot, nadir_label, ufls_label,
        )

    def draw_transient_instability_plot(self):
        # Show loss of synchronism as a monotonic rotor angle increase.
        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 5.5, 1],
            x_length=6.8,
            y_length=3.2,
            axis_config={"color": self.colors["muted"], "stroke_width": 2},
            tips=False,
        )
        x_label = self.Text("tempo", font_size=22, color=self.colors["text"]).next_to(axes.x_axis, DOWN, buff=0.22)
        y_label = self.MathTex(r"\delta", color=self.colors["text"], font_size=32)
        y_label.next_to(axes.y_axis, LEFT, buff=0.24)
        curve = axes.plot(
            lambda x: 0.40 + 0.18 * x + 0.09 * x ** 2,
            x_range=[0, 7],
            color=self.colors["red"],
            stroke_width=5,
        )
        label = self.Tex("perda de sincronismo", font_size=26, color=self.colors["red"])
        label.move_to(axes.c2p(3.35, 5.00) + RIGHT * 0.40 + DOWN * 0.40)
        return VGroup(axes, x_label, y_label, curve, label)

    def draw_delta_definition(self, angle_tracker=None):
        # Introduce the rotor angle before writing the linearized stability equations.
        origin = LEFT * 3.55 + DOWN * 0.05
        rotor_length = 2.25
        reference_length = 2.85

        def current_angle():
            if angle_tracker is None:
                return 0.72
            return angle_tracker.get_value()

        def make_rotor_axis():
            theta = current_angle()
            return Arrow(
                start=origin,
                end=origin + rotor_length * np.array([np.cos(theta), np.sin(theta), 0]),
                buff=0,
                color=self.colors["yellow"],
                stroke_width=6,
                max_tip_length_to_length_ratio=0.12,
            )

        def make_rotor_label():
            theta = current_angle()
            label = self.Tex("eixo do rotor", font_size=25, color=self.colors["yellow"])
            label.next_to(origin + rotor_length * np.array([np.cos(theta), np.sin(theta), 0]), UP + RIGHT, buff=0.12)
            return label

        def make_angle_arc():
            theta = current_angle()
            angle = Arc(radius=0.72, start_angle=0, angle=theta, color=self.colors["green"], stroke_width=5)
            angle.shift(origin)
            return angle

        def make_delta_label():
            theta = current_angle()
            label = self.MathTex(r"\delta", font_size=40, color=self.colors["green"])
            label.move_to(origin + 1.04 * np.array([np.cos(theta / 2), np.sin(theta / 2), 0]))
            return label

        reference = Line(origin, origin + RIGHT * reference_length, color=self.colors["muted"], stroke_width=3.5)
        reference_label = self.Tex("referencial síncrono", font_size=25, color=self.colors["muted"])
        reference_label.next_to(reference, DOWN, buff=0.16)

        if angle_tracker is None:
            rotor_axis = make_rotor_axis()
            rotor_label = make_rotor_label()
            angle = make_angle_arc()
            delta_label = make_delta_label()
        else:
            rotor_axis = always_redraw(make_rotor_axis)
            rotor_label = always_redraw(make_rotor_label)
            angle = always_redraw(make_angle_arc)
            delta_label = always_redraw(make_delta_label)

        diagram = VGroup(reference, reference_label, rotor_axis, rotor_label, angle, delta_label)

        definition = VGroup(
            self.MathTex(r"\Delta\delta", "=", r"\delta", "-", r"\delta_0", font_size=52),
            VGroup(
                self.Tex(r"$\delta$ é o ângulo elétrico do rotor", font_size=28, color=self.colors["text"]),
                self.Tex("em relação ao referencial síncrono.", font_size=28, color=self.colors["text"]),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.10),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        self.highlight_terms(definition[0], {r"\Delta\delta": self.colors["green"], r"\delta": self.colors["green"]})

        definition.move_to(RIGHT * 2.10 + UP * 0.18)

        kinematic_eq = self.MathTex(r"\frac{d\Delta\delta}{dt}", "=", r"\Delta\omega", font_size=44)
        self.highlight_terms(kinematic_eq, {
            r"\Delta\delta": self.colors["green"],
            r"\Delta\omega": self.colors["blue"],
        })
        kinematic_text = self.Tex(
            r"variação angular ligada à velocidade relativa do rotor",
            font_size=26,
            color=self.colors["text"],
        )
        kinematic = VGroup(kinematic_eq, kinematic_text).arrange(DOWN, buff=0.16)
        kinematic_box = RoundedRectangle(
            corner_radius=0.08,
            width=kinematic.width + 0.70,
            height=kinematic.height + 0.38,
            stroke_color=self.colors["green"],
            stroke_width=1.8,
            fill_color="#101A33",
            fill_opacity=0.45,
        )
        kinematic_box.move_to(kinematic)
        kinematic_panel = VGroup(kinematic_box, kinematic).move_to(DOWN * 2.35)

        group = VGroup(diagram, definition, kinematic_panel)
        return group

    # -------------------------------------------------------------------------
    # Scene blocks
    # -------------------------------------------------------------------------
