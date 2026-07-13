#!/usr/bin/env python
"""Generate deterministic SVG graphics for Vibes to Verified."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "media" / "exports"

BG = "#090B0D"
PANEL = "#11161A"
PANEL_2 = "#151C21"
WHITE = "#F2F0E9"
MUTED = "#87939C"
GRID = "#1A2329"
ACCENT = "#42F59E"
CYAN = "#55D8FF"
RED = "#FF5C6C"
YELLOW = "#FFD166"


def defs() -> str:
    return f"""
    <defs>
      <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="{GRID}" stroke-width="1" opacity="0.45"/>
      </pattern>
      <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="7" result="blur"/>
        <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
      <linearGradient id="accentLine" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#58636B"/>
        <stop offset="0.35" stop-color="{CYAN}"/>
        <stop offset="1" stop-color="{ACCENT}"/>
      </linearGradient>
      <style>
        .sans {{ font-family: 'Segoe UI', Arial, sans-serif; }}
        .mono {{ font-family: 'Cascadia Mono', 'Consolas', monospace; }}
        .caps {{ letter-spacing: 3px; }}
      </style>
    </defs>
    """


def frame(width: int, height: int, body: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    {defs()}
    <rect width="{width}" height="{height}" fill="{BG}"/>
    <rect width="{width}" height="{height}" fill="url(#grid)"/>
    {body}
    </svg>
    """


def v2v_scale() -> str:
    levels = [
        ("V0", "VIBES", "a claim exists", "#69757D"),
        ("V1", "GROUNDED", "sources + artifacts", "#6896A8"),
        ("V2", "TESTED", "repeatable criteria", CYAN),
        ("V3", "ADVERSARIAL", "independent refutation", "#59E7C2"),
        ("V4", "OPERATIONAL", "natural path + read-back", ACCENT),
    ]
    cards = []
    x0, y, w, h, gap = 90, 330, 260, 250, 28
    for index, (level, name, detail, color) in enumerate(levels):
        x = x0 + index * (w + gap)
        cards.append(f"""
        <g>
          <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{PANEL}" stroke="{color}" stroke-width="2"/>
          <rect x="{x}" y="{y}" width="{w}" height="8" rx="4" fill="{color}"/>
          <text x="{x + 28}" y="{y + 72}" class="mono" font-size="38" font-weight="700" fill="{color}">{level}</text>
          <text x="{x + 28}" y="{y + 125}" class="sans caps" font-size="22" font-weight="700" fill="{WHITE}">{name}</text>
          <line x1="{x + 28}" y1="{y + 156}" x2="{x + w - 28}" y2="{y + 156}" stroke="{GRID}" stroke-width="2"/>
          <text x="{x + 28}" y="{y + 205}" class="sans" font-size="20" fill="{MUTED}">{detail}</text>
        </g>
        """)
        if index < len(levels) - 1:
            ax = x + w + 7
            cards.append(f'<path d="M {ax} {y + h/2} L {ax + 14} {y + h/2}" stroke="{MUTED}" stroke-width="3"/><path d="M {ax+10} {y+h/2-6} L {ax+18} {y+h/2} L {ax+10} {y+h/2+6}" fill="none" stroke="{MUTED}" stroke-width="3"/>')
    return frame(1600, 900, f"""
      <text x="90" y="88" class="mono caps" font-size="19" fill="{ACCENT}">VIBES TO VERIFIED / EVIDENCE MATURITY</text>
      <text x="90" y="180" class="sans" font-size="70" font-weight="750" fill="{WHITE}">confidence is not evidence.</text>
      <text x="90" y="235" class="sans" font-size="28" fill="{MUTED}">authority should rise only when the evidence does.</text>
      {''.join(cards)}
      <rect x="90" y="660" width="1420" height="2" fill="url(#accentLine)"/>
      <text x="90" y="730" class="sans" font-size="26" fill="{WHITE}">verdict and evidence maturity are separate.</text>
      <text x="90" y="780" class="mono" font-size="22" fill="{MUTED}">RED / V4 can be more rigorous than GREEN / V0.</text>
      <text x="1510" y="844" text-anchor="end" class="mono caps" font-size="17" fill="{ACCENT}">MAKE YOUR AGENTS PROVE IT.</text>
    """)


def workflow() -> str:
    approaches = [
        ("BUILDER", "construct"),
        ("INVARIANT", "formalize"),
        ("ADVERSARY", "break"),
        ("OPERATOR", "run"),
        ("EVIDENCE", "audit"),
    ]
    nodes = []
    for i, (name, verb) in enumerate(approaches):
        y = 260 + i * 92
        color = RED if name == "ADVERSARY" else CYAN
        nodes.append(f"""
          <rect x="250" y="{y}" width="230" height="64" rx="14" fill="{PANEL}" stroke="{color}" stroke-width="2"/>
          <circle cx="279" cy="{y+32}" r="8" fill="{color}"/>
          <text x="303" y="{y+29}" class="mono" font-size="18" font-weight="700" fill="{WHITE}">{name}</text>
          <text x="303" y="{y+50}" class="sans" font-size="15" fill="{MUTED}">{verb}</text>
          <path d="M 480 {y+32} C 560 {y+32}, 550 450, 635 450" fill="none" stroke="{MUTED}" stroke-width="2" opacity="0.6"/>
        """)
    return frame(1600, 900, f"""
      <text x="80" y="80" class="mono caps" font-size="19" fill="{ACCENT}">VIBES TO VERIFIED / WORKFLOW</text>
      <text x="80" y="165" class="sans" font-size="64" font-weight="750" fill="{WHITE}">independence before consensus.</text>
      <text x="80" y="215" class="sans" font-size="25" fill="{MUTED}">different approaches propose. refuters attack. artifacts decide.</text>

      <rect x="70" y="392" width="145" height="116" rx="18" fill="{PANEL_2}" stroke="{WHITE}" stroke-width="2"/>
      <text x="142" y="433" text-anchor="middle" class="mono" font-size="17" fill="{MUTED}">EXACT</text>
      <text x="142" y="462" text-anchor="middle" class="mono" font-size="22" font-weight="700" fill="{WHITE}">CLAIM</text>
      <text x="142" y="488" text-anchor="middle" class="sans" font-size="14" fill="{MUTED}">falsifiable</text>
      <path d="M 215 450 L 230 450" stroke="{ACCENT}" stroke-width="3"/>
      <path d="M 230 292 L 230 660" stroke="{ACCENT}" stroke-width="2" opacity="0.8"/>
      <path d="M 230 292 L 245 292 M 230 384 L 245 384 M 230 476 L 245 476 M 230 568 L 245 568 M 230 660 L 245 660" stroke="{ACCENT}" stroke-width="3"/>
      <path d="M 239 286 L 247 292 L 239 298 M 239 378 L 247 384 L 239 390 M 239 470 L 247 476 L 239 482 M 239 562 L 247 568 L 239 574 M 239 654 L 247 660 L 239 666" fill="none" stroke="{ACCENT}" stroke-width="2"/>

      {''.join(nodes)}

      <rect x="635" y="345" width="230" height="210" rx="22" fill="{PANEL_2}" stroke="{CYAN}" stroke-width="2"/>
      <text x="750" y="402" text-anchor="middle" class="mono" font-size="18" fill="{CYAN}">APPROACH</text>
      <text x="750" y="432" text-anchor="middle" class="mono" font-size="21" font-weight="700" fill="{WHITE}">REGISTRY</text>
      <line x1="675" y1="460" x2="825" y2="460" stroke="{GRID}" stroke-width="2"/>
      <text x="675" y="495" class="sans" font-size="16" fill="{MUTED}">active</text>
      <text x="760" y="495" class="sans" font-size="16" fill="{YELLOW}">blocked</text>
      <text x="675" y="525" class="sans" font-size="16" fill="{RED}">refuted</text>
      <text x="760" y="525" class="sans" font-size="16" fill="{ACCENT}">survived</text>

      <path d="M 865 450 L 930 450" stroke="{ACCENT}" stroke-width="3"/>
      <path d="M 922 442 L 932 450 L 922 458" fill="none" stroke="{ACCENT}" stroke-width="3"/>

      <rect x="935" y="330" width="230" height="240" rx="22" fill="{PANEL_2}" stroke="{RED}" stroke-width="2"/>
      <text x="1050" y="390" text-anchor="middle" class="mono" font-size="18" fill="{RED}">INDEPENDENT</text>
      <text x="1050" y="422" text-anchor="middle" class="mono" font-size="22" font-weight="700" fill="{WHITE}">REFUTATION</text>
      <line x1="977" y1="451" x2="1123" y2="451" stroke="{GRID}" stroke-width="2"/>
      <text x="1050" y="490" text-anchor="middle" class="sans" font-size="17" fill="{MUTED}">atomic claims</text>
      <text x="1050" y="520" text-anchor="middle" class="sans" font-size="17" fill="{MUTED}">counter-evidence</text>
      <text x="1050" y="550" text-anchor="middle" class="sans" font-size="17" fill="{MUTED}">reproduction</text>

      <path d="M 1165 450 L 1230 450" stroke="{ACCENT}" stroke-width="3"/>
      <path d="M 1222 442 L 1232 450 L 1222 458" fill="none" stroke="{ACCENT}" stroke-width="3"/>

      <rect x="1235" y="345" width="285" height="210" rx="22" fill="{PANEL_2}" stroke="{ACCENT}" stroke-width="2" filter="url(#glow)"/>
      <text x="1377" y="402" text-anchor="middle" class="mono" font-size="17" fill="{ACCENT}">FINAL</text>
      <text x="1377" y="435" text-anchor="middle" class="mono" font-size="22" font-weight="700" fill="{WHITE}">EVIDENCE CARD</text>
      <line x1="1280" y1="462" x2="1475" y2="462" stroke="{GRID}" stroke-width="2"/>
      <text x="1280" y="498" class="mono" font-size="15" fill="{MUTED}">VERDICT</text>
      <text x="1475" y="498" text-anchor="end" class="mono" font-size="15" fill="{ACCENT}">SCOPED</text>
      <text x="1280" y="528" class="mono" font-size="15" fill="{MUTED}">V2V LEVEL</text>
      <text x="1475" y="528" text-anchor="end" class="mono" font-size="15" fill="{ACCENT}">EVIDENCED</text>

      <text x="80" y="810" class="sans" font-size="27" fill="{WHITE}">the goal is not to make agents agree.</text>
      <text x="80" y="852" class="sans" font-size="27" fill="{ACCENT}">it is to make unsupported claims die before they reach you.</text>
    """)


def receipt() -> str:
    cards = [
        ("REVIEW 01", "RED", RED, "signed states +", "duplicate actions"),
        ("REVIEW 02", "RED", RED, "concurrent authority +", "bypass paths"),
        ("PRIVATE REVIEW 03", "GREEN", ACCENT, "no remaining P0/P1", "private scope"),
    ]
    blocks = []
    for i, (review, verdict, color, line1, line2) in enumerate(cards):
        x = 100 + i * 500
        blocks.append(f"""
          <rect x="{x}" y="285" width="400" height="245" rx="24" fill="{PANEL}" stroke="{color}" stroke-width="2"/>
          <text x="{x+35}" y="340" class="mono caps" font-size="17" fill="{MUTED}">{review}</text>
          <text x="{x+35}" y="410" class="mono" font-size="48" font-weight="800" fill="{color}">{verdict}</text>
          <line x1="{x+35}" y1="438" x2="{x+365}" y2="438" stroke="{GRID}" stroke-width="2"/>
          <text x="{x+35}" y="478" class="sans" font-size="21" fill="{WHITE}">{line1}</text>
          <text x="{x+35}" y="508" class="sans" font-size="21" fill="{WHITE}">{line2}</text>
        """)
        if i < 2:
            ax = x + 420
            blocks.append(f'<path d="M {ax} 407 L {ax+52} 407" stroke="{MUTED}" stroke-width="3"/><path d="M {ax+43} 398 L {ax+54} 407 L {ax+43} 416" fill="none" stroke="{MUTED}" stroke-width="3"/>')
    return frame(1600, 900, f"""
      <text x="100" y="80" class="mono caps" font-size="19" fill="{ACCENT}">SANITIZED CASE / OPTIONS PAPER TRADING</text>
      <text x="100" y="165" class="sans" font-size="62" font-weight="750" fill="{WHITE}">productive disagreement changes the artifact.</text>
      <text x="100" y="215" class="sans" font-size="24" fill="{MUTED}">no live capital. no strategy disclosed. verification process only.</text>
      {''.join(blocks)}
      <rect x="100" y="605" width="1400" height="135" rx="22" fill="{PANEL_2}" stroke="{GRID}" stroke-width="2"/>
      <text x="170" y="662" class="mono" font-size="34" font-weight="750" fill="{WHITE}">186</text>
      <text x="170" y="702" class="sans" font-size="18" fill="{MUTED}">passing tests</text>
      <text x="500" y="662" class="mono" font-size="34" font-weight="750" fill="{WHITE}">42</text>
      <text x="500" y="702" class="sans" font-size="18" fill="{MUTED}">passing subtests</text>
      <text x="830" y="662" class="mono" font-size="34" font-weight="750" fill="{WHITE}">20</text>
      <text x="830" y="702" class="sans" font-size="18" fill="{MUTED}">forced races</text>
      <text x="1160" y="662" class="mono" font-size="34" font-weight="750" fill="{WHITE}">1</text>
      <text x="1160" y="702" class="sans" font-size="18" fill="{MUTED}">natural PAPER run</text>
      <text x="100" y="815" class="sans" font-size="20" fill="{MUTED}">private receipts reported; raw artifacts withheld. no live-money or profitability claim.</text>
      <text x="1500" y="815" text-anchor="end" class="mono caps" font-size="17" fill="{ACCENT}">RED CAN BE A VERIFIED RESULT.</text>
    """)


def social_card() -> str:
    bars = [("V0", "VIBES", "#69757D"), ("V1", "GROUNDED", "#6896A8"), ("V2", "TESTED", CYAN), ("V3", "ADVERSARIAL", "#59E7C2"), ("V4", "OPERATIONAL", ACCENT)]
    elements = []
    for i, (level, name, color) in enumerate(bars):
        x = 80 + i * 225
        elements.append(f"""
          <rect x="{x}" y="445" width="196" height="78" rx="14" fill="{PANEL}" stroke="{color}" stroke-width="2"/>
          <text x="{x+20}" y="478" class="mono" font-size="18" font-weight="700" fill="{color}">{level}</text>
          <text x="{x+20}" y="507" class="sans caps" font-size="14" font-weight="700" fill="{WHITE}">{name}</text>
        """)
    return frame(1280, 640, f"""
      <circle cx="1130" cy="115" r="190" fill="{ACCENT}" opacity="0.08" filter="url(#glow)"/>
      <text x="80" y="82" class="mono caps" font-size="17" fill="{ACCENT}">OPEN-SOURCE AGENT SKILL</text>
      <text x="80" y="190" class="sans" font-size="78" font-weight="800" fill="{WHITE}">vibes to verified</text>
      <text x="80" y="260" class="sans" font-size="34" fill="{MUTED}">make your agents prove it.</text>
      <rect x="80" y="320" width="1120" height="3" fill="url(#accentLine)"/>
      <text x="80" y="382" class="sans" font-size="23" fill="{WHITE}">keep the speed. add the proof.</text>
      {''.join(elements)}
      <text x="80" y="588" class="mono" font-size="18" fill="{MUTED}">INSTALL • FORK • VERIFY</text>
      <text x="1200" y="588" text-anchor="end" class="mono" font-size="18" fill="{ACCENT}">v0.1</text>
    """)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assets = {
        "v2v-scale.svg": v2v_scale(),
        "v2v-workflow.svg": workflow(),
        "paper-trading-receipt.svg": receipt(),
        "github-social-card.svg": social_card(),
    }
    for name, content in assets.items():
        path = OUT / name
        normalized = "\n".join(line.rstrip() for line in content.splitlines()).strip() + "\n"
        path.write_text(normalized, encoding="utf-8")
        print(f"wrote {path} {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
