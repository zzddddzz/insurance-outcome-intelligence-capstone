/* global React, ReactDOM, ActionTag */
/* global Topbar, FilterRail, KpiStrip, Quadrant, RankedTable, ChartsRow */
/* global Drawer, MethodView, MobileView, StateLoading, StateEmpty, StateError */
/* global SEGMENTS, YEARS, Icon */

const { useState: uS } = React;

// Main exec dashboard composition.
// `compact` collapses the right drawer into a small inline summary so the
// dashboard reads at narrow review widths without a horizontal scroll.
const ExecDashboard = ({ withDrawer = true, initialSelected = 'S-014', compact = false }) => {
  const [filters, setFilters] = uS({
    years: YEARS, products: [], channels: [], ages: [], policies: [], actions: []
  });
  const [selectedId, setSelectedId] = uS(initialSelected);
  const seg = SEGMENTS.find(s => s.id === selectedId) || SEGMENTS[0];

  const showDrawer = withDrawer && !compact;
  const cols = showDrawer ? '232px 1fr 380px' : (compact ? '208px 1fr' : '232px 1fr');

  return (
    <div className={`app-shell ${compact ? 'is-compact' : ''}`}>
      <Topbar />
      <div style={{
        display: 'grid',
        gridTemplateColumns: cols,
        height: '100%',
        minHeight: 0,
        overflow: 'hidden'
      }}>
        <FilterRail filters={filters} setFilters={setFilters} />

        <main style={{ padding: 12, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 12, minWidth: 0 }}>
          <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', flexWrap: 'wrap', gap: '8px 16px', minWidth: 0 }}>
            <div style={{ minWidth: 0, flex: '1 1 280px' }}>
              <span className="h-eyebrow">Q3 2026 portfolio review</span>
              <h1 className="h-section" style={{ marginTop: 4, overflowWrap: 'anywhere' }}>Action plan · 64,910 members under review</h1>
            </div>
            <div style={{ display: 'flex', gap: 6, alignItems: 'center', flexWrap: 'wrap', rowGap: 6 }}>
              <span className="t-meta">View:</span>
              <div className="seg">
                <button className="is-on">Executive</button>
                <button>Pricing</button>
                <button>Retention</button>
                <button>Medical</button>
              </div>
              <button className="btn"><Icon name="download" size={11} /> Export</button>
              <button className="btn primary"><Icon name="flag" size={11} /> Submit plan</button>
            </div>
          </div>

          {compact && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 10px', background: '#fff', border: '1px solid var(--line-1)', borderRadius: 4, flexWrap: 'wrap' }}>
              <span className="h-eyebrow">Selected</span>
              <ActionTag value={seg.action} />
              <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--ink-1)', minWidth: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{seg.label}</span>
              <span className="t-meta" style={{ marginLeft: 'auto' }}>Tap a row to open the segment drawer.</span>
            </div>
          )}

          <KpiStrip rows={SEGMENTS} />
          <Quadrant rows={SEGMENTS} selectedId={selectedId} onSelect={setSelectedId} />
          <RankedTable rows={SEGMENTS} selectedId={selectedId} onSelect={setSelectedId} />
          <ChartsRow />
          <MethodView />
          <div style={{ height: 4 }} />
        </main>

        {showDrawer && <Drawer seg={seg} onClose={() => {}} />}
      </div>
    </div>
  );
};

Object.assign(window, { ExecDashboard });
