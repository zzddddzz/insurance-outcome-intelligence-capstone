/* global React, Icon, Sparkline, MiniBar, ActionTag, Delta, fmtN, fmt$, fmtPct */
/* global SEGMENTS, ACTIONS */

const { useState: useStateMid, useMemo: useMemoMid } = React;

// ─────────────────────────────────────────────────────────────
// Decision Quadrant — claim pressure × lapse risk
// bubbles sized by N, colored by action
// ─────────────────────────────────────────────────────────────
const Quadrant = ({ rows, selectedId, onSelect }) => {
  const maxLapse = 28;       // y axis (top = high)
  const maxClaim = 16000;    // x axis (right = high)
  const maxN = Math.max(...rows.map(r => r.n));

  return (
    <div className="card">
      <div className="card-head">
        <div className="title">
          <h3 className="h-card">Decision quadrant</h3>
          <span className="t-meta">claim pressure × lapse risk · bubble size = members</span>
        </div>
        <div className="actions">
          <span className="t-meta">color =</span>
          {ACTIONS.map(a => <span key={a} className={`tag ${a.toLowerCase()}`}>{a}</span>)}
        </div>
      </div>
      <div className="quad-wrap">
        <div className="quad" style={{ marginLeft: 22, marginBottom: 18 }}>
          <span className="quad-quadlabel" style={{ top: 8, left: 12 }}>Low pressure · high lapse</span>
          <span className="quad-quadlabel" style={{ top: 8, right: 12, color: 'var(--red-700)' }}>High pressure · high lapse</span>
          <span className="quad-quadlabel" style={{ bottom: 8, left: 12 }}>Low pressure · low lapse</span>
          <span className="quad-quadlabel" style={{ bottom: 8, right: 12 }}>High pressure · low lapse</span>

          {rows.map(r => {
            const x = Math.min(99, (r.claim / maxClaim) * 100);
            const y = 100 - Math.min(99, (r.lapse / maxLapse) * 100);
            const size = 14 + (r.n / maxN) * 36;
            const isSelected = r.id === selectedId;
            return (
              <span
                key={r.id}
                className={`quad-bubble b-${r.action.toLowerCase()} ${isSelected ? 'is-selected' : ''}`}
                style={{ left: `${x}%`, top: `${y}%`, width: size, height: size }}
                title={`${r.label} · ${r.action} · ${fmtN(r.n)} members`}
                onClick={() => onSelect(r.id)}
              />
            );
          })}

          <span className="quad-axis-y">Lapse risk →</span>
          <span className="quad-axis-x">
            <span>Claim pressure $0</span>
            <span>$8k</span>
            <span>$16k+</span>
          </span>
        </div>
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────────────────────
// Ranked segment table
// ─────────────────────────────────────────────────────────────
const SortHead = ({ k, label, current, dir, onClick, num }) => (
  <th className={current === k ? 'sorted' : ''} style={num ? { textAlign: 'right' } : {}} onClick={() => onClick(k)}>
    {label}
    <span className="sort">{current === k ? (dir === 'desc' ? '▼' : '▲') : '↕'}</span>
  </th>
);

const RankedTable = ({ rows, selectedId, onSelect }) => {
  const [sortKey, setSortKey] = useStateMid('priority');
  const [dir, setDir] = useStateMid('desc');

  const sorted = useMemoMid(() => {
    const out = [...rows];
    out.sort((a, b) => (a[sortKey] - b[sortKey]) * (dir === 'desc' ? -1 : 1));
    return out;
  }, [rows, sortKey, dir]);

  const setSort = (k) => {
    if (k === sortKey) setDir(d => d === 'desc' ? 'asc' : 'desc');
    else { setSortKey(k); setDir('desc'); }
  };

  return (
    <div className="card" style={{ overflow: 'hidden' }}>
      <div className="card-head">
        <div className="title">
          <h3 className="h-card">Ranked segments</h3>
          <span className="t-meta">{rows.length} of 482 segments · sorted by {sortKey}</span>
        </div>
        <div className="actions">
          <button className="btn"><Icon name="sort" size={11} /> Sort</button>
          <button className="btn"><Icon name="download" size={11} /> Export CSV</button>
        </div>
      </div>
      <div style={{ maxHeight: 360, overflowY: 'auto' }}>
        <table className="tbl">
          <thead>
            <tr>
              <SortHead k="priority" label="#" current={sortKey} dir={dir} onClick={setSort} />
              <th style={{ width: '32%' }}>Segment</th>
              <th>Action</th>
              <SortHead k="n"        label="Members"     current={sortKey} dir={dir} onClick={setSort} num />
              <SortHead k="lapse"    label="Lapse"       current={sortKey} dir={dir} onClick={setSort} num />
              <SortHead k="claim"    label="Claim/yr"    current={sortKey} dir={dir} onClick={setSort} num />
              <SortHead k="premium"  label="Premium"     current={sortKey} dir={dir} onClick={setSort} num />
              <SortHead k="gap"      label="Gap"         current={sortKey} dir={dir} onClick={setSort} num />
              <th style={{ width: 80 }}>Util</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((r, i) => (
              <tr key={r.id} className={r.id === selectedId ? 'is-selected' : ''} onClick={() => onSelect(r.id)}>
                <td className="priority tnum">{String(i + 1).padStart(2, '0')}</td>
                <td>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                    <span style={{ color: 'var(--ink-1)', fontWeight: 500 }}>{r.label}</span>
                    <span className="t-mono" style={{ color: 'var(--ink-4)' }}>{r.id} · {r.policyType}</span>
                  </div>
                </td>
                <td><ActionTag value={r.action} /></td>
                <td className="num">{fmtN(r.n)}</td>
                <td className="num">
                  <MiniBar value={r.lapse} max={28} tone={r.lapse > 18 ? 'high' : r.lapse > 10 ? 'med' : 'low'} width={36} />
                  {r.lapse.toFixed(1)}%
                </td>
                <td className="num">{fmt$(r.claim)}</td>
                <td className="num" style={{ color: 'var(--ink-3)' }}>{fmt$(r.premium)}</td>
                <td className="num" style={{ color: r.gap > 0 ? 'var(--red-700)' : 'var(--green-700)', fontWeight: 500 }}>
                  {r.gap > 0 ? '+' : '−'}{fmt$(Math.abs(r.gap))}
                </td>
                <td className="num">
                  <MiniBar value={r.util * 100} tone="teal" width={40} />
                  {Math.round(r.util * 100)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────────────────────
// Mini charts row
// ─────────────────────────────────────────────────────────────
const StackedBar = ({ data, height = 130 }) => {
  // data = [{label, retain, reprice, monitor, review}]
  const max = Math.max(...data.map(d => d.retain + d.reprice + d.monitor + d.review));
  return (
    <svg viewBox={`0 0 ${data.length * 36 + 8} ${height + 22}`} width="100%" preserveAspectRatio="none" style={{ overflow: 'visible' }}>
      {data.map((d, i) => {
        const x = i * 36 + 4;
        const total = d.retain + d.reprice + d.monitor + d.review;
        const h = (total / max) * height;
        let y0 = height - h + 6;
        const segs = [
          { v: d.retain, c: 'var(--green-500)' },
          { v: d.monitor, c: 'var(--amber-500)' },
          { v: d.reprice, c: 'var(--red-500)' },
          { v: d.review, c: 'var(--violet-500)' },
        ];
        return (
          <g key={i}>
            {segs.map((s, j) => {
              const sh = (s.v / max) * height;
              const rect = <rect key={j} x={x} y={y0} width={26} height={sh} fill={s.c} />;
              y0 += sh;
              return rect;
            })}
            <text x={x + 13} y={height + 18} textAnchor="middle" fontSize="9.5" fill="var(--ink-4)" fontFamily="var(--font-sans)">{d.label}</text>
          </g>
        );
      })}
    </svg>
  );
};

const LapseLine = ({ height = 130 }) => {
  const series = [
    { label: '2017', mid: 6.8, any: 17.6 },
    { label: '2018', mid: 7.0, any: 17.9 },
    { label: '2019', mid: 7.1, any: 18.1 },
    { label: 'View',  mid: 11.4, any: 21.7 },
  ];
  const w = 280;
  const stepX = w / (series.length - 1);
  const pts = (key, max) => series.map((s, i) => [i * stepX, height - (s[key] / max) * (height - 12) - 6]);
  const pathFor = (arr) => arr.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' ');
  const midPts = pts('mid', 25), anyPts = pts('any', 25);
  return (
    <svg viewBox={`0 0 ${w} ${height + 22}`} width="100%" preserveAspectRatio="none" style={{ overflow: 'visible' }}>
      {[5, 10, 15, 20].map(g => {
        const y = height - (g / 25) * (height - 12) - 6;
        return <g key={g}><line x1="0" x2={w} y1={y} y2={y} stroke="var(--line-2)" strokeDasharray="2 3" /><text x={w} y={y - 2} textAnchor="end" fontSize="9" fill="var(--ink-4)">{g}%</text></g>;
      })}
      <path d={pathFor(anyPts)} fill="none" stroke="var(--amber-500)" strokeWidth="1.6" />
      <path d={pathFor(midPts)} fill="none" stroke="var(--red-500)" strokeWidth="1.6" />
      {anyPts.map((p, i) => <circle key={'a' + i} cx={p[0]} cy={p[1]} r="2" fill="var(--amber-500)" />)}
      {midPts.map((p, i) => <circle key={'m' + i} cx={p[0]} cy={p[1]} r="2" fill="var(--red-500)" />)}
      {series.map((s, i) => <text key={i} x={i * stepX} y={height + 18} textAnchor={i === 0 ? 'start' : i === series.length - 1 ? 'end' : 'middle'} fontSize="9.5" fill="var(--ink-4)">{s.label}</text>)}
      {/* book benchmark */}
      <line x1="0" x2={w} y1={height - (7.1 / 25) * (height - 12) - 6} y2={height - (7.1 / 25) * (height - 12) - 6} stroke="var(--ink-3)" strokeDasharray="3 3" />
      <text x="2" y={height - (7.1 / 25) * (height - 12) - 8} fontSize="9" fill="var(--ink-3)">book mid 7.1%</text>
    </svg>
  );
};

const PremiumGap = ({ height = 130 }) => {
  // diverging horizontal bars by product
  const data = [
    { label: 'PPO', gap: +1840 },
    { label: 'HMO', gap: -340 },
    { label: 'EPO', gap: +780 },
    { label: 'POS', gap: +210 },
  ];
  const max = 2200;
  const w = 280, midX = w * 0.55;
  return (
    <svg viewBox={`0 0 ${w} ${height + 22}`} width="100%" preserveAspectRatio="none">
      <line x1={midX} x2={midX} y1="0" y2={height} stroke="var(--line-2)" />
      {data.map((d, i) => {
        const y = i * 28 + 8;
        const ratio = d.gap / max;
        const barW = Math.abs(ratio) * (w * 0.4);
        const x = ratio > 0 ? midX : midX - barW;
        return (
          <g key={i}>
            <text x={midX - 8} y={y + 11} textAnchor="end" fontSize="10.5" fill="var(--ink-2)" fontFamily="var(--font-sans)">{d.label}</text>
            <rect x={x} y={y} width={barW} height={14} fill={d.gap > 0 ? 'var(--red-500)' : 'var(--green-500)'} opacity="0.85" />
            <text x={ratio > 0 ? x + barW + 4 : x - 4} y={y + 11} textAnchor={ratio > 0 ? 'start' : 'end'} fontSize="10" fill="var(--ink-2)" fontFamily="var(--font-sans)" fontVariant="tabular-nums">
              {d.gap > 0 ? '+$' : '−$'}{Math.abs(d.gap).toLocaleString()}
            </text>
          </g>
        );
      })}
      <text x="0" y={height + 18} fontSize="9" fill="var(--ink-4)">claims surplus →</text>
      <text x={w} y={height + 18} textAnchor="end" fontSize="9" fill="var(--ink-4)">premium surplus →</text>
    </svg>
  );
};

const ChartsRow = () => (
  <div className="chart-row">
    <div className="chart-mini">
      <div className="title"><h4>Action mix by product</h4><span className="meta">members \u00b7 view-filtered</span></div>
      <StackedBar data={[
        { label: 'PPO', retain: 7180, monitor: 4280, reprice: 9100, review: 3140 },
        { label: 'HMO', retain: 14880, monitor: 7390, reprice: 0,    review: 2480 },
        { label: 'EPO', retain: 0,    monitor: 5840, reprice: 8150, review: 0 },
        { label: 'POS', retain: 14730, monitor: 0,    reprice: 3920, review: 0 },
      ]} />
      <div style={{ display: 'flex', gap: 10, marginTop: 6, fontSize: 10, color: 'var(--ink-4)' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}><span style={{ width: 8, height: 8, background: 'var(--green-500)', borderRadius: 1 }} /> Retain</span>
        <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}><span style={{ width: 8, height: 8, background: 'var(--amber-500)', borderRadius: 1 }} /> Monitor</span>
        <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}><span style={{ width: 8, height: 8, background: 'var(--red-500)', borderRadius: 1 }} /> Reprice</span>
        <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}><span style={{ width: 8, height: 8, background: 'var(--violet-500)', borderRadius: 1 }} /> Review</span>
      </div>
    </div>
    <div className="chart-mini">
      <div className="title"><h4>Lapse trajectory</h4><span className="meta">view vs book benchmark</span></div>
      <LapseLine />
      <div style={{ display: 'flex', gap: 10, marginTop: 4, fontSize: 10, color: 'var(--ink-4)' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}><span style={{ width: 10, height: 2, background: 'var(--red-500)' }} /> Mid-year lapse</span>
        <span style={{ display: 'flex', alignItems: 'center', gap: 4 }}><span style={{ width: 10, height: 2, background: 'var(--amber-500)' }} /> Any-lapse</span>
      </div>
    </div>
    <div className="chart-mini">
      <div className="title"><h4>Premium gap by product</h4><span className="meta">claims minus premium, $/yr</span></div>
      <PremiumGap />
    </div>
  </div>
);

Object.assign(window, { Quadrant, RankedTable, ChartsRow });
