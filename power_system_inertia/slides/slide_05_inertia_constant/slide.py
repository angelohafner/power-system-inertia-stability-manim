from manim import *
import numpy as np


def play(scene):
    # Bind language-aware text constructors for this slide.
    Text = scene.Text
    Tex = scene.Tex
    MathTex = scene.MathTex
    title_text = VGroup(
        Text("Frequência e constante de inércia", font_size=34, weight=BOLD, color=scene.colors["text"]),
        MathTex(r"H", font_size=43, color=scene.colors["text"]),
    ).arrange(RIGHT, buff=0.12)
    title_text.to_edge(UP, buff=0.35)
    underline = Line(LEFT, RIGHT, color=scene.colors["blue"]).set_width(11.5)
    underline.next_to(title_text, DOWN, buff=0.10)
    title = VGroup(VGroup(title_text), underline)

    hierarchy = scene.legend_block(
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
    scene.highlight_terms(relation_1, {"H": scene.colors["blue"], "J_m": scene.colors["blue"]})
    scene.highlight_terms(relation_2, {"J_m": scene.colors["blue"], "H": scene.colors["blue"]})
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
    scene.highlight_terms(pu_eq, {
        r"H_{sys}": scene.colors["blue"],
        r"\Delta P_{pu}": scene.colors["red"],
        r"D_{pu}": scene.colors["purple"],
    })
    pu_box = scene.equation_box(pu_eq, color=scene.colors["blue"], buff=0.18)
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
    scene.highlight_terms(conversion, {
        r"H_{sys}": scene.colors["blue"],
        r"\Delta P_{pu}": scene.colors["red"],
        r"D_{pu}": scene.colors["purple"],
    })
    conversion.move_to(DOWN * 0.38)

    explanation = VGroup(
        VGroup(
            Tex("Quanto maior a inércia equivalente", font_size=34, color=scene.colors["text"]),
            MathTex(r"H_{sys}", font_size=39, color=scene.colors["blue"]),
            Tex(",", font_size=34, color=scene.colors["text"]),
        ).arrange(RIGHT, buff=0.08),
        Tex("menor o módulo da taxa inicial de variação da frequência.", font_size=34, color=scene.colors["text"]),
    ).arrange(DOWN, buff=0.08)
    explanation.set_width(10.9)
    explanation.move_to(DOWN * 1.98)

    plot_low = scene.draw_frequency_plot(high_inertia=False, show_tangent=True).scale(0.70).move_to(LEFT * 3.2 + DOWN * 1.95)
    plot_high = scene.draw_frequency_plot(high_inertia=True, show_tangent=True).scale(0.70).move_to(RIGHT * 3.2 + DOWN * 1.95)
    plot_low.remove(plot_low[4])
    plot_high.remove(plot_high[4])
    h_low = MathTex(r"H_{sys}\ \text{baixo}", font_size=32, color=scene.colors["red"]).next_to(plot_low, UP, buff=0.08)
    h_low.shift(DOWN * 0.28)
    h_high = MathTex(r"H_{sys}\ \text{alto}", font_size=32, color=scene.colors["blue"]).next_to(plot_high, UP, buff=0.08)
    h_high.shift(DOWN * 0.28)
    plot_group = VGroup(explanation, plot_low, plot_high, h_low, h_high)

    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
    scene.play(FadeIn(hierarchy, shift=RIGHT * 0.15), Write(relations), run_time=1.2)
    scene.wait(0.35)
    scene.play(FadeOut(VGroup(hierarchy, relations)), run_time=0.55)
    scene.play(Write(pu_box), run_time=1.0)
    scene.play(Circumscribe(pu_box[1][0], color=scene.colors["blue"]), run_time=0.8)
    scene.play(Write(conversion), run_time=1.1)
    scene.play(Write(explanation), run_time=0.8)
    scene.wait(0.55)
    scene.play(FadeOut(VGroup(pu_box, conversion)), explanation.animate.move_to(UP * 1.25), run_time=0.8)
    scene.play(Create(plot_low), Write(h_low), run_time=1.2)
    scene.play(FadeIn(plot_high, shift=LEFT * 0.15), Write(h_high), run_time=1.3)
    scene.play(Indicate(plot_high[3], color=scene.colors["blue"]), Indicate(h_high, color=scene.colors["blue"]), run_time=1.0)
    scene.wait(1.0)
    scene.clear_scene()


