from manim import *
import numpy as np


def play(scene):
    # Bind language-aware text constructors for this slide.
    Text = scene.Text
    Tex = scene.Tex
    MathTex = scene.MathTex
    title = scene.make_title("Equilíbrio entre geração e carga")
    diagram = scene.draw_power_system("60,0 Hz")
    diagram.scale(0.95).shift(UP * 0.15)
    turbine_rotor = diagram[0][1]
    flow_pulses = scene.make_energy_pulses(
        [diagram[1], diagram[3], diagram[5]],
        color=scene.colors["yellow"],
        speed=0.44,
        radius=0.040,
    )

    statement = scene.make_caption(
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
    scene.highlight_terms(balance, {
        r"P_{\text{geração}}": scene.colors["cyan"],
        r"P_{\text{carga}}": scene.colors["orange"],
        r"P_{\text{perdas}}": scene.colors["red"],
    })
    balance.move_to(DOWN * 1.60)

    generator_balance = MathTex(r"P_m", "=", r"P_e", font_size=44)
    scene.highlight_terms(generator_balance, {r"P_m": scene.colors["cyan"], r"P_e": scene.colors["orange"]})
    generator_note = Tex("(desprezando perdas internas do gerador)", font_size=21, color=scene.colors["muted"])
    generator_group = VGroup(generator_balance, generator_note).arrange(DOWN, buff=0.08)
    generator_group.move_to(DOWN * 2.24 + LEFT * 2.05)

    freq = MathTex(r"f", r"\approx", r"f_0", font_size=48)
    freq.set_color_by_tex("f", scene.colors["green"])
    freq.move_to(DOWN * 2.24 + RIGHT * 2.55)

    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
    scene.play(FadeIn(diagram[:7], shift=UP * 0.2), run_time=1.2)
    scene.start_turbine(turbine_rotor, center_point=diagram[0][0].get_center())
    scene.add(flow_pulses)
    scene.play(FadeIn(diagram[7]), Write(diagram[8]), Write(diagram[9]), run_time=1.3)
    scene.play(Write(statement), run_time=1.5)
    scene.play(FadeOut(diagram[9][1]), run_time=0.35)
    scene.play(Write(balance), run_time=0.9)
    scene.play(Indicate(diagram[2][0], color=scene.colors["blue"]), Indicate(balance, color=scene.colors["green"]),
              run_time=1.1)
    scene.play(Write(generator_group), Write(freq), run_time=0.8)
    scene.play(Circumscribe(diagram[7], color=scene.colors["green"]), Circumscribe(freq, color=scene.colors["green"]),
              run_time=1.2)
    scene.wait(1.1)
    scene.stop_turbine(turbine_rotor)
    scene.clear_energy_pulses(flow_pulses)
    scene.clear_scene()


