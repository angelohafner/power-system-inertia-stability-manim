from manim import *
import numpy as np


def play(scene):
    # Bind language-aware text constructors for this slide.
    Text = scene.Text
    Tex = scene.Tex
    MathTex = scene.MathTex
    title_text = VGroup(
        Tex(r"\textbf{Damping}", font_size=42, color=scene.colors["text"]),
        MathTex(r"D", font_size=48, color=scene.colors["text"]),
    ).arrange(RIGHT, buff=0.10)
    title_text.to_edge(UP, buff=0.35)
    underline = Line(LEFT, RIGHT, color=scene.colors["blue"]).set_width(11.5)
    underline.next_to(title_text, DOWN, buff=0.10)
    title = VGroup(VGroup(title_text), underline)

    gen_block = VGroup(
        Tex("No gerador:", font_size=25, color=scene.colors["cyan"]),
        MathTex(
            r"D_{gen}",
            "=",
            r"D_{mec}",
            "+",
            r"D_{amort}",
            r"\quad[\mathrm{pu\cdot s/rad}]",
            font_size=31,
        ),
        Tex("atrito mecânico + enrolamentos amortecedores", font_size=20, color=scene.colors["text"]),
    ).arrange(DOWN, buff=0.16)
    scene.highlight_terms(gen_block[1], {r"D_{gen}": scene.colors["purple"]})
    gen_box = scene.equation_box(gen_block, color=scene.colors["cyan"], buff=0.22)
    gen_box.move_to(LEFT * 3.10 + UP * 1.20)

    load_block = VGroup(
        Tex("Na rede:", font_size=25, color=scene.colors["green"]),
        MathTex(
            r"D_{load}",
            "=",
            r"\frac{\partial P_{carga}}{\partial f}",
            r"\quad[\mathrm{pu/Hz}]",
            font_size=31,
        ),
        Tex(r"auto-regulação da carga, tipicamente 1 a 2 \%/Hz", font_size=20,
            color=scene.colors["text"]),
    ).arrange(DOWN, buff=0.16)
    scene.highlight_terms(load_block[1], {r"D_{load}": scene.colors["green"]})
    load_box = scene.equation_box(load_block, color=scene.colors["green"], buff=0.22)
    load_box.move_to(RIGHT * 3.10 + UP * 1.20)

    system_block = VGroup(
        Tex("No sistema (após conversão de unidades):", font_size=25, color=scene.colors["muted"]),
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
    scene.highlight_terms(system_block[1], {
        r"D_{sys}": scene.colors["purple"],
        r"D_{gen}": scene.colors["cyan"],
        r"D_{load}": scene.colors["green"],
    })
    system_box = scene.equation_box(system_block, color=scene.colors["purple"], buff=0.24)
    system_box.move_to(DOWN * 0.75)

    load_note = scene.legend_block(
        [
            r"\frac{\partial P_{carga}}{\partial f}>0\ \Rightarrow\ \text{carga ajuda a amortecer a queda de frequência}",
        ],
        font_size=24,
    )
    load_note.move_to(DOWN * 2.85)

    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
    scene.play(FadeIn(gen_box, shift=RIGHT * 0.15), FadeIn(load_box, shift=LEFT * 0.15), run_time=1.1)
    scene.play(Write(system_box), run_time=1.0)
    scene.play(FadeIn(load_note, shift=UP * 0.1), Circumscribe(load_box, color=scene.colors["green"]),
              run_time=1.0)
    scene.wait(1.7)
    scene.clear_scene()


