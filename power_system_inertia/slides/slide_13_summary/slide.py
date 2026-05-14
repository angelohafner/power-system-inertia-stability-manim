from manim import *
import numpy as np


def play(scene):
    # Bind language-aware text constructors for this slide.
    Text = scene.Text
    Tex = scene.Tex
    MathTex = scene.MathTex
    title = scene.make_title("Resumo")

    summary_1 = MathTex(
        r"\text{Sistema estável}", r"\Rightarrow",
        r"\text{inércia suficiente}", "+",
        r"\text{amortecimento suficiente}", "+",
        r"\text{controle adequado}",
        font_size=38,
    )
    summary_1.set_color_by_tex(r"\text{Sistema estável}", scene.colors["green"])
    summary_1.set_color_by_tex(r"\text{inércia suficiente}", scene.colors["blue"])
    summary_1.set_width(10.9)

    summary_2 = MathTex(
        r"\text{Baixa inércia}", r"\Rightarrow",
        r"\text{maior RoCoF}", r"\Rightarrow",
        r"\text{menor tempo para atuação dos controles}",
        font_size=39,
    )
    summary_2.set_color_by_tex(r"\text{Baixa inércia}", scene.colors["red"])
    summary_2.set_color_by_tex(r"\text{maior RoCoF}", scene.colors["yellow"])
    summary_2.set_width(10.7)

    summary_3 = Tex(
        r"Inércia $\neq$ resposta primária. Inércia limita o RoCoF; "
        r"é a reserva primária (governadores e baterias com FFR) que define o nadir.",
        font_size=27,
        color=scene.colors["text"],
    )
    summary_3.set_width(10.8)

    summaries = VGroup(summary_1, summary_2, summary_3).arrange(DOWN, buff=0.62)
    summaries.move_to(DOWN * 0.20)

    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
    scene.play(Write(summary_1), run_time=1.1)
    scene.play(Write(summary_2), run_time=1.0)
    scene.play(Write(summary_3), run_time=1.0)
    scene.play(Circumscribe(summary_1, color=scene.colors["green"]), Circumscribe(summary_2, color=scene.colors["yellow"]),
              Circumscribe(summary_3, color=scene.colors["blue"]), run_time=1.1)
    scene.wait(2.6)
    scene.clear_scene()

