import { useEffect, useState } from 'react';
import { apiEndpoint, getCollection } from '../api/client.js';
import DataTable from './DataTable.js';

type Team = { id?: string; name: string; mascot?: string; members?: string[] };
const endpoint = apiEndpoint('/api/teams/');

export default function Teams() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    console.log('Teams REST API endpoint:', endpoint);
    getCollection<Team>(endpoint, 'teams')
      .then((data) => {
        console.log('Teams fetched data:', data);
        if (active) setTeams(data);
      })
      .catch((cause: unknown) => {
        if (active) setError(cause instanceof Error ? cause.message : 'Unable to load teams.');
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => { active = false; };
  }, []);

  return (
    <DataTable
      title="Teams"
      description="Browse your teams and the members who belong to them."
      rows={teams}
      columns={[
        { key: 'team', header: 'Team', render: (team) => <span className="fw-semibold">{team.name}</span> },
        { key: 'mascot', header: 'Mascot', render: (team) => team.mascot || '—' },
        { key: 'members', header: 'Members', render: (team) => <span className="badge text-bg-light border rounded-pill">{team.members?.length ?? 0}</span> },
      ]}
      rowKey={(team, index) => team.id ?? `${team.name}-${index}`}
      loading={loading}
      error={error}
      emptyMessage="No teams found yet."
    />
  );
}
