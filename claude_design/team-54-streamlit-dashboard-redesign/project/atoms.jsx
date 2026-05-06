/* global React */
// Reusable atoms — icons, sparklines, mini bars, etc.

const { useMemo } = React;

const Icon = ({ name, size = 14, color = "currentColor", strokeWidth = 1.6 }) => {
  const paths = {
    chevron:   <polyline points="6 9 12 15 18 9" />,
    chevR:     <polyline points="9 6 15 12 9 18" />,
    search:    <><circle cx="11" cy="11" r="7" /><line x1="21" y1="21" x2="16" y2="16" /></>,
    download:  <><path d="M12 3v12" /><polyline points="7 10 12 15 17 10" /><path d="M5 21h14" /></>,
    filter:    <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />,
    info:      <><circle cx="12" cy="12" r="9" /><line x1="12" y1="11" x2="12" y2="16" /><line x1="12" y1="8" x2="12" y2="8" /></>,
    sort:      <><polyline points="8 6 8 18" /><polyline points="5 9 8 6 11 9" /><polyline points="16 6 16 18" /><polyline points="13 15 16 18 19 15" /></>,
    grid:      <><rect x="3" y="3" width="7" height="7" /><rect x="14" y="3" width="7" height="7" /><rect x="3" y="14" width="7" height="7" /><rect x="14" y="14" width="7" height="7" /></>,
    list:      <><line x1="8" y1="6" x2="21" y2="6" /><line x1="8" y1="12" x2="21" y2="12" /><line x1="8" y1="18" x2="21" y2="18" /><circle cx="4" cy="6" r="0.5" fill={color} /><circle cx="4" cy="12" r="0.5" fill={color} /><circle cx="4" cy="18" r="0.5" fill={color} /></>,
    refresh:   <><polyline points="23 4 23 10 17 10" /><polyline points="1 20 1 14 7 14" /><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" /></>,
    close:     <><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></>,
    menu:      <><line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="18" x2="21" y2="18" /></>,
    ext:       <><path d="M14 3h7v7" /><path d="M10 14L21 3" /><path d="M21 14v6a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h6" /></>,
    spark:     <polyline points="3 17 8 11 13 14 21 5" />,
    arrowUp:   <polyline points="6 14 12 8 18 14" />,
    arrowDn:   <polyline points="6 10 12 16 18 10" />,
    flat:      <line x1="6" y1="12" x2="18" y2="12" />,
    flag:      <><path d="M4 21V4h12l-2 4 2 4H4" /></>,
    book:      <><path d="M4 4h13a2 2 0 0 1 2 2v14H6a2 2 0 0 1-2-2z" /><line x1="8" y1="8" x2="15" y2="8" /><line x1="8" y1="12" x2="15" y2="12" /></>,
    play:      <polygon points="6 4 20 12 6 20 6 4" />,
    cog:       <><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1A1.7 1.7 0 0 0 4.6 9a1.7 1.7 0 0 0-.3-1.8l-.1-.1A2 2 0 1 1 7 4.3l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z" /></>,
    user:      <><circle cx="12" cy="8" r="4" /><path d="M4 21a8 8 0 0 1 16 0" /></>,
  };
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={{ flex: '0 0 auto' }}>
      {paths[name]}
    </svg>
  );
};

// Sparkline — pass array of numbers, 0..1 normalised internally
const Sparkline = ({ data, color = '#29363c', fill = 'rgba(41,54,60,0.08)', width = 100, height = 22 }) => {
  const d = data;
  const min = Math.min(...d), max = Math.max(...d);
  const range = max - min || 1;
  const stepX = width / (d.length - 1);
  const points = d.map((v, i) => [i * stepX, height - ((v - min) / range) * (height - 4) - 2]);
  const linePath = points.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' ');
  const fillPath = `${linePath} L${width} ${height} L0 ${height} Z`;
  return (
    <svg className="spark" viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="none">
      <path d={fillPath} fill={fill} stroke="none" />
      <path d={linePath} fill="none" stroke={color} strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx={points[points.length - 1][0]} cy={points[points.length - 1][1]} r="1.6" fill={color} />
    </svg>
  );
};

// Mini horizontal bar with label + value
const MiniBar = ({ value, max = 100, tone = 'teal', width = 56 }) => (
  <span className={`bar ${tone}`} style={{ width }}>
    <span style={{ width: `${Math.max(2, Math.min(100, (value / max) * 100))}%` }} />
  </span>
);

// Tag for action category
const ActionTag = ({ value }) => (
  <span className={`tag ${value.toLowerCase()}`}>{value}</span>
);

// Delta arrow
const Delta = ({ value, suffix = '', invert = false }) => {
  const isUp = value > 0;
  const isFlat = Math.abs(value) < 0.05;
  const tone = isFlat ? 'flat' : (isUp ? (invert ? 'up' : 'down') : (invert ? 'down' : 'up'));
  const arrow = isFlat ? 'flat' : isUp ? 'arrowUp' : 'arrowDn';
  return (
    <span className={`delta ${tone}`} style={{ display: 'inline-flex', alignItems: 'center', gap: 2 }}>
      <Icon name={arrow} size={11} strokeWidth={2} />
      {Math.abs(value).toFixed(1)}{suffix}
    </span>
  );
};

const fmtN = (n) => n >= 1000 ? n.toLocaleString() : String(n);
const fmt$ = (n) => `$${Math.round(n).toLocaleString()}`;
const fmtPct = (n) => `${n.toFixed(1)}%`;

Object.assign(window, { Icon, Sparkline, MiniBar, ActionTag, Delta, fmtN, fmt$, fmtPct });
