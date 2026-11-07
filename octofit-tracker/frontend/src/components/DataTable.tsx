import type { ReactNode } from 'react';

export type DataColumn<T> = {
  key: string;
  header: string;
  render: (row: T, index: number) => ReactNode;
};

type Props<T> = {
  title: string;
  description: string;
  rows: T[];
  columns: DataColumn<T>[];
  rowKey: (row: T, index: number) => string;
  loading: boolean;
  error: string | null;
  emptyMessage: string;
};

export default function DataTable<T>({
  title,
  description,
  rows,
  columns,
  rowKey,
  loading,
  error,
  emptyMessage,
}: Props<T>) {
  return (
    <section className="card data-card">
      <header className="card-header">
        <div>
          <h2 className="h3">{title}</h2>
          <p>{description}</p>
        </div>
        {!loading && !error && <span className="data-count">{rows.length} records</span>}
      </header>
      {loading && <p className="data-loading" role="status">Loading {title.toLowerCase()}...</p>}
      {error && <div className="alert alert-danger data-alert" role="alert">Unable to load {title.toLowerCase()}: {error}</div>}
      {!loading && !error && rows.length === 0 && <p className="data-empty">{emptyMessage}</p>}
      {!loading && !error && rows.length > 0 && (
        <div className="table-responsive">
          <table className="table table-striped table-hover align-middle">
            <thead>
              <tr>{columns.map((column) => <th scope="col" key={column.key}>{column.header}</th>)}</tr>
            </thead>
            <tbody>
              {rows.map((row, index) => (
                <tr key={rowKey(row, index)}>
                  {columns.map((column) => <td key={column.key}>{column.render(row, index)}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
