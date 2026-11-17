import React from 'react';
import { Calendar, Plus, RefreshCw, Wand2, ShieldAlert, Sparkles, Database } from 'lucide-react';
import { Button } from '../common/Button';

export function CommandBar({
  onOpenRecovery,
  onOpenCourseModal,
  onOpenCommitmentModal,
  onOpenDeadlineModal,
  onSeedDemo,
  onAutoFitAll,
  missedCount = 0,
  isSeeding = false,
  isFitting = false,
}) {
  return (
    <header
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '12px 24px',
        backgroundColor: 'var(--bg-surface)',
        borderBottom: '1px solid var(--border-subtle)',
        position: 'sticky',
        top: 0,
        zIndex: 100,
      }}
    >
      {/* Brand Identity */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div
            style={{
              width: '28px',
              height: '28px',
              borderRadius: 'var(--radius-md)',
              backgroundColor: 'var(--accent-focus)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--text-inverse)',
            }}
          >
            <Calendar size={16} />
          </div>
          <div>
            <span className="title-app" style={{ color: 'var(--text-primary)' }}>
              AutoPace
            </span>
            <span
              style={{
                marginLeft: '8px',
                fontSize: '11px',
                padding: '2px 6px',
                borderRadius: 'var(--radius-sm)',
                backgroundColor: 'var(--bg-surface-subtle)',
                color: 'var(--text-secondary)',
                fontWeight: '600',
              }}
            >
              OS v1.0
            </span>
          </div>
        </div>
      </div>

      {/* Primary Actions */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Button variant="secondary" onClick={onSeedDemo} disabled={isSeeding} icon={Database}>
          {isSeeding ? 'Seeding...' : 'Seed Demo Week'}
        </Button>

        <Button variant="secondary" onClick={onAutoFitAll} disabled={isFitting} icon={Wand2}>
          {isFitting ? 'Optimizing...' : 'Auto-Fit All'}
        </Button>

        <div style={{ height: '20px', width: '1px', backgroundColor: 'var(--border-subtle)', margin: '0 4px' }} />

        <Button variant="secondary" onClick={onOpenCourseModal} icon={Plus}>
          Course
        </Button>

        <Button variant="secondary" onClick={onOpenCommitmentModal} icon={Plus}>
          Fixed Anchor
        </Button>

        <Button variant="secondary" onClick={onOpenDeadlineModal} icon={Plus}>
          Deadline
        </Button>

        <div style={{ height: '20px', width: '1px', backgroundColor: 'var(--border-subtle)', margin: '0 4px' }} />

        <Button
          variant="recovery"
          onClick={onOpenRecovery}
          icon={RefreshCw}
          style={{ position: 'relative' }}
        >
          Recover Schedule
          {missedCount > 0 && (
            <span
              style={{
                marginLeft: '6px',
                backgroundColor: 'var(--accent-danger)',
                color: 'var(--text-inverse)',
                padding: '1px 5px',
                borderRadius: '10px',
                fontSize: '10px',
                fontWeight: '700',
              }}
            >
              {missedCount}
            </span>
          )}
        </Button>
      </div>
    </header>
  );
}
