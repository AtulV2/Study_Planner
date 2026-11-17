import React from 'react';
import { AlertTriangle, CheckCircle, ShieldCheck } from 'lucide-react';

export function BurnoutMeter({ dailyStats = [], maxDailyHours = 5.5 }) {
  const maxMinutes = maxDailyHours * 60;

  return (
    <div
      style={{
        backgroundColor: 'var(--bg-surface)',
        borderBottom: '1px solid var(--border-subtle)',
        padding: '12px 24px',
        display: 'grid',
        gridTemplateColumns: 'repeat(7, 1fr)',
        gap: '12px',
      }}
    >
      {dailyStats.map((stat, idx) => {
        const totalMinutes = stat.studyMinutes || 0;
        const totalHours = (totalMinutes / 60).toFixed(1);
        const ratio = Math.min(1.0, totalMinutes / maxMinutes);
        const isOverload = totalMinutes > maxMinutes;
        const isNear = totalMinutes >= maxMinutes * 0.8 && !isOverload;

        const barColor = isOverload
          ? 'var(--accent-warning)'
          : isNear
          ? '#F59E0B'
          : 'var(--accent-focus)';

        return (
          <div
            key={idx}
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '4px',
              padding: '6px 8px',
              borderRadius: 'var(--radius-md)',
              backgroundColor: isOverload ? 'var(--accent-warning-light)' : 'transparent',
              border: isOverload ? '1px solid #FCD34D' : '1px solid transparent',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span className="text-micro" style={{ color: 'var(--text-secondary)' }}>
                {stat.dayName}
              </span>
              <span className="mono" style={{ fontSize: '11px', fontWeight: '600', color: isOverload ? 'var(--accent-warning)' : 'var(--text-primary)' }}>
                {totalHours}h / {maxDailyHours}h
              </span>
            </div>

            {/* Gauge Bar */}
            <div
              style={{
                height: '4px',
                width: '100%',
                backgroundColor: 'var(--border-subtle)',
                borderRadius: '2px',
                overflow: 'hidden',
              }}
            >
              <div
                style={{
                  height: '100%',
                  width: `${Math.min(100, (totalMinutes / maxMinutes) * 100)}%`,
                  backgroundColor: barColor,
                  borderRadius: '2px',
                  transition: 'width 0.3s ease',
                }}
              />
            </div>

            {isOverload && (
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                  fontSize: '10px',
                  color: 'var(--accent-warning)',
                  fontWeight: '600',
                }}
              >
                <AlertTriangle size={10} /> Overload (+{((totalMinutes - maxMinutes) / 60).toFixed(1)}h)
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
