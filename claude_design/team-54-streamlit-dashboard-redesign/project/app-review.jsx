/* global React, Icon, Sparkline, MiniBar, ActionTag, Delta, fmtN, fmt$, fmtPct */
/* global SEGMENTS, ACTIONS, TOTAL, PRODUCTS, CHANNELS, AGES, YEARS */

// Compact "Review pane" — designed to fit a ~390-420px preview pane.
// Same exec content, tablet/mobile-first stack, no horizontal overflow.

const ReviewPane = () => {
  const [sel, setSel] = React.useState('S-014');
  const [tab, setTab] = React.useState('All');
  const visible = tab === 'All' ? SEGMENTS : SEGMENTS.filter(s => s.action === tab);
  const seg = SEGMENTS.find(s => s.id === sel) || SEGMENTS[0];

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', background: 'var(--bg-page)', overflow: 'hidden' }}>
      {/* compact topbar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '8px 12px', background: '#fff', borderBottom: '1px solid var(--line-1)', minHeight: 44 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, minWidth: 0 }}>
          <div className="brand-mark">PA</div>
          <div style={{ display: 'flex', flexDirection: 'column', minWidth: 0 }}>
            <span style={{ fontSize: 12.5, fontWeight: 600, color: 'var(--ink-1)', letterSpacing: '-0.01em', whiteSpace: 'nowrap' }}>Portfolio Action</span>
            <span style={{ fontSize: 10, color: 'var(--ink-4)', whiteSpace: 'nowrap' }}>Q3 2026 · 64,910 in view</span>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span className="run-pill" style={{ padding: '2px 7px' }}><span className="dot" /> live</span>
          <button className="icon-btn" title="Refresh"><Icon name="refresh" size={12} /></button>
        </div>
      </div>

      {/* scrollable body */}
      <div style={{ flex: 1, overflowY: 'auto', padding: 12, display: 'flex', flexDirection: 'column', gap: 10, minHeight: 0 }}>

        {/* page header */}
        <div>
          <span className="h-eyebrow">Q3 2026 review</span>
          <h1 className="h-section" style={{ marginTop: 3, fontSize: 18, lineHeight: 1.2 }}>Action plan</h1>
          <p style={{ fontSize: 12, color: 'var(--ink-3)', margin: '4px 0 0', lineHeight: 1.45 }}>15 segments · 64,910 members · sorted by priority.</p>
        </div>

        {/* compact KPIs — 2x2 grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 0, background: '#fff', border: '1px solid var(--line-1)', borderRadius: 4, overflow: 'hidden' }}>
          {[
            { l: 'Mid-year lapse', v: '11.4', u: '%', d: '+4.3pp', tone: 'up',  sub: 'vs 7.1% book' },
            { l: 'Any-lapse',      v: '21.7', u: '%', d: '+3.6pp', tone: 'up',  sub: 'vs 18.1% book' },
            { l: 'Loss ratio',     v: '0.94',         d: '+0.16',  tone: 'up',  sub: 'vs 0.78 target' },
            { l: 'Reprice cands',  v: '17.2k',        d: '4 segs', tone: 'flat',sub: 'view-filtered' },
          ].map((k, i) => (
            <div key={i} style={{ padding: '10px 12px', borderRight: i % 2 === 0 ? '1px solid var(--line-2)' : 0, borderTop: i >= 2 ? '1px solid var(--line-2)' : 0, minWidth: 0 }}>
              <div className="kpi-label" style={{ marginBottom: 4 }}>{k.l}</div>
              <div style={{ fontSize: 19, fontWeight: 500, color: 'var(--ink-1)', letterSpacing: '-0.02em', fontVariantNumeric: 'tabular-nums', lineHeight: 1.05 }}>
                {k.v}{k.u && <span style={{ fontSize: 11.5, color: 'var(--ink-3)', marginLeft: 1 }}>{k.u}</span>}
              </div>
              <div style={{ display: 'flex', gap: 6, marginTop: 3, alignItems: 'center', fontSize: 10.5, flexWrap: 'wrap' }}>
                <span className={`delta ${k.tone}`}>{k.d}</span>
                <span style={{ color: 'var(--ink-4)', minWidth: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{k.sub}</span>
              </div>
            </div>
          ))}
        </div>

        {/* filter chip row */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6 }}>
            <span className="h-eyebrow">Filters</span>
            <span className="t-meta">7 active</span>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, paddingBottom: 2 }}>
            {[
              { l: '2017–19', on: true },
              { l: 'PPO', on: true },
              { l: 'HMO', on: true },
              { l: 'Broker', on: true },
              { l: '45+', on: true },
              { l: 'Lapse 3–28%', on: true },
              { l: 'Family', on: false },
            ].map((c, i) => (
              <span key={i} className={`chip ${c.on ? 'is-on' : ''}`} style={{ flex: '0 0 auto', whiteSpace: 'nowrap' }}>
                {c.l}{c.on && <span className="x">×</span>}
              </span>
            ))}
            <span className="chip" style={{ flex: '0 0 auto' }}><Icon name="filter" size={10} /> more</span>
          </div>
        </div>

        {/* action category toggle */}
        <div className="seg" style={{ width: '100%' }}>
          {['All', 'Reprice', 'Monitor', 'Retain', 'Review'].map(a => (
            <button key={a} className={tab === a ? 'is-on' : ''} style={{ flex: 1, padding: '5px 0', fontSize: 11 }} onClick={() => setTab(a)}>{a}</button>
          ))}
        </div>

        {/* compact decision quadrant */}
        <div className="card" style={{ overflow: 'hidden' }}>
          <div style={{ padding: '9px 12px 6px', borderBottom: '1px solid var(--line-2)' }}>
            <h3 className="h-card">Decision quadrant</h3>
            <div className="t-meta" style={{ marginTop: 2 }}>claim pressure × lapse risk</div>
          </div>
          <div style={{ padding: '10px 14px 14px' }}>
            <div className="quad" style={{ height: 180, marginLeft: 18, marginBottom: 16 }}>
              <span className="quad-quadlabel" style={{ top: 6, left: 8, fontSize: 9 }}>low · high</span>
              <span className="quad-quadlabel" style={{ top: 6, right: 8, fontSize: 9, color: 'var(--red-700)' }}>high · high</span>
              <span className="quad-quadlabel" style={{ bottom: 6, left: 8, fontSize: 9 }}>low · low</span>
              <span className="quad-quadlabel" style={{ bottom: 6, right: 8, fontSize: 9 }}>high · low</span>
              {SEGMENTS.map(r => {
                const x = Math.min(99, (r.claim / 16000) * 100);
                const y = 100 - Math.min(99, (r.lapse / 28) * 100);
                const size = 10 + (r.n / 9120) * 22;
                return (
                  <span key={r.id}
                    className={`quad-bubble b-${r.action.toLowerCase()} ${r.id === sel ? 'is-selected' : ''}`}
                    style={{ left: `${x}%`, top: `${y}%`, width: size, height: size }}
                    title={r.label}
                    onClick={() => setSel(r.id)}
                  />
                );
              })}
              <span className="quad-axis-y" style={{ fontSize: 9 }}>Lapse →</span>
              <span className="quad-axis-x" style={{ fontSize: 9 }}>
                <span>$0</span><span>claim/yr</span><span>$16k</span>
              </span>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 4 }}>
              {ACTIONS.map(a => <span key={a} className={`tag ${a.toLowerCase()}`}>{a}</span>)}
            </div>
          </div>
        </div>

        {/* ranked segment cards */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6 }}>
            <span className="h-eyebrow">Ranked segments</span>
            <span className="t-meta" style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              {visible.length} of 482 · priority <Icon name="chevron" size={9} />
            </span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {visible.slice(0, 6).map((r, i) => (
              <div key={r.id}
                onClick={() => setSel(r.id)}
                style={{
                  background: '#fff',
                  border: '1px solid ' + (r.id === sel ? 'var(--teal-600)' : 'var(--line-1)'),
                  boxShadow: r.id === sel ? 'inset 2px 0 0 var(--teal-600)' : 'none',
                  borderRadius: 4, padding: '9px 10px', cursor: 'pointer',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 6 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, minWidth: 0, flex: 1 }}>
                    <span className="t-mono" style={{ color: 'var(--ink-4)', fontSize: 10, flex: '0 0 auto' }}>#{String(SEGMENTS.indexOf(r) + 1).padStart(2, '0')}</span>
                    <span style={{ fontSize: 12.5, fontWeight: 600, color: 'var(--ink-1)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {r.product} · {r.channel} · {r.age}
                    </span>
                  </div>
                  <ActionTag value={r.action} />
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 6, marginTop: 6 }}>
                  <div><div style={{ fontSize: 9.5, color: 'var(--ink-4)', letterSpacing: '0.04em', textTransform: 'uppercase' }}>Members</div><div style={{ fontSize: 12, fontWeight: 500, color: 'var(--ink-1)', fontVariantNumeric: 'tabular-nums' }}>{fmtN(r.n)}</div></div>
                  <div><div style={{ fontSize: 9.5, color: 'var(--ink-4)', letterSpacing: '0.04em', textTransform: 'uppercase' }}>Lapse</div><div style={{ fontSize: 12, fontWeight: 500, color: 'var(--ink-1)', fontVariantNumeric: 'tabular-nums' }}>{r.lapse.toFixed(1)}%</div></div>
                  <div><div style={{ fontSize: 9.5, color: 'var(--ink-4)', letterSpacing: '0.04em', textTransform: 'uppercase' }}>Claim</div><div style={{ fontSize: 12, fontWeight: 500, color: 'var(--ink-1)', fontVariantNumeric: 'tabular-nums' }}>{fmt$(r.claim)}</div></div>
                  <div><div style={{ fontSize: 9.5, color: 'var(--ink-4)', letterSpacing: '0.04em', textTransform: 'uppercase' }}>Gap</div><div style={{ fontSize: 12, fontWeight: 500, color: r.gap > 0 ? 'var(--red-700)' : 'var(--green-700)', fontVariantNumeric: 'tabular-nums' }}>{r.gap > 0 ? '+' : '−'}{fmt$(Math.abs(r.gap))}</div></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* selected segment summary */}
        <div style={{ background: '#fff', border: '1px solid var(--line-1)', borderRadius: 4, overflow: 'hidden' }}>
          <div style={{ padding: '10px 12px', borderBottom: '1px solid var(--line-2)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 6, flexWrap: 'wrap' }}>
              <span className="h-eyebrow">Selected segment</span>
              <ActionTag value={seg.action} />
            </div>
            <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--ink-1)', marginTop: 4, lineHeight: 1.3 }}>
              {seg.product} · {seg.channel} · {seg.age} · {seg.policyType}
            </div>
            <div className="t-mono" style={{ color: 'var(--ink-4)', marginTop: 2 }}>{seg.id} · {fmtN(seg.n)} members</div>
          </div>
          <div style={{ padding: '10px 12px' }}>
            {[
              { name: 'Mid-year lapse', a: seg.lapse, max: 28, suf: '%', book: TOTAL.midLapse, tone: seg.lapse > TOTAL.midLapse ? 'high' : 'low' },
              { name: 'Any-lapse',      a: seg.anyLapse, max: 35, suf: '%', book: TOTAL.anyLapse, tone: seg.anyLapse > TOTAL.anyLapse ? 'med' : 'low' },
              { name: 'Premium gap',    a: Math.max(0, seg.gap), max: 3000, suf: '', pre: '$', book: 0, tone: seg.gap > 0 ? 'high' : 'low' },
              { name: 'Utilization',    a: seg.util * 100, max: 100, suf: '', book: 65, tone: seg.util > 0.85 ? 'high' : 'med' },
            ].map((s, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '6px 0', borderBottom: i < 3 ? '1px dashed var(--line-2)' : 0 }}>
                <span style={{ fontSize: 11.5, color: 'var(--ink-2)', flex: 1, minWidth: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{s.name}</span>
                <MiniBar value={s.a} max={s.max} tone={s.tone} width={70} />
                <span className="t-mono" style={{ fontSize: 10.5, color: 'var(--ink-2)', width: 52, textAlign: 'right' }}>{s.pre || ''}{s.a.toFixed(s.suf === '%' ? 1 : 0)}{s.suf}</span>
              </div>
            ))}
            <div style={{ display: 'flex', gap: 6, marginTop: 10 }}>
              <button className="btn" style={{ flex: 1, justifyContent: 'center' }}>Watchlist</button>
              <button className="btn primary" style={{ flex: 1, justifyContent: 'center' }}>Apply {seg.action}</button>
            </div>
          </div>
        </div>

        <div style={{ height: 4 }} />
      </div>
    </div>
  );
};

Object.assign(window, { ReviewPane });
