/**
 * FE-10 -- a transient /controls failure keeps the last good surface on
 * screen (with a banner), and control names are URL-encoded in write paths.
 */
import { act, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ControlHubPanel } from './ControlHubPanel.jsx';

const api = vi.hoisted(() => ({ fetch: null }));
vi.mock('../../hooks/useApi', async (importOriginal) => ({
  ...(await importOriginal()),
  apiFetch: (...args) => api.fetch(...args),
}));

const SURFACE = { controls: [{ name: 'a b/c', group: 'g', kind: 'text', value: 'x' }] };

afterEach(() => vi.restoreAllMocks());

describe('ControlHubPanel', () => {
  it('keeps the loaded surface and shows a banner when a refresh fails', async () => {
    api.fetch = vi.fn().mockResolvedValueOnce({ ok: true, json: async () => SURFACE })
      .mockResolvedValue({ ok: false, status: 503 });
    const { rerender } = render(<ControlHubPanel operatorAction={vi.fn()} refreshToken={0} />);
    await screen.findByText('a b/c');
    await act(async () => { rerender(<ControlHubPanel operatorAction={vi.fn()} refreshToken={1} />); });
    expect(await screen.findByRole('alert')).toBeTruthy();
    expect(screen.getByText('a b/c')).toBeTruthy();
  });

  it('URL-encodes the control name when writing', async () => {
    api.fetch = vi.fn().mockResolvedValue({ ok: true, json: async () => SURFACE });
    const op = vi.fn().mockResolvedValue({ ok: true });
    render(<ControlHubPanel operatorAction={op} refreshToken={0} />);
    const input = await screen.findByDisplayValue('x');
    fireEvent.change(input, { target: { value: 'y' } });
    fireEvent.blur(input);
    await vi.waitFor(() => expect(op).toHaveBeenCalled());
    expect(op.mock.calls[0][0]).toBe('/controls/a%20b%2Fc');
  });
});
