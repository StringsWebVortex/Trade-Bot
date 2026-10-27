/**
 * FE-02..FE-05 -- operator controls do not write on every input event or
 * blur, ask before high-impact actions, ignore double-clicks while a request
 * is in flight, and a crashing panel is contained by an error boundary.
 */
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { ActionButton, ModeSwitcher, NumberInput, Slider } from './Controls.jsx';
import { ErrorBoundary } from './ErrorBoundary.jsx';

describe('Slider (FE-02)', () => {
  it('sends one write on release, not one per input event', () => {
    const onChange = vi.fn();
    const { container } = render(<Slider value={1} onChange={onChange} min={0} max={10} step={1} label="x" />);
    const input = container.querySelector('input[type=range]');
    fireEvent.change(input, { target: { value: '3' } });
    fireEvent.change(input, { target: { value: '4' } });
    fireEvent.change(input, { target: { value: '5' } });
    expect(onChange).not.toHaveBeenCalled();
    fireEvent.pointerUp(input);
    expect(onChange).toHaveBeenCalledTimes(1);
    expect(onChange).toHaveBeenCalledWith(5);
  });

  it('does not write when released without a change', () => {
    const onChange = vi.fn();
    const { container } = render(<Slider value={1} onChange={onChange} min={0} max={10} step={1} label="x" />);
    fireEvent.pointerUp(container.querySelector('input[type=range]'));
    expect(onChange).not.toHaveBeenCalled();
  });
});

describe('NumberInput (FE-03)', () => {
  it('does not write on blur when the value is unchanged', () => {
    const onChange = vi.fn();
    render(<NumberInput value={5} onChange={onChange} label="n" />);
    const input = screen.getByRole('spinbutton');
    fireEvent.focus(input);
    fireEvent.blur(input);
    expect(onChange).not.toHaveBeenCalled();
  });

  it('writes a changed value once, and refuses an out-of-range one', () => {
    const onChange = vi.fn();
    render(<NumberInput value={5} onChange={onChange} label="n" min={0} max={10} />);
    const input = screen.getByRole('spinbutton');
    fireEvent.focus(input);
    fireEvent.change(input, { target: { value: '99' } });
    fireEvent.blur(input);
    expect(onChange).not.toHaveBeenCalled();
    expect(input.value).toBe('5');
    fireEvent.focus(input);
    fireEvent.change(input, { target: { value: '7' } });
    fireEvent.blur(input);
    expect(onChange).toHaveBeenCalledWith(7);
  });
});

describe('confirmation and in-flight state (FE-04)', () => {
  it('asks before switching to automatic and honours a refusal', () => {
    const onSwitch = vi.fn();
    const confirm = vi.spyOn(window, 'confirm').mockReturnValue(false);
    render(<ModeSwitcher current="restricted" onSwitch={onSwitch} />);
    fireEvent.click(screen.getByText('automatic'));
    expect(confirm).toHaveBeenCalled();
    expect(onSwitch).not.toHaveBeenCalled();
    confirm.mockReturnValue(true);
    fireEvent.click(screen.getByText('automatic'));
    expect(onSwitch).toHaveBeenCalledWith('automatic');
    fireEvent.click(screen.getByText('manual'));
    expect(onSwitch).toHaveBeenCalledWith('manual');
  });

  it('sends a confirmed action once despite a double click, and not at all if declined', async () => {
    let release;
    const onAction = vi.fn(() => new Promise((r) => { release = r; }));
    const confirm = vi.spyOn(window, 'confirm').mockReturnValue(true);
    render(<ActionButton onAction={onAction} confirmMessage="sure?">Go</ActionButton>);
    const btn = screen.getByText('Go');
    fireEvent.click(btn);
    fireEvent.click(btn);
    expect(onAction).toHaveBeenCalledTimes(1);
    expect(btn.disabled).toBe(true);
    release();
    await waitFor(() => expect(btn.disabled).toBe(false));
    confirm.mockReturnValue(false);
    fireEvent.click(btn);
    expect(onAction).toHaveBeenCalledTimes(1);
  });
});

describe('ErrorBoundary (FE-05)', () => {
  it('shows the failure inside the wrapped panel and keeps siblings mounted', () => {
    vi.spyOn(console, 'error').mockImplementation(() => {});
    const Bad = () => { throw new Error('boom'); };
    render(
      <div>
        <ErrorBoundary label="Bad panel"><Bad /></ErrorBoundary>
        <span>sibling</span>
      </div>,
    );
    expect(screen.getByRole('alert').textContent).toContain('boom');
    expect(screen.getByText('sibling')).toBeTruthy();
  });
});
