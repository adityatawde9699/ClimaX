export type AccountRole = 'CITIZEN' | 'AUTHORITY' | 'RESEARCHER' | 'ADMIN';

export function readTokenRole(token: string): AccountRole {
  try {
    const role = JSON.parse(window.atob(token.split('.')[1]))?.role;
    if (['CITIZEN', 'AUTHORITY', 'RESEARCHER', 'ADMIN'].includes(role)) return role;
  } catch {
    // Invalid tokens are handled by authenticated API requests.
  }
  return 'CITIZEN';
}

export function landingPageForRole(role: AccountRole): string {
  if (role === 'CITIZEN') return '/reports';
  if (role === 'RESEARCHER') return '/map';
  return '/dashboard';
}
