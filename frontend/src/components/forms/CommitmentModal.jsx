import React, { useState } from 'react';
import { Modal } from '../common/Modal';
import { Button } from '../common/Button';

export function CommitmentModal({ isOpen, onClose, courses = [], onSave }) {
  const [courseId, setCourseId] = useState('');
  const [title, setTitle] = useState('');
  const [commitmentType, setCommitmentType] = useState('lecture');
  const [dayOfWeek, setDayOfWeek] = useState(0);
  const [startTime, setStartTime] = useState('10:00');
  const [endTime, setEndTime] = useState('11:30');
  const [location, setLocation] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsSubmitting(true);
    try {
      await onSave({
        course_id: courseId ? Number(courseId) : null,
        title,
        commitment_type: commitmentType,
        day_of_week: Number(dayOfWeek),
        start_time: startTime,
        end_time: endTime,
        location: location || null,
      });
      setTitle('');
      setLocation('');
      onClose();
    } catch (err) {
      alert(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const days = [
    { id: 0, label: 'Monday' },
    { id: 1, label: 'Tuesday' },
    { id: 2, label: 'Wednesday' },
    { id: 3, label: 'Thursday' },
    { id: 4, label: 'Friday' },
    { id: 5, label: 'Saturday' },
    { id: 6, label: 'Sunday' },
  ];

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Add Fixed Calendar Anchor"
      footer={
        <>
          <Button variant="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleSubmit} disabled={isSubmitting}>
            {isSubmitting ? 'Saving...' : 'Add Anchor'}
          </Button>
        </>
      }
    >
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Title *</label>
          <input
            className="form-control"
            placeholder="e.g. CS 240 Lecture or Campus Job"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Associated Course (Optional)</label>
          <select
            className="form-control"
            value={courseId}
            onChange={(e) => setCourseId(e.target.value)}
          >
            <option value="">None (Personal / Work Shift)</option>
            {courses.map((c) => (
              <option key={c.id} value={c.id}>
                {c.code} — {c.name}
              </option>
            ))}
          </select>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          <div className="form-group">
            <label className="form-label">Type</label>
            <select
              className="form-control"
              value={commitmentType}
              onChange={(e) => setCommitmentType(e.target.value)}
            >
              <option value="lecture">Lecture</option>
              <option value="lab">Lab</option>
              <option value="discussion">Discussion</option>
              <option value="work">Work Shift</option>
              <option value="sport">Athletics</option>
              <option value="personal">Personal</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Day of Week</label>
            <select
              className="form-control"
              value={dayOfWeek}
              onChange={(e) => setDayOfWeek(e.target.value)}
            >
              {days.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          <div className="form-group">
            <label className="form-label">Start Time (24h)</label>
            <input
              type="time"
              className="form-control"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">End Time (24h)</label>
            <input
              type="time"
              className="form-control"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Location (Optional)</label>
          <input
            className="form-control"
            placeholder="e.g. Turing Hall 101"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
        </div>
      </form>
    </Modal>
  );
}
