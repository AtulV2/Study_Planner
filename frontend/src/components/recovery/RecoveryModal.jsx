import React, { useState, useEffect } from 'react';
import { RefreshCw, ArrowRight, CheckCircle2, ShieldAlert, Sparkles, Clock, AlertTriangle } from 'lucide-react';
import { Modal } from '../common/Modal';
import { Button } from '../common/Button';
import { api } from '../../services/api';

export function RecoveryModal({
  isOpen,
  onClose,
  onRecoveryApplied,
}) {
  const [activeTab, setActiveTab] = useState('auto_heal'); // 'auto_heal', 'triage', 'shift_today'
  const [previewData, setPreviewData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isApplying, setIsApplying] = useState(false);
  const [shiftMinutes, setShiftMinutes] = useState(60);

  useEffect(() => {
    if (isOpen) {
      loadPreview(activeTab);
    }
  }, [isOpen, activeTab]);

  const loadPreview = async (tab) => {
    setIsLoading(true);
    try {
      if (tab === 'auto_heal') {
        const res = await api.previewRecovery('auto_heal');
        setPreviewData(res);
      } else {
        setPreviewData(null);
      }
    } catch (err) {
      console.error('Failed to load preview diff:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleApply = async () => {
    setIsApplying(true);
    try {
      let result;
      if (activeTab === 'auto_heal') {
        result = await api.autoHeal();
      } else if (activeTab === 'triage') {
        result = await api.triageMvp();
      } else if (activeTab === 'shift_today') {
        result = await api.shiftToday(shiftMinutes);
      }
      onRecoveryApplied(result, activeTab);
      onClose();
    } catch (err) {
      alert(`Recovery failed: ${err.message}`);
    } finally {
      setIsApplying(false);
    }
  };

  const tabs = [
    { id: 'auto_heal', label: '1. Auto-Heal Buffers' },
    { id: 'triage', label: '2. Triage (MVP Mode)' },
    { id: 'shift_today', label: '3. Shift Today' },
  ];

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Dynamic Schedule Recovery"
      maxWidth="680px"
      footer={
        <>
          <Button variant="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button variant="recovery" onClick={handleApply} disabled={isApplying || isLoading}>
            {isApplying ? 'Applying Plan...' : 'Apply Recovery Plan'}
          </Button>
        </>
      }
    >
      <div>
        {/* Strategy Tabs */}
        <div
          style={{
            display: 'flex',
            borderBottom: '1px solid var(--border-subtle)',
            marginBottom: '16px',
          }}
        >
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                padding: '8px 14px',
                fontSize: '13px',
                fontWeight: '600',
                border: 'none',
                background: 'none',
                cursor: 'pointer',
                borderBottom: activeTab === tab.id ? '2px solid var(--accent-recovery)' : '2px solid transparent',
                color: activeTab === tab.id ? 'var(--accent-recovery)' : 'var(--text-secondary)',
                marginBottom: '-1px',
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab 1: Auto-Heal Diff */}
        {activeTab === 'auto_heal' && (
          <div>
            <div style={{ marginBottom: '14px', fontSize: '13px', color: 'var(--text-secondary)' }}>
              Locates all disrupted/missed study sessions and mathematically fits them into upcoming buffer gaps without breaching the 5.5h daily cognitive cap.
            </div>

            {isLoading ? (
              <div style={{ padding: '30px', textAlign: 'center', color: 'var(--text-muted)' }}>
                Evaluating available calendar gaps...
              </div>
            ) : previewData?.changes?.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: '1fr 24px 1fr',
                    fontSize: '11px',
                    fontWeight: '700',
                    color: 'var(--text-muted)',
                    textTransform: 'uppercase',
                    padding: '0 8px',
                  }}
                >
                  <span>Before (Disrupted)</span>
                  <span />
                  <span>After (Healed)</span>
                </div>

                {previewData.changes.map((change, idx) => (
                  <div
                    key={idx}
                    style={{
                      display: 'grid',
                      gridTemplateColumns: '1fr 24px 1fr',
                      alignItems: 'center',
                      gap: '8px',
                      padding: '10px 12px',
                      backgroundColor: 'var(--bg-surface-subtle)',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--border-subtle)',
                    }}
                  >
                    <div>
                      <div className="title-card" style={{ fontSize: '12px' }}>
                        {change.title}
                      </div>
                      <span className="mono" style={{ fontSize: '11px', color: 'var(--accent-danger)' }}>
                        {change.original_slot || 'Missed slot'}
                      </span>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'center', color: 'var(--accent-recovery)' }}>
                      <ArrowRight size={14} />
                    </div>

                    <div>
                      <div className="title-card" style={{ fontSize: '12px', color: 'var(--accent-safe)' }}>
                        {change.status_change}
                      </div>
                      <span className="mono" style={{ fontSize: '11px', color: 'var(--accent-safe)' }}>
                        {change.proposed_slot || 'Reallocated'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div
                style={{
                  padding: '24px',
                  textAlign: 'center',
                  backgroundColor: 'var(--bg-surface-subtle)',
                  borderRadius: 'var(--radius-md)',
                  color: 'var(--text-secondary)',
                  fontSize: '13px',
                }}
              >
                <CheckCircle2 size={24} color="var(--accent-safe)" style={{ margin: '0 auto 8px' }} />
                No missed sessions detected. Your calendar is currently in sync!
              </div>
            )}
          </div>
        )}

        {/* Tab 2: Triage MVP Mode */}
        {activeTab === 'triage' && (
          <div>
            <div style={{ marginBottom: '14px', fontSize: '13px', color: 'var(--text-secondary)' }}>
              When scheduled workload exceeds total available hours before deadlines, Triage mode scales down non-critical assignments to protect your exam prep and health:
            </div>

            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '8px',
                marginBottom: '16px',
              }}
            >
              <div
                style={{
                  padding: '10px 14px',
                  borderRadius: 'var(--radius-md)',
                  backgroundColor: 'var(--bg-surface-subtle)',
                  border: '1px solid var(--border-subtle)',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div>
                  <div style={{ fontWeight: '600', fontSize: '13px' }}>Low Priority Deliverables</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Optional readings, minor homework</div>
                </div>
                <span className="mono" style={{ color: 'var(--accent-safe)', fontWeight: '700', fontSize: '13px' }}>
                  -30% Study Hours
                </span>
              </div>

              <div
                style={{
                  padding: '10px 14px',
                  borderRadius: 'var(--radius-md)',
                  backgroundColor: 'var(--bg-surface-subtle)',
                  border: '1px solid var(--border-subtle)',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div>
                  <div style={{ fontWeight: '600', fontSize: '13px' }}>Medium Priority Deliverables</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Regular assignments, quizzes</div>
                </div>
                <span className="mono" style={{ color: 'var(--accent-warning)', fontWeight: '700', fontSize: '13px' }}>
                  -20% Study Hours
                </span>
              </div>

              <div
                style={{
                  padding: '10px 14px',
                  borderRadius: 'var(--radius-md)',
                  backgroundColor: 'var(--bg-surface-subtle)',
                  border: '1px solid var(--border-subtle)',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div>
                  <div style={{ fontWeight: '600', fontSize: '13px' }}>High Priority (Exams & Capstones)</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Core exams and major projects</div>
                </div>
                <span className="mono" style={{ color: 'var(--text-primary)', fontWeight: '700', fontSize: '13px' }}>
                  100% Protected (0% cut)
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: Shift Today */}
        {activeTab === 'shift_today' && (
          <div>
            <div style={{ marginBottom: '14px', fontSize: '13px', color: 'var(--text-secondary)' }}>
              Falling behind schedule today? Push today's remaining sessions forward. If study crosses your configured bedtime (23:00), it safely cascades into tomorrow morning.
            </div>

            <div className="form-group">
              <label className="form-label">Shift Duration</label>
              <select
                className="form-control"
                value={shiftMinutes}
                onChange={(e) => setShiftMinutes(Number(e.target.value))}
              >
                <option value={30}>Shift forward 30 minutes</option>
                <option value={60}>Shift forward 1 hour (60 min)</option>
                <option value={90}>Shift forward 1.5 hours (90 min)</option>
                <option value={120}>Shift forward 2 hours (120 min)</option>
              </select>
            </div>
          </div>
        )}
      </div>
    </Modal>
  );
}
