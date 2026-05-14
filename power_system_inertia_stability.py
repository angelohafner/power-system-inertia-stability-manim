from manim import *
import numpy as np


class CommaDecimalNumber(DecimalNumber):
    # Keep the animated gauge value in Portuguese decimal format.
    def _get_num_string(self, number):
        return super()._get_num_string(number).replace(".", ",")


class PowerSystemInertiaStability(Scene):
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

    def construct(self):
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

        self.scene_1_balance()
        self.scene_2_disturbance()
        self.scene_3_kinetic_energy()
        self.scene_4_swing_equation()
        self.scene_5_inertia_constant()
        self.scene_6_rocof()
        self.scene_7_minimum_inertia()
        self.scene_8_angular_stability()
        self.scene_9_synthetic_inertia_grid_forming()
        self.scene_10_hsys_reduction_example()
        self.scene_10_nadir_vs_rocof()
        self.scene_11_damping_appendix()
        self.scene_12_summary()

    # -------------------------------------------------------------------------
    # General helpers
    # -------------------------------------------------------------------------
    def make_title(self, text, subtitle=None):
        title = Text(text, font_size=34, weight=BOLD, color=self.colors["text"])
        title.to_edge(UP, buff=0.35)
        if subtitle:
            subtitle_mob = Text(subtitle, font_size=17, color=self.colors["muted"])
            subtitle_mob.next_to(title, DOWN, buff=0.06)
            subtitle_mob.set_width(min(subtitle_mob.width, 10.8))
            title_group = VGroup(title, subtitle_mob)
        else:
            title_group = VGroup(title)
        underline = Line(LEFT, RIGHT, color=self.colors["blue"]).set_width(11.5)
        underline.next_to(title_group, DOWN, buff=0.10)
        return VGroup(title_group, underline)

    def make_caption(self, text, width=10.8, font_size=25):
        caption = Text(text, font_size=font_size, color=self.colors["text"], line_spacing=0.85)
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
            *[MathTex(row, font_size=font_size, color=text_color) for row in rows]
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
        label = MathTex(label_tex, color=color, font_size=34)
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
            Text("Turbina", font_size=22, color=self.colors["text"]).shift(DOWN * 0.82),
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
            Text("Gerador", font_size=22, color=self.colors["text"]).shift(DOWN * 0.92),
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
            Text("Rede", font_size=22, color=self.colors["text"]).move_to(grid_center + DOWN * 0.98),
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
            Text("Carga", font_size=22, color=self.colors["text"]).shift(DOWN * 0.85),
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
            disturbance_label = Text(
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
        title = Text("frequência", font_size=19, color=self.colors["muted"])
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
        omega = MathTex(r"\omega", color=self.colors["yellow"], font_size=42)
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
        x_label = Text("tempo", font_size=22, color=self.colors["text"]).next_to(axes.x_axis, DOWN, buff=0.22)
        y_label = Text("frequência", font_size=22, color=self.colors["text"]).rotate(90 * DEGREES)
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
            label = Text("alta inércia", font_size=22, color=self.colors["blue"]).next_to(curve, UP, buff=0.08)
        else:
            curve = axes.plot(low_curve, x_range=[0, 6], color=self.colors["red"], stroke_width=5)
            label = Text("baixa inércia", font_size=22, color=self.colors["red"]).next_to(curve, DOWN, buff=0.08)

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
            rocof = MathTex(r"RoCoF", color=self.colors["yellow"], font_size=30)
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
        x_label = Text("tempo", font_size=22, color=self.colors["text"]).next_to(axes.x_axis, DOWN, buff=0.22)
        y_label = Text("frequência", font_size=22, color=self.colors["text"]).rotate(90 * DEGREES)
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
        high_label = Text("alta inércia", font_size=25, color=self.colors["blue"]).next_to(high, UP, buff=0.08)
        high_label.shift(DOWN * 0.40)
        low_label = Text("baixa inércia", font_size=25, color=self.colors["red"]).next_to(low, DOWN, buff=0.08)
        tangent_high = initial_tangent_to(high_curve, high_slope, dx=1.35, color=self.colors["cyan"], stroke_width=4)
        tangent_low = initial_tangent_to(low_curve, low_slope, dx=1.12, color=self.colors["yellow"], stroke_width=5)
        tangent_low.set_z_index(4)
        tangent_high.set_z_index(3)

        rocof = MathTex(r"RoCoF", color=self.colors["yellow"], font_size=30)
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
        x_label = Text("tempo", font_size=22, color=self.colors["text"]).next_to(axes, DOWN, buff=0.22)
        y_label = MathTex(r"\Delta\delta", color=self.colors["text"], font_size=32)
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
                   Text("bem amortecido", font_size=23, color=self.colors["green"])).arrange(RIGHT, buff=0.14),
            VGroup(Line(LEFT * 0.22, RIGHT * 0.22, color=self.colors["yellow"], stroke_width=4),
                   Text("pouco amortecido", font_size=23, color=self.colors["yellow"])).arrange(RIGHT, buff=0.14),
            VGroup(Line(LEFT * 0.22, RIGHT * 0.22, color=self.colors["red"], stroke_width=4),
                   Text("instável", font_size=23, color=self.colors["red"])).arrange(RIGHT, buff=0.14),
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
        x_label = Text("tempo", font_size=22, color=self.colors["text"]).next_to(axes.x_axis, DOWN, buff=0.20)
        y_label = Text("frequência", font_size=22, color=self.colors["text"]).rotate(90 * DEGREES)
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
        rocof_label = MathTex(r"RoCoF", font_size=30, color=self.colors["yellow"])
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
        nadir_label = MathTex(r"\text{Nadir}", font_size=30, color=self.colors["red"])
        nadir_label.next_to(nadir_dot, DOWN + RIGHT, buff=0.12)

        ufls_band = Rectangle(
            width=axes.x_axis.get_width(),
            height=axes.c2p(0, 59.5)[1] - axes.c2p(0, 58.5)[1],
            stroke_width=0,
            fill_color=self.colors["red"],
            fill_opacity=0.14,
        )
        ufls_band.move_to((axes.c2p(5, 59.5) + axes.c2p(5, 58.5)) / 2)
        ufls_label = MathTex(r"\text{UFLS }59{,}5\text{ a }58{,}5\ \mathrm{Hz}",
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
        x_label = Text("tempo", font_size=22, color=self.colors["text"]).next_to(axes.x_axis, DOWN, buff=0.22)
        y_label = MathTex(r"\delta", color=self.colors["text"], font_size=32)
        y_label.next_to(axes.y_axis, LEFT, buff=0.24)
        curve = axes.plot(
            lambda x: 0.40 + 0.18 * x + 0.09 * x ** 2,
            x_range=[0, 7],
            color=self.colors["red"],
            stroke_width=5,
        )
        label = Tex("perda de sincronismo", font_size=26, color=self.colors["red"])
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
            label = Tex("eixo do rotor", font_size=25, color=self.colors["yellow"])
            label.next_to(origin + rotor_length * np.array([np.cos(theta), np.sin(theta), 0]), UP + RIGHT, buff=0.12)
            return label

        def make_angle_arc():
            theta = current_angle()
            angle = Arc(radius=0.72, start_angle=0, angle=theta, color=self.colors["green"], stroke_width=5)
            angle.shift(origin)
            return angle

        def make_delta_label():
            theta = current_angle()
            label = MathTex(r"\delta", font_size=40, color=self.colors["green"])
            label.move_to(origin + 1.04 * np.array([np.cos(theta / 2), np.sin(theta / 2), 0]))
            return label

        reference = Line(origin, origin + RIGHT * reference_length, color=self.colors["muted"], stroke_width=3.5)
        reference_label = Tex("referencial síncrono", font_size=25, color=self.colors["muted"])
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
            MathTex(r"\Delta\delta", "=", r"\delta", "-", r"\delta_0", font_size=52),
            VGroup(
                Tex(r"$\delta$ é o ângulo elétrico do rotor", font_size=28, color=self.colors["text"]),
                Tex("em relação ao referencial síncrono.", font_size=28, color=self.colors["text"]),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.10),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        self.highlight_terms(definition[0], {r"\Delta\delta": self.colors["green"], r"\delta": self.colors["green"]})

        definition.move_to(RIGHT * 2.10 + UP * 0.18)

        kinematic_eq = MathTex(r"\frac{d\Delta\delta}{dt}", "=", r"\Delta\omega", font_size=44)
        self.highlight_terms(kinematic_eq, {
            r"\Delta\delta": self.colors["green"],
            r"\Delta\omega": self.colors["blue"],
        })
        kinematic_text = Tex(
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
    def scene_1_balance(self):
        title = self.make_title("Equilíbrio entre geração e carga")
        diagram = self.draw_power_system("60,0 Hz")
        diagram.scale(0.95).shift(UP * 0.15)
        turbine_rotor = diagram[0][1]
        flow_pulses = self.make_energy_pulses(
            [diagram[1], diagram[3], diagram[5]],
            color=self.colors["yellow"],
            speed=0.44,
            radius=0.040,
        )

        statement = self.make_caption(
            "Em regime permanente, a frequência permanece estável quando a\n"
            "potência gerada equilibra a potência consumida mais as perdas.",
            width=10.0,
            font_size=25,
        )
        statement.to_edge(DOWN, buff=0.34)

        balance = MathTex(
            r"P_{\text{geração}}", "=",
            r"P_{\text{carga}}", "+", r"P_{\text{perdas}}",
            font_size=44,
        )
        self.highlight_terms(balance, {
            r"P_{\text{geração}}": self.colors["cyan"],
            r"P_{\text{carga}}": self.colors["orange"],
            r"P_{\text{perdas}}": self.colors["red"],
        })
        balance.move_to(DOWN * 1.60)

        generator_balance = MathTex(r"P_m", "=", r"P_e", font_size=44)
        self.highlight_terms(generator_balance, {r"P_m": self.colors["cyan"], r"P_e": self.colors["orange"]})
        generator_note = Tex("(desprezando perdas internas do gerador)", font_size=21, color=self.colors["muted"])
        generator_group = VGroup(generator_balance, generator_note).arrange(DOWN, buff=0.08)
        generator_group.move_to(DOWN * 2.24 + LEFT * 2.05)

        freq = MathTex(r"f", r"\approx", r"f_0", font_size=48)
        freq.set_color_by_tex("f", self.colors["green"])
        freq.move_to(DOWN * 2.24 + RIGHT * 2.55)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(diagram[:7], shift=UP * 0.2), run_time=1.2)
        self.start_turbine(turbine_rotor, center_point=diagram[0][0].get_center())
        self.add(flow_pulses)
        self.play(FadeIn(diagram[7]), Write(diagram[8]), Write(diagram[9]), run_time=1.3)
        self.play(Write(statement), run_time=1.5)
        self.play(FadeOut(diagram[9][1]), run_time=0.35)
        self.play(Write(balance), run_time=0.9)
        self.play(Indicate(diagram[2][0], color=self.colors["blue"]), Indicate(balance, color=self.colors["green"]),
                  run_time=1.1)
        self.play(Write(generator_group), Write(freq), run_time=0.8)
        self.play(Circumscribe(diagram[7], color=self.colors["green"]), Circumscribe(freq, color=self.colors["green"]),
                  run_time=1.2)
        self.wait(1.1)
        self.stop_turbine(turbine_rotor)
        self.clear_energy_pulses(flow_pulses)
        self.clear_scene()

    def scene_2_disturbance(self):
        title = self.make_title("Desequilíbrio de potência")
        diagram = self.draw_power_system("60,0 Hz", disturbed=True, meter_disturbed=False)
        diagram.scale(0.84).shift(DOWN * 0.08)
        turbine_rotor = diagram[0][1]
        flow_pulses = self.make_energy_pulses(
            [diagram[1], diagram[3]],
            color=self.colors["yellow"],
            speed=0.42,
            radius=0.036,
        )
        load_pulses = self.make_energy_pulses(
            [diagram[5]],
            color=self.colors["red"],
            speed=0.95,
            radius=0.052,
            phases=(0.0, 0.25, 0.50, 0.75),
        )

        inequality = MathTex(r"P_m", r"<", r"P_e", font_size=56)
        self.highlight_terms(inequality, {r"P_m": self.colors["cyan"], r"P_e": self.colors["orange"]})
        inequality.move_to(LEFT * 3.0 + DOWN * 2.25)

        deficit = MathTex(r"\Delta P", "=", r"P_m", "-", r"P_e", "<", "0", font_size=50)
        self.highlight_terms(deficit, {
            r"\Delta P": self.colors["red"],
            r"P_m": self.colors["cyan"],
            r"P_e": self.colors["orange"],
        })
        deficit.move_to(RIGHT * 2.25 + DOWN * 2.25)

        statement = VGroup(
            Tex("Quando a carga supera a geração,", font_size=30, color=self.colors["text"]),
            Tex("o sistema precisa retirar energia", font_size=30, color=self.colors["text"]),
            Tex("de algum lugar nos primeiros instantes.", font_size=30, color=self.colors["text"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        statement.next_to(title, DOWN, buff=0.36)
        statement.shift(LEFT * 1.05)
        transient_note = Tex(
            "excursão transitória (resposta inercial) — não é regime permanente",
            font_size=21,
            color=self.colors["muted"],
        )
        transient_note.to_edge(DOWN, buff=0.18)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(diagram[:8], shift=UP * 0.15), run_time=1.0)
        omega_ref = self.start_turbine(turbine_rotor, center_point=diagram[0][0].get_center())
        self.add(flow_pulses)
        self.play(Write(diagram[8]), Write(diagram[9]), run_time=0.8)
        self.play_frequency_meter_drop(
            diagram[7],
            Create(diagram[10][0]),
            Write(diagram[10][1]),
            FadeIn(load_pulses),
            Flash(diagram[10][0].get_end(), color=self.colors["red"]),
            omega_ref=omega_ref,
        )
        self.play(FadeIn(transient_note, shift=UP * 0.05), run_time=0.5)
        self.play(Write(inequality), run_time=0.8)
        self.play(ReplacementTransform(inequality.copy(), deficit), run_time=1.1)
        self.play(Write(statement), Circumscribe(diagram[7], color=self.colors["red"]), run_time=1.4)
        self.wait(1.7)
        self.stop_turbine(turbine_rotor)
        self.clear_energy_pulses(flow_pulses)
        self.clear_energy_pulses(load_pulses)
        self.clear_scene()

    def scene_3_kinetic_energy(self):
        title = self.make_title("Energia cinética e inércia")
        rotor = self.draw_rotor().scale(1.25).move_to(LEFT * 3.55 + DOWN * 0.05)

        statement = self.make_caption("O rotor das máquinas síncronas armazena energia cinética.",
                                      width=6.1, font_size=28)
        statement.move_to(RIGHT * 2.65 + UP * 1.7)

        energy = MathTex(r"E_k", "=", r"\frac{1}{2}", "J_m", r"\omega_m^2", font_size=58)
        self.highlight_terms(energy, {r"E_k": self.colors["green"], "J_m": self.colors["blue"], r"\omega_m": self.colors["yellow"]})
        energy.move_to(RIGHT * 2.85 + UP * 0.88)

        term_labels = VGroup(
            MathTex(r"J_m:\ \text{momento de inércia mecânico }[\mathrm{kg\,m^2}]",
                    font_size=27, color=self.colors["blue"]),
            MathTex(r"\omega_m:\ \text{velocidade angular mecânica }[\mathrm{rad/s}]",
                    font_size=27, color=self.colors["yellow"]),
            MathTex(r"E_k:\ \text{energia cinética armazenada }[\mathrm{J}]",
                    font_size=27, color=self.colors["green"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        term_labels.move_to(RIGHT * 2.85 + DOWN * 0.88)

        power_support = Arrow(rotor.get_right() + RIGHT * 0.16 + DOWN * 1.15, LEFT * 0.35 + DOWN * 1.15,
                              color=self.colors["green"], stroke_width=6)
        support_label = Text("resposta inicial", font_size=23, color=self.colors["green"]).next_to(power_support, DOWN, buff=0.1)

        conclusion = self.make_caption(
            "A inércia não impede a queda de frequência, mas reduz a rapidez dessa queda.",
            width=10.6,
            font_size=27,
        )
        conclusion.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(rotor[0]), Create(rotor[1]), Write(rotor[2]), run_time=1.2)
        rotor[0].add_updater(lambda mob, dt: mob.rotate(1.30 * dt, about_point=mob.get_center()))
        self.play(Write(statement), run_time=0.9)
        self.play(Write(energy), run_time=1.1)
        self.play(Indicate(energy[3], color=self.colors["blue"]), Indicate(energy[4], color=self.colors["yellow"]),
                  run_time=1.0)
        self.play(FadeIn(term_labels, shift=UP * 0.2), run_time=1.2)
        self.play(Create(power_support), Write(support_label), run_time=0.8)
        self.play(Write(conclusion), Circumscribe(energy, color=self.colors["green"]), run_time=1.3)
        self.wait(1.8)
        rotor[0].clear_updaters()
        self.clear_scene()

    def scene_4_swing_equation(self):
        title = self.make_title("Equação de oscilação")

        torque_label = Tex("(a) Forma em torque, fisicamente exata:", font_size=22, color=self.colors["muted"])
        torque_eq = MathTex(
            r"J_m\frac{d\omega_m}{dt}",
            "=",
            r"T_m",
            "-",
            r"T_e",
            "-",
            r"D_m(\omega_m-\omega_{0,m})",
            font_size=32,
        )
        self.highlight_terms(torque_eq, {"J_m": self.colors["blue"], "T_m": self.colors["cyan"],
                                         "T_e": self.colors["orange"], "D_m": self.colors["purple"]})
        torque_panel = VGroup(torque_label, self.equation_box(torque_eq, color=self.colors["blue"], buff=0.12))
        torque_panel.arrange(DOWN, aligned_edge=LEFT, buff=0.16)

        power_label = Tex(r"(b) Forma em potência, válida para $\omega_m \approx \omega_{0,m}$:", font_size=22,
                          color=self.colors["muted"])
        power_eq = MathTex(
            r"J_m\omega_{0,m}\frac{d\omega_m}{dt}",
            "=",
            r"P_m",
            "-",
            r"P_e",
            "-",
            r"D_g(\omega_m-\omega_{0,m})",
            font_size=32,
        )
        self.highlight_terms(power_eq, {"J_m": self.colors["blue"], r"P_m": self.colors["cyan"],
                                        r"P_e": self.colors["orange"], "D_g": self.colors["purple"]})
        power_panel = VGroup(power_label, self.equation_box(power_eq, color=self.colors["orange"], buff=0.12))
        power_panel.arrange(DOWN, aligned_edge=LEFT, buff=0.16)

        pu_label = Tex("(c) Forma normalizada em pu:", font_size=22, color=self.colors["muted"])
        pu_eq = MathTex(
            r"2H\frac{d\Delta\omega_{pu}}{dt}",
            "=",
            r"\Delta P_{pu}",
            "-",
            r"D_{pu}\Delta\omega_{pu}",
            font_size=32,
        )
        self.highlight_terms(pu_eq, {"H": self.colors["blue"], r"\Delta P_{pu}": self.colors["red"],
                                     r"D_{pu}": self.colors["purple"]})
        pu_panel = VGroup(pu_label, self.equation_box(pu_eq, color=self.colors["green"], buff=0.12))
        pu_panel.arrange(DOWN, aligned_edge=LEFT, buff=0.16)

        equation_panels = VGroup(torque_panel, power_panel, pu_panel)
        equation_panels.arrange(DOWN, aligned_edge=LEFT, buff=0.36)
        equation_panels.move_to(LEFT * 3.08 + DOWN * 0.02)

        legend = self.legend_block(
            [
                r"T:\ \text{torque }[\mathrm{N\cdot m}]",
                r"P:\ \text{potência }[\mathrm{W}\ \text{ou } \mathrm{pu}]",
                r"D_m:\ \text{amortecimento mecânico }[\mathrm{N\cdot m\cdot s/rad}]",
                r"D_g:\ \text{amortecimento em potência }[\mathrm{W\cdot s/rad}]",
                r"D_{pu}:\ \text{amortecimento normalizado }[\mathrm{pu/pu}]",
                r"D_{pu}:\ \text{frequentemente tratado como adimensional na prática}",
            ],
            font_size=20,
            line_buff=0.12,
        )
        legend.move_to(RIGHT * 3.30 + DOWN * 0.25)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(torque_panel[0], shift=UP * 0.1), Write(torque_panel[1]), run_time=1.2)
        self.play(Circumscribe(torque_panel[1][1][0], color=self.colors["blue"]), run_time=0.7)
        self.play(FadeIn(power_panel[0], shift=UP * 0.1), Write(power_panel[1]), run_time=1.2)
        self.play(Circumscribe(power_panel[1][1][2:5], color=self.colors["red"]), run_time=0.7)
        self.play(FadeIn(pu_panel[0], shift=UP * 0.1), Write(pu_panel[1]), run_time=1.2)
        self.play(Circumscribe(pu_panel[1][1][0], color=self.colors["blue"]), run_time=0.7)
        self.play(FadeIn(legend, shift=UP * 0.1), run_time=0.8)
        self.wait(1.1)
        self.clear_scene()

    def scene_5_inertia_constant(self):
        title_text = VGroup(
            Text("Frequência e constante de inércia", font_size=34, weight=BOLD, color=self.colors["text"]),
            MathTex(r"H", font_size=43, color=self.colors["text"]),
        ).arrange(RIGHT, buff=0.12)
        title_text.to_edge(UP, buff=0.35)
        underline = Line(LEFT, RIGHT, color=self.colors["blue"]).set_width(11.5)
        underline.next_to(title_text, DOWN, buff=0.10)
        title = VGroup(VGroup(title_text), underline)

        hierarchy = self.legend_block(
            [
                r"J_m:\ \text{momento de inércia mecânico }[\mathrm{kg\,m^2}]",
                r"H:\ \text{constante de inércia em pu }[\mathrm{s}]",
                r"\quad \text{energia cinética nominal}/S_{base}",
                r"S_{base}:\ \text{potência aparente base }[\mathrm{VA\ ou\ MVA}]",
                r"\omega_{0,m},\omega_0:\ \text{velocidades nominais }[\mathrm{rad/s}]",
                r"M=\frac{2H}{\omega_0}:\ \text{constante de partida }[\mathrm{s^2}]",
                r"H_{sys}:\ \text{inércia equivalente do sistema }[\mathrm{s}]",
            ],
            font_size=26,
            line_buff=0.10,
        )
        hierarchy.move_to(LEFT * 3.35 + UP * 0.92)

        relation_1 = MathTex(
            r"H", "=", r"\frac{1}{2}\frac{J_m\omega_{0,m}^2}{S_{base}}",
            font_size=40,
        )
        relation_2 = MathTex(
            r"J_m", "=", r"\frac{2HS_{base}}{\omega_{0,m}^2}",
            font_size=40,
        )
        self.highlight_terms(relation_1, {"H": self.colors["blue"], "J_m": self.colors["blue"]})
        self.highlight_terms(relation_2, {"J_m": self.colors["blue"], "H": self.colors["blue"]})
        relations = VGroup(relation_1, relation_2).arrange(DOWN, buff=0.50)
        relations.move_to(RIGHT * 3.78 + UP * 0.96)

        pu_eq = MathTex(
            r"2H_{sys}\frac{d\Delta\omega_{pu}}{dt}",
            "=",
            r"\Delta P_{pu}",
            "-",
            r"D_{pu}\Delta\omega_{pu}",
            font_size=40,
        )
        self.highlight_terms(pu_eq, {
            r"H_{sys}": self.colors["blue"],
            r"\Delta P_{pu}": self.colors["red"],
            r"D_{pu}": self.colors["purple"],
        })
        pu_box = self.equation_box(pu_eq, color=self.colors["blue"], buff=0.18)
        pu_box.move_to(UP * 0.90)

        conversion = MathTex(
            r"\Delta\omega_{pu}=\frac{\Delta f}{f_0}",
            r"\qquad",
            r"\frac{d\Delta f}{dt}",
            "=",
            r"\frac{f_0}{2H_{sys}}\Delta P_{pu}",
            "-",
            r"\frac{D_{pu}}{2H_{sys}}\Delta f",
            font_size=34,
        )
        self.highlight_terms(conversion, {
            r"H_{sys}": self.colors["blue"],
            r"\Delta P_{pu}": self.colors["red"],
            r"D_{pu}": self.colors["purple"],
        })
        conversion.move_to(DOWN * 0.38)

        explanation = VGroup(
            VGroup(
                Tex("Quanto maior a inércia equivalente", font_size=34, color=self.colors["text"]),
                MathTex(r"H_{sys}", font_size=39, color=self.colors["blue"]),
                Tex(",", font_size=34, color=self.colors["text"]),
            ).arrange(RIGHT, buff=0.08),
            Tex("menor o módulo da taxa inicial de variação da frequência.", font_size=34, color=self.colors["text"]),
        ).arrange(DOWN, buff=0.08)
        explanation.set_width(10.9)
        explanation.move_to(DOWN * 1.98)

        plot_low = self.draw_frequency_plot(high_inertia=False, show_tangent=True).scale(0.70).move_to(LEFT * 3.2 + DOWN * 1.95)
        plot_high = self.draw_frequency_plot(high_inertia=True, show_tangent=True).scale(0.70).move_to(RIGHT * 3.2 + DOWN * 1.95)
        plot_low.remove(plot_low[4])
        plot_high.remove(plot_high[4])
        h_low = MathTex(r"H_{sys}\ \text{baixo}", font_size=32, color=self.colors["red"]).next_to(plot_low, UP, buff=0.08)
        h_low.shift(DOWN * 0.28)
        h_high = MathTex(r"H_{sys}\ \text{alto}", font_size=32, color=self.colors["blue"]).next_to(plot_high, UP, buff=0.08)
        h_high.shift(DOWN * 0.28)
        plot_group = VGroup(explanation, plot_low, plot_high, h_low, h_high)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(hierarchy, shift=RIGHT * 0.15), Write(relations), run_time=1.2)
        self.wait(0.35)
        self.play(FadeOut(VGroup(hierarchy, relations)), run_time=0.55)
        self.play(Write(pu_box), run_time=1.0)
        self.play(Circumscribe(pu_box[1][0], color=self.colors["blue"]), run_time=0.8)
        self.play(Write(conversion), run_time=1.1)
        self.play(Write(explanation), run_time=0.8)
        self.wait(0.55)
        self.play(FadeOut(VGroup(pu_box, conversion)), explanation.animate.move_to(UP * 1.25), run_time=0.8)
        self.play(Create(plot_low), Write(h_low), run_time=1.2)
        self.play(FadeIn(plot_high, shift=LEFT * 0.15), Write(h_high), run_time=1.3)
        self.play(Indicate(plot_high[3], color=self.colors["blue"]), Indicate(h_high, color=self.colors["blue"]), run_time=1.0)
        self.wait(1.0)
        self.clear_scene()

    def scene_6_rocof(self):
        title = self.make_title(
            "RoCoF",
            "(Rate of Change of Frequency - Taxa de Variação de Frequência)",
        )

        rocof = MathTex(r"RoCoF", "=", r"\frac{df}{dt}", font_size=52)
        self.highlight_terms(rocof, {"RoCoF": self.colors["yellow"]})
        rocof.move_to(UP * 2.22 + LEFT * 3.35)

        initial = MathTex(
            r"\left.\frac{d\Delta f}{dt}\right|_{t=0}",
            r"\approx",
            r"\frac{f_0}{2H_{sys}}",
            r"\Delta P_{pu}",
            font_size=38,
        )
        self.highlight_terms(initial, {r"H_{sys}": self.colors["blue"], r"\Delta P_{pu}": self.colors["red"]})
        initial.move_to(UP * 2.22 + RIGHT * 2.25)

        inverse = MathTex(r"RoCoF", r"\propto", r"\frac{1}{H_{sys}}", font_size=44)
        self.highlight_terms(inverse, {"RoCoF": self.colors["yellow"], r"H_{sys}": self.colors["blue"]})
        inverse_note = Tex("para a mesma perturbação", font_size=23, color=self.colors["muted"])
        inverse_group = VGroup(inverse_note, inverse).arrange(DOWN, buff=0.06)
        inverse_group.move_to(UP * 0.86)

        plot = self.draw_frequency_comparison_plot().scale(0.68).move_to(DOWN * 1.42)
        statement = Text("Baixa inércia causa maior RoCoF.", font_size=28, color=self.colors["yellow"])
        statement.to_edge(DOWN, buff=0.30)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.play(Write(rocof), run_time=0.8)
        self.play(Write(initial), run_time=1.1)
        self.play(TransformMatchingTex(initial.copy(), inverse), run_time=0.9)
        self.play(FadeIn(inverse_note, shift=DOWN * 0.05), run_time=0.45)
        self.play(Create(plot[:3]), run_time=0.8)
        self.play(Create(plot[3]), Write(plot[5]), run_time=0.8)
        self.play(Create(plot[4]), Write(plot[6]), run_time=0.8)
        self.play(Create(plot[7]), Create(plot[8]), Write(plot[9]), run_time=0.9)
        self.play(Write(statement), Circumscribe(VGroup(plot[7], plot[8]), color=self.colors["yellow"]), run_time=1.0)
        self.wait(1.0)
        self.clear_scene()

    def scene_7_minimum_inertia(self):
        title = self.make_title("Condição mínima de inércia")

        limit = MathTex(r"\left|\frac{df}{dt}\right|", r"\leq", r"RoCoF_{max}", font_size=52)
        self.highlight_terms(limit, {r"RoCoF_{max}": self.colors["yellow"]})
        limit.move_to(UP * 2.1)

        substituted = MathTex(
            r"\left|",
            r"\frac{f_0}{2H_{sys}}",
            r"\Delta P_{pu}",
            r"\right|",
            r"\leq",
            r"RoCoF_{max}",
            font_size=46,
        )
        self.highlight_terms(substituted, {
            r"H_{sys}": self.colors["blue"],
            r"\Delta P_{pu}": self.colors["red"],
            r"RoCoF_{max}": self.colors["yellow"],
        })
        substituted.move_to(UP * 1.05)

        minimum = MathTex(
            r"H_{sys}",
            r"\geq",
            r"\frac{f_0|\Delta P_{pu}|}{2RoCoF_{max}}",
            font_size=52,
        )
        self.highlight_terms(minimum, {
            r"H_{sys}": self.colors["blue"],
            r"\Delta P_{pu}": self.colors["red"],
            r"RoCoF_{max}": self.colors["yellow"],
        })
        minimum_box = self.equation_box(minimum, color=self.colors["green"], buff=0.28)
        minimum_box.move_to(UP * 0.42)

        explanation = self.make_caption(
            "Essa inequação representa a inércia mínima necessária\n"
            "para limitar a variação brusca da frequência.",
            width=10.8,
            font_size=23,
        )
        explanation.move_to(DOWN * 1.26)

        equivalent = MathTex(
            r"H_{sys}",
            "=",
            r"\frac{\sum_i H_iS_i}{S_{total}}",
            font_size=36,
        )
        self.highlight_terms(equivalent, {r"H_{sys}": self.colors["blue"]})
        equivalent_units = MathTex(
            r"H_i[\mathrm{s}],\quad S_i[\mathrm{MVA}],\quad S_{total}[\mathrm{MVA}]",
            font_size=22,
            color=self.colors["muted"],
        )
        implication = VGroup(
            Tex(
                r"Substituir geradores síncronos por inversores fotovoltaicos/eólicos",
                font_size=21,
                color=self.colors["text"],
            ),
            Tex(
                r"($H \approx 0$ com $S$ não-nulo) reduz $H_{sys}$ e aumenta RoCoF.",
                font_size=21,
                color=self.colors["text"],
            ),
        ).arrange(DOWN, buff=0.04)
        implication.set_width(9.8)
        equivalent_block_content = VGroup(equivalent, equivalent_units, implication).arrange(DOWN, buff=0.10)
        equivalent_block = self.equation_box(equivalent_block_content, color=self.colors["blue"], buff=0.20)
        equivalent_block.move_to(DOWN * 0.95)

        axis = NumberLine(
            x_range=[0, 10, 1],
            length=8.6,
            include_numbers=False,
            tick_size=0.08,
            color=self.colors["muted"],
        )
        axis.move_to(DOWN * 2.75)
        threshold_x = axis.n2p(4.7)
        rail = Line(axis.n2p(0.2), axis.n2p(9.8), color=self.colors["muted"],
                    stroke_width=16).set_opacity(0.28)
        left_bar = Line(axis.n2p(0.3), axis.n2p(4.55), color=self.colors["red"], stroke_width=12)
        right_bar = Line(axis.n2p(4.85), axis.n2p(9.7), color=self.colors["green"], stroke_width=12)
        threshold = DashedLine(threshold_x + UP * 0.55, threshold_x + DOWN * 0.47,
                               color=self.colors["green"], stroke_width=3.5)
        marker = Triangle(color=self.colors["green"], fill_color=self.colors["green"], fill_opacity=1)
        marker.scale(0.13).rotate(PI).move_to(threshold_x + UP * 0.42)
        hmin = MathTex(r"H_{min}", font_size=32, color=self.colors["green"]).next_to(marker, UP, buff=0.04)
        hmin.shift(UP * 0.08)
        h_axis = MathTex(r"H_{sys}", font_size=27, color=self.colors["muted"]).next_to(axis, RIGHT, buff=0.18)
        critical = VGroup(
            MathTex(r"H_{sys}<H_{min}", font_size=24, color=self.colors["red"]),
            Text("região crítica", font_size=24, color=self.colors["red"]),
        ).arrange(DOWN, buff=0.05).move_to(axis.n2p(2.25) + DOWN * 0.58)
        safe = VGroup(
            MathTex(r"H_{sys}\geq H_{min}", font_size=24, color=self.colors["green"]),
            Text("região segura", font_size=24, color=self.colors["green"]),
        ).arrange(DOWN, buff=0.05).move_to(axis.n2p(7.25) + DOWN * 0.58)
        regions = VGroup(rail, axis, left_bar, right_bar, threshold, marker, hmin, h_axis, critical, safe)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.play(Write(limit), run_time=0.9)
        self.play(ReplacementTransform(limit, substituted), run_time=1.0)
        self.play(ReplacementTransform(substituted, minimum_box), run_time=1.2)
        self.play(Circumscribe(minimum_box, color=self.colors["green"]), run_time=0.9)
        self.play(Write(explanation), run_time=0.9)
        self.play(Create(rail), Create(axis), Create(left_bar), Create(right_bar), run_time=1.0)
        self.play(Create(threshold), FadeIn(marker, shift=DOWN * 0.05), Write(hmin), Write(h_axis), run_time=0.8)
        self.play(Write(critical), Write(safe), run_time=0.7)
        self.wait(0.45)
        self.play(FadeOut(VGroup(explanation, regions)), minimum_box.animate.move_to(UP * 1.70), run_time=0.8)
        self.play(Write(equivalent_block), run_time=1.0)
        self.wait(1.1)
        self.clear_scene()

    def scene_8_angular_stability(self):
        title = self.make_title("Estabilidade angular")
        delta_angle = ValueTracker(0.48)
        delta_intro = self.draw_delta_definition(delta_angle)

        second_order = MathTex(
            r"M", r"\frac{d^2\Delta\delta}{dt^2}", "+",
            r"D", r"\frac{d\Delta\delta}{dt}", "+",
            r"K_s", r"\Delta\delta", "=", "0",
            r",\quad", r"M=\frac{2H}{\omega_0}",
            font_size=37,
        )
        self.highlight_terms(second_order, {"M": self.colors["blue"], "D": self.colors["purple"], r"K_s": self.colors["green"]})
        second_order.move_to(UP * 1.55)

        characteristic = MathTex(r"M", "s^2", "+", r"D", "s", "+", r"K_s", "=", "0", font_size=40)
        self.highlight_terms(characteristic, {"M": self.colors["blue"], "D": self.colors["purple"], r"K_s": self.colors["green"]})
        characteristic.move_to(UP * 0.82)

        ks_note = MathTex(
            r"K_s",
            "=",
            r"\left.\frac{\partial P_e}{\partial\delta}\right|_{\delta_0}",
            r"\approx",
            r"\frac{EV}{X}\cos(\delta_0)",
            font_size=32,
        )
        self.highlight_terms(ks_note, {r"K_s": self.colors["green"]})
        equation_stack = VGroup(second_order, characteristic, ks_note)
        equation_stack.arrange(DOWN, buff=0.30)
        equation_stack.move_to(UP * 1.42)

        term_labels = self.legend_block(
            [
                r"M:\ \text{constante de partida }[\mathrm{s^2}]",
                r"D:\ \text{amortecimento }[\mathrm{pu\cdot s/rad}]",
                r"K_s:\ \text{sincronismo elétrico }[\mathrm{pu/rad}]",
                r"\delta:\ \text{ângulo elétrico }[\mathrm{rad}]",
            ],
            font_size=19,
            line_buff=0.07,
        )
        term_labels.move_to(RIGHT * 4.23 + UP * 0.08)

        curves = self.draw_angular_stability_curves().scale(0.56).move_to(DOWN * 2.10 + LEFT * 3.55)

        first_statement = Tex(
            "A inércia reduz a rapidez da variação da frequência.",
            font_size=21,
            color=self.colors["text"],
        )
        second_statement = VGroup(
            Tex("A estabilidade também depende do amortecimento",
                font_size=21, color=self.colors["text"]),
            Tex("e do sincronismo elétrico.",
                font_size=21, color=self.colors["text"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        statement = VGroup(first_statement, second_statement).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        statement.move_to(RIGHT * 3.42 + DOWN * 1.86)

        loading_note = VGroup(
            Tex(r"Conforme o sistema é mais carregado ($\delta_0$ cresce),",
                font_size=24, color=self.colors["text"]),
            Tex(r"$K_s$ diminui e a margem de estabilidade encolhe.",
                font_size=24, color=self.colors["text"]),
        ).arrange(DOWN, buff=0.08)
        loading_note.move_to(LEFT * 3.10 + DOWN * 0.70)

        transient_plot = self.draw_transient_instability_plot().scale(0.76).move_to(LEFT * 2.65 + DOWN * 0.35)
        transient_text = VGroup(
            Tex("Instabilidade transitória:", font_size=30, color=self.colors["red"]),
            Tex("perda de sincronismo", font_size=30, color=self.colors["red"]),
            Tex(r"Após uma falta severa, $\delta$ pode crescer", font_size=25, color=self.colors["text"]),
            Tex("monotonicamente, sem oscilar em torno do equilíbrio.", font_size=25, color=self.colors["text"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        transient_text.move_to(RIGHT * 2.95 + DOWN * 0.20)
        transient_method_note = VGroup(
            Tex("Para análise transitória usa-se o método das áreas iguais", font_size=20,
                color=self.colors["muted"]),
            Tex("(Equal Area Criterion) ou simulação no domínio do tempo,", font_size=20,
                color=self.colors["muted"]),
            Tex("não o autovalor da equação linearizada.", font_size=20, color=self.colors["muted"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        transient_method_note.move_to(RIGHT * 2.95 + DOWN * 2.25)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.play(
            FadeIn(delta_intro[0], shift=RIGHT * 0.2),
            Write(delta_intro[1]),
            FadeIn(delta_intro[2], shift=UP * 0.15),
            run_time=1.2,
        )
        self.play(delta_angle.animate.set_value(0.98), run_time=0.9, rate_func=smooth)
        self.play(delta_angle.animate.set_value(0.64), run_time=0.8, rate_func=smooth)
        self.play(
            Circumscribe(delta_intro[1][0], color=self.colors["green"]),
            Indicate(delta_intro[2][1][0], color=self.colors["green"]),
            run_time=0.8,
        )
        self.wait(0.5)
        self.play(FadeOut(delta_intro), run_time=0.6)
        self.play(Write(second_order), run_time=1.2)
        self.play(Write(characteristic), run_time=0.9)
        self.play(Write(ks_note), FadeIn(term_labels, shift=UP * 0.2), run_time=1.0)
        self.play(Write(loading_note), run_time=0.8)
        self.play(Create(curves[:3]), run_time=0.7)
        self.play(Create(curves[3]), Create(curves[4]), Create(curves[5]), FadeIn(curves[6]), run_time=1.4)
        self.play(Write(statement), run_time=1.1)
        self.wait(0.8)
        self.play(
            FadeOut(VGroup(second_order, characteristic, ks_note, term_labels, curves, statement,
                           loading_note)),
            run_time=0.8,
        )
        self.play(Create(transient_plot[:3]), run_time=0.7)
        self.play(Create(transient_plot[3]), Write(transient_plot[4]), Write(transient_text), run_time=1.2)
        self.bring_to_front(transient_plot[4])
        self.play(Write(transient_method_note), run_time=0.9)
        self.wait(1.8)
        self.clear_scene()

    def scene_9_synthetic_inertia_grid_forming(self):
        title = self.make_title("Inércia sintética e Grid-Forming")

        intro = Tex(
            "Sistemas modernos têm penetração crescente de inversores.",
            font_size=27,
            color=self.colors["text"],
        )
        intro.move_to(UP * 2.18)

        gfl = VGroup(
            Tex("Grid-Following (GFL)", font_size=28, color=self.colors["orange"]),
            Tex("segue a frequência da rede", font_size=22, color=self.colors["text"]),
            Tex("NÃO entrega inércia naturalmente", font_size=22, color=self.colors["red"]),
        ).arrange(DOWN, buff=0.14)
        gfl_box = self.equation_box(gfl, color=self.colors["orange"], buff=0.26)
        gfl_box.move_to(LEFT * 3.05 + UP * 0.98)

        gfm = VGroup(
            Tex("Grid-Forming (GFM)", font_size=28, color=self.colors["blue"]),
            Tex("impõe tensão/frequência", font_size=22, color=self.colors["text"]),
            Tex("pode emular inércia por controle", font_size=22, color=self.colors["green"]),
        ).arrange(DOWN, buff=0.14)
        gfm_box = self.equation_box(gfm, color=self.colors["blue"], buff=0.26)
        gfm_box.move_to(RIGHT * 3.05 + UP * 0.98)

        gfl_note = VGroup(
            Tex("GFL pode fazer Fast Frequency Response (FFR), mas depende", font_size=18,
                color=self.colors["text"]),
            Tex("de PLL e tem delay.", font_size=18, color=self.colors["text"]),
        ).arrange(DOWN, buff=0.04)
        gfm_note = VGroup(
            Tex("GFM emula comportamento inercial de forma mais natural,", font_size=18,
                color=self.colors["text"]),
            Tex(r"sem depender de PLL para seguir uma rede forte.", font_size=18,
                color=self.colors["text"]),
        ).arrange(DOWN, buff=0.04)
        gfl_gfm_note = VGroup(gfl_note, gfm_note).arrange(DOWN, buff=0.16)
        gfl_gfm_note.set_width(9.2)
        gfl_gfm_note.move_to(DOWN * 0.88)

        convention = VGroup(
            Tex("Convenção:", font_size=21, color=self.colors["muted"]),
            MathTex(
                r"\Delta P_{inv,pu}",
                "=",
                r"-2H_v\frac{d\Delta\omega_{pu}}{dt}",
                font_size=31,
            ),
        ).arrange(DOWN, buff=0.10)
        self.highlight_terms(convention[1], {r"H_v": self.colors["blue"]})
        convention_box = self.equation_box(convention, color=self.colors["green"], buff=0.18)

        hz_form = VGroup(
            Tex(r"Em Hz (com $\Delta\omega_{pu}=\Delta f/f_0$):", font_size=21,
                color=self.colors["muted"]),
            MathTex(
                r"\Delta P_{inv,pu}",
                "=",
                r"-\frac{2H_v}{f_0}\frac{d\Delta f}{dt}",
                font_size=31,
            ),
        ).arrange(DOWN, buff=0.10)
        self.highlight_terms(hz_form[1], {r"H_v": self.colors["blue"]})
        hz_box = self.equation_box(hz_form, color=self.colors["green"], buff=0.18)

        control_boxes = VGroup(convention_box, hz_box).arrange(RIGHT, buff=0.42)
        control_boxes.move_to(UP * 1.45)

        sign_note = Tex(
            r"\textit{O sinal negativo significa que o inversor injeta potência quando a frequência está caindo, opondo-se à variação.}",
            font_size=17,
            color=self.colors["muted"],
        )
        sign_note.set_width(10.2)
        sign_note.move_to(DOWN * 0.04)

        comparison = VGroup(
            VGroup(
                Tex("síncrona:", font_size=21, color=self.colors["cyan"]),
                Tex("inércia física, instantânea, sem controle", font_size=19, color=self.colors["text"]),
            ).arrange(RIGHT, buff=0.18),
            VGroup(
                Tex("inversor:", font_size=21, color=self.colors["yellow"]),
                Tex(r"``inércia'' via software, com delay, saturação e energia DC disponível", font_size=19,
                    color=self.colors["text"]),
            ).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        comparison.set_width(10.6)
        comparison.move_to(DOWN * 1.30)

        ffr = Tex(
            "Fast Frequency Response (FFR) das baterias atua nos primeiros segundos, "
            "complementando (não substituindo) a inércia.",
            font_size=21,
            color=self.colors["text"],
        )
        ffr.set_width(10.6)
        ffr.move_to(DOWN * 2.55)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.play(Write(intro), run_time=0.8)
        self.play(FadeIn(gfl_box, shift=RIGHT * 0.15), FadeIn(gfm_box, shift=LEFT * 0.15), run_time=1.1)
        self.play(Write(gfl_gfm_note), run_time=0.9)
        self.wait(0.9)
        self.play(FadeOut(VGroup(intro, gfl_box, gfm_box, gfl_gfm_note)), run_time=0.7)
        self.play(Write(control_boxes), run_time=1.0)
        self.play(Write(sign_note), run_time=0.8)
        self.play(Write(comparison), run_time=1.0)
        self.play(Write(ffr), Circumscribe(control_boxes, color=self.colors["green"]), run_time=1.1)
        self.wait(1.4)
        self.clear_scene()

    def scene_10_hsys_reduction_example(self):
        title_text = Tex(r"\textbf{Exemplo: redução de }$H_{sys}$", font_size=43, color=self.colors["text"])
        title_text.to_edge(UP, buff=0.35)
        underline = Line(LEFT, RIGHT, color=self.colors["blue"]).set_width(11.5)
        underline.next_to(title_text, DOWN, buff=0.10)
        title = VGroup(VGroup(title_text), underline)

        formula = MathTex(
            r"H_{sys}",
            "=",
            r"\frac{\sum_i H_iS_i}{S_{total}}",
            font_size=44,
        )
        self.highlight_terms(formula, {r"H_{sys}": self.colors["blue"]})
        formula.move_to(UP * 2.28)

        def scenario_card(title_text, rows, result_tex, color):
            header = Tex(title_text, font_size=25, color=color)
            body = VGroup(*[
                MathTex(row, font_size=24, color=self.colors["text"]) for row in rows
            ]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            result = MathTex(result_tex, font_size=29, color=color)
            content = VGroup(header, body, result).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
            box = RoundedRectangle(
                corner_radius=0.08,
                width=5.45,
                height=3.55,
                stroke_color=color,
                stroke_width=2,
                fill_color="#101A33",
                fill_opacity=0.68,
            )
            box.move_to(content)
            return VGroup(box, content)

        scenario_a = scenario_card(
            r"Cenario A (síncrono 100\%)",
            [
                r"\text{Térmica 1: }H=5\,\mathrm{s},\ S=500\,\mathrm{MVA}",
                r"\text{Térmica 2: }H=6\,\mathrm{s},\ S=400\,\mathrm{MVA}",
                r"\text{Hidrelétrica: }H=4\,\mathrm{s},\ S=600\,\mathrm{MVA}",
            ],
            r"H_{sys}\approx4{,}87\,\mathrm{s}",
            self.colors["cyan"],
        )
        scenario_a.move_to(LEFT * 3.05 + DOWN * 0.20)

        scenario_b = scenario_card(
            r"Cenario B (50\% IBR)",
            [
                r"\text{Térmica 1: }H=5\,\mathrm{s},\ S=500\,\mathrm{MVA}",
                r"\text{Solar/Eólica (IBR): }H=0,\ S=1000\,\mathrm{MVA}",
            ],
            r"H_{sys}\approx1{,}67\,\mathrm{s}",
            self.colors["orange"],
        )
        scenario_b.move_to(RIGHT * 3.05 + DOWN * 0.20)

        conclusion = VGroup(
            Tex(r"Mesma capacidade instalada, $H_{sys}$ cai $\sim 3\times$.", font_size=28,
                color=self.colors["text"]),
            Tex(r"RoCoF para o mesmo $\Delta P$ triplica.", font_size=28,
                color=self.colors["text"]),
        ).arrange(DOWN, buff=0.08)
        conclusion.set_width(9.45)
        conclusion_box = self.equation_box(conclusion, color=self.colors["yellow"], buff=0.26)
        conclusion_box.move_to(DOWN * 3.05)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.play(Write(formula), run_time=0.8)
        self.play(FadeIn(scenario_a, shift=RIGHT * 0.15), FadeIn(scenario_b, shift=LEFT * 0.15), run_time=1.1)
        self.play(Write(conclusion_box), run_time=1.0)
        self.play(Circumscribe(conclusion_box, color=self.colors["yellow"]), run_time=0.8)
        self.wait(1.6)
        self.clear_scene()

    def scene_10_nadir_vs_rocof(self):
        title = self.make_title("Nadir de frequência vs RoCoF")

        plot = self.draw_nadir_rocof_plot().scale(0.72).move_to(LEFT * 2.95 + DOWN * 0.25)
        reserve_dependency = VGroup(
            Tex(r"Depende de reserva primária, droop $R$ e tempo", font_size=21,
                color=self.colors["text"]),
            Tex("da governação e amortecimento da carga.", font_size=21,
                color=self.colors["text"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        bullets = VGroup(
            Tex(r"$\mathrm{RoCoF}$: declividade inicial ($df/dt$ em $t=0^+$).", font_size=21,
                color=self.colors["text"]),
            Tex(r"Depende de $H_{sys}$ e $\Delta P$.", font_size=21, color=self.colors["text"]),
            Tex("Nadir: frequência mínima atingida durante o transitório.", font_size=21,
                color=self.colors["text"]),
            reserve_dependency,
            Tex(r"$\mathrm{UFLS}$ em sistemas 60 Hz: tipicamente 59,5 a 58,5 Hz.", font_size=21,
                color=self.colors["muted"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        bullets.set_width(5.72)
        bullets.move_to(RIGHT * 3.22 + UP * 1.68)

        steady_eq = MathTex(
            r"\Delta f_{ss}",
            "=",
            r"\frac{\Delta P}{1/R+D_f}",
            font_size=28,
        )
        steady_units = MathTex(
            r"R[\mathrm{Hz/pu}],\quad D_f=\frac{\partial P_{carga}}{\partial f}[\mathrm{pu/Hz}]",
            font_size=19,
            color=self.colors["muted"],
        )
        nadir_eq = MathTex(
            r"|\Delta f_{nadir}|",
            ">",
            r"|\Delta f_{ss}|",
            font_size=26,
        )
        nadir_dependence = Tex(
            r"dependendo de $H_{sys}$, $\Delta P$, $R$, $D_f$ e tempo de resposta do governador $T_g$.",
            font_size=18,
            color=self.colors["text"],
        )
        nadir_dependence.set_width(5.2)
        canonical_block_content = VGroup(steady_eq, steady_units, nadir_eq, nadir_dependence).arrange(DOWN, buff=0.12)
        canonical_block = self.equation_box(canonical_block_content, color=self.colors["blue"], buff=0.18)
        canonical_block.move_to(RIGHT * 3.22 + DOWN * 1.35)

        final_note = VGroup(
            Tex(r"RoCoF depende de $H_{sys}$ e $\Delta P$.", font_size=18, color=self.colors["yellow"]),
            Tex(r"Nadir depende de $H_{sys}$, $\Delta P$, reserva, droop, $D_f$ e dinâmica do governador.",
                font_size=17, color=self.colors["yellow"]),
        ).arrange(DOWN, buff=0.04)
        final_note.set_width(5.55)
        final_note.move_to(RIGHT * 3.22 + DOWN * 3.18)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.play(Create(plot[:4]), run_time=0.8)
        self.play(Create(plot[4]), run_time=0.8)
        self.play(Create(plot[5]), Write(plot[6]), run_time=0.8)
        self.bring_to_front(plot[6])
        self.play(FadeIn(plot[7]), FadeIn(plot[8]), Write(plot[9]), FadeIn(plot[0]), Write(plot[10]), run_time=1.0)
        self.bring_to_front(plot[6])
        self.play(Write(bullets), run_time=1.3)
        self.play(Write(canonical_block), run_time=1.1)
        self.play(Write(final_note), run_time=0.8)
        self.wait(1.8)
        self.clear_scene()

    def scene_11_damping_appendix(self):
        title_text = VGroup(
            Tex(r"\textbf{Damping}", font_size=42, color=self.colors["text"]),
            MathTex(r"D", font_size=48, color=self.colors["text"]),
        ).arrange(RIGHT, buff=0.10)
        title_text.to_edge(UP, buff=0.35)
        underline = Line(LEFT, RIGHT, color=self.colors["blue"]).set_width(11.5)
        underline.next_to(title_text, DOWN, buff=0.10)
        title = VGroup(VGroup(title_text), underline)

        gen_block = VGroup(
            Tex("No gerador:", font_size=25, color=self.colors["cyan"]),
            MathTex(
                r"D_{gen}",
                "=",
                r"D_{mec}",
                "+",
                r"D_{amort}",
                r"\quad[\mathrm{pu\cdot s/rad}]",
                font_size=31,
            ),
            Tex("atrito mecânico + enrolamentos amortecedores", font_size=20, color=self.colors["text"]),
        ).arrange(DOWN, buff=0.16)
        self.highlight_terms(gen_block[1], {r"D_{gen}": self.colors["purple"]})
        gen_box = self.equation_box(gen_block, color=self.colors["cyan"], buff=0.22)
        gen_box.move_to(LEFT * 3.10 + UP * 1.20)

        load_block = VGroup(
            Tex("Na rede:", font_size=25, color=self.colors["green"]),
            MathTex(
                r"D_{load}",
                "=",
                r"\frac{\partial P_{carga}}{\partial f}",
                r"\quad[\mathrm{pu/Hz}]",
                font_size=31,
            ),
            Tex(r"auto-regulação da carga, tipicamente 1 a 2 \%/Hz", font_size=20,
                color=self.colors["text"]),
        ).arrange(DOWN, buff=0.16)
        self.highlight_terms(load_block[1], {r"D_{load}": self.colors["green"]})
        load_box = self.equation_box(load_block, color=self.colors["green"], buff=0.22)
        load_box.move_to(RIGHT * 3.10 + UP * 1.20)

        system_block = VGroup(
            Tex("No sistema (após conversão de unidades):", font_size=25, color=self.colors["muted"]),
            MathTex(
                r"D_{sys}",
                "=",
                r"D_{gen}",
                "+",
                r"\frac{f_0D_{load}}{\omega_0}",
                r"\approx",
                r"D_{gen}",
                "+",
                r"\frac{D_{load}}{2\pi}",
                font_size=34,
            ),
        ).arrange(DOWN, buff=0.18)
        self.highlight_terms(system_block[1], {
            r"D_{sys}": self.colors["purple"],
            r"D_{gen}": self.colors["cyan"],
            r"D_{load}": self.colors["green"],
        })
        system_box = self.equation_box(system_block, color=self.colors["purple"], buff=0.24)
        system_box.move_to(DOWN * 0.75)

        load_note = self.legend_block(
            [
                r"\frac{\partial P_{carga}}{\partial f}>0\ \Rightarrow\ \text{carga ajuda a amortecer a queda de frequência}",
            ],
            font_size=24,
        )
        load_note.move_to(DOWN * 2.85)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(gen_box, shift=RIGHT * 0.15), FadeIn(load_box, shift=LEFT * 0.15), run_time=1.1)
        self.play(Write(system_box), run_time=1.0)
        self.play(FadeIn(load_note, shift=UP * 0.1), Circumscribe(load_box, color=self.colors["green"]),
                  run_time=1.0)
        self.wait(1.7)
        self.clear_scene()

    def scene_12_summary(self):
        title = self.make_title("Resumo")

        summary_1 = MathTex(
            r"\text{Sistema estável}", r"\Rightarrow",
            r"\text{inércia suficiente}", "+",
            r"\text{amortecimento suficiente}", "+",
            r"\text{controle adequado}",
            font_size=38,
        )
        summary_1.set_color_by_tex(r"\text{Sistema estável}", self.colors["green"])
        summary_1.set_color_by_tex(r"\text{inércia suficiente}", self.colors["blue"])
        summary_1.set_width(10.9)

        summary_2 = MathTex(
            r"\text{Baixa inércia}", r"\Rightarrow",
            r"\text{maior RoCoF}", r"\Rightarrow",
            r"\text{menor tempo para atuação dos controles}",
            font_size=39,
        )
        summary_2.set_color_by_tex(r"\text{Baixa inércia}", self.colors["red"])
        summary_2.set_color_by_tex(r"\text{maior RoCoF}", self.colors["yellow"])
        summary_2.set_width(10.7)

        summary_3 = Tex(
            r"Inércia $\neq$ resposta primária. Inércia limita o RoCoF; "
            r"é a reserva primária (governadores e baterias com FFR) que define o nadir.",
            font_size=27,
            color=self.colors["text"],
        )
        summary_3.set_width(10.8)

        summaries = VGroup(summary_1, summary_2, summary_3).arrange(DOWN, buff=0.62)
        summaries.move_to(DOWN * 0.20)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.play(Write(summary_1), run_time=1.1)
        self.play(Write(summary_2), run_time=1.0)
        self.play(Write(summary_3), run_time=1.0)
        self.play(Circumscribe(summary_1, color=self.colors["green"]), Circumscribe(summary_2, color=self.colors["yellow"]),
                  Circumscribe(summary_3, color=self.colors["blue"]), run_time=1.1)
        self.wait(2.6)
        self.clear_scene()
