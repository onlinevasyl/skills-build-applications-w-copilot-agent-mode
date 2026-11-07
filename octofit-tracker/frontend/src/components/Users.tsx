import { useEffect, useState } from 'react';
import { apiEndpoint, getCollection } from '../api/client.js';
import DataTable from './DataTable.js';

type User = { id?: string; name: string; email: string; team?: string | null; fitnessGoal?: string };
const endpoint = apiEndpoint('/api/users/');

export default function Users() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    console.log('Users REST API endpoint:', endpoint);
    getCollection<User>(endpoint, 'users')
      .then((data) => {
        console.log('Users fetched data:', data);
        if (active) setUsers(data);
      })
      .catch((cause: unknown) => {
        if (active) setError(cause instanceof Error ? cause.message : 'Unable to load users.');
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => { active = false; };
  }, []);

  return (
    <DataTable
      title="Users"
      description="View account details and fitness goals."
      rows={users}
      columns={[
        { key: 'name', header: 'Name', render: (user) => <span className="fw-semibold">{user.name}</span> },
        { key: 'email', header: 'Email', render: (user) => user.email },
        { key: 'team', header: 'Team', render: (user) => user.team ?? '—' },
        { key: 'goal', header: 'Fitness goal', render: (user) => user.fitnessGoal || '—' },
      ]}
      rowKey={(user, index) => user.id ?? `${user.email}-${index}`}
      loading={loading}
      error={error}
      emptyMessage="No users found yet."
    />
  );
}
