import { useState, useCallback, useRef } from 'react';

/**
 * A button for a high-impact operator action (FE-04): optionally asks for
 * confirmation first, and stays disabled while the request is in flight so a
 * double-click cannot send the action twice.
 */
export function ActionButton({ onAction, confirmMessage, children, disabled, ...rest }) {
  const [pending, setPending] = useState(false);
  const busy = useRef(false);
  const handle = async () => {
    if (busy.current) return;
    if (confirmMessage && !window.confirm(confirmMessage)) return;
    busy.current = true;
    setPending(true);
    try {
      await onAction();
    } finally {
      busy.current = false;
      setPending(false);
    }
  };
  return (
    <button type="button" {...rest} disabled={disabled || pending} aria-busy={pending} onClick={handle}>
      {children}
    </button>
  );
}

export function Toggle({ checked, onChange, label, disabled }) {
  return (
    <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 10, cursor: disabled ? 'default' : 'pointer', opacity: disabled ? 0.5 : 1 }}>
      <span style={{ color: 'var(--c-text)', fontSize: 12 }}>{label}</span>
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        disabled={disabled}
        onClick={() => !disabled && onChange(!checked)}
        className={`toggle-track ${checked ? 'on' : 'off'}`}
      >
        <span className="toggle-thumb" />
      </button>
    </label>
  );
}

export function Slider({ value, onChange, min, max, step, label, unit, decimals = 2 }) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState('');
  // FE-02: dragging only moves local state; one write is sent on release.
  const [drag, setDrag] = useState(null);
  const dragRef = useRef(null);
  const commitDrag = () => {
    const v = dragRef.current;
    dragRef.current = null;
    setDrag(null);
    if (v != null && v !== value) onChange(v);
  };

  const handleSubmit = useCallback(() => {
    const n = parseFloat(draft);
    if (!Number.isNaN(n) && n >= min && n <= max) {
      onChange(n);
    }
    setEditing(false);
  }, [draft, min, max, onChange]);

  return (
    <div style={{ marginBottom: 8 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 3 }}>
        <span style={{ fontSize: 11, color: 'var(--c-muted)' }}>{label}</span>
        <span style={{ fontSize: 10, color: 'var(--c-faint)' }}>{min} — {max}{unit ? ` ${unit}` : ''}</span>
      </div>
      <div className="slider-container">
        <input
          type="range"
          min={min}
          max={max}
          step={step || (max - min) / 100}
          value={drag ?? value ?? min}
          onChange={(e) => {
            const v = parseFloat(e.target.value);
            dragRef.current = v;
            setDrag(v);
          }}
          onPointerUp={commitDrag}
          onKeyUp={commitDrag}
          onBlur={commitDrag}
        />
        {editing ? (
          <input
            className="slider-val"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onBlur={handleSubmit}
            onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
            autoFocus
            style={{ width: 60 }}
          />
        ) : (
          <button
            className="slider-val"
            onClick={() => { setDraft(String(value != null ? Number(value).toFixed(decimals) : '')); setEditing(true); }}
            title="Click to type value"
          >
            {value != null ? Number(value).toFixed(decimals) : '—'}{unit || ''}
          </button>
        )}
      </div>
    </div>
  );
}

export function NumberInput({ value, onChange, label, min, max, step, unit }) {
  const [draft, setDraft] = useState(String(value ?? ''));
  const [focused, setFocused] = useState(false);

  const commit = () => {
    const n = parseFloat(draft);
    // FE-03: write only a valid, changed value; anything else just leaves
    // draft mode (an out-of-range entry reverts to the current value).
    if (!Number.isNaN(n) && !(min != null && n < min) && !(max != null && n > max) && n !== Number(value)) {
      onChange(n);
    }
    setFocused(false);
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
      <span style={{ fontSize: 11, color: 'var(--c-muted)', minWidth: 100 }}>{label}</span>
      <input
        className="input-sm"
        type="number"
        step={step || 1}
        min={min}
        max={max}
        value={focused ? draft : (value ?? '')}
        onChange={(e) => { setDraft(e.target.value); if (!focused) setFocused(true); }}
        onFocus={() => { setDraft(String(value ?? '')); setFocused(true); }}
        onBlur={commit}
        onKeyDown={(e) => e.key === 'Enter' && commit()}
        style={{ width: 80, textAlign: 'right' }}
      />
      {unit && <span style={{ fontSize: 10, color: 'var(--c-faint)' }}>{unit}</span>}
    </div>
  );
}

export function ModeSwitcher({ current, onSwitch }) {
  const modes = ['automatic', 'restricted', 'manual'];
  const activeClass = { automatic: 'active-auto', restricted: 'active-restricted', manual: 'active-manual' };
  return (
    <div style={{ display: 'flex', gap: 3 }}>
      {modes.map((m) => (
        <button
          key={m}
          onClick={() => {
            if (m === current) return;
            if (m === 'automatic' && !window.confirm('Switch to AUTOMATIC execution mode? Trades will be placed without approval.')) return;
            onSwitch(m);
          }}
          className={`mode-btn ${current === m ? activeClass[m] : ''}`}
        >
          {m}
        </button>
      ))}
    </div>
  );
}

export function StatCard({ label, value, sub, color, icon }) {
  return (
    <div className="stat-card">
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 4 }}>
        {icon && <span style={{ fontSize: 12, color: 'var(--c-cyan)' }}>{icon}</span>}
        <span style={{ fontSize: 10, color: 'var(--c-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{label}</span>
      </div>
      <div style={{ fontSize: 20, fontWeight: 700, fontFamily: 'var(--font-mono, monospace)', color: color || 'var(--c-text)' }}>{value}</div>
      {sub && <div style={{ fontSize: 10, color: 'var(--c-faint)', marginTop: 2 }}>{sub}</div>}
    </div>
  );
}
