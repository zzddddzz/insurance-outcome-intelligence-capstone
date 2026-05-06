/* global React, Icon, Sparkline, MiniBar, ActionTag, fmtN, fmt$, fmtPct */
/* global SEGMENTS, TOTAL */

// ─────────────────────────────────────────────────────────────
// Mobile / narrow viewport
// ─────────────────────────────────────────────────────────────
const MobileView = () => {
  const top = SEGMENTS.slice(0, 8);
  return (
    <div className="m-shell" style={{ position: 'relative', overflow: 'hidden' }}>
      <div className="m-top">
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <button className="icon-btn" style={{ border: 0 }}><Icon name="menu" size={14} /></button>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--ink-1)', letterSpacing: '-0.01em' }}>Portfolio Action</span>
            <span style={{ fontSize: 10, color: 'var(--ink-4)' }}>Q3 view · 64,910 members</span>
          </div>
        </div>
        <button className="icon-btn"><Icon name="search" size={13} /></button>
      </div>

      {/* collapsed filter */}
      <div style={{ padding: '10px 14px 0', display: 'flex', gap: 6, overflowX: 'auto' }}>
        {[
          { l: 'All years', on: true },
          { l: 'Reprice + Review' },
          { l: 'PPO · HMO' },
          { l: '45+' },
        ].map((c, i) => (
          <span key={i} className={`chip ${c.on ? 'is-on' : ''}`} style={{ flex: '0 0 auto', whiteSpace: 'nowrap' }}>
            {c.l}{c.on && <span className="x">×</span>}
          </span>
        ))}
        <span className="chip" style={{ flex: '0 0 auto' }}><Icon name="filter" size={10} /> +3</span>
      </div>

      {/* mini KPI strip */}
      <div style={{ padding: '10px 14px', display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 6 }}>
        {[
          { l: 'Lapse', v: '11.4%', d: '+4.3pp', tone: 'up' },
          { l: 'Loss',  v: '0.94',  d: '+0.16',  tone: 'up' },
          { l: 'Reprice', v: '17.2k', d: '12 segs', tone: 'flat' },
        ].map((k, i) => (
          <div key={i} style={{ background: '#fff', border: '1px solid var(--line-1)', borderRadius: 6, padding: '8px 10px' }}>
            <div className="kpi-label" style={{ fontSize: 9.5, marginBottom: 2 }}>{k.l}</div>
            <div style={{ fontSize: 16, fontWeight: 500, color: 'var(--ink-1)', letterSpacing: '-0.02em', fontVariantNumeric: 'tabular-nums' }}>{k.v}</div>
            <div className={`delta ${k.tone}`} style={{ fontSize: 10 }}>{k.d}</div>
          </div>
        ))}
      </div>

      <div style={{ padding: '4px 14px 8px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span className="h-eyebrow">Ranked segments · {top.length}</span>
        <span className="t-meta" style={{ display: 'flex', alignItems: 'center', gap: 4 }}>Sort: priority <Icon name="chevron" size={10} /></span>
      </div>

      <div className="m-cards">
        {top.map((r, i) => (
          <div key={r.id} className="m-card">
            <div className="row1">
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <span className="t-mono" style={{ color: 'var(--ink-4)', fontSize: 10 }}>#{String(i + 1).padStart(2, '0')}</span>
                  <span className="seg-name">{r.product} · {r.age}</span>
                </div>
                <span className="t-meta" style={{ marginTop: 2 }}>{r.channel} · {r.policyType} · {fmtN(r.n)} members</span>
              </div>
              <ActionTag value={r.action} />
            </div>
            <div className="row2">
              <div className="stat"><div className="l">Lapse</div><div className="v">{r.lapse.toFixed(1)}%</div></div>
              <div className="stat"><div className="l">Claim</div><div className="v">{fmt$(r.claim)}</div></div>
              <div className="stat"><div className="l">Gap</div><div className="v" style={{ color: r.gap > 0 ? 'var(--red-700)' : 'var(--green-700)' }}>{r.gap > 0 ? '+' : '−'}{fmt$(Math.abs(r.gap))}</div></div>
            </div>
          </div>
        ))}
      </div>

      {/* sticky action summary */}
      <div className="m-sticky">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <div className="t-meta">View summary</div>
            <div style={{ fontSize: 13, color: 'var(--ink-1)', fontWeight: 600 }}>17.2k members up for reprice</div>
          </div>
          <div style={{ display: 'flex', gap: 4 }}>
            <span className="tag reprice">12</span>
            <span className="tag monitor">8</span>
            <span className="tag retain">6</span>
            <span className="tag review">3</span>
          </div>
        </div>
        <button className="btn primary" style={{ justifyContent: 'center' }}>Open action plan</button>
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────────────────────
// State variants — loading / empty / error
// ─────────────────────────────────────────────────────────────
const StateLoading = () => (
  <div style={{ padding: 12, display: 'flex', flexDirection: 'column', gap: 12 }}>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 0, border: '1px solid var(--line-1)', borderRadius: 4, background: '#fff' }}>
      {[0,1,2,3,4].map(i => (
        <div key={i} style={{ padding: '10px 14px', borderRight: i < 4 ? '1px solid var(--line-2)' : 0 }}>
          <div className="skel" style={{ height: 9, width: '60%', marginBottom: 8 }} />
          <div className="skel" style={{ height: 22, width: '70%', marginBottom: 6 }} />
          <div className="skel" style={{ height: 8, width: '40%' }} />
        </div>
      ))}
    </div>
    <div className="card">
      <div className="card-head">
        <div className="skel" style={{ height: 12, width: 140 }} />
        <div className="skel" style={{ height: 12, width: 60 }} />
      </div>
      <div style={{ padding: 12 }}>
        <div className="skel" style={{ height: 240, width: '100%', borderRadius: 3 }} />
      </div>
    </div>
    <div className="card" style={{ padding: 12 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
        <div className="skel" style={{ height: 11, width: 90 }} />
        <div className="skel" style={{ height: 11, width: 60 }} />
        <div className="skel" style={{ height: 11, width: 60 }} />
        <div className="skel" style={{ height: 11, width: 60 }} />
      </div>
      {[0,1,2,3,4,5,6].map(i => (
        <div key={i} style={{ display: 'flex', gap: 12, padding: '8px 0', borderBottom: '1px solid var(--line-2)' }}>
          <div className="skel" style={{ height: 10, width: 14 }} />
          <div className="skel" style={{ height: 10, width: '34%' }} />
          <div className="skel" style={{ height: 10, width: 50 }} />
          <div className="skel" style={{ height: 10, width: 50, marginLeft: 'auto' }} />
          <div className="skel" style={{ height: 10, width: 50 }} />
          <div className="skel" style={{ height: 10, width: 50 }} />
        </div>
      ))}
    </div>
    <div style={{ position: 'absolute', top: 60, right: 16, display: 'flex', alignItems: 'center', gap: 8, padding: '6px 10px', background: '#fff', border: '1px solid var(--line-1)', borderRadius: 4, fontSize: 11.5, color: 'var(--ink-3)', boxShadow: 'var(--sh-2)' }}>
      <span style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--blue-500)', animation: 'shimmer 1s linear infinite' }} />
      Loading 228,711 records · joining claims aggregate · 4 / 7 steps
    </div>
  </div>
);

const StateEmpty = () => (
  <div style={{ padding: 14, display: 'flex', flexDirection: 'column', gap: 14 }}>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', background: '#fff', border: '1px solid var(--line-1)', borderRadius: 4 }}>
      {['Members in view', 'Mid-year lapse', 'Any-lapse', 'Loss ratio', 'Reprice cands'].map((l, i, a) => (
        <div key={l} style={{ padding: '10px 14px', borderRight: i < a.length - 1 ? '1px solid var(--line-2)' : 0 }}>
          <div className="kpi-label">{l}</div>
          <div style={{ fontSize: 22, fontWeight: 500, color: 'var(--ink-5)', letterSpacing: '-0.02em' }}>—</div>
          <div className="t-meta">no records</div>
        </div>
      ))}
    </div>

    <div className="card" style={{ padding: 28 }}>
      <div style={{ textAlign: 'center', maxWidth: 360, margin: '24px auto' }}>
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none" stroke="var(--ink-4)" strokeWidth="1.4" style={{ margin: '0 auto 12px' }}>
          <rect x="8" y="10" width="32" height="28" rx="2" />
          <line x1="8" y1="18" x2="40" y2="18" />
          <line x1="14" y1="26" x2="30" y2="26" strokeDasharray="2 3" />
          <line x1="14" y1="32" x2="24" y2="32" strokeDasharray="2 3" />
        </svg>
        <h3 className="h-section" style={{ marginBottom: 6 }}>No segments match this filter set.</h3>
        <p style={{ fontSize: 13, color: 'var(--ink-3)', margin: '0 0 14px' }}>
          Filter narrowed by year (2017), product (POS), channel (Worksite), age band (65+). 0 of 482 segments fit.
        </p>
        <div style={{ display: 'flex', gap: 6, justifyContent: 'center', flexWrap: 'wrap' }}>
          <button className="btn">Drop age 65+</button>
          <button className="btn">Drop Worksite</button>
          <button className="btn primary">Reset all filters</button>
        </div>
        <div style={{ marginTop: 18, fontSize: 11, color: 'var(--ink-4)' }}>
          Data integrity: 228,711 / 228,711 records loaded · all filters applied client-side.
        </div>
      </div>
    </div>
  </div>
);

const StateError = () => (
  <div style={{ padding: 14, display: 'flex', flexDirection: 'column', gap: 14 }}>
    <div style={{ background: 'var(--red-100)', border: '1px solid #e2c0bd', borderRadius: 4, padding: '10px 14px', display: 'flex', alignItems: 'flex-start', gap: 10 }}>
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="var(--red-700)" strokeWidth="1.4">
        <circle cx="8" cy="8" r="6.5" />
        <line x1="8" y1="5" x2="8" y2="9" />
        <line x1="8" y1="11" x2="8" y2="11" />
      </svg>
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 12.5, fontWeight: 600, color: 'var(--red-700)' }}>Claims aggregate unavailable — falling back to last good snapshot (May 4, 06:14 CT).</div>
        <div style={{ fontSize: 11.5, color: 'var(--ink-3)', marginTop: 2 }}>
          ConnectionError on <code className="t-mono">claims_pipe.parquet</code> · retried 3× · pipeline owner paged.
        </div>
      </div>
      <button className="btn">Retry</button>
      <button className="btn primary">Use snapshot</button>
    </div>

    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', background: '#fff', border: '1px solid var(--line-1)', borderRadius: 4 }}>
      {[
        { l: 'Members in view', v: '64,910', sub: 'snapshot · stale 2d' },
        { l: 'Mid-year lapse',  v: '11.4', u: '%', sub: 'stale' },
        { l: 'Any-lapse',       v: '21.7', u: '%', sub: 'stale' },
        { l: 'Loss ratio',      v: '—',     sub: 'unavailable', err: true },
        { l: 'Reprice cands',   v: '—',     sub: 'unavailable', err: true },
      ].map((k, i, a) => (
        <div key={i} style={{ padding: '10px 14px', borderRight: i < a.length - 1 ? '1px solid var(--line-2)' : 0, opacity: k.err ? 0.7 : 1 }}>
          <div className="kpi-label">{k.l}</div>
          <div style={{ fontSize: 22, fontWeight: 500, color: k.err ? 'var(--ink-5)' : 'var(--ink-1)', letterSpacing: '-0.02em', fontVariantNumeric: 'tabular-nums' }}>{k.v}{k.u && <span style={{ fontSize: 12, color: 'var(--ink-3)' }}>{k.u}</span>}</div>
          <div className="t-meta" style={{ color: k.err ? 'var(--red-700)' : 'var(--ink-4)' }}>{k.sub}</div>
        </div>
      ))}
    </div>

    <div className="card" style={{ padding: 14 }}>
      <h4 className="h-card" style={{ marginBottom: 8 }}>Diagnostics</h4>
      <div className="t-mono log" style={{ fontSize: 11, color: 'var(--ink-3)', background: 'var(--bg-inset)', padding: 10, borderRadius: 3, lineHeight: 1.55 }}>
{`14:08:22  INFO   loaded portfolio_book_v3.parquet  rows=228,711
14:08:24  INFO   joined product_dim, channel_dim     ok
14:08:25  WARN   claims_pipe.parquet read timeout (s3://team54/feeds/claims/2026-05-06)
14:08:31  ERROR  ConnectionError after 3 retries     fallback=snapshot_2026-05-04
14:08:32  INFO   serving cached aggregates           degraded=true`}
      </div>
      <div style={{ display: 'flex', gap: 6, marginTop: 10 }}>
        <button className="btn">Open run log</button>
        <button className="btn">Page pipeline owner</button>
        <button className="btn">Export current view</button>
      </div>
    </div>
  </div>
);

Object.assign(window, { MobileView, StateLoading, StateEmpty, StateError });
