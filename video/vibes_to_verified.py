from __future__ import annotations

from manim import (
    Arrow,
    BOLD,
    Create,
    DL,
    DOWN,
    DR,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromCenter,
    LaggedStart,
    LEFT,
    Line,
    NORMAL,
    RegularPolygon,
    RIGHT,
    RoundedRectangle,
    Scene,
    Text,
    UL,
    UP,
    UR,
    VGroup,
    Write,
    config,
)

config.background_color = "#090B0D"
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

BG = "#090B0D"
PANEL = "#13191D"
WHITE = "#F2F0E9"
MUTED = "#87939C"
GRID = "#273139"
ACCENT = "#42F59E"
CYAN = "#55D8FF"
RED = "#FF5C6C"
YELLOW = "#FFD166"

SANS = "Segoe UI"
MONO = "Consolas"


def label(text: str, size: int = 28, color: str = WHITE, weight: str = NORMAL) -> Text:
    return Text(text, font=MONO, font_size=size, color=color, weight=weight)


def body(text: str, size: int = 34, color: str = WHITE, weight: str = NORMAL) -> Text:
    return Text(text, font=SANS, font_size=size, color=color, weight=weight)


def card(width: float, height: float, stroke: str = CYAN, fill: str = PANEL) -> RoundedRectangle:
    return RoundedRectangle(
        corner_radius=0.18,
        width=width,
        height=height,
        stroke_color=stroke,
        stroke_width=2.2,
        fill_color=fill,
        fill_opacity=0.96,
    )


class VibesToVerified(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.shared_blind_spot()
        self.independent_approaches()
        self.refutation()
        self.scale()
        self.identity()

    def shared_blind_spot(self):
        kicker = label("VIBES TO VERIFIED", 22, ACCENT, BOLD).to_edge(UP, buff=0.65)
        headline = body("64 agents can still\nshare one blind spot.", 50, WHITE, BOLD)
        headline.next_to(kicker, DOWN, buff=0.45)
        self.play(FadeIn(kicker, shift=0.15 * DOWN), Write(headline), run_time=1.2)

        dots = VGroup()
        for row in range(8):
            for col in range(8):
                dot = Dot(
                    point=[-2.75 + col * 0.78, 2.15 - row * 0.62, 0],
                    radius=0.055,
                    color=WHITE,
                )
                dot.set_opacity(0.88)
                dots.add(dot)
        dots.scale(0.78).shift(0.25 * DOWN)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.01), run_time=1.1)

        conclusion = RegularPolygon(n=8, radius=0.72, color=WHITE, fill_color="#D9D6CE", fill_opacity=0.2)
        conclusion.move_to([0, -3.1, 0])
        paths = VGroup(*[
            Line(d.get_center(), conclusion.get_center(), stroke_color=MUTED, stroke_width=0.8, stroke_opacity=0.38)
            for d in dots
        ])
        self.play(Create(paths), GrowFromCenter(conclusion), run_time=1.1)

        crack = VGroup(
            Line([-0.18, -2.48, 0], [0.12, -3.0, 0], color=RED, stroke_width=4),
            Line([0.12, -3.0, 0], [-0.10, -3.35, 0], color=RED, stroke_width=4),
            Line([-0.10, -3.35, 0], [0.18, -3.75, 0], color=RED, stroke_width=4),
        )
        self.play(Create(crack), conclusion.animate.set_stroke(RED), run_time=0.65)

        verdict = body("agreement ≠ verification", 38, RED, BOLD).next_to(conclusion, DOWN, buff=0.55)
        self.play(Write(verdict), run_time=0.7)
        self.wait(0.7)
        self.play(FadeOut(VGroup(kicker, headline, dots, paths, conclusion, crack, verdict)), run_time=0.8)

    def independent_approaches(self):
        title = body("independence\nbefore consensus.", 48, WHITE, BOLD).to_edge(UP, buff=0.7)
        subtitle = body("different routes. different failure modes.", 25, MUTED)
        subtitle.next_to(title, DOWN, buff=0.28)
        self.play(Write(title), FadeIn(subtitle), run_time=0.9)

        claim_box = card(5.2, 1.1, WHITE)
        claim_text = VGroup(label("EXACT CLAIM", 24, WHITE, BOLD), body("atomic + falsifiable", 21, MUTED)).arrange(DOWN, buff=0.12)
        claim = VGroup(claim_box, claim_text).move_to([0, 3.3, 0])
        self.play(FadeIn(claim, shift=0.2 * DOWN), run_time=0.6)

        specs = [
            ("BUILDER", "construct", CYAN),
            ("INVARIANT", "formalize", "#7BB8CC"),
            ("ADVERSARY", "break", RED),
            ("OPERATOR", "run", "#59E7C2"),
            ("EVIDENCE", "audit", ACCENT),
        ]
        roles = VGroup()
        arrows = VGroup()
        for index, (name, verb, color) in enumerate(specs):
            x = -2.15 if index % 2 == 0 else 2.15
            y = 1.75 - index * 1.15
            box = card(3.55, 0.9, color)
            dot = Dot(radius=0.07, color=color).move_to(box.get_left() + 0.34 * RIGHT)
            texts = VGroup(label(name, 20, WHITE, BOLD), body(verb, 17, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
            texts.move_to(box.get_center() + 0.23 * RIGHT)
            role = VGroup(box, dot, texts).move_to([x, y, 0])
            roles.add(role)
            arrows.add(Arrow(claim.get_bottom(), role.get_top(), color=color, stroke_width=1.6, buff=0.1, max_tip_length_to_length_ratio=0.12))

        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.08), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(r, shift=0.15 * DOWN) for r in roles], lag_ratio=0.1), run_time=1.0)

        registry_box = card(6.6, 1.55, CYAN)
        registry_text = VGroup(
            label("APPROACH REGISTRY", 24, CYAN, BOLD),
            body("active   blocked   refuted   survived", 18, MUTED),
        ).arrange(DOWN, buff=0.2)
        registry = VGroup(registry_box, registry_text).move_to([0, -4.7, 0])
        registry_arrows = VGroup(*[
            Arrow(r.get_bottom(), registry.get_top(), color=MUTED, stroke_width=1.3, buff=0.12, max_tip_length_to_length_ratio=0.08)
            for r in roles
        ])
        self.play(LaggedStart(*[GrowArrow(a) for a in registry_arrows], lag_ratio=0.06), run_time=0.7)
        self.play(FadeIn(registry, shift=0.2 * UP), run_time=0.7)
        self.wait(0.6)
        self.play(FadeOut(VGroup(title, subtitle, claim, roles, arrows, registry_arrows, registry)), run_time=0.8)

    def refutation(self):
        title = body("make every claim\neasy to attack.", 48, WHITE, BOLD).to_edge(UP, buff=0.7)
        self.play(Write(title), run_time=0.8)

        claims = VGroup()
        for index in range(4):
            box = card(5.5, 1.0, MUTED)
            text = label(f"CLAIM 0{index + 1}", 24, WHITE, BOLD)
            claims.add(VGroup(box, text))
        claims.arrange(DOWN, buff=0.33).move_to([0, 1.8, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=0.2 * RIGHT) for c in claims], lag_ratio=0.12), run_time=1.0)

        gate_box = card(6.3, 1.35, RED)
        gate_text = VGroup(label("INDEPENDENT REFUTATION", 25, RED, BOLD), body("counter-evidence decides", 19, MUTED)).arrange(DOWN, buff=0.13)
        gate = VGroup(gate_box, gate_text).move_to([0, -2.25, 0])
        self.play(FadeIn(gate, shift=0.2 * UP), run_time=0.6)

        weak = VGroup(claims[0], claims[2])
        survive = VGroup(claims[1], claims[3])
        self.play(
            weak.animate.shift(0.6 * LEFT),
            survive.animate.shift(0.6 * RIGHT),
            run_time=0.55,
        )
        self.play(
            *[item[0].animate.set_stroke(RED) for item in weak],
            *[item[1].animate.set_color(RED) for item in weak],
            *[item[0].animate.set_stroke(ACCENT) for item in survive],
            *[item[1].animate.set_color(WHITE) for item in survive],
            run_time=0.35,
        )
        crosses = VGroup()
        for item in weak:
            center = item.get_center()
            crosses.add(Line(center + 0.33 * UL, center + 0.33 * DR, color=RED, stroke_width=5))
            crosses.add(Line(center + 0.33 * UR, center + 0.33 * DL, color=RED, stroke_width=5))
        self.play(Create(crosses), run_time=0.45)
        self.play(FadeOut(weak, shift=0.5 * LEFT), FadeOut(crosses), run_time=0.65)

        caption = body("reward agents for breaking the answer.", 29, ACCENT, BOLD).to_edge(DOWN, buff=1.0)
        self.play(survive.animate.arrange(DOWN, buff=0.5).move_to([0, 0.8, 0]), Write(caption), run_time=0.9)
        self.wait(0.7)
        self.play(FadeOut(VGroup(title, survive, gate, caption)), run_time=0.8)

    def scale(self):
        title = body("evidence has levels.", 50, WHITE, BOLD).to_edge(UP, buff=0.75)
        subtitle = body("authority should rise only when the evidence does.", 23, MUTED)
        subtitle.next_to(title, DOWN, buff=0.28)
        self.play(Write(title), FadeIn(subtitle), run_time=0.8)

        levels = [
            ("V0", "VIBES", "a claim exists", "#69757D"),
            ("V1", "GROUNDED", "sources + artifacts", "#6896A8"),
            ("V2", "TESTED", "repeatable criteria", CYAN),
            ("V3", "ADVERSARIAL", "independent refutation", "#59E7C2"),
            ("V4", "OPERATIONAL", "natural path + read-back", ACCENT),
        ]
        rows = VGroup()
        for level, name, detail, color in levels:
            box = card(6.8, 1.35, color)
            level_text = label(level, 30, color, BOLD)
            name_text = label(name, 20, WHITE, BOLD)
            detail_text = body(detail, 16, MUTED)
            level_text.move_to(box.get_left() + 0.55 * RIGHT)
            descriptor = VGroup(name_text, detail_text).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            descriptor.move_to(box.get_center() + 0.55 * RIGHT)
            rows.add(VGroup(box, level_text, descriptor))
        rows.arrange(DOWN, buff=0.3).move_to([0, -0.4, 0])

        for row in rows:
            self.play(FadeIn(row, shift=0.2 * RIGHT), run_time=0.42)
        final = body("confidence is not evidence.", 34, ACCENT, BOLD).to_edge(DOWN, buff=0.7)
        self.play(Write(final), run_time=0.7)
        self.wait(0.8)
        self.play(FadeOut(VGroup(title, subtitle, rows, final)), run_time=0.8)

    def identity(self):
        mark = label("V2V", 48, ACCENT, BOLD)
        mark.move_to([0, 2.5, 0])
        title = body("VIBES TO\nVERIFIED", 72, WHITE, BOLD,).next_to(mark, DOWN, buff=0.5)
        title.set_color_by_gradient(WHITE, ACCENT)
        line = Line([-2.6, -0.2, 0], [2.6, -0.2, 0], color=ACCENT, stroke_width=3)
        tagline = body("make your agents prove it.", 32, WHITE, BOLD).next_to(line, DOWN, buff=0.6)
        close = body("keep the speed. add the proof.", 25, MUTED).next_to(tagline, DOWN, buff=0.45)

        self.play(GrowFromCenter(mark), run_time=0.5)
        self.play(Write(title), run_time=0.9)
        self.play(Create(line), Write(tagline), run_time=0.75)
        self.play(FadeIn(close, shift=0.15 * UP), run_time=0.6)
        self.wait(1.4)
