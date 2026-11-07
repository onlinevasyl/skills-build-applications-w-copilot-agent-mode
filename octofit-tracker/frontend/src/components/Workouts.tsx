import { useEffect, useState } from 'react';
import { apiEndpoint, getCollection } from '../api/client.js';
import DataTable from './DataTable.js';

type Workout = {
  id?: string;
  title: string;
  focus?: string;
  minutes?: number;
  difficulty?: string;
  reason?: string;
};
const endpoint = apiEndpoint(`/api/workouts/suggestions/${encodeURIComponent('mona@example.com')}`);

export default function Workouts() {
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    console.log('Workouts REST API endpoint:', endpoint);
    getCollection<Workout>(endpoint, 'suggestions')
      .then((data) => {
        console.log('Workouts fetched data:', data);
        if (active) setWorkouts(data);
      })
      .catch((cause: unknown) => {
        if (active) setError(cause instanceof Error ? cause.message : 'Unable to load workouts.');
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => { active = false; };
  }, []);

  return (
    <DataTable
      title="Workout suggestions"
      description="Recommended sessions tailored to current fitness goals."
      rows={workouts}
      columns={[
        { key: 'workout', header: 'Workout', render: (workout) => <span className="fw-semibold">{workout.title}</span> },
        { key: 'focus', header: 'Focus', render: (workout) => workout.focus || '—' },
        { key: 'duration', header: 'Duration', render: (workout) => workout.minutes !== undefined ? `${workout.minutes} min` : '—' },
        { key: 'difficulty', header: 'Difficulty', render: (workout) => workout.difficulty || '—' },
        { key: 'reason', header: 'Why this workout', render: (workout) => workout.reason || '—' },
      ]}
      rowKey={(workout, index) => workout.id ?? `${workout.title}-${index}`}
      loading={loading}
      error={error}
      emptyMessage="No workout suggestions found yet."
    />
  );
}
