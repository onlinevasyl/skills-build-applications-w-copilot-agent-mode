import { useEffect, useState } from 'react';
import { apiEndpoint, getCollection } from '../api/client.js';
import DataTable from './DataTable.js';

type Activity = {
  id?: string;
  type: string;
  minutes: number;
  points: number;
  user?: string;
  team?: string;
  occurredAt?: string;
};

const endpoint = apiEndpoint('/api/activities/');

export default function Activities() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    console.log('Activities REST API endpoint:', endpoint);
    getCollection<Activity>(endpoint, 'activities')
      .then((data) => {
        console.log('Activities fetched data:', data);
        if (active) setActivities(data);
      })
      .catch((cause: unknown) => {
        if (active) setError(cause instanceof Error ? cause.message : 'Unable to load activities.');
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => { active = false; };
  }, []);

  return (
    <DataTable
      title="Activities"
      description="Track activity minutes and points across your teams."
      rows={activities}
      columns={[
        { key: 'activity', header: 'Activity', render: (activity) => <span className="fw-semibold text-capitalize">{activity.type}</span> },
        { key: 'minutes', header: 'Minutes', render: (activity) => activity.minutes },
        { key: 'points', header: 'Points', render: (activity) => <span className="badge text-bg-primary rounded-pill">{activity.points}</span> },
        { key: 'user', header: 'User', render: (activity) => activity.user ?? '—' },
        { key: 'team', header: 'Team', render: (activity) => activity.team ?? '—' },
      ]}
      rowKey={(activity, index) => activity.id ?? `${activity.type}-${index}`}
      loading={loading}
      error={error}
      emptyMessage="No activities found yet."
    />
  );
}
