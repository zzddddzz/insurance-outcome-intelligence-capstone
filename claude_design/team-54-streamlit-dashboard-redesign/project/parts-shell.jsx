/* global React, Icon, Sparkline, MiniBar, ActionTag, Delta, fmtN, fmt$, fmtPct */
/* global SEGMENTS, ACTIONS, TOTAL, PRODUCTS, CHANNELS, AGES, POLICIES, YEARS */

const { useState: useStateShell, useMemo: useMemoShell } = React;

// ─────────────────────────────────────────────────────────────
// Topbar — Streamlit-app shell
// ─────────────────────────────────────────────────────────────
const Topbar = ({ runState = 'live' }) => (
  <div className="topbar">
    <div className="topbar-left">
      <div className="topbar-brand">
        <div className="brand-mark">PA</div>
        <span>Portfolio Action Console</span>
      </div>
      <div className="crumbs">
        <span>Workbook · book_v3.parquet</span>
        <span className="sep">/</span>
        <span style={{ color: 'var(--ink-2)' }}>Executive view</span>
      </div>
    </div>
    <div className="topbar-right">
      <div className="run-pill">
        <span className="dot" />
        <span>Last refresh 06:14 CT · 228,711 rows</span>
      </div>
      <button className="icon-btn" title="Refresh"><Icon name="refresh" size={13} /></button>
      <button className="icon-btn" title="Settings"><Icon name="cog" size={13} /></button>
      <div style={{ width: 22, height: 22, borderRadius: '50%', background: 'var(--teal-700)', color: '#fff', display: 'grid', placeItems: 'center', fontSize: 10, fontWeight: 600 }}>NW</div>
    </div>
  </div>
);

// ─────────────────────────────────────────────────────────────
// Filter rail
// ─────────────────────────────────────────────────────────────
const Chip = ({ label, on, onClick }) => (
  <span className={`chip ${on ? 'is-on' : ''}`} onClick={onClick}>
    {label}{on && <span className="x">×</span>}
  </span>
);

const RailGroup = ({ label, clear, children }) => (
  <div className="rail-group">
    <div className="rail-label">
      <span>{label}</span>
      {clear && <span className="clear" onClick={clear}>reset</span>}
    </div>
    {children}
  </div>
);

const FilterRail = ({ filters, setFilters }) => {
  const toggle = (key, val) => {
    setFilters((f) => {
      const cur = f[key];
      return { ...f, [key]: cur.includes(val) ? cur.filter(x => x !== val) : [...cur, val] };
    });
  };
  return (
    <aside className="rail">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 14 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'var(--ink-1)', fontSize: 12, fontWeight: 600 }}>
          <Icon name="filter" size={12} /> Filters
        </div>
        <span className="t-meta">7 active</span>
      </div>

      <div style={{ marginBottom: 14 }}>
        <div style={{ position: 'relative' }}>
          <input
            placeholder="Search segment id, label…"
            style={{
              width: '100%', padding: '6px 8px 6px 26px', fontSize: 12, fontFamily: 'inherit',
              border: '1px solid var(--line-1)', borderRadius: 3, background: '#fff',
              color: 'var(--ink-2)',
            }}
          />
          <span style={{ position: 'absolute', left: 8, top: 7, color: 'var(--ink-4)' }}>
            <Icon name="search" size={12} />
          </span>
        </div>
      </div>

      <RailGroup label="Observation Year" clear={() => setFilters(f => ({ ...f, years: YEARS }))}>
        <div className="seg" style={{ width: '100%' }}>
          {YEARS.map((y) => (
            <button key={y}
              className={filters.years.includes(y) ? 'is-on' : ''}
              style={{ flex: 1 }}
              onClick={() => toggle('years', y)}
            >{y}</button>
          ))}
        </div>
      </RailGroup>

      <RailGroup label="Product" clear={() => setFilters(f => ({ ...f, products: [] }))}>
        <div className="chips">
          {PRODUCTS.map((p) => (
            <Chip key={p} label={p} on={filters.products.includes(p)} onClick={() => toggle('products', p)} />
          ))}
        </div>
      </RailGroup>

      <RailGroup label="Channel" clear={() => setFilters(f => ({ ...f, channels: [] }))}>
        <div className="chips">
          {CHANNELS.map((c) => (
            <Chip key={c} label={c} on={filters.channels.includes(c)} onClick={() => toggle('channels', c)} />
          ))}
        </div>
      </RailGroup>

      <RailGroup label="Age band" clear={() => setFilters(f => ({ ...f, ages: [] }))}>
        <div className="chips">
          {AGES.map((a) => (
            <Chip key={a} label={a} on={filters.ages.includes(a)} onClick={() => toggle('ages', a)} />
          ))}
        </div>
      </RailGroup>

      <RailGroup label="Policy type">
        <div className="chips">
          {POLICIES.map((p) => (
            <Chip key={p} label={p} on={filters.policies.includes(p)} onClick={() => toggle('policies', p)} />
          ))}
        </div>
      </RailGroup>

      <RailGroup label="Lapse risk threshold">
        <div className="range">
          <div className="range-track">
            <div className="range-fill" style={{ left: '15%', width: '70%' }} />
            <div className="range-handle" style={{ left: '15%' }} />
            <div className="range-handle" style={{ left: '85%' }} />
          </div>
          <div className="range-vals"><span>3%</span><span>28%</span></div>
        </div>
      </RailGroup>

      <RailGroup label="Segment size (members)">
        <div className="range">
          <div className="range-track">
            <div className="range-fill" style={{ left: '20%', width: '80%' }} />
            <div className="range-handle" style={{ left: '20%' }} />
            <div className="range-handle" style={{ left: '100%' }} />
          </div>
          <div className="range-vals"><span>2,000</span><span>10,000+</span></div>
        </div>
      </RailGroup>

      <RailGroup label="Action category">
        <label className="check on"><span className="box" /> Reprice <span style={{ marginLeft: 'auto', color: 'var(--ink-4)' }}>4</span></label>
        <label className="check on"><span className="box" /> Monitor <span style={{ marginLeft: 'auto', color: 'var(--ink-4)' }}>4</span></label>
        <label className="check on"><span className="box" /> Retain  <span style={{ marginLeft: 'auto', color: 'var(--ink-4)' }}>5</span></label>
        <label className="check on"><span className="box" /> Review  <span style={{ marginLeft: 'auto', color: 'var(--ink-4)' }}>2</span></label>
      </RailGroup>

      <div style={{ display: 'flex', gap: 6, marginTop: 4 }}>
        <button className="btn primary" style={{ flex: 1, justifyContent: 'center' }}>Apply</button>
        <button className="btn" style={{ flex: 1, justifyContent: 'center' }}>Reset all</button>
      </div>
    </aside>
  );
};

// ─────────────────────────────────────────────────────────────
// KPI strip
// ─────────────────────────────────────────────────────────────
const Kpi = ({ label, value, unit, sub, delta, deltaSuffix = 'pp', invert, sparkData, sparkColor = 'var(--teal-600)' }) => (
  <div className="kpi">
    <div className="kpi-label">{label}<span className="info" title={label}>i</span></div>
    <div className="kpi-value">
      {value}{unit && <span className="unit">{unit}</span>}
    </div>
    <div className="kpi-sub">
      {delta !== undefined && <Delta value={delta} suffix={deltaSuffix} invert={invert} />}
      <span style={{ color: 'var(--ink-4)' }}>{sub}</span>
    </div>
    {sparkData && (
      <div style={{ marginTop: 6 }}>
        <Sparkline data={sparkData} color={sparkColor} fill="rgba(22,122,120,0.10)" width={140} height={22} />
      </div>
    )}
  </div>
);

const KpiStrip = ({ rows }) => {
  const total = rows.reduce((a, r) => a + r.n, 0);
  const wLapse = rows.reduce((a, r) => a + r.lapse * r.n, 0) / Math.max(1, total);
  const wAny = rows.reduce((a, r) => a + r.anyLapse * r.n, 0) / Math.max(1, total);
  const claimsTotal = rows.reduce((a, r) => a + r.claim * r.n, 0);
  const premTotal = rows.reduce((a, r) => a + r.premium * r.n, 0);
  const lossRatio = claimsTotal / Math.max(1, premTotal);
  const repriceN = rows.filter(r => r.action === 'Reprice').reduce((a, r) => a + r.n, 0);

  return (
    <div className="kpis">
      <Kpi
        label="Members in view"
        value={fmtN(total)}
        sub="across 15 segments"
        sparkData={[42,46,49,52,55,57,59,61,64,66,67,68,72,76,total/1000]}
        sparkColor="#0e1a1f"
      />
      <Kpi
        label="Mid-year lapse rate"
        value={wLapse.toFixed(1)}
        unit="%"
        delta={+(wLapse - TOTAL.midLapse).toFixed(1)}
        invert
        sub={`vs book ${TOTAL.midLapse}%`}
        sparkData={[6.4,6.7,6.9,7.0,7.1,7.0,7.2,7.4,7.6,7.9,8.2,8.6,9.1,9.6,wLapse]}
        sparkColor="#b9484a"
      />
      <Kpi
        label="Any-lapse rate"
        value={wAny.toFixed(1)}
        unit="%"
        delta={+(wAny - TOTAL.anyLapse).toFixed(1)}
        invert
        sub={`vs book ${TOTAL.anyLapse}%`}
        sparkData={[16.8,17.1,17.4,17.7,17.9,18.0,18.1,18.4,18.7,19.1,19.5,20.0,20.6,21.2,wAny]}
        sparkColor="#c08a2d"
      />
      <Kpi
        label="Loss ratio"
        value={lossRatio.toFixed(2)}
        unit=""
        delta={+(lossRatio - 0.78).toFixed(2)}
        deltaSuffix=""
        invert
        sub="vs target 0.78"
        sparkData={[0.74,0.75,0.76,0.78,0.79,0.81,0.82,0.83,0.85,0.86,0.88,0.90,0.92,0.94,lossRatio]}
        sparkColor="#1f4a82"
      />
      <Kpi
        label="Reprice candidates"
        value={fmtN(repriceN)}
        sub={`${rows.filter(r => r.action === 'Reprice').length} segments flagged`}
        sparkData={[8,9,10,11,12,12,13,13,14,15,16,17,18,19,repriceN/1500]}
        sparkColor="#8a2a2a"
      />
    </div>
  );
};

Object.assign(window, { Topbar, FilterRail, KpiStrip });
