# readme-ux-kit
Build beautiful, animated, and structured GitHub READMEs


# SVG - Divider

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 20" width="800" height="20">
  <line x1="0" y1="10" x2="800" y2="10" stroke="#334155" stroke-width="2"/>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 30" width="800" height="30">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <line x1="0" y1="15" x2="360" y2="15" stroke="#475569" stroke-width="2"/>
  <line x1="440" y1="15" x2="800" y2="15" stroke="#475569" stroke-width="2"/>
  <circle cx="400" cy="15" r="5" fill="#38bdf8" filter="url(#glow)"/>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 24" width="800" height="24">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <line x1="0" y1="12" x2="800" y2="12" stroke="#0f172a" stroke-width="6"/>
  <line x1="0" y1="12" x2="800" y2="12" stroke="#a855f7" stroke-width="2" filter="url(#glow)">
    <animate attributeName="stroke-opacity" values="0.35;1;0.35" dur="2s" repeatCount="indefinite"/>
  </line>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 24" width="800" height="24">
  <line x1="0" y1="12" x2="800" y2="12" stroke="#22c55e" stroke-width="2" stroke-dasharray="8 8"/>
  <text x="400" y="17" text-anchor="middle" font-family="Courier New, monospace" font-size="12" fill="#22c55e">
    //////////////
  </text>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 30" width="800" height="30">
  <line x1="0" y1="15" x2="380" y2="15" stroke="#64748b" stroke-width="2"/>
  <line x1="420" y1="15" x2="800" y2="15" stroke="#64748b" stroke-width="2"/>
  <polygon points="400,8 407,15 400,22 393,15" fill="#f43f5e"/>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 40" width="800" height="40">
  <line x1="80" y1="20" x2="260" y2="20" stroke="#334155" stroke-width="2"/>
  <line x1="540" y1="20" x2="720" y2="20" stroke="#334155" stroke-width="2"/>

  <line x1="260" y1="20" x2="340" y2="10" stroke="#38bdf8" stroke-width="2"/>
  <line x1="260" y1="20" x2="340" y2="30" stroke="#38bdf8" stroke-width="2"/>
  <line x1="460" y1="20" x2="340" y2="10" stroke="#38bdf8" stroke-width="2"/>
  <line x1="460" y1="20" x2="340" y2="30" stroke="#38bdf8" stroke-width="2"/>

  <line x1="340" y1="10" x2="400" y2="20" stroke="#38bdf8" stroke-width="2"/>
  <line x1="340" y1="30" x2="400" y2="20" stroke="#38bdf8" stroke-width="2"/>
  <line x1="400" y1="20" x2="460" y2="20" stroke="#38bdf8" stroke-width="2"/>

  <circle cx="260" cy="20" r="4" fill="#94a3b8"/>
  <circle cx="340" cy="10" r="4" fill="#94a3b8"/>
  <circle cx="340" cy="30" r="4" fill="#94a3b8"/>
  <circle cx="400" cy="20" r="5" fill="#a855f7"/>
  <circle cx="460" cy="20" r="4" fill="#94a3b8"/>
</svg>



<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 40" width="800" height="40">
  <path d="M0 20 Q 50 5, 100 20 T 200 20 T 300 20 T 400 20 T 500 20 T 600 20 T 700 20 T 800 20"
        fill="none"
        stroke="#06b6d4"
        stroke-width="3"/>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 28" width="800" height="28">
  <defs>
    <linearGradient id="scan" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="45%" stop-color="#0f172a"/>
      <stop offset="50%" stop-color="#22d3ee"/>
      <stop offset="55%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#0f172a"/>
      <animateTransform attributeName="gradientTransform" type="translate" from="-800 0" to="800 0" dur="2.5s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>

  <rect x="0" y="12" width="800" height="4" fill="#1e293b"/>
  <rect x="0" y="11" width="800" height="6" fill="url(#scan)"/>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 36" width="800" height="36">
  <line x1="0" y1="18" x2="300" y2="18" stroke="#475569" stroke-width="2"/>
  <line x1="500" y1="18" x2="800" y2="18" stroke="#475569" stroke-width="2"/>

  <polygon points="340,18 355,8 375,8 390,18 375,28 355,28" fill="none" stroke="#22c55e" stroke-width="2"/>
  <polygon points="410,18 425,8 445,8 460,18 445,28 425,28" fill="none" stroke="#22c55e" stroke-width="2"/>

  <line x1="390" y1="18" x2="410" y2="18" stroke="#22c55e" stroke-width="2"/>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 30" width="800" height="30">
  <rect x="0" y="13" width="800" height="4" fill="#1e293b"/>

  <rect x="120" y="11" width="80" height="8" fill="#06b6d4">
    <animate attributeName="x" values="120;140;120" dur="1.6s" repeatCount="indefinite"/>
  </rect>

  <rect x="350" y="11" width="60" height="8" fill="#a855f7">
    <animate attributeName="x" values="350;330;350" dur="1.2s" repeatCount="indefinite"/>
  </rect>

  <rect x="560" y="11" width="100" height="8" fill="#f43f5e">
    <animate attributeName="x" values="560;580;560" dur="1.8s" repeatCount="indefinite"/>
  </rect>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 30" width="800" height="30">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f5ff"/>
      <stop offset="50%" stop-color="#a855f7"/>
      <stop offset="100%" stop-color="#00f5ff"/>
      <animateTransform attributeName="gradientTransform" type="translate"
        from="-800 0" to="800 0" dur="3s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>

  <rect x="0" y="14" width="800" height="3" fill="url(#grad)"/>
</svg>



<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 40" width="800" height="40">
  <line x1="0" y1="20" x2="800" y2="20" stroke="#1e293b" stroke-width="2"/>

  <g fill="#22d3ee">
    <circle cx="100" cy="20" r="4">
      <animate attributeName="r" values="4;8;4" dur="1.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="300" cy="20" r="4">
      <animate attributeName="r" values="4;8;4" dur="1.5s" begin="0.3s" repeatCount="indefinite"/>
    </circle>
    <circle cx="500" cy="20" r="4">
      <animate attributeName="r" values="4;8;4" dur="1.5s" begin="0.6s" repeatCount="indefinite"/>
    </circle>
    <circle cx="700" cy="20" r="4">
      <animate attributeName="r" values="4;8;4" dur="1.5s" begin="0.9s" repeatCount="indefinite"/>
    </circle>
  </g>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 30" width="800" height="30">
  <line x1="0" y1="15" x2="800" y2="15" stroke="#1e293b" stroke-width="3"/>

  <circle r="5" fill="#38bdf8">
    <animateMotion dur="2s" repeatCount="indefinite"
      path="M0 15 L800 15"/>
  </circle>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 40" width="800" height="40">
  <rect width="800" height="40" fill="#020617"/>

  <g stroke="#22c55e" stroke-width="2">
    <line x1="100" y1="0" x2="100" y2="40">
      <animate attributeName="y1" values="-40;40" dur="1.5s" repeatCount="indefinite"/>
      <animate attributeName="y2" values="0;80" dur="1.5s" repeatCount="indefinite"/>
    </line>
    <line x1="300" y1="0" x2="300" y2="40">
      <animate attributeName="y1" values="-40;40" dur="2s" repeatCount="indefinite"/>
      <animate attributeName="y2" values="0;80" dur="2s" repeatCount="indefinite"/>
    </line>
  </g>
</svg>



<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 40" width="800" height="40">
  <line x1="0" y1="20" x2="800" y2="20" stroke="#1e293b" stroke-width="2"/>

  <circle cx="400" cy="20" r="5" fill="#f43f5e">
    <animate attributeName="r" values="5;20;5" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;0;1" dur="2s" repeatCount="indefinite"/>
  </circle>
</svg>



<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 30" width="800" height="30">
  <rect x="0" y="14" width="800" height="2" fill="#94a3b8"/>

  <rect x="0" y="12" width="800" height="2" fill="#f43f5e">
    <animate attributeName="x" values="0;5;-5;0" dur="0.2s" repeatCount="indefinite"/>
  </rect>

  <rect x="0" y="16" width="800" height="2" fill="#22d3ee">
    <animate attributeName="x" values="0;-5;5;0" dur="0.2s" repeatCount="indefinite"/>
  </rect>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 50" width="800" height="50">
  <line x1="0" y1="25" x2="800" y2="25" stroke="#1e293b" stroke-width="2"/>

  <g transform="translate(400,25)">
    <polygon points="0,-10 10,0 0,10 -10,0" fill="#a855f7">
      <animateTransform attributeName="transform" type="rotate"
        from="0" to="360" dur="2s" repeatCount="indefinite"/>
    </polygon>
  </g>
</svg>



<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 50" width="800" height="50">
  <line x1="0" y1="25" x2="800" y2="25" stroke="#1e293b" stroke-width="2"/>

  <line x1="400" y1="25" x2="450" y2="25" stroke="#22d3ee" stroke-width="3">
    <animateTransform attributeName="transform" type="rotate"
      from="0 400 25" to="360 400 25" dur="2s" repeatCount="indefinite"/>
  </line>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 40" width="800" height="40">
  <path d="M0 20 Q 100 5, 200 20 T 400 20 T 600 20 T 800 20"
        fill="none" stroke="#06b6d4" stroke-width="2">
    <animate attributeName="d"
      values="
      M0 20 Q 100 5, 200 20 T 400 20 T 600 20 T 800 20;
      M0 20 Q 100 35, 200 20 T 400 20 T 600 20 T 800 20;
      M0 20 Q 100 5, 200 20 T 400 20 T 600 20 T 800 20"
      dur="2s" repeatCount="indefinite"/>
  </path>
</svg>



<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 30" width="800" height="30">
  <rect x="0" y="12" width="800" height="6" fill="#1e293b"/>

  <rect x="0" y="12" height="6" fill="#22c55e">
    <animate attributeName="width" values="0;800;0" dur="3s" repeatCount="indefinite"/>
  </rect>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 60" width="800" height="60">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <line x1="0" y1="30" x2="330" y2="30" stroke="#1e293b" stroke-width="2"/>
  <line x1="470" y1="30" x2="800" y2="30" stroke="#1e293b" stroke-width="2"/>

  <g transform="translate(400,30)" filter="url(#glow)">
    <circle r="16" fill="none" stroke="#22d3ee" stroke-width="2"/>
    <circle r="8" fill="#22d3ee" opacity="0.9">
      <animate attributeName="r" values="8;10;8" dur="1.8s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.9;0.5;0.9" dur="1.8s" repeatCount="indefinite"/>
    </circle>
    <g>
      <line x1="0" y1="-22" x2="0" y2="-12" stroke="#67e8f9" stroke-width="2"/>
      <line x1="0" y1="12" x2="0" y2="22" stroke="#67e8f9" stroke-width="2"/>
      <line x1="-22" y1="0" x2="-12" y2="0" stroke="#67e8f9" stroke-width="2"/>
      <line x1="12" y1="0" x2="22" y2="0" stroke="#67e8f9" stroke-width="2"/>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="6s" repeatCount="indefinite"/>
    </g>
  </g>
</svg>





<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 40" width="800" height="40">
  <rect width="800" height="40" fill="transparent"/>
  <line x1="0" y1="20" x2="800" y2="20" stroke="#0f172a" stroke-width="8"/>

  <g>
    <rect x="0" y="17" width="120" height="6" fill="#38bdf8">
      <animate attributeName="x" values="-140;820" dur="3.2s" repeatCount="indefinite"/>
    </rect>
    <rect x="0" y="17" width="60" height="6" fill="#a855f7">
      <animate attributeName="x" values="-80;820" dur="2.4s" begin="0.4s" repeatCount="indefinite"/>
    </rect>
    <rect x="0" y="17" width="30" height="6" fill="#f43f5e">
      <animate attributeName="x" values="-40;820" dur="1.7s" begin="0.8s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 60" width="800" height="60">
  <g stroke="#334155" stroke-width="1.5" fill="#0ea5e9">
    <line x1="80" y1="30" x2="200" y2="15"/>
    <line x1="80" y1="30" x2="200" y2="45"/>
    <line x1="200" y1="15" x2="320" y2="30"/>
    <line x1="200" y1="45" x2="320" y2="30"/>

    <line x1="480" y1="30" x2="600" y2="15"/>
    <line x1="480" y1="30" x2="600" y2="45"/>
    <line x1="600" y1="15" x2="720" y2="30"/>
    <line x1="600" y1="45" x2="720" y2="30"/>

    <circle cx="80" cy="30" r="4"/>
    <circle cx="200" cy="15" r="4"/>
    <circle cx="200" cy="45" r="4"/>
    <circle cx="320" cy="30" r="4"/>
    <circle cx="480" cy="30" r="4"/>
    <circle cx="600" cy="15" r="4"/>
    <circle cx="600" cy="45" r="4"/>
    <circle cx="720" cy="30" r="4"/>
  </g>

  <circle cx="80" cy="30" r="5" fill="#22d3ee">
    <animateMotion dur="2.8s" repeatCount="indefinite" path="M80 30 L200 15 L320 30 L480 30 L600 45 L720 30"/>
  </circle>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 70" width="800" height="70">
  <line x1="0" y1="35" x2="800" y2="35" stroke="#1e293b" stroke-width="2"/>

  <g transform="translate(400,35)">
    <circle r="22" fill="#0f172a" stroke="#475569" stroke-width="2"/>
    <circle r="22" fill="#facc15" opacity="0.9">
      <animate attributeName="cx" values="-10;10;-10" dur="3s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.35;0.9;0.35" dur="3s" repeatCount="indefinite"/>
    </circle>
    <circle r="22" fill="#020617"/>
  </g>
</svg>



<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 90" width="800" height="90">
  <defs>
    <filter id="gateglow">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <line x1="0" y1="45" x2="290" y2="45" stroke="#334155" stroke-width="2"/>
  <line x1="510" y1="45" x2="800" y2="45" stroke="#334155" stroke-width="2"/>

  <g transform="translate(400,45)" filter="url(#gateglow)">
    <ellipse rx="42" ry="22" fill="none" stroke="#22d3ee" stroke-width="2"/>
    <ellipse rx="24" ry="42" fill="none" stroke="#a855f7" stroke-width="2"/>
    <circle r="6" fill="#f8fafc">
      <animate attributeName="r" values="6;10;6" dur="1.8s" repeatCount="indefinite"/>
    </circle>
  </g>
</svg>



<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 60" width="800" height="60">
  <line x1="0" y1="30" x2="800" y2="30" stroke="#1e293b" stroke-width="2"/>

  <g transform="translate(250,30)" stroke="#38bdf8" stroke-width="2" fill="none">
    <path d="M-10 12 L-10 -12 L10 -12 L10 0 L-10 0"/>
    <animate attributeName="opacity" values="0.3;1;0.3" dur="1.8s" repeatCount="indefinite"/>
  </g>

  <g transform="translate(400,30)" stroke="#a855f7" stroke-width="2" fill="none">
    <path d="M0 -14 L0 14 M-10 -4 L0 -14 L10 -4"/>
    <animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/>
  </g>

  <g transform="translate(550,30)" stroke="#f43f5e" stroke-width="2" fill="none">
    <path d="M-10 -12 L10 12 M10 -12 L-10 12"/>
    <animate attributeName="opacity" values="0.3;1;0.3" dur="1.8s" begin="0.4s" repeatCount="indefinite"/>
  </g>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 80" width="800" height="80">
  <defs>
    <radialGradient id="portal" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="30%" stop-color="#22d3ee"/>
      <stop offset="65%" stop-color="#7c3aed"/>
      <stop offset="100%" stop-color="#020617"/>
    </radialGradient>
  </defs>

  <line x1="0" y1="40" x2="320" y2="40" stroke="#1e293b" stroke-width="2"/>
  <line x1="480" y1="40" x2="800" y2="40" stroke="#1e293b" stroke-width="2"/>

  <g transform="translate(400,40)">
    <circle r="10" fill="url(#portal)">
      <animate attributeName="r" values="10;26;10" dur="2.4s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;0.55;1" dur="2.4s" repeatCount="indefinite"/>
    </circle>
    <circle r="3" fill="#ffffff"/>
  </g>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 80" width="800" height="80">
  <line x1="0" y1="40" x2="320" y2="40" stroke="#1e293b" stroke-width="2"/>
  <line x1="480" y1="40" x2="800" y2="40" stroke="#1e293b" stroke-width="2"/>

  <g transform="translate(400,40)">
    <g>
      <circle r="28" fill="none" stroke="#818cf8" stroke-width="2" stroke-dasharray="6 6"/>
      <animateTransform
        attributeName="transform"
        type="rotate"
        from="0"
        to="360"
        dur="8s"
        repeatCount="indefinite"/>
    </g>

    <g>
      <circle r="18" fill="none" stroke="#22d3ee" stroke-width="2" stroke-dasharray="2 5"/>
      <animateTransform
        attributeName="transform"
        type="rotate"
        from="360"
        to="0"
        dur="5s"
        repeatCount="indefinite"/>
    </g>

    <polygon points="0,-8 8,0 0,8 -8,0" fill="#f8fafc">
      <animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/>
    </polygon>
  </g>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 70" width="800" height="70">
  <defs>
    <linearGradient id="serp1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#22d3ee"/>
      <stop offset="100%" stop-color="#a855f7"/>
    </linearGradient>
    <linearGradient id="serp2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#a855f7"/>
      <stop offset="100%" stop-color="#22d3ee"/>
    </linearGradient>
  </defs>

  <path id="wave1"
        d="M0 35 C100 10, 200 10, 300 35 S500 60, 800 35"
        fill="none"
        stroke="url(#serp1)"
        stroke-width="3"
        stroke-linecap="round"
        stroke-dasharray="12 10">
    <animate attributeName="stroke-dashoffset" from="0" to="-44" dur="2.5s" repeatCount="indefinite"/>
  </path>

  <path id="wave2"
        d="M0 35 C100 60, 200 60, 300 35 S500 10, 800 35"
        fill="none"
        stroke="url(#serp2)"
        stroke-width="3"
        stroke-linecap="round"
        stroke-dasharray="12 10"
        opacity="0.8">
    <animate attributeName="stroke-dashoffset" from="0" to="44" dur="2.5s" repeatCount="indefinite"/>
  </path>

  <circle r="4" fill="#22d3ee">
    <animateMotion dur="3s" repeatCount="indefinite" rotate="auto">
      <mpath href="#wave1"/>
    </animateMotion>
  </circle>

  <circle r="4" fill="#a855f7">
    <animateMotion dur="3s" repeatCount="indefinite" rotate="auto">
      <mpath href="#wave2"/>
    </animateMotion>
  </circle>
</svg>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 70" width="800" height="70">
  <defs>
    <filter id="pinkglow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <line x1="0" y1="35" x2="300" y2="35" stroke="#334155" stroke-width="2"/>
  <line x1="500" y1="35" x2="800" y2="35" stroke="#334155" stroke-width="2"/>

  <g transform="translate(400,35)" filter="url(#pinkglow)">
    <g stroke="#f472b6" fill="none" stroke-width="2">
      <polygon points="0,-22 19,-11 19,11 0,22 -19,11 -19,-11"/>
      <polygon points="0,-10 9,-5 9,5 0,10 -9,5 -9,-5"/>
      <line x1="-32" y1="0" x2="-19" y2="0"/>
      <line x1="19" y1="0" x2="32" y2="0"/>
      <line x1="0" y1="-35" x2="0" y2="-22"/>
      <line x1="0" y1="22" x2="0" y2="35"/>

      <animateTransform
        attributeName="transform"
        type="rotate"
        from="0"
        to="360"
        dur="8s"
        repeatCount="indefinite"/>
    </g>
  </g>
</svg>

