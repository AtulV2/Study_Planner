import React, { useState } from 'react';
import { useSchedule } from './hooks/useSchedule';
import { CommandBar } from './components/canvas/CommandBar';
import { BurnoutMeter } from './components/canvas/BurnoutMeter';
import { MicroActionBanner } from './components/recovery/MicroActionBanner';
import { WeeklyCanvas } from './components/canvas/WeeklyCanvas';
import { RecoveryModal } from './components/recovery/RecoveryModal';
import { CourseModal } from './components/forms/CourseModal';
import { CommitmentModal } from './components/forms/CommitmentModal';
import { DeadlineModal } from './components/forms/DeadlineModal';
import { Toast } from './components/common/Toast';

export function App() {
  const {
    courses,
    coursesMap,
    days,
    dailyStats,
    config,
    microAction,
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
  } = useSchedule();

  const [isRecoveryOpen, setIsRecoveryOpen] = useState(false);
  const [isCourseModalOpen, setIsCourseModalOpen] = useState(false);
  const [isCommitmentModalOpen, setIsCommitmentModalOpen] = useState(false);
  const [isDeadlineModalOpen, setIsDeadlineModalOpen] = useState(false);

  const handleStartMicroAction = (action) => {
    if (action.block_id) {
      updateBlockStatus(action.block_id, 'completed');
    } else {
      setToast({ message: `Sprint timer started for "${action.title}"! Focus for ${action.duration_minutes}m.`, type: 'success' });
    }
  };

  const handleRecoveryApplied = (result, strategy) => {
    loadAll();
    setToast({
      message: `Recovery plan applied successfully (${strategy}). Schedule realigned!`,
      type: 'success',
    });
  };

  return (
    <div className="app-container">
      {/* 1. Global Command Bar */}
      <CommandBar
        onOpenRecovery={() => setIsRecoveryOpen(true)}
        onOpenCourseModal={() => setIsCourseModalOpen(true)}
        onOpenCommitmentModal={() => setIsCommitmentModalOpen(true)}
        onOpenDeadlineModal={() => setIsDeadlineModalOpen(true)}
        onSeedDemo={seedDemo}
        onAutoFitAll={autoFitAll}
        missedCount={missedCount}
      />

      {/* 2. Burnout Guardrail Meter */}
      <BurnoutMeter
        dailyStats={dailyStats}
        maxDailyHours={config?.max_daily_study_hours || 5.5}
      />

      {/* Main Content Area */}
      <main className="main-content">
        {/* Micro-Action Starter Banner */}
        <MicroActionBanner
          microAction={microAction}
          onStartMicroAction={handleStartMicroAction}
        />

        {/* 3. The Weekly Canvas Grid */}
        <WeeklyCanvas
          days={days}
          coursesMap={coursesMap}
          onUpdateStatus={updateBlockStatus}
          onDeleteEvent={deleteItem}
        />
      </main>

      {/* Modals & Dialogs */}
      <RecoveryModal
        isOpen={isRecoveryOpen}
        onClose={() => setIsRecoveryOpen(false)}
        onRecoveryApplied={handleRecoveryApplied}
      />

      <CourseModal
        isOpen={isCourseModalOpen}
        onClose={() => setIsCourseModalOpen(false)}
        onSave={addCourse}
      />

      <CommitmentModal
        isOpen={isCommitmentModalOpen}
        onClose={() => setIsCommitmentModalOpen(false)}
        courses={courses}
        onSave={addCommitment}
      />

      <DeadlineModal
        isOpen={isDeadlineModalOpen}
        onClose={() => setIsDeadlineModalOpen(false)}
        courses={courses}
        onSave={addDeadline}
      />

      {/* Non-blocking Toast */}
      <Toast toast={toast} onDismiss={() => setToast(null)} />
    </div>
  );
}

export default App;
