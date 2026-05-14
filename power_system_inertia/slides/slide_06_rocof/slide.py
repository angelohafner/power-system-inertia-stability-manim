from manim import *
import numpy as np


def play(scene):
    # Bind language-aware text constructors for this slide.
    Text = scene.Text
    Tex = scene.Tex
    MathTex = scene.MathTex
    title = scene.make_title(
        "RoCoF",
        "(Rate of Change of Frequency - Taxa de Variação de Frequência)",
    )

    rocof = MathTex(r"RoCoF", "=", r"\frac{df}{dt}", font_size=52)
    scene.highlight_terms(rocof, {"RoCoF": scene.colors["yellow"]})
    rocof.move_to(UP * 2.22 + LEFT * 3.35)

    initial = MathTex(
        r"\left.\frac{d\Delta f}{dt}\right|_{t=0}",
        r"\approx",
        r"\frac{f_0}{2H_{sys}}",
        r"\Delta P_{pu}",
        font_size=38,
    )
    scene.highlight_terms(initial, {r"H_{sys}": scene.colors["blue"], r"\Delta P_{pu}": scene.colors["red"]})
    initial.move_to(UP * 2.22 + RIGHT * 2.25)

    inverse = MathTex(r"RoCoF", r"\propto", r"\frac{1}{H_{sys}}", font_size=44)
    scene.highlight_terms(inverse, {"RoCoF": scene.colors["yellow"], r"H_{sys}": scene.colors["blue"]})
    inverse_note = Tex("para a mesma perturbação", font_size=23, color=scene.colors["muted"])
    inverse_group = VGroup(inverse_note, inverse).arrange(DOWN, buff=0.06)
    inverse_group.move_to(UP * 0.86)

    plot = scene.draw_frequency_comparison_plot().scale(0.68).move_to(DOWN * 1.42)
    statement = Text("Baixa inércia causa maior RoCoF.", font_size=28, color=scene.colors["yellow"])
    statement.to_edge(DOWN, buff=0.30)

    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
    scene.play(Write(rocof), run_time=0.8)
    scene.play(Write(initial), run_time=1.1)
    scene.play(TransformMatchingTex(initial.copy(), inverse), run_time=0.9)
    scene.play(FadeIn(inverse_note, shift=DOWN * 0.05), run_time=0.45)
    scene.play(Create(plot[:3]), run_time=0.8)
    scene.play(Create(plot[3]), Write(plot[5]), run_time=0.8)
    scene.play(Create(plot[4]), Write(plot[6]), run_time=0.8)
    scene.play(Create(plot[7]), Create(plot[8]), Write(plot[9]), run_time=0.9)
    scene.play(Write(statement), Circumscribe(VGroup(plot[7], plot[8]), color=scene.colors["yellow"]), run_time=1.0)
    scene.wait(1.0)
    scene.clear_scene()


