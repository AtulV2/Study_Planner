/**
 * Study Planner REST API Client
 */

const BASE_URL = '/api/v1';

async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  const response = await fetch(url, { ...options, headers });

  if (response.status === 204) {
    return null;
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const errorMsg = data?.error?.message || data?.detail || `HTTP ${response.status} error`;
    const err = new Error(errorMsg);
    err.status = response.status;
    err.details = data?.error?.details || null;
    throw err;
  }

  return data;
}

export const api = {
  // Diagnostics
  getHealth: () => request('/health'),
  seedScenario: () => request('/seed', { method: 'POST' }),

  // Config
  getConfig: () => request('/config'),
  updateConfig: (payload) => request('/config', { method: 'PATCH', body: JSON.stringify(payload) }),

  // Courses
  getCourses: () => request('/courses'),
  createCourse: (payload) => request('/courses', { method: 'POST', body: JSON.stringify(payload) }),
  updateCourse: (id, payload) => request(`/courses/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }),
  deleteCourse: (id) => request(`/courses/${id}`, { method: 'DELETE' }),

  // Commitments
  getCommitments: () => request('/commitments'),
  createCommitment: (payload) => request('/commitments', { method: 'POST', body: JSON.stringify(payload) }),
  updateCommitment: (id, payload) => request(`/commitments/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }),
  deleteCommitment: (id) => request(`/commitments/${id}`, { method: 'DELETE' }),

  // Deadlines
  getDeadlines: () => request('/deadlines'),
  createDeadline: (payload) => request('/deadlines', { method: 'POST', body: JSON.stringify(payload) }),
  updateDeadline: (id, payload) => request(`/deadlines/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }),
  deleteDeadline: (id) => request(`/deadlines/${id}`, { method: 'DELETE' }),
  autoScheduleDeadline: (id) => request(`/deadlines/${id}/auto-schedule`, { method: 'POST' }),

  // Study Blocks
  getStudyBlocks: () => request('/study-blocks'),
  createStudyBlock: (payload) => request('/study-blocks', { method: 'POST', body: JSON.stringify(payload) }),
  updateStudyBlock: (id, payload) => request(`/study-blocks/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }),
  deleteStudyBlock: (id) => request(`/study-blocks/${id}`, { method: 'DELETE' }),
  autoFitAll: () => request('/schedule/auto-fit-all', { method: 'POST' }),

  // Recovery
  previewRecovery: (strategy = 'auto_heal') => request(`/recovery/preview?strategy=${strategy}`, { method: 'POST' }),
  autoHeal: () => request('/recovery/auto-heal', { method: 'POST' }),
  triageMvp: () => request('/recovery/triage-mvp', { method: 'POST' }),
  shiftToday: (shiftMinutes = 60) => request('/recovery/shift-today', {
    method: 'POST',
    body: JSON.stringify({ shift_minutes: shiftMinutes }),
  }),
  getMicroAction: () => request('/recovery/micro-action'),
  getRecoveryHistory: () => request('/recovery/history'),
};
