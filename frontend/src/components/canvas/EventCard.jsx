import React, { useState } from 'react';
import { Check, AlertCircle, Trash2, Clock, MapPin, Undo2 } from 'lucide-react';
import { Badge } from '../common/Badge';

export function EventCard({
  item,
  isFixed = false,
  course = null,
  onUpdateStatus,
  onDelete,
}) {
  const [isHovered, setIsHovered] = useState(false);

  // Format time display
  const timeDisplay = isFixed
    ? `${item.start_time} – ${item.end_time}`
    : `${new Date(item.start_datetime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false })} – ${new Date(item.end_datetime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false })}`;

  const courseColor = course?.color || '#3B82F6';

  if (isFixed) {
    return (
      <div
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        style={{
          backgroundColor: 'var(--bg-surface)',
          border: '1px solid var(--border-subtle)',
          borderLeft: `3px solid ${courseColor}`,
          borderRadius: 'var(--radius-md)',
          padding: '8px 10px',
          marginBottom: '8px',
          boxShadow: 'var(--shadow-sm)',
          position: 'relative',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2px' }}>
          <span className="mono" style={{ fontSize: '10px', fontWeight: '700', color: courseColor }}>
            {course ? course.code : 'FIXED'}
          </span>
          <span className="text-time" style={{ color: 'var(--text-muted)' }}>
            {timeDisplay}
          </span>
        </div>

        <div className="title-card" style={{ color: 'var(--text-primary)', marginBottom: '4px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {item.title}
        </div>

        {item.location && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', color: 'var(--text-secondary)' }}>
            <MapPin size={11} /> {item.location}
          </div>
        )}

        {isHovered && (
          <div
            style={{
              position: 'absolute',
              top: '6px',
              right: '6px',
              display: 'flex',
              gap: '4px',
              backgroundColor: 'var(--bg-surface)',
              padding: '2px',
              borderRadius: 'var(--radius-sm)',
              boxShadow: 'var(--shadow-sm)',
            }}
          >
            <button
              onClick={() => onDelete(item.id, true)}
              title="Delete Fixed Commitment"
              style={{
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                color: 'var(--text-muted)',
                padding: '2px',
              }}
            >
              <Trash2 size={13} />
            </button>
          </div>
        )}
      </div>
    );
  }

  // Flexible Study Block Card
  const isCompleted = item.status === 'completed';
  const isMissed = item.status === 'missed';
  const isRecovered = item.status === 'recovered';

  const cardBorder = isMissed
    ? '1px solid var(--accent-danger)'
    : isRecovered
    ? '1px dashed var(--accent-recovery)'
    : isCompleted
    ? '1px solid var(--border-subtle)'
    : '1px solid var(--border-subtle)';

  const cardBg = isCompleted
    ? 'var(--bg-surface-subtle)'
    : isMissed
    ? 'var(--accent-danger-light)'
    : isRecovered
    ? 'var(--accent-recovery-light)'
    : 'var(--bg-surface)';

  return (
    <div
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        backgroundColor: cardBg,
        border: cardBorder,
        borderRadius: 'var(--radius-lg)',
        padding: '10px',
        marginBottom: '8px',
        boxShadow: 'var(--shadow-sm)',
        position: 'relative',
        transition: 'all 0.15s ease',
        opacity: isCompleted ? 0.75 : 1.0,
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
        <Badge variant={item.status}>{item.status}</Badge>
        <span className="text-time" style={{ color: 'var(--text-muted)' }}>
          {timeDisplay}
        </span>
      </div>

      <div
        className="title-card"
        style={{
          color: 'var(--text-primary)',
          textDecoration: isCompleted ? 'line-through' : 'none',
          marginBottom: '4px',
        }}
      >
        {item.title}
      </div>

      {item.notes && (
        <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: '4px', fontStyle: 'italic' }}>
          {item.notes}
        </div>
      )}

      {/* Action Buttons on Hover */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-end',
          justifyContent: 'flex-start',
          gap: '4px',
          marginTop: '6px',
          paddingTop: '6px',
          borderTop: '1px solid var(--border-subtle)',
        }}
      >
        {!isCompleted ? (
          <button
            onClick={() => onUpdateStatus(item.id, 'completed')}
            title="Mark as Completed"
            style={{
              background: 'none',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-sm)',
              padding: '3px 6px',
              fontSize: '11px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              color: 'var(--accent-safe)',
            }}
          >
            <Check size={12} /> Complete
          </button>
        ) : (
          <button
            onClick={() => onUpdateStatus(item.id, 'scheduled')}
            title="Undo Completion"
            style={{
              background: 'none',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-sm)',
              padding: '3px 6px',
              fontSize: '11px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              color: 'var(--text-secondary)',
            }}
          >
            <Undo2 size={12} /> Undo
          </button>
        )}

        {!isMissed && !isCompleted && (
          <button
            onClick={() => onUpdateStatus(item.id, 'missed')}
            title="Mark as Missed (Triggers Auto-Heal)"
            style={{
              background: 'none',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-sm)',
              padding: '3px 6px',
              fontSize: '11px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              color: 'var(--accent-danger)',
            }}
          >
            <AlertCircle size={12} /> Missed
          </button>
        )}

        <button
          onClick={() => onDelete(item.id, false)}
          title="Delete Study Session"
          style={{
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            color: 'var(--text-muted)',
            padding: '3px',
          }}
        >
          <Trash2 size={13} />
        </button>
      </div>
    </div>
  );
}
