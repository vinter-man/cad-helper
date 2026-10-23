import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import {loadFont as loadMono} from "@remotion/google-fonts/JetBrainsMono";
import {loadFont as loadSans} from "@remotion/google-fonts/Inter";
import {FIRE_PIT, LINES, Line, PHASES, V1_AT, V2_AT} from "./script";

const {fontFamily: mono} = loadMono("normal", {weights: ["400", "700"], subsets: ["latin"]});
const {fontFamily: sans} = loadSans("normal", {weights: ["400", "600", "800"], subsets: ["latin"]});

const C = {
  page: "#0d1117",
  panel: "#161b22",
  border: "#30363d",
  text: "#e6edf3",
  dim: "#8b949e",
  accent: "#d97757", // assistant bullet
  user: "#79c0ff",
  ok: "#3fb950",
  err: "#f85149",
  cad: "#212830", // AutoCAD model space
};

const clamp = {extrapolateLeft: "clamp", extrapolateRight: "clamp"} as const;

// ─── Terminal ────────────────────────────────────────────────────────────────

const TerminalLine: React.FC<{line: Line; frame: number}> = ({line, frame}) => {
  const local = frame - line.at;
  const opacity = interpolate(local, [0, 4], [0, 1], clamp);
  const base: React.CSSProperties = {opacity, fontSize: 17, lineHeight: 1.45, whiteSpace: "pre-wrap"};

  if (line.kind === "user") {
    const shown = Math.floor(interpolate(local, [0, line.typeFor], [0, line.text.length], clamp));
    const typing = local < line.typeFor + 6;
    return (
      <div style={{...base, opacity: 1, margin: "10px 0 6px", padding: "8px 12px",
        background: "#1f2630", borderLeft: `3px solid ${C.user}`, borderRadius: 4, color: C.text}}>
        <span style={{color: C.user, fontWeight: 700}}>&gt; </span>
        {line.text.slice(0, shown)}
        {typing && Math.floor(frame / 8) % 2 === 0 ? <span style={{color: C.user}}>▍</span> : null}
      </div>
    );
  }
  if (line.kind === "claude") {
    return (
      <div style={{...base, color: C.text, display: "flex", gap: 10, marginTop: 6}}>
        <span style={{color: C.accent}}>⏺</span>
        <span style={{fontFamily: sans, fontSize: 18}}>{line.text}</span>
      </div>
    );
  }
  if (line.kind === "tool") {
    return (
      <div style={{...base, color: C.text, display: "flex", gap: 10, marginTop: 6}}>
        <span style={{color: C.ok}}>⏺</span>
        <span>
          <b>Bash</b>
          <span style={{color: C.dim}}>(</span>
          {line.text}
          <span style={{color: C.dim}}>)</span>
        </span>
      </div>
    );
  }
  const color = line.kind === "ok" ? C.ok : line.kind === "err" ? C.err : C.dim;
  return (
    <div style={{...base, color, paddingLeft: 26, fontWeight: line.kind === "out" ? 400 : 700}}>
      <span style={{color: C.dim}}>⎿ </span>
      {line.text}
    </div>
  );
};

const Terminal: React.FC<{frame: number}> = ({frame}) => {
  const phase = [...PHASES].reverse().find((p) => frame >= p.from)!.label;
  return (
    <div style={{flex: 1.55, display: "flex", flexDirection: "column", background: C.panel,
      border: `1px solid ${C.border}`, borderRadius: 12, overflow: "hidden"}}>
      <div style={{display: "flex", alignItems: "center", gap: 8, padding: "10px 14px",
        borderBottom: `1px solid ${C.border}`, fontFamily: sans, fontSize: 14, color: C.dim}}>
        {["#ff5f57", "#febc2e", "#28c840"].map((c) => (
          <div key={c} style={{width: 11, height: 11, borderRadius: 6, background: c}} />
        ))}
        <span style={{marginLeft: 10}}>claude · ~/cad-helper</span>
        <div style={{marginLeft: "auto", display: "flex", gap: 6}}>
          {["brief", "plan", "build", "review"].map((p) => (
            <span key={p} style={{padding: "2px 9px", borderRadius: 10, fontSize: 13,
              background: p === phase ? C.accent : "transparent",
              color: p === phase ? "#fff" : C.dim,
              border: `1px solid ${p === phase ? C.accent : C.border}`}}>
              {p}
            </span>
          ))}
        </div>
      </div>
      <div style={{flex: 1, display: "flex", flexDirection: "column", justifyContent: "flex-end",
        padding: "0 18px 16px", fontFamily: mono, overflow: "hidden"}}>
        {LINES.filter((l) => frame >= l.at).map((l, i) => (
          <TerminalLine key={i} line={l} frame={frame} />
        ))}
      </div>
    </div>
  );
};

// ─── Drawing viewport ────────────────────────────────────────────────────────

const Viewport: React.FC<{frame: number}> = ({frame}) => {
  const {fps} = useVideoConfig();
  const reveal = interpolate(frame - V1_AT, [0, 36], [100, 0], {...clamp, easing: Easing.out(Easing.cubic)});
  const v2 = interpolate(frame - V2_AT, [0, 18], [0, 1], clamp);
  const ring = spring({frame: frame - V2_AT - 14, fps, config: {damping: 12}});
  const ringFade = interpolate(frame - V2_AT, [14, 30, 75, 95], [0, 1, 1, 0], clamp);
  const version = frame >= V2_AT ? "v2" : frame >= V1_AT ? "v1" : "";
  // Ease into the garden half of the plan once the first drawing is in.
  const zoom = interpolate(frame - V1_AT, [45, 110], [1, 1.32], {...clamp, easing: Easing.inOut(Easing.cubic)});

  return (
    <div style={{flex: 1, display: "flex", flexDirection: "column", background: C.cad,
      border: `1px solid ${C.border}`, borderRadius: 12, overflow: "hidden"}}>
      <div style={{display: "flex", padding: "10px 14px", borderBottom: `1px solid ${C.border}`,
        fontFamily: sans, fontSize: 14, color: C.dim, background: C.panel}}>
        <span>sofia_garden.dxf</span>
        {version && (
          <span style={{marginLeft: "auto", color: version === "v2" ? C.ok : C.text, fontWeight: 600}}>
            {version}
          </span>
        )}
      </div>
      <div style={{flex: 1, position: "relative", display: "flex", alignItems: "center",
        justifyContent: "center", padding: 10, overflow: "hidden"}}>
        {frame < V1_AT ? (
          <div style={{fontFamily: sans, color: "#4b5563", fontSize: 16}}>no drawing yet</div>
        ) : (
          <div style={{position: "relative", height: "100%", aspectRatio: "1600 / 2049",
            transform: `scale(${zoom})`, transformOrigin: "45% 78%"}}>
            <Img src={staticFile("v1.png")}
              style={{position: "absolute", inset: 0, width: "100%", height: "100%",
                clipPath: `inset(${reveal}% 0 0 0)`}} />
            <Img src={staticFile("v2.png")}
              style={{position: "absolute", inset: 0, width: "100%", height: "100%", opacity: v2}} />
            <div style={{position: "absolute", left: `${FIRE_PIT.x * 100}%`, top: `${FIRE_PIT.y * 100}%`,
              width: 110, height: 110, marginLeft: -55, marginTop: -55, borderRadius: "50%",
              border: `3px solid ${C.ok}`, opacity: ringFade, transform: `scale(${0.6 + ring * 0.4})`}} />
          </div>
        )}
      </div>
    </div>
  );
};

export const Demo: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: C.page, padding: 22, flexDirection: "row", gap: 18}}>
      <Terminal frame={frame} />
      <Viewport frame={frame} />
    </AbsoluteFill>
  );
};
