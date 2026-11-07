const configuredApiBaseUrl = import.meta.env.VITE_API_BASE_URL;
const codespaceName = import.meta.env.REACT_APP_CODESPACE_NAME;

export const apiBaseUrl = (
  configuredApiBaseUrl ||
  (codespaceName ? `https://${codespaceName}-8000.app.github.dev` : '')
).replace(/\/$/, '');

export function apiEndpoint(resourcePath: string): string {
  const path = resourcePath.startsWith('/') ? resourcePath : `/${resourcePath}`;
  return `${apiBaseUrl}${path}`;
}

export async function getJson<T>(endpoint: string): Promise<T> {
  const response = await fetch(endpoint);
  if (!response.ok) {
    throw new Error(`Request to ${endpoint} failed with status ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function collectionFromResponse<T>(payload: unknown, key: string): T[] {
  if (Array.isArray(payload)) return payload as T[];
  if (!payload || typeof payload !== 'object') return [];

  const record = payload as Record<string, unknown>;
  if (Array.isArray(record.results)) return record.results as T[];

  const resource = record[key];
  if (Array.isArray(resource)) return resource as T[];
  if (resource && typeof resource === 'object') {
    const nestedResults = (resource as Record<string, unknown>).results;
    if (Array.isArray(nestedResults)) return nestedResults as T[];
  }

  return [];
}

export async function getCollection<T>(endpoint: string, key: string): Promise<T[]> {
  const payload = await getJson<unknown>(endpoint);
  return collectionFromResponse<T>(payload, key);
}
