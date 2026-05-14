from manim import *
import numpy as np


def play(scene):
    # Bind language-aware text constructors for this slide.
    Text = scene.Text
    Tex = scene.Tex
    MathTex = scene.MathTex
    title = scene.make_title("Equação de oscilação")

    torque_label = Tex("(a) Forma em torque, fisicamente exata:", font_size=22, color=scene.colors["muted"])
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
    scene.highlight_terms(torque_eq, {"J_m": scene.colors["blue"], "T_m": scene.colors["cyan"],
                                     "T_e": scene.colors["orange"], "D_m": scene.colors["purple"]})
    torque_panel = VGroup(torque_label, scene.equation_box(torque_eq, color=scene.colors["blue"], buff=0.12))
    torque_panel.arrange(DOWN, aligned_edge=LEFT, buff=0.16)

    power_label = Tex(r"(b) Forma em potência, válida para $\omega_m \approx \omega_{0,m}$:", font_size=22,
                      color=scene.colors["muted"])
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
    scene.highlight_terms(power_eq, {"J_m": scene.colors["blue"], r"P_m": scene.colors["cyan"],
                                    r"P_e": scene.colors["orange"], "D_g": scene.colors["purple"]})
    power_panel = VGroup(power_label, scene.equation_box(power_eq, color=scene.colors["orange"], buff=0.12))
    power_panel.arrange(DOWN, aligned_edge=LEFT, buff=0.16)

    pu_label = Tex("(c) Forma normalizada em pu:", font_size=22, color=scene.colors["muted"])
    pu_eq = MathTex(
        r"2H\frac{d\Delta\omega_{pu}}{dt}",
        "=",
        r"\Delta P_{pu}",
        "-",
        r"D_{pu}\Delta\omega_{pu}",
        font_size=32,
    )
    scene.highlight_terms(pu_eq, {"H": scene.colors["blue"], r"\Delta P_{pu}": scene.colors["red"],
                                 r"D_{pu}": scene.colors["purple"]})
    pu_panel = VGroup(pu_label, scene.equation_box(pu_eq, color=scene.colors["green"], buff=0.12))
    pu_panel.arrange(DOWN, aligned_edge=LEFT, buff=0.16)

    equation_panels = VGroup(torque_panel, power_panel, pu_panel)
    equation_panels.arrange(DOWN, aligned_edge=LEFT, buff=0.36)
    equation_panels.move_to(LEFT * 3.08 + DOWN * 0.02)

    legend = scene.legend_block(
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

    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
    scene.play(FadeIn(torque_panel[0], shift=UP * 0.1), Write(torque_panel[1]), run_time=1.2)
    scene.play(Circumscribe(torque_panel[1][1][0], color=scene.colors["blue"]), run_time=0.7)
    scene.play(FadeIn(power_panel[0], shift=UP * 0.1), Write(power_panel[1]), run_time=1.2)
    scene.play(Circumscribe(power_panel[1][1][2:5], color=scene.colors["red"]), run_time=0.7)
    scene.play(FadeIn(pu_panel[0], shift=UP * 0.1), Write(pu_panel[1]), run_time=1.2)
    scene.play(Circumscribe(pu_panel[1][1][0], color=scene.colors["blue"]), run_time=0.7)
    scene.play(FadeIn(legend, shift=UP * 0.1), run_time=0.8)
    scene.wait(1.1)
    scene.clear_scene()


