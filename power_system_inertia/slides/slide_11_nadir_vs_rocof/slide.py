from manim import *
import numpy as np


def play(scene):
    # Bind language-aware text constructors for this slide.
    Text = scene.Text
    Tex = scene.Tex
    MathTex = scene.MathTex
    title = scene.make_title("Nadir de frequência vs RoCoF")

    plot = scene.draw_nadir_rocof_plot().scale(0.72).move_to(LEFT * 2.95 + DOWN * 0.25)
    reserve_dependency = VGroup(
        Tex(r"Depende de reserva primária, droop $R$ e tempo", font_size=21,
            color=scene.colors["text"]),
        Tex("da governação e amortecimento da carga.", font_size=21,
            color=scene.colors["text"]),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
    bullets = VGroup(
        Tex(r"$\mathrm{RoCoF}$: declividade inicial ($df/dt$ em $t=0^+$).", font_size=21,
            color=scene.colors["text"]),
        Tex(r"Depende de $H_{sys}$ e $\Delta P$.", font_size=21, color=scene.colors["text"]),
        Tex("Nadir: frequência mínima atingida durante o transitório.", font_size=21,
            color=scene.colors["text"]),
        reserve_dependency,
        Tex(r"$\mathrm{UFLS}$ em sistemas 60 Hz: tipicamente 59,5 a 58,5 Hz.", font_size=21,
            color=scene.colors["muted"]),
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
        color=scene.colors["muted"],
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
        color=scene.colors["text"],
    )
    nadir_dependence.set_width(5.2)
    canonical_block_content = VGroup(steady_eq, steady_units, nadir_eq, nadir_dependence).arrange(DOWN, buff=0.12)
    canonical_block = scene.equation_box(canonical_block_content, color=scene.colors["blue"], buff=0.18)
    canonical_block.move_to(RIGHT * 3.22 + DOWN * 1.35)

    final_note = VGroup(
        Tex(r"RoCoF depende de $H_{sys}$ e $\Delta P$.", font_size=18, color=scene.colors["yellow"]),
        Tex(r"Nadir depende de $H_{sys}$, $\Delta P$, reserva, droop, $D_f$ e dinâmica do governador.",
            font_size=17, color=scene.colors["yellow"]),
    ).arrange(DOWN, buff=0.04)
    final_note.set_width(5.55)
    final_note.move_to(RIGHT * 3.22 + DOWN * 3.18)

    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
    scene.play(Create(plot[:4]), run_time=0.8)
    scene.play(Create(plot[4]), run_time=0.8)
    scene.play(Create(plot[5]), Write(plot[6]), run_time=0.8)
    scene.bring_to_front(plot[6])
    scene.play(FadeIn(plot[7]), FadeIn(plot[8]), Write(plot[9]), FadeIn(plot[0]), Write(plot[10]), run_time=1.0)
    scene.bring_to_front(plot[6])
    scene.play(Write(bullets), run_time=1.3)
    scene.play(Write(canonical_block), run_time=1.1)
    scene.play(Write(final_note), run_time=0.8)
    scene.wait(1.8)
    scene.clear_scene()


