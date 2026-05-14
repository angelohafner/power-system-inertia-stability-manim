from manim import *
import numpy as np


def play(scene):
    # Bind language-aware text constructors for this slide.
    Text = scene.Text
    Tex = scene.Tex
    MathTex = scene.MathTex
    title_text = Tex(r"\textbf{Exemplo: redução de }$H_{sys}$", font_size=43, color=scene.colors["text"])
    title_text.to_edge(UP, buff=0.35)
    underline = Line(LEFT, RIGHT, color=scene.colors["blue"]).set_width(11.5)
    underline.next_to(title_text, DOWN, buff=0.10)
    title = VGroup(VGroup(title_text), underline)

    formula = MathTex(
        r"H_{sys}",
        "=",
        r"\frac{\sum_i H_iS_i}{S_{total}}",
        font_size=44,
    )
    scene.highlight_terms(formula, {r"H_{sys}": scene.colors["blue"]})
    formula.move_to(UP * 2.28)

    def scenario_card(title_text, rows, result_tex, color):
        header = Tex(title_text, font_size=25, color=color)
        body = VGroup(*[
            MathTex(row, font_size=24, color=scene.colors["text"]) for row in rows
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
        scene.colors["cyan"],
    )
    scenario_a.move_to(LEFT * 3.05 + DOWN * 0.20)

    scenario_b = scenario_card(
        r"Cenario B (50\% IBR)",
        [
            r"\text{Térmica 1: }H=5\,\mathrm{s},\ S=500\,\mathrm{MVA}",
            r"\text{Solar/Eólica (IBR): }H=0,\ S=1000\,\mathrm{MVA}",
        ],
        r"H_{sys}\approx1{,}67\,\mathrm{s}",
        scene.colors["orange"],
    )
    scenario_b.move_to(RIGHT * 3.05 + DOWN * 0.20)

    conclusion = VGroup(
        Tex(r"Mesma capacidade instalada, $H_{sys}$ cai $\sim 3\times$.", font_size=28,
            color=scene.colors["text"]),
        Tex(r"RoCoF para o mesmo $\Delta P$ triplica.", font_size=28,
            color=scene.colors["text"]),
    ).arrange(DOWN, buff=0.08)
    conclusion.set_width(9.45)
    conclusion_box = scene.equation_box(conclusion, color=scene.colors["yellow"], buff=0.26)
    conclusion_box.move_to(DOWN * 3.05)

    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
    scene.play(Write(formula), run_time=0.8)
    scene.play(FadeIn(scenario_a, shift=RIGHT * 0.15), FadeIn(scenario_b, shift=LEFT * 0.15), run_time=1.1)
    scene.play(Write(conclusion_box), run_time=1.0)
    scene.play(Circumscribe(conclusion_box, color=scene.colors["yellow"]), run_time=0.8)
    scene.wait(1.6)
    scene.clear_scene()


