import React from 'react';
import { Sparkles, ArrowRight, Play } from 'lucide-react';
import { Button } from '../common/Button';

export function MicroActionBanner({ microAction, onStartMicroAction }) {
  if (!microAction) return null;

  return (
    <div
      style={{
        margin: '12px 0',
        padding: '10px 16px',
        backgroundColor: 'var(--accent-focus-light)',
        border: '1px solid #BFDBFE',
        borderRadius: 'var(--radius-lg)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '16px',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <div
          style={{
            backgroundColor: 'var(--accent-focus)',
            color: 'var(--text-inverse)',
            width: '24px',
            height: '24px',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Sparkles size={13} />
        </div>
        <div>
          <span style={{ fontSize: '13px', fontWeight: '600', color: 'var(--accent-focus)' }}>
            {microAction.title}
          </span>
          <span style={{ fontSize: '12px', color: 'var(--text-secondary)', marginLeft: '8px' }}>
            {microAction.suggested_prompt} ({microAction.duration_minutes} min focus)
          </span>
        </div>
      </div>

      <Button
        variant="primary"
        onClick={() => onStartMicroAction(microAction)}
        icon={Play}
        style={{ padding: '4px 10px', fontSize: '12px' }}
      >
        Start Sprint
      </Button>
    </div>
  );
}
