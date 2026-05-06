// Synthetic segment data for the Portfolio Action Console.
// All labels are aggregate/synthetic — no member-level data.

const ACTIONS = ['Retain', 'Reprice', 'Monitor', 'Review'];

// raw rows — segment-level only
const SEGMENTS = [
  { id: 'S-014', label: 'PPO · Broker · 55–64 · IL',  product: 'PPO',  channel: 'Broker', age: '55–64', policyType: 'Family',     n: 4820, lapse: 24.6, anyLapse: 33.1, claim: 11820, premium: 9740,  util: 0.92, action: 'Reprice' },
  { id: 'S-027', label: 'HMO · Direct · 35–44 · TX',  product: 'HMO',  channel: 'Direct', age: '35–44', policyType: 'Individual', n: 7390, lapse: 19.2, anyLapse: 28.4, claim: 4720,  premium: 5280,  util: 0.71, action: 'Monitor' },
  { id: 'S-041', label: 'EPO · Worksite · 45–54 · CA',product: 'EPO',  channel: 'Worksite',age: '45–54', policyType: 'Family',     n: 5210, lapse: 21.4, anyLapse: 30.7, claim: 8940,  premium: 8120,  util: 0.84, action: 'Reprice' },
  { id: 'S-052', label: 'POS · Broker · 25–34 · NY',  product: 'POS',  channel: 'Broker', age: '25–34', policyType: 'Individual', n: 9120, lapse:  6.4, anyLapse: 14.2, claim: 2180,  premium: 3680,  util: 0.46, action: 'Retain'  },
  { id: 'S-063', label: 'PPO · Direct · 65+ · FL',    product: 'PPO',  channel: 'Direct', age: '65+',   policyType: 'Individual', n: 3140, lapse: 11.8, anyLapse: 20.4, claim: 14210, premium: 12430, util: 0.96, action: 'Review'  },
  { id: 'S-078', label: 'HMO · Worksite · 45–54 · OH',product: 'HMO',  channel: 'Worksite',age: '45–54', policyType: 'Family',     n: 6470, lapse:  4.9, anyLapse: 12.8, claim: 5210,  premium: 6940,  util: 0.62, action: 'Retain'  },
  { id: 'S-082', label: 'EPO · Direct · 35–44 · GA',  product: 'EPO',  channel: 'Direct', age: '35–44', policyType: 'Individual', n: 5840, lapse: 16.7, anyLapse: 25.9, claim: 3940,  premium: 4710,  util: 0.69, action: 'Monitor' },
  { id: 'S-091', label: 'PPO · Broker · 45–54 · NJ',  product: 'PPO',  channel: 'Broker', age: '45–54', policyType: 'Family',     n: 4280, lapse: 13.2, anyLapse: 22.1, claim: 9120,  premium: 8910,  util: 0.81, action: 'Monitor' },
  { id: 'S-104', label: 'HMO · Broker · 25–34 · AZ',  product: 'HMO',  channel: 'Broker', age: '25–34', policyType: 'Individual', n: 8410, lapse:  8.1, anyLapse: 16.7, claim: 2640,  premium: 3940,  util: 0.51, action: 'Retain'  },
  { id: 'S-118', label: 'POS · Direct · 55–64 · WA',  product: 'POS',  channel: 'Direct', age: '55–64', policyType: 'Family',     n: 3920, lapse: 15.3, anyLapse: 24.8, claim: 10840, premium: 9120,  util: 0.88, action: 'Reprice' },
  { id: 'S-126', label: 'PPO · Worksite · 35–44 · MI',product: 'PPO',  channel: 'Worksite',age: '35–44', policyType: 'Family',     n: 7180, lapse:  5.7, anyLapse: 13.4, claim: 6210,  premium: 7340,  util: 0.66, action: 'Retain'  },
  { id: 'S-137', label: 'EPO · Broker · 55–64 · NC',  product: 'EPO',  channel: 'Broker', age: '55–64', policyType: 'Individual', n: 2940, lapse: 17.4, anyLapse: 27.2, claim: 9420,  premium: 8240,  util: 0.83, action: 'Reprice' },
  { id: 'S-148', label: 'HMO · Direct · 65+ · PA',    product: 'HMO',  channel: 'Direct', age: '65+',   policyType: 'Individual', n: 2480, lapse:  9.4, anyLapse: 18.6, claim: 13420, premium: 11820, util: 0.94, action: 'Review'  },
  { id: 'S-159', label: 'POS · Worksite · 45–54 · MN',product: 'POS',  channel: 'Worksite',age: '45–54', policyType: 'Family',     n: 5610, lapse:  7.2, anyLapse: 15.1, claim: 5840,  premium: 6420,  util: 0.64, action: 'Retain'  },
  { id: 'S-167', label: 'PPO · Direct · 25–34 · MA',  product: 'PPO',  channel: 'Direct', age: '25–34', policyType: 'Individual', n: 6210, lapse: 10.2, anyLapse: 19.3, claim: 3120,  premium: 4280,  util: 0.58, action: 'Monitor' },
];

// Compute derived priority score and gap once.
SEGMENTS.forEach((s) => {
  s.gap = s.claim - s.premium;
  // simple weighted score: lapse + claim pressure + premium gap, normalized
  s.priority = Math.round(
    (s.lapse * 1.6) +
    (s.claim / 220) +
    (Math.max(0, s.gap) / 110) +
    (s.util * 14)
  );
});

// sort by priority desc default
SEGMENTS.sort((a, b) => b.priority - a.priority);

const TOTAL = {
  records: 228711,
  policies: 76240,
  variables: 42,
  yearsLabel: '2017 – 2019',
  midLapse: 7.1,
  anyLapse: 18.1,
};

const PRODUCTS  = ['PPO', 'HMO', 'EPO', 'POS'];
const CHANNELS  = ['Broker', 'Direct', 'Worksite'];
const AGES      = ['25–34', '35–44', '45–54', '55–64', '65+'];
const POLICIES  = ['Individual', 'Family'];
const YEARS     = ['2017', '2018', '2019'];

Object.assign(window, { SEGMENTS, ACTIONS, TOTAL, PRODUCTS, CHANNELS, AGES, POLICIES, YEARS });
