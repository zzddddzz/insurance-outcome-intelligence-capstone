/* global React, Icon, Sparkline, MiniBar, ActionTag, Delta, fmtN, fmt$, fmtPct */
/* global SEGMENTS, ACTIONS, TOTAL */

const { useState: useStateD } = React;

// ─────────────────────────────────────────────────────────────
// Segment detail drawer
// ─────────────────────────────────────────────────────────────
const RULES = {
  Reprice: 'Premium below expected claims by ≥ $1k and lapse signal manageable. Repricing protects margin while retention stays above book.',
  Retain:  'Premium adequate, lapse below book, utilization moderate. Hold pricing; consider loyalty levers at renewal.',
  Monitor: 'Mixed signals — modeled lapse above book but margin intact, or margin thin but retention strong. Re-evaluate next quarter.',
  Review:  'High utilization and high claims relative to premium with material book share. Refer to medical review and reinsurance team.',
};

const Why = ({ seg }) => (
  <ol style={{ paddingLeft: 16, margin: 0, fontSize: 12, color: 'var(--ink-2)', lineHeight: 1.55 }}>
    <li>Mid-year lapse is <strong>{seg.lapse.toFixed(1)}%</strong> — {(seg.lapse - TOTAL.midLapse).toFixed(1)}pp above the book benchmark of {TOTAL.midLapse}%.</li>
    <li>Annual claim cost is <strong>{fmt$(seg.claim)}</strong> against premium of <strong>{fmt$(seg.premium)}</strong> ({seg.gap > 0 ? 'shortfall' : 'surplus'} of {fmt$(Math.abs(seg.gap))}).</li>
    <li>Utilization sits at <strong>{Math.round(seg.util * 100)}</strong> of expected, in the {seg.util > 0.85 ? 'top quintile' : seg.util > 0.7 ? 'upper half' : 'lower half'}.</li>
    <li>Segment carries <strong>{fmtN(seg.n)}</strong> members — {((seg.n / TOTAL.policies) * 100).toFixed(1)}% of book by lives.</li>
  </ol>
);

const Drawer = ({ seg, onClose }) => {
  const [action, setAction] = useStateD(seg.action);
  if (!seg) return null;

  return (
    <section className="drawer">
      <div className="drawer-head">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
          <div>
            <span className="h-eyebrow">Segment detail</span>
            <h2 className="h-section" style={{ marginTop: 4 }}>{seg.label}</h2>
            <div className="t-mono" style={{ color: 'var(--ink-4)', marginTop: 4 }}>
              {seg.id} · {seg.product} · {seg.channel} · {seg.policyType} · {fmtN(seg.n)} members
            </div>
          </div>
          <button className="icon-btn" onClick={onClose}><Icon name="close" size={12} /></button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 10, flexWrap: 'wrap' }}>
          <span className="t-meta">Recommended:</span>
          <ActionTag value={seg.action} />
          <span className="t-meta" style={{ marginLeft: 4 }}>Override:</span>
          <div className="seg">
            {ACTIONS.map(a => (
              <button key={a} className={action === a ? 'is-on' : ''} onClick={() => setAction(a)}>{a}</button>
            ))}
          </div>
        </div>
      </div>

      <div className="drawer-body">
        {/* Headline numbers */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 0, border: '1px solid var(--line-1)', borderRadius: 4, marginBottom: 14 }}>
          {[
            { l: 'Lapse risk',     v: `${seg.lapse.toFixed(1)}%`,  d: `${(seg.lapse - TOTAL.midLapse).toFixed(1)}pp`, tone: 'up' },
            { l: 'Claim / yr',     v: fmt$(seg.claim),             d: `${seg.gap > 0 ? '+' : '−'}${fmt$(Math.abs(seg.gap))} vs prem`, tone: seg.gap > 0 ? 'up' : 'down' },
            { l: 'Utilization',    v: `${Math.round(seg.util * 100)}`, d: `pctile ${seg.util > 0.85 ? '85+' : seg.util > 0.7 ? '60-85' : '<60'}`, tone: 'flat' },
          ].map((m, i, arr) => (
            <div key={i} style={{ padding: '10px 12px', borderRight: i < arr.length - 1 ? '1px solid var(--line-2)' : 0 }}>
              <div className="kpi-label" style={{ marginBottom: 4 }}>{m.l}</div>
              <div style={{ fontSize: 19, fontWeight: 500, color: 'var(--ink-1)', letterSpacing: '-0.02em', fontVariantNumeric: 'tabular-nums' }}>{m.v}</div>
              <div className={`delta ${m.tone}`} style={{ fontSize: 11, marginTop: 2 }}>{m.d}</div>
            </div>
          ))}
        </div>

        {/* Why ranked */}
        <div style={{ marginBottom: 14 }}>
          <h4 className="h-card" style={{ marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
            <span className="t-mono" style={{ color: 'var(--ink-4)', fontSize: 10 }}>01</span>
            Why this segment is ranked here
          </h4>
          <Why seg={seg} />
        </div>

        {/* Risk / cost / premium signals */}
        <div style={{ marginBottom: 14 }}>
          <h4 className="h-card" style={{ marginBottom: 6, display: 'flex', alignItems: 'center', gap: 6 }}>
            <span className="t-mono" style={{ color: 'var(--ink-4)', fontSize: 10 }}>02</span>
            Signals vs book
          </h4>
          {[
            { name: 'Mid-year lapse',     a: seg.lapse,             b: TOTAL.midLapse, max: 28, suf: '%', tone: seg.lapse > TOTAL.midLapse ? 'high' : 'low' },
            { name: 'Any-lapse',          a: seg.anyLapse,          b: TOTAL.anyLapse, max: 35, suf: '%', tone: seg.anyLapse > TOTAL.anyLapse ? 'med' : 'low' },
            { name: 'Claim load',         a: seg.claim / 220,       b: 32,             max: 80, suf: '',  tone: seg.claim > 7000 ? 'high' : seg.claim > 4000 ? 'med' : 'low' },
            { name: 'Premium adequacy',   a: 100 - Math.max(0, seg.gap / 130), b: 92,    max: 100, suf: '', tone: seg.gap > 0 ? 'high' : 'low' },
            { name: 'Utilization index',  a: seg.util * 100,        b: 65,             max: 100, suf: '', tone: seg.util > 0.85 ? 'high' : 'med' },
          ].map((s, i) => (
            <div className="signal" key={i}>
              <span className="name">{s.name}</span>
              <span className="vbar">
                <MiniBar value={s.a} max={s.max} tone={s.tone} width={130} />
                <span className="t-mono" style={{ width: 56, textAlign: 'right', color: 'var(--ink-2)' }}>{s.a.toFixed(s.suf === '%' ? 1 : 0)}{s.suf}</span>
                <span className="t-meta" style={{ width: 50, textAlign: 'right' }}>book {s.b.toFixed(0)}{s.suf}</span>
              </span>
            </div>
          ))}
        </div>

        {/* Recommendation */}
        <div style={{ background: 'var(--bg-rail)', border: '1px solid var(--line-2)', borderRadius: 4, padding: 12, marginBottom: 14 }}>
          <h4 className="h-card" style={{ marginBottom: 6 }}>Recommended action · {action}</h4>
          <p style={{ margin: 0, fontSize: 12.5, color: 'var(--ink-2)', lineHeight: 1.55 }}>{RULES[action]}</p>
        </div>

        {/* Next steps */}
        <div>
          <h4 className="h-card" style={{ marginBottom: 8, display: 'flex', alignItems: 'center', gap: 6 }}>
            <span className="t-mono" style={{ color: 'var(--ink-4)', fontSize: 10 }}>03</span>
            Next-step notes
          </h4>
          <div className="bullet">
            <span className="num">a.</span>
            <div className="b-body">
              <div className="h">Pricing</div>
              <div className="p">Model {action === 'Reprice' ? '+4–7%' : action === 'Review' ? '+8% with reinsurance review' : 'flat'} renewal premium for plan year 2026, holding network unchanged.</div>
            </div>
          </div>
          <div className="bullet">
            <span className="num">b.</span>
            <div className="b-body">
              <div className="h">Retention play</div>
              <div className="p">Pair with broker-channel outreach in Q3; offer wellness rider. Expected lift: 2.4pp on mid-year lapse.</div>
            </div>
          </div>
          <div className="bullet">
            <span className="num">c.</span>
            <div className="b-body">
              <div className="h">Owners</div>
              <div className="p">Pricing — D. Voss · Retention — A. Mehra · Medical review — Dr. K. Lin (only if Review).</div>
            </div>
          </div>
        </div>
      </div>

      <div className="drawer-foot">
        <button className="btn">Add to watchlist</button>
        <button className="btn">Export brief</button>
        <button className="btn primary">Submit override · {action}</button>
      </div>
    </section>
  );
};

// ─────────────────────────────────────────────────────────────
// Method / evidence view
// ─────────────────────────────────────────────────────────────
const MethodView = () => (
  <div className="card">
    <div className="card-head">
      <div className="title">
        <h3 className="h-card">Method &amp; evidence</h3>
        <span className="t-meta">data coverage, model inputs, confidence and limitations</span>
      </div>
      <div className="actions">
        <button className="btn"><Icon name="book" size={11} /> Open data dictionary</button>
      </div>
    </div>
    <div style={{ padding: 14 }}>
      <div className="method-grid">
        {/* Data coverage */}
        <div>
          <div className="h-eyebrow" style={{ marginBottom: 8 }}>Data coverage</div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginBottom: 10 }}>
            <div className="fact"><span className="n">228,711</span><span className="l">policy-year records</span></div>
            <div className="fact"><span className="n">76,240</span><span className="l">distinct policies</span></div>
            <div className="fact"><span className="n">42</span><span className="l">variables tracked</span></div>
            <div className="fact"><span className="n">2017–19</span><span className="l">observation window</span></div>
          </div>
          <div className="bullet"><span className="num">a.</span>
            <div className="b-body">
              <div className="h">Source</div>
              <div className="p">Internal portfolio workbook (book_v3.parquet). Joined with claims aggregate at policy-year grain. No member-level PHI.</div>
            </div>
          </div>
          <div className="bullet"><span className="num">b.</span>
            <div className="b-body">
              <div className="h">Lapse definitions</div>
              <div className="p"><strong>Mid-year lapse</strong> — termination on or before month 7. <strong>Any-lapse</strong> — termination at any point in policy year. Book benchmarks: 7.1% / 18.1%.</div>
            </div>
          </div>
        </div>

        {/* Model inputs */}
        <div>
          <div className="h-eyebrow" style={{ marginBottom: 8 }}>Model inputs</div>
          <table className="tbl" style={{ borderTop: '1px solid var(--line-2)' }}>
            <thead><tr><th>Feature</th><th>Type</th><th className="num" style={{ textAlign: 'right' }}>Importance</th></tr></thead>
            <tbody>
              {[
                ['premium_to_claim_ratio', 'derived', 0.21],
                ['utilization_index',      'derived', 0.18],
                ['age_band',                'cat',    0.14],
                ['channel',                 'cat',    0.11],
                ['product_line',            'cat',    0.10],
                ['policy_tenure_months',    'num',    0.09],
                ['reimbursement_lag_d',     'num',    0.07],
                ['region_state',            'cat',    0.06],
              ].map((row, i) => (
                <tr key={i} style={{ cursor: 'default' }}>
                  <td className="t-mono" style={{ color: 'var(--ink-1)' }}>{row[0]}</td>
                  <td><span className="tag ghost">{row[1]}</span></td>
                  <td className="num">
                    <MiniBar value={row[2] * 100} tone="blue" width={70} />
                    {row[2].toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Confidence + limitations */}
        <div>
          <div className="h-eyebrow" style={{ marginBottom: 8 }}>Confidence &amp; limitations</div>
          <div className="fact" style={{ marginBottom: 10 }}>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
              <span style={{ fontFamily: 'var(--font-serif)', fontSize: 28, color: 'var(--ink-1)', letterSpacing: '-0.02em', fontVariantNumeric: 'tabular-nums' }}>0.83</span>
              <span className="t-meta">ROC-AUC, hold-out 2019</span>
            </div>
            <div style={{ display: 'flex', gap: 16, marginTop: 8 }}>
              <div><div className="t-meta">Calibration</div><div style={{ fontWeight: 500, color: 'var(--ink-1)' }}>Brier 0.061</div></div>
              <div><div className="t-meta">Lift @ top decile</div><div style={{ fontWeight: 500, color: 'var(--ink-1)' }}>3.4×</div></div>
              <div><div className="t-meta">Recall @ 20%</div><div style={{ fontWeight: 500, color: 'var(--ink-1)' }}>0.61</div></div>
            </div>
          </div>
          <div className="bullet"><span className="num">⚠</span>
            <div className="b-body">
              <div className="h">Out-of-sample drift</div>
              <div className="p">2020+ telehealth uptake shifts utilization patterns; refresh recommended before applying to plan year 2026.</div>
            </div>
          </div>
          <div className="bullet"><span className="num">⚠</span>
            <div className="b-body">
              <div className="h">Coverage gap</div>
              <div className="p">Worksite channel under-represented for ages 65+. Treat that intersection as advisory, not actionable.</div>
            </div>
          </div>
          <div className="bullet"><span className="num">i</span>
            <div className="b-body">
              <div className="h">Privacy</div>
              <div className="p">All views are segment-aggregated to ≥ 100 lives. No individual member, claim, or diagnosis is exposed.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
);

Object.assign(window, { Drawer, MethodView });
