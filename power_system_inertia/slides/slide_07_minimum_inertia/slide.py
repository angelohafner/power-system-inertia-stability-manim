from manim import *
import numpy as np


def play(scene):
    # Bind language-aware text constructors for this slide.
    Text = scene.Text
    Tex = scene.Tex
    MathTex = scene.MathTex
    title = scene.make_title("Condição mínima de inércia")

    limit = MathTex(r"\left|\frac{df}{dt}\right|", r"\leq", r"RoCoF_{max}", font_size=52)
    scene.highlight_terms(limit, {r"RoCoF_{max}": scene.colors["yellow"]})
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
    scene.highlight_terms(substituted, {
        r"H_{sys}": scene.colors["blue"],
        r"\Delta P_{pu}": scene.colors["red"],
        r"RoCoF_{max}": scene.colors["yellow"],
    })
    substituted.move_to(UP * 1.05)

    minimum = MathTex(
        r"H_{sys}",
        r"\geq",
        r"\frac{f_0|\Delta P_{pu}|}{2RoCoF_{max}}",
        font_size=52,
    )
    scene.highlight_terms(minimum, {
        r"H_{sys}": scene.colors["blue"],
        r"\Delta P_{pu}": scene.colors["red"],
        r"RoCoF_{max}": scene.colors["yellow"],
    })
    minimum_box = scene.equation_box(minimum, color=scene.colors["green"], buff=0.28)
    minimum_box.move_to(UP * 0.42)

    explanation = scene.make_caption(
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
    scene.highlight_terms(equivalent, {r"H_{sys}": scene.colors["blue"]})
    equivalent_units = MathTex(
        r"H_i[\mathrm{s}],\quad S_i[\mathrm{MVA}],\quad S_{total}[\mathrm{MVA}]",
        font_size=22,
        color=scene.colors["muted"],
    )
    implication = VGroup(
        Tex(
            r"Substituir geradores síncronos por inversores fotovoltaicos/eólicos",
            font_size=21,
            color=scene.colors["text"],
        ),
        Tex(
            r"($H \approx 0$ com $S$ não-nulo) reduz $H_{sys}$ e aumenta RoCoF.",
            font_size=21,
            color=scene.colors["text"],
        ),
    ).arrange(DOWN, buff=0.04)
    implication.set_width(9.8)
    equivalent_block_content = VGroup(equivalent, equivalent_units, implication).arrange(DOWN, buff=0.10)
    equivalent_block = scene.equation_box(equivalent_block_content, color=scene.colors["blue"], buff=0.20)
    equivalent_block.move_to(DOWN * 0.95)

    axis = NumberLine(
        x_range=[0, 10, 1],
        length=8.6,
        include_numbers=False,
        tick_size=0.08,
        color=scene.colors["muted"],
    )
    axis.move_to(DOWN * 2.75)
    threshold_x = axis.n2p(4.7)
    rail = Line(axis.n2p(0.2), axis.n2p(9.8), color=scene.colors["muted"],
                stroke_width=16).set_opacity(0.28)
    left_bar = Line(axis.n2p(0.3), axis.n2p(4.55), color=scene.colors["red"], stroke_width=12)
    right_bar = Line(axis.n2p(4.85), axis.n2p(9.7), color=scene.colors["green"], stroke_width=12)
    threshold = DashedLine(threshold_x + UP * 0.55, threshold_x + DOWN * 0.47,
                           color=scene.colors["green"], stroke_width=3.5)
    marker = Triangle(color=scene.colors["green"], fill_color=scene.colors["green"], fill_opacity=1)
    marker.scale(0.13).rotate(PI).move_to(threshold_x + UP * 0.42)
    hmin = MathTex(r"H_{min}", font_size=32, color=scene.colors["green"]).next_to(marker, UP, buff=0.04)
    hmin.shift(UP * 0.08)
    h_axis = MathTex(r"H_{sys}", font_size=27, color=scene.colors["muted"]).next_to(axis, RIGHT, buff=0.18)
    critical = VGroup(
        MathTex(r"H_{sys}<H_{min}", font_size=24, color=scene.colors["red"]),
        Text("região crítica", font_size=24, color=scene.colors["red"]),
    ).arrange(DOWN, buff=0.05).move_to(axis.n2p(2.25) + DOWN * 0.58)
    safe = VGroup(
        MathTex(r"H_{sys}\geq H_{min}", font_size=24, color=scene.colors["green"]),
        Text("região segura", font_size=24, color=scene.colors["green"]),
    ).arrange(DOWN, buff=0.05).move_to(axis.n2p(7.25) + DOWN * 0.58)
    regions = VGroup(rail, axis, left_bar, right_bar, threshold, marker, hmin, h_axis, critical, safe)

    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
    scene.play(Write(limit), run_time=0.9)
    scene.play(ReplacementTransform(limit, substituted), run_time=1.0)
    scene.play(ReplacementTransform(substituted, minimum_box), run_time=1.2)
    scene.play(Circumscribe(minimum_box, color=scene.colors["green"]), run_time=0.9)
    scene.play(Write(explanation), run_time=0.9)
    scene.play(Create(rail), Create(axis), Create(left_bar), Create(right_bar), run_time=1.0)
    scene.play(Create(threshold), FadeIn(marker, shift=DOWN * 0.05), Write(hmin), Write(h_axis), run_time=0.8)
    scene.play(Write(critical), Write(safe), run_time=0.7)
    scene.wait(0.45)
    scene.play(FadeOut(VGroup(explanation, regions)), minimum_box.animate.move_to(UP * 1.70), run_time=0.8)
    scene.play(Write(equivalent_block), run_time=1.0)
    scene.wait(1.1)
    scene.clear_scene()


