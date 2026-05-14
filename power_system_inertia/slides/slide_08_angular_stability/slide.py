from manim import *
import numpy as np


def play(scene):
    # Bind language-aware text constructors for this slide.
    Text = scene.Text
    Tex = scene.Tex
    MathTex = scene.MathTex
    title = scene.make_title("Estabilidade angular")
    delta_angle = ValueTracker(0.48)
    delta_intro = scene.draw_delta_definition(delta_angle)

    second_order = MathTex(
        r"M", r"\frac{d^2\Delta\delta}{dt^2}", "+",
        r"D", r"\frac{d\Delta\delta}{dt}", "+",
        r"K_s", r"\Delta\delta", "=", "0",
        r",\quad", r"M=\frac{2H}{\omega_0}",
        font_size=37,
    )
    scene.highlight_terms(second_order, {"M": scene.colors["blue"], "D": scene.colors["purple"], r"K_s": scene.colors["green"]})
    second_order.move_to(UP * 1.55)

    characteristic = MathTex(r"M", "s^2", "+", r"D", "s", "+", r"K_s", "=", "0", font_size=40)
    scene.highlight_terms(characteristic, {"M": scene.colors["blue"], "D": scene.colors["purple"], r"K_s": scene.colors["green"]})
    characteristic.move_to(UP * 0.82)

    ks_note = MathTex(
        r"K_s",
        "=",
        r"\left.\frac{\partial P_e}{\partial\delta}\right|_{\delta_0}",
        r"\approx",
        r"\frac{EV}{X}\cos(\delta_0)",
        font_size=32,
    )
    scene.highlight_terms(ks_note, {r"K_s": scene.colors["green"]})
    equation_stack = VGroup(second_order, characteristic, ks_note)
    equation_stack.arrange(DOWN, buff=0.30)
    equation_stack.move_to(UP * 1.42)

    term_labels = scene.legend_block(
        [
            r"M:\ \text{constante de partida }[\mathrm{s^2}]",
            r"D:\ \text{amortecimento }[\mathrm{pu\cdot s/rad}]",
            r"K_s:\ \text{sincronismo elétrico }[\mathrm{pu/rad}]",
            r"\delta:\ \text{ângulo elétrico }[\mathrm{rad}]",
        ],
        font_size=19,
        line_buff=0.07,
    )
    term_labels.move_to(RIGHT * 4.23 + UP * 0.08)

    curves = scene.draw_angular_stability_curves().scale(0.56).move_to(DOWN * 2.10 + LEFT * 3.55)

    first_statement = Tex(
        "A inércia reduz a rapidez da variação da frequência.",
        font_size=21,
        color=scene.colors["text"],
    )
    second_statement = VGroup(
        Tex("A estabilidade também depende do amortecimento",
            font_size=21, color=scene.colors["text"]),
        Tex("e do sincronismo elétrico.",
            font_size=21, color=scene.colors["text"]),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    statement = VGroup(first_statement, second_statement).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
    statement.move_to(RIGHT * 3.42 + DOWN * 1.86)

    loading_note = VGroup(
        Tex(r"Conforme o sistema é mais carregado ($\delta_0$ cresce),",
            font_size=24, color=scene.colors["text"]),
        Tex(r"$K_s$ diminui e a margem de estabilidade encolhe.",
            font_size=24, color=scene.colors["text"]),
    ).arrange(DOWN, buff=0.08)
    loading_note.move_to(LEFT * 3.10 + DOWN * 0.70)

    transient_plot = scene.draw_transient_instability_plot().scale(0.76).move_to(LEFT * 2.65 + DOWN * 0.35)
    transient_text = VGroup(
        Tex("Instabilidade transitória:", font_size=30, color=scene.colors["red"]),
        Tex("perda de sincronismo", font_size=30, color=scene.colors["red"]),
        Tex(r"Após uma falta severa, $\delta$ pode crescer", font_size=25, color=scene.colors["text"]),
        Tex("monotonicamente, sem oscilar em torno do equilíbrio.", font_size=25, color=scene.colors["text"]),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    transient_text.move_to(RIGHT * 2.95 + DOWN * 0.20)
    transient_method_note = VGroup(
        Tex("Para análise transitória usa-se o método das áreas iguais", font_size=20,
            color=scene.colors["muted"]),
        Tex("(Equal Area Criterion) ou simulação no domínio do tempo,", font_size=20,
            color=scene.colors["muted"]),
        Tex("não o autovalor da equação linearizada.", font_size=20, color=scene.colors["muted"]),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    transient_method_note.move_to(RIGHT * 2.95 + DOWN * 2.25)

    scene.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
    scene.play(
        FadeIn(delta_intro[0], shift=RIGHT * 0.2),
        Write(delta_intro[1]),
        FadeIn(delta_intro[2], shift=UP * 0.15),
        run_time=1.2,
    )
    scene.play(delta_angle.animate.set_value(0.98), run_time=0.9, rate_func=smooth)
    scene.play(delta_angle.animate.set_value(0.64), run_time=0.8, rate_func=smooth)
    scene.play(
        Circumscribe(delta_intro[1][0], color=scene.colors["green"]),
        Indicate(delta_intro[2][1][0], color=scene.colors["green"]),
        run_time=0.8,
    )
    scene.wait(0.5)
    scene.play(FadeOut(delta_intro), run_time=0.6)
    scene.play(Write(second_order), run_time=1.2)
    scene.play(Write(characteristic), run_time=0.9)
    scene.play(Write(ks_note), FadeIn(term_labels, shift=UP * 0.2), run_time=1.0)
    scene.play(Write(loading_note), run_time=0.8)
    scene.play(Create(curves[:3]), run_time=0.7)
    scene.play(Create(curves[3]), Create(curves[4]), Create(curves[5]), FadeIn(curves[6]), run_time=1.4)
    scene.play(Write(statement), run_time=1.1)
    scene.wait(0.8)
    scene.play(
        FadeOut(VGroup(second_order, characteristic, ks_note, term_labels, curves, statement,
                       loading_note)),
        run_time=0.8,
    )
    scene.play(Create(transient_plot[:3]), run_time=0.7)
    scene.play(Create(transient_plot[3]), Write(transient_plot[4]), Write(transient_text), run_time=1.2)
    scene.bring_to_front(transient_plot[4])
    scene.play(Write(transient_method_note), run_time=0.9)
    scene.wait(1.8)
    scene.clear_scene()


