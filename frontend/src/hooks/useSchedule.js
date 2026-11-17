import { useState, useEffect, useCallback } from 'react';
import { api } from '../services/api';

export function useSchedule() {
  const [courses, setCourses] = useState([]);
  const [commitments, setCommitments] = useState([]);
  const [deadlines, setDeadlines] = useState([]);
  const [studyBlocks, setStudyBlocks] = useState([]);
  const [config, setConfig] = useState(null);
  const [microAction, setMicroAction] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [toast, setToast] = useState(null);

  // Compute Monday of current week
  const getMonday = (d) => {
    const date = new Date(d);
    const day = date.getDay();
    const diff = date.getDate() - day + (day === 0 ? -6 : 1);
    return new Date(date.setDate(diff));
  };

  const [currentWeekStart, setCurrentWeekStart] = useState(() => getMonday(new Date()));

  const showToast = (message, type = 'success', undoAction = null) => {
    setToast({ message, type, undoAction });
    setTimeout(() => setToast(null), 5000);
  };

  const loadAll = useCallback(async () => {
    setIsLoading(true);
    try {
      const [coursesRes, commitmentsRes, deadlinesRes, blocksRes, configRes, microRes] = await Promise.all([
        api.getCourses(),
        api.getCommitments(),
        api.getDeadlines(),
        api.getStudyBlocks(),
        api.getConfig(),
        api.getMicroAction().catch(() => null),
      ]);

      setCourses(coursesRes || []);
      setCommitments(commitmentsRes || []);
      setDeadlines(deadlinesRes || []);
      setStudyBlocks(blocksRes || []);
      setConfig(configRes || { max_daily_study_hours: 5.5 });
      setMicroAction(microRes || null);
    } catch (err) {
      console.error('Error loading schedule state:', err);
      showToast(err.message, 'error');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadAll();
  }, [loadAll]);

  // Map courses by ID
  const coursesMap = courses.reduce((acc, c) => {
    acc[c.id] = c;
    return acc;
  }, {});

  // Build 7 calendar days (Mon - Sun)
  const days = Array.from({ length: 7 }).map((_, idx) => {
    const dayDate = new Date(currentWeekStart);
    dayDate.setDate(currentWeekStart.getDate() + idx);
    const dayDateStr = dayDate.toISOString().split('T')[0];

    const todayStr = new Date().toISOString().split('T')[0];
    const isToday = dayDateStr === todayStr;

    // Commitments for this day of week (0=Mon, 6=Sun)
    const dayCommitments = commitments.filter((c) => c.day_of_week === idx);

    // Study blocks for this day
    const dayStudyBlocks = studyBlocks.filter((b) => {
      const bDateStr = new Date(b.start_datetime).toISOString().split('T')[0];
      return bDateStr === dayDateStr;
    });

    const studyMinutes = dayStudyBlocks
      .filter((b) => ['scheduled', 'completed', 'recovered'].includes(b.status))
      .reduce((sum, b) => sum + (b.duration_minutes || 0), 0);

    const dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

    return {
      dayIndex: idx,
      dayName: dayNames[idx],
      dateString: dayDate.toLocaleDateString([], { month: 'short', day: 'numeric' }),
      fullDateStr: dayDateStr,
      isToday,
      fixedCommitments: dayCommitments,
      studyBlocks: dayStudyBlocks,
      studyMinutes,
    };
  });

  // Daily stats for Burnout Meter
  const dailyStats = days.map((d) => ({
    dayName: d.dayName,
    studyMinutes: d.studyMinutes,
  }));

  // Actions
  const updateBlockStatus = async (blockId, status) => {
    const prevBlocks = [...studyBlocks];
    // Optimistic UI update
    setStudyBlocks((prev) =>
      prev.map((b) => (b.id === blockId ? { ...b, status } : b))
    );

    try {
      await api.updateStudyBlock(blockId, { status });
      showToast(`Session marked as ${status}`);
    } catch (err) {
      setStudyBlocks(prevBlocks);
      showToast(`Failed to update session: ${err.message}`, 'error');
    }
  };

  const deleteItem = async (id, isFixed) => {
    try {
      if (isFixed) {
        await api.deleteCommitment(id);
        setCommitments((prev) => prev.filter((c) => c.id !== id));
        showToast('Fixed anchor removed');
      } else {
        await api.deleteStudyBlock(id);
        setStudyBlocks((prev) => prev.filter((b) => b.id !== id));
        showToast('Study session deleted');
      }
    } catch (err) {
      showToast(`Delete failed: ${err.message}`, 'error');
    }
  };

  const seedDemo = async () => {
    try {
      await api.seedScenario();
      showToast('Realistic demo schedule seeded successfully');
      await loadAll();
    } catch (err) {
      showToast(`Seed failed: ${err.message}`, 'error');
    }
  };

  const autoFitAll = async () => {
    try {
      const res = await api.autoFitAll();
      showToast(`Auto-fit completed: ${res.study_blocks_created} sessions allocated`);
      await loadAll();
    } catch (err) {
      showToast(`Auto-fit failed: ${err.message}`, 'error');
    }
  };

  const addCourse = async (payload) => {
    const res = await api.createCourse(payload);
    setCourses((prev) => [...prev, res]);
    showToast(`Course '${res.code}' enrolled`);
    return res;
  };

  const addCommitment = async (payload) => {
    const res = await api.createCommitment(payload);
    setCommitments((prev) => [...prev, res]);
    showToast(`Fixed anchor '${res.title}' added`);
    return res;
  };

  const addDeadline = async (payload, autoFit = true) => {
    const res = await api.createDeadline(payload);
    setDeadlines((prev) => [...prev, res]);
    if (autoFit) {
      await api.autoScheduleDeadline(res.id);
      showToast(`Deadline created & study sessions auto-allocated`);
    } else {
      showToast(`Deadline '${res.title}' created`);
    }
    await loadAll();
    return res;
  };

  // Count missed sessions
  const missedCount = studyBlocks.filter((b) => b.status === 'missed').length;

  return {
    courses,
    coursesMap,
    commitments,
    deadlines,
    studyBlocks,
    config,
    microAction,
    days,
    dailyStats,
    isLoading,
    toast,
    missedCount,
    loadAll,
    updateBlockStatus,
    deleteItem,
    seedDemo,
    autoFitAll,
    addCourse,
    addCommitment,
    addDeadline,
    setToast,
  };
}
