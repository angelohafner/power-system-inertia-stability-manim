from manim import *
import numpy as np


def play(scene):
    # Bind language-aware text constructors for this slide.
    Text = scene.Text
    Tex = scene.Tex
    MathTex = scene.MathTex
    title = scene.make_title("Inércia sintética e Grid-Forming")

    intro = Tex(
        "Sistemas modernos têm penetração crescente de inversores.",
        font_size=27,
        color=scene.colors["text"],
    )
    intro.move_to(UP * 2.18)

    gfl = VGroup(
        Tex("Grid-Following (GFL)", font_size=28, color=scene.colors["orange"]),
        Tex("segue a frequência da rede", font_size=22, color=scene.colors["text"]),
        Tex("NÃO entrega inércia naturalmente", font_size=22, color=scene.colors["red"]),
    ).arrange(DOWN, buff=0.14)
    gfl_box = scene.equation_box(gfl, color=scene.colors["orange"], buff=0.26)
    gfl_box.move_to(LEFT * 3.05 + UP * 0.98)

    gfm = VGroup(
        Tex("Grid-Forming (GFM)", font_size=28, color=scene.colors["blue"]),
        Tex("impõe tensão/frequência", font_size=22, color=scene.colors["text"]),
        Tex("pode emular inércia por controle", font_size=22, color=scene.colors["green"]),
    ).arrange(DOWN, buff=0.14)
    gfm_box = scene.equation_box(gfm, color=scene.colors["blue"], buff=0.26)
    gfm_box.move_to(RIGHT * 3.05 + UP * 0.98)

    gfl_note = VGroup(
        Tex("GFL pode fazer Fast Frequency Response (FFR), mas depende", font_size=18,
            color=scene.colors["text"]),
        Tex("de PLL e tem delay.", font_size=18, color=scene.colors["text"]),
    ).arrange(DOWN, buff=0.04)
    gfm_note = VGroup(
        Tex("GFM emula comportamento inercial de forma mais natural,", font_size=18,
            color=scene.colors["text"]),
        Tex(r"sem depender de PLL para seguir uma rede forte.", font_size=18,
            color=scene.colors["text"]),
    ).arrange(DOWN, buff=0.04)
    gfl_gfm_note = VGroup(gfl_note, gfm_note).arrange(DOWN, buff=0.16)
    gfl_gfm_note.set_width(9.2)
    gfl_gfm_note.move_to(DOWN * 0.88)

    convention = VGroup(
        Tex("Convenção:", font_size=21, color=scene.colors["muted"]),
        MathTex(
            r"\Delta P_{inv,pu}",
            "=",
            r"-2H_v\frac{d\Delta\omega_{pu}}{dt}",
            font_size=31,
        ),
    ).arrange(DOWN, buff=0.10)
    scene.highlight_terms(convention[1], {r"H_v": scene.colors["blue"]})
    convention_box = scene.equation_box(convention, color=scene.colors["green"], buff=0.18)

    hz_form = VGroup(
        Tex(r"Em Hz (com $\Delta\omega_{pu}=\Delta f/f_0$):", font_size=21,
            color=scene.colors["muted"]),
        MathTex(
            r"\Delta P_{inv,pu}",
            "=",
            r"-\frac{2H_v}{f_0}\frac{d\Delta f}{dt}",
            font_size=31,
        ),
    ).arrange(DOWN, buff=0.10)
    scene.highlight_terms(hz_form[1], {r"H_v": scene.colors["blue"]})
    hz_box = scene.equation_box(hz_form, color=scene.colors["green"], buff=0.18)

    control_boxes = VGroup(convention_box, hz_box).arrange(RIGHT, buff=0.42)
    control_boxes.move_to(UP * 1.45)

    sign_note = Tex(
        r"\textit{O sinal negativo significa que o inversor injeta potência quando a frequência está caindo, opondo-se à variação.}",
        font_size=17,
        color=scene.colors["muted"],
    )
    sign_note.set_width(10.2)
    sign_note.move_to(DOWN * 0.04)

    comparison = VGroup(
        VGroup(
            Tex("síncrona:", font_size=21, color=scene.colors["cyan"]),
            Tex("inércia física, instantânea, sem controle", font_size=19, color=scene.colors["text"]),
        ).arrange(RIGHT, buff=0.18),
        VGroup(
            Tex("inversor:", font_size=21, color=scene.colors["yellow"]),
            Tex(r"``inércia'' via software, com delay, saturação e energia DC disponível", font_size=19,
                color=scene.colors["text"]),
        ).arrange(RIGHT, buff=0.18),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    comparison.set_width(10.6)
    comparison.move_to(DOWN * 1.30)

    ffr = Tex(
        "Fast Frequency Response (FFR) das baterias atua nos primeiros segundos, "
        "complementando (não substituindo) a inércia.",
        font_size=21,
        color=scene.colors["text"],
    )
    ffr.set_width(10.6)
    ffr.move_to(DOWN * 2.55)

    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
    scene.play(Write(intro), run_time=0.8)
    scene.play(FadeIn(gfl_box, shift=RIGHT * 0.15), FadeIn(gfm_box, shift=LEFT * 0.15), run_time=1.1)
    scene.play(Write(gfl_gfm_note), run_time=0.9)
    scene.wait(0.9)
    scene.play(FadeOut(VGroup(intro, gfl_box, gfm_box, gfl_gfm_note)), run_time=0.7)
    scene.play(Write(control_boxes), run_time=1.0)
    scene.play(Write(sign_note), run_time=0.8)
    scene.play(Write(comparison), run_time=1.0)
    scene.play(Write(ffr), Circumscribe(control_boxes, color=scene.colors["green"]), run_time=1.1)
    scene.wait(1.4)
    scene.clear_scene()


