import React from 'react';
import { AlertCircle, CheckCircle2, RotateCcw } from 'lucide-react';

export function Toast({ toast, onDismiss, onUndo }) {
  if (!toast) return null;

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '24px',
        right: '24px',
        zIndex: 2000,
        backgroundColor: 'var(--text-primary)',
        color: 'var(--text-inverse)',
        padding: '12px 18px',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-modal)',
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        fontSize: '13px',
        maxWidth: '420px',
      }}
    >
      {toast.type === 'error' ? (
        <AlertCircle size={16} color="var(--accent-danger)" />
      ) : (
        <CheckCircle2 size={16} color="var(--accent-safe)" />
      )}
      <div style={{ flex: 1 }}>{toast.message}</div>
      {toast.undoAction && (
        <button
          onClick={onUndo}
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--accent-recovery)',
            cursor: 'pointer',
            fontSize: '12px',
            fontWeight: '600',
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
          }}
        >
          <RotateCcw size={12} /> Undo
        </button>
      )}
    </div>
  );
}
