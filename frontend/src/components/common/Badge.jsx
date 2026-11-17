import React from 'react';

export function Badge({ children, variant = 'default', color = null }) {
  const styles = {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '4px',
    padding: '2px 6px',
    borderRadius: 'var(--radius-sm)',
    fontSize: '11px',
    fontWeight: '600',
    letterSpacing: '0.02em',
    lineHeight: '1.2',
  };

  if (color) {
    return (
      <span
        style={{
          ...styles,
          backgroundColor: `${color}18`,
          color: color,
          border: `1px solid ${color}30`,
        }}
      >
        {children}
      </span>
    );
  }

  const variantStyles = {
    scheduled: { backgroundColor: 'var(--accent-focus-light)', color: 'var(--accent-focus)' },
    completed: { backgroundColor: 'var(--accent-safe-light)', color: 'var(--accent-safe)' },
    missed: { backgroundColor: 'var(--accent-danger-light)', color: 'var(--accent-danger)' },
    recovered: { backgroundColor: 'var(--accent-recovery-light)', color: 'var(--accent-recovery)' },
    warning: { backgroundColor: 'var(--accent-warning-light)', color: 'var(--accent-warning)' },
    fixed: { backgroundColor: 'var(--bg-surface-subtle)', color: 'var(--text-secondary)' },
  }[variant] || { backgroundColor: 'var(--bg-surface-subtle)', color: 'var(--text-secondary)' };

  return <span style={{ ...styles, ...variantStyles }}>{children}</span>;
}
