from manim import *
import numpy as np


def play(scene):
    # Bind language-aware text constructors for this slide.
    Text = scene.Text
    Tex = scene.Tex
    MathTex = scene.MathTex
    title = scene.make_title("Energia cinética e inércia")
    rotor = scene.draw_rotor().scale(1.25).move_to(LEFT * 3.55 + DOWN * 0.05)

    statement = scene.make_caption("O rotor das máquinas síncronas armazena energia cinética.",
                                  width=6.1, font_size=28)
    statement.move_to(RIGHT * 2.65 + UP * 1.7)

    energy = MathTex(r"E_k", "=", r"\frac{1}{2}", "J_m", r"\omega_m^2", font_size=58)
    scene.highlight_terms(energy, {r"E_k": scene.colors["green"], "J_m": scene.colors["blue"], r"\omega_m": scene.colors["yellow"]})
    energy.move_to(RIGHT * 2.85 + UP * 0.88)

    term_labels = VGroup(
        MathTex(r"J_m:\ \text{momento de inércia mecânico }[\mathrm{kg\,m^2}]",
                font_size=27, color=scene.colors["blue"]),
        MathTex(r"\omega_m:\ \text{velocidade angular mecânica }[\mathrm{rad/s}]",
                font_size=27, color=scene.colors["yellow"]),
        MathTex(r"E_k:\ \text{energia cinética armazenada }[\mathrm{J}]",
                font_size=27, color=scene.colors["green"]),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
    term_labels.move_to(RIGHT * 2.85 + DOWN * 0.88)

    power_support = Arrow(rotor.get_right() + RIGHT * 0.16 + DOWN * 1.15, LEFT * 0.35 + DOWN * 1.15,
                          color=scene.colors["green"], stroke_width=6)
    support_label = Text("resposta inicial", font_size=23, color=scene.colors["green"]).next_to(power_support, DOWN, buff=0.1)

    conclusion = scene.make_caption(
        "A inércia não impede a queda de frequência, mas reduz a rapidez dessa queda.",
        width=10.6,
        font_size=27,
    )
    conclusion.to_edge(DOWN, buff=0.42)

    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
    scene.play(FadeIn(rotor[0]), Create(rotor[1]), Write(rotor[2]), run_time=1.2)
    rotor[0].add_updater(lambda mob, dt: mob.rotate(1.30 * dt, about_point=mob.get_center()))
    scene.play(Write(statement), run_time=0.9)
    scene.play(Write(energy), run_time=1.1)
    scene.play(Indicate(energy[3], color=scene.colors["blue"]), Indicate(energy[4], color=scene.colors["yellow"]),
              run_time=1.0)
    scene.play(FadeIn(term_labels, shift=UP * 0.2), run_time=1.2)
    scene.play(Create(power_support), Write(support_label), run_time=0.8)
    scene.play(Write(conclusion), Circumscribe(energy, color=scene.colors["green"]), run_time=1.3)
    scene.wait(1.8)
    rotor[0].clear_updaters()
    scene.clear_scene()


