import { useApiResource } from '../../hooks/useApi';

/**
 * Read-only view of the bot's real settings, rendered from GET /controls.
 * It used to show ~100 hardcoded literals that drifted from .env (FE-09).
 */
export function ConfigPanel() {
  const { data, problem } = useApiResource('/controls', 15000);

  if (problem) {
    return <div role="alert" style={{ fontSize: 12 }}>Configuration unavailable: {problem.message}</div>;
  }
  if (!data) return <div style={{ fontSize: 12 }}>Loading configuration…</div>;

  const groups = new Map();
  for (const c of data.controls ?? []) {
    if (!groups.has(c.group)) groups.set(c.group, []);
    groups.get(c.group).push(c);
  }

  return (
    <div>
      {[...groups].map(([group, controls]) => (
        <section key={group} style={{ marginBottom: 12 }}>
          <div style={{ fontSize: 11, textTransform: 'uppercase', color: 'var(--c-muted)', marginBottom: 4 }}>
            {group}
          </div>
          {controls.map((c) => (
            <div key={c.name} style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, padding: '2px 0' }}>
              <span>{c.name}</span>
              <span>
                {c.protected ? 'protected' : String(c.value)}
                {c.requires_restart ? ' (restart)' : ''}
              </span>
            </div>
          ))}
        </section>
      ))}
      <div style={{ fontSize: 10, color: 'var(--c-faint)', paddingTop: 8, borderTop: '1px solid var(--c-border)' }}>
        Live values from the API. Adjust them in the Control Hub.
      </div>
    </div>
  );
}
