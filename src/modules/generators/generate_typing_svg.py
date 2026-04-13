from pathlib import Path
import argparse
import html

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 80" width="{width}" height="90">
    <defs>
        <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="2" dy="3" stdDeviation="2" flood-color="#000000" flood-opacity="0.8"/>
        </filter>
        <clipPath id="typing-mask">
            <rect x="0" y="0" width="0" height="90" class="mask-anim"/>
        </clipPath>
    </defs>

    <style>
        .code {{
            font-family: {font_family};
            font-size: {font_size}px;
            font-weight: 700;
            fill: {text_color};
            stroke: #000000;
            stroke-width: 2px;
            stroke-linejoin: round;
            filter: url(#shadow);
        }}
        .mask-anim {{
            animation: typing {duration}s steps({steps}, end) forwards;
        }}
        .cursor {{
            animation: blink 1s step-end infinite;
        }}
        @keyframes typing {{
            from {{ width: 0; }}
            to {{ width: {width}px; }}
        }}
        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0; }}
        }}
    </style>

    <g clip-path="url(#typing-mask)">
        <text x="10" y="60" class="code">{text}<tspan class="cursor">_</tspan></text>
    </g>
</svg>
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--text-color", default="#a04b4b")
    parser.add_argument("--font-size", type=int, default=75)
    parser.add_argument("--font-family", default="'Courier New', Consolas, monospace")
    parser.add_argument("--width", type=int, default=850)
    parser.add_argument("--duration", type=float, default=3.5)
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--output", default="typing.svg")
    args = parser.parse_args()

    safe_text = html.escape(args.text)

    svg = TEMPLATE.format(
        text=safe_text,
        text_color=args.text_color,
        font_size=args.font_size,
        font_family=args.font_family,
        width=args.width,
        duration=args.duration,
        steps=args.steps,
    )

    Path(args.output).write_text(svg, encoding="utf-8")
    print(f"Generated {args.output}")

if __name__ == "__main__":
    main()