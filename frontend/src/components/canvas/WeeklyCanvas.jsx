import React from 'react';
import { EventCard } from './EventCard';
import { Sparkles, Calendar } from 'lucide-react';

export function WeeklyCanvas({
  days = [],
  coursesMap = {},
  onUpdateStatus,
  onDeleteEvent,
}) {
  const hasAnyEvents = days.some(
    (d) => (d.fixedCommitments?.length || 0) + (d.studyBlocks?.length || 0) > 0
  );

  if (!hasAnyEvents) {
    return (
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '80px 24px',
          textAlign: 'center',
          backgroundColor: 'var(--bg-surface)',
          borderRadius: 'var(--radius-xl)',
          border: '1px dashed var(--border-strong)',
          margin: '24px 0',
        }}
      >
        <div
          style={{
            width: '48px',
            height: '48px',
            borderRadius: '24px',
            backgroundColor: 'var(--bg-surface-subtle)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--accent-focus)',
            marginBottom: '16px',
          }}
        >
          <Calendar size={24} />
        </div>
        <h3 className="title-section" style={{ marginBottom: '8px' }}>
          Your week is completely open
        </h3>
        <p className="text-body" style={{ color: 'var(--text-secondary)', maxWidth: '440px', marginBottom: '20px' }}>
          Add your recurring classes and upcoming assignments, or click <strong>Seed Demo Week</strong> in the command bar to explore a realistic workload scenario.
        </p>
      </div>
    );
  }

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(7, 1fr)',
        gap: '12px',
        marginTop: '16px',
        alignItems: 'start',
      }}
    >
      {days.map((day, idx) => {
        const isToday = day.isToday;
        return (
          <div
            key={idx}
            style={{
              backgroundColor: 'var(--bg-surface)',
              borderRadius: 'var(--radius-xl)',
              border: isToday ? '2px solid var(--accent-focus)' : '1px solid var(--border-subtle)',
              overflow: 'hidden',
              boxShadow: 'var(--shadow-sm)',
              minHeight: '600px',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            {/* Column Day Header */}
            <div
              style={{
                padding: '10px 12px',
                borderBottom: '1px solid var(--border-subtle)',
                backgroundColor: isToday ? 'var(--accent-focus-light)' : 'var(--bg-surface-subtle)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
              }}
            >
              <div>
                <span
                  style={{
                    fontSize: '11px',
                    fontWeight: '700',
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase',
                    color: isToday ? 'var(--accent-focus)' : 'var(--text-secondary)',
                  }}
                >
                  {day.dayName}
                </span>
                <div className="title-card" style={{ fontSize: '14px', marginTop: '1px' }}>
                  {day.dateString}
                </div>
              </div>
              {isToday && (
                <span
                  style={{
                    backgroundColor: 'var(--accent-focus)',
                    color: 'var(--text-inverse)',
                    fontSize: '9px',
                    fontWeight: '700',
                    padding: '2px 5px',
                    borderRadius: 'var(--radius-sm)',
                    textTransform: 'uppercase',
                  }}
                >
                  Today
                </span>
              )}
            </div>

            {/* Event List Container */}
            <div style={{ padding: '10px', flex: 1, overflowY: 'auto' }}>
              {/* Fixed Commitments (Solid Pillars) */}
              {day.fixedCommitments && day.fixedCommitments.length > 0 && (
                <div style={{ marginBottom: '12px' }}>
                  <div
                    style={{
                      fontSize: '10px',
                      fontWeight: '700',
                      letterSpacing: '0.05em',
                      textTransform: 'uppercase',
                      color: 'var(--text-muted)',
                      marginBottom: '6px',
                    }}
                  >
                    Anchors & Classes
                  </div>
                  {day.fixedCommitments.map((fc) => (
                    <EventCard
                      key={`fc-${fc.id}`}
                      item={fc}
                      isFixed={true}
                      course={coursesMap[fc.course_id]}
                      onDelete={onDeleteEvent}
                    />
                  ))}
                </div>
              )}

              {/* Flexible Study Blocks */}
              <div>
                <div
                  style={{
                    fontSize: '10px',
                    fontWeight: '700',
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase',
                    color: 'var(--text-muted)',
                    marginBottom: '6px',
                  }}
                >
                  Study Sessions
                </div>
                {day.studyBlocks && day.studyBlocks.length > 0 ? (
                  day.studyBlocks.map((sb) => (
                    <EventCard
                      key={`sb-${sb.id}`}
                      item={sb}
                      isFixed={false}
                      onUpdateStatus={onUpdateStatus}
                      onDelete={onDeleteEvent}
                    />
                  ))
                ) : (
                  <div
                    style={{
                      padding: '16px 8px',
                      textAlign: 'center',
                      color: 'var(--text-muted)',
                      fontSize: '11px',
                      border: '1px dashed var(--border-subtle)',
                      borderRadius: 'var(--radius-md)',
                    }}
                  >
                    No focus sessions scheduled
                  </div>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
