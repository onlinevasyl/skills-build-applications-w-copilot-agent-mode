import { useEffect, useState } from 'react';
import { apiEndpoint, getCollection } from '../api/client.js';
import DataTable from './DataTable.js';

type LeaderboardEntry = { teamName: string; totalPoints: number; rank?: number };
const endpoint = apiEndpoint('/api/leaderboard/');

export default function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    console.log('Leaderboard REST API endpoint:', endpoint);
    getCollection<LeaderboardEntry>(endpoint, 'leaderboard')
      .then((data) => {
        console.log('Leaderboard fetched data:', data);
        if (active) setLeaderboard(data);
      })
      .catch((cause: unknown) => {
        if (active) setError(cause instanceof Error ? cause.message : 'Unable to load leaderboard.');
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => { active = false; };
  }, []);

  return (
    <DataTable
      title="Leaderboard"
      description="See how teams are progressing against one another."
      rows={leaderboard}
      columns={[
        { key: 'rank', header: 'Rank', render: (entry, index) => <span className="badge text-bg-light border rounded-pill">#{entry.rank ?? index + 1}</span> },
        { key: 'team', header: 'Team', render: (entry) => <span className="fw-semibold">{entry.teamName}</span> },
        { key: 'points', header: 'Total points', render: (entry) => <span className="badge text-bg-primary rounded-pill">{entry.totalPoints}</span> },
      ]}
      rowKey={(entry, index) => `${entry.teamName}-${index}`}
      loading={loading}
      error={error}
      emptyMessage="No leaderboard scores found yet."
    />
  );
}
