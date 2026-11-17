import React, { useState } from 'react';
import { Modal } from '../common/Modal';
import { Button } from '../common/Button';

export function DeadlineModal({ isOpen, onClose, courses = [], onSave }) {
  const [courseId, setCourseId] = useState('');
  const [title, setTitle] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [dueTime, setDueTime] = useState('23:59');
  const [estimatedHours, setEstimatedHours] = useState('4.0');
  const [priority, setPriority] = useState('high');
  const [notes, setNotes] = useState('');
  const [autoScheduleNow, setAutoScheduleNow] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !courseId || !dueDate) return;

    setIsSubmitting(true);
    try {
      const due_datetime = new Date(`${dueDate}T${dueTime}:00Z`).toISOString();
      await onSave(
        {
          course_id: Number(courseId),
          title,
          due_datetime,
          estimated_hours: parseFloat(estimatedHours),
          priority,
          notes: notes || null,
        },
        autoScheduleNow
      );
      setTitle('');
      setNotes('');
      onClose();
    } catch (err) {
      alert(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Add Assignment / Exam Deadline"
      footer={
        <>
          <Button variant="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleSubmit} disabled={isSubmitting}>
            {isSubmitting ? 'Saving...' : 'Add Deadline'}
          </Button>
        </>
      }
    >
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Deliverable Title *</label>
          <input
            className="form-control"
            placeholder="e.g. Problem Set 3 — Balanced Trees"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Course *</label>
          <select
            className="form-control"
            value={courseId}
            onChange={(e) => setCourseId(e.target.value)}
            required
          >
            <option value="">Select Course...</option>
            {courses.map((c) => (
              <option key={c.id} value={c.id}>
                {c.code} — {c.name}
              </option>
            ))}
          </select>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          <div className="form-group">
            <label className="form-label">Due Date *</label>
            <input
              type="date"
              className="form-control"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Due Time</label>
            <input
              type="time"
              className="form-control"
              value={dueTime}
              onChange={(e) => setDueTime(e.target.value)}
              required
            />
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          <div className="form-group">
            <label className="form-label">Estimated Study Hours</label>
            <input
              type="number"
              step="0.5"
              min="0.5"
              max="40"
              className="form-control"
              value={estimatedHours}
              onChange={(e) => setEstimatedHours(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Priority</label>
            <select
              className="form-control"
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
            >
              <option value="high">High (Exams, Major Projects)</option>
              <option value="medium">Medium (Regular Assignments)</option>
              <option value="low">Low (Optional Reading, Extra Credit)</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Notes (Optional)</label>
          <textarea
            className="form-control"
            rows="2"
            placeholder="Focus areas, key readings, or sub-deliverables..."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '12px' }}>
          <input
            type="checkbox"
            id="autoScheduleCheck"
            checked={autoScheduleNow}
            onChange={(e) => setAutoScheduleNow(e.target.checked)}
          />
          <label htmlFor="autoScheduleCheck" style={{ fontSize: '13px', color: 'var(--text-primary)', cursor: 'pointer' }}>
            Auto-schedule study blocks into free gaps before deadline
          </label>
        </div>
      </form>
    </Modal>
  );
}
