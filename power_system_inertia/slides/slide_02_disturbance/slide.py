from manim import *
import numpy as np


def play(scene):
    # Bind language-aware text constructors for this slide.
    Text = scene.Text
    Tex = scene.Tex
    MathTex = scene.MathTex
    title = scene.make_title("Desequilíbrio de potência")
    diagram = scene.draw_power_system("60,0 Hz", disturbed=True, meter_disturbed=False)
    diagram.scale(0.84).shift(DOWN * 0.08)
    turbine_rotor = diagram[0][1]
    flow_pulses = scene.make_energy_pulses(
        [diagram[1], diagram[3]],
        color=scene.colors["yellow"],
        speed=0.42,
        radius=0.036,
    )
    load_pulses = scene.make_energy_pulses(
        [diagram[5]],
        color=scene.colors["red"],
        speed=0.95,
        radius=0.052,
        phases=(0.0, 0.25, 0.50, 0.75),
    )

    inequality = MathTex(r"P_m", r"<", r"P_e", font_size=56)
    scene.highlight_terms(inequality, {r"P_m": scene.colors["cyan"], r"P_e": scene.colors["orange"]})
    inequality.move_to(LEFT * 3.0 + DOWN * 2.25)

    deficit = MathTex(r"\Delta P", "=", r"P_m", "-", r"P_e", "<", "0", font_size=50)
    scene.highlight_terms(deficit, {
        r"\Delta P": scene.colors["red"],
        r"P_m": scene.colors["cyan"],
        r"P_e": scene.colors["orange"],
    })
    deficit.move_to(RIGHT * 2.25 + DOWN * 2.25)

    statement = VGroup(
        Tex("Quando a carga supera a geração,", font_size=30, color=scene.colors["text"]),
        Tex("o sistema precisa retirar energia", font_size=30, color=scene.colors["text"]),
        Tex("de algum lugar nos primeiros instantes.", font_size=30, color=scene.colors["text"]),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    statement.next_to(title, DOWN, buff=0.36)
    statement.shift(LEFT * 1.05)
    transient_note = Tex(
        "excursão transitória (resposta inercial) — não é regime permanente",
        font_size=21,
        color=scene.colors["muted"],
    )
    transient_note.to_edge(DOWN, buff=0.18)

    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
    scene.play(FadeIn(diagram[:8], shift=UP * 0.15), run_time=1.0)
    omega_ref = scene.start_turbine(turbine_rotor, center_point=diagram[0][0].get_center())
    scene.add(flow_pulses)
    scene.play(Write(diagram[8]), Write(diagram[9]), run_time=0.8)
    scene.play_frequency_meter_drop(
        diagram[7],
        Create(diagram[10][0]),
        Write(diagram[10][1]),
        FadeIn(load_pulses),
        Flash(diagram[10][0].get_end(), color=scene.colors["red"]),
        omega_ref=omega_ref,
    )
    scene.play(FadeIn(transient_note, shift=UP * 0.05), run_time=0.5)
    scene.play(Write(inequality), run_time=0.8)
    scene.play(ReplacementTransform(inequality.copy(), deficit), run_time=1.1)
    scene.play(Write(statement), Circumscribe(diagram[7], color=scene.colors["red"]), run_time=1.4)
    scene.wait(1.7)
    scene.stop_turbine(turbine_rotor)
    scene.clear_energy_pulses(flow_pulses)
    scene.clear_energy_pulses(load_pulses)
    scene.clear_scene()


