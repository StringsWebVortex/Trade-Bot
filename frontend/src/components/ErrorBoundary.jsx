import { Component } from 'react';

/**
 * Contains a render error to the subtree it wraps (FE-05), so one panel
 * receiving an unexpected null cannot unmount the approvals and controls.
 */
export class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    console.error(`[${this.props.label || 'panel'}] render failed`, error, info?.componentStack);
  }

  render() {
    const { error } = this.state;
    if (!error) return this.props.children;
    return (
      <div role="alert" style={{ color: 'var(--c-red)', fontSize: 12, padding: 12 }}>
        {this.props.label || 'Panel'} failed to render: {String(error?.message || error)}
        <div>
          <button type="button" className="btn" onClick={() => this.setState({ error: null })}>Retry</button>
        </div>
      </div>
    );
  }
}
