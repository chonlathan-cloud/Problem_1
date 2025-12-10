import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ChakraProvider } from '@chakra-ui/react';
import { BrowserRouter as Router } from 'react-router-dom';
import { vi } from 'vitest';

import AccountingEntryPage from '../src/pages/AccountingEntryPage';
import * as apiClient from '../src/services/api_client';

// Mock the AccountingEntryForm component
vi.mock('../src/components/AccountingEntryForm', () => ({
  __esModule: true,
  default: vi.fn(({ onSubmit, isLoading }) => (
    <form data-testid="accounting-entry-form" onSubmit={(e) => {
      e.preventDefault();
      onSubmit({
        date: '2024-01-01',
        document_type: 'Invoice',
        description: 'Test Description',
        amount: 100,
        vat: 5,
        recorder_id: 'EMP001',
        remarks: 'Some remarks',
        attach_proof: [new File(['dummy content'], 'test.pdf', { type: 'application/pdf' })] as any
      });
    }}>
      <button type="submit" data-testid="submit-button" disabled={isLoading}>Submit</button>
    </form>
  )),
}));

// Mock the API client
vi.mock('../src/services/api_client', () => ({
  createAccountingEntry: vi.fn(),
}));

const ChakraRouterWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <ChakraProvider>
    <Router>{children}</Router>
  </ChakraProvider>
);

describe('AccountingEntryPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test('renders the AccountingEntryForm', () => {
    render(<AccountingEntryPage />, { wrapper: ChakraRouterWrapper });
    expect(screen.getByTestId('accounting-entry-form')).toBeInTheDocument();
  });

  test('handles successful form submission', async () => {
    (apiClient.createAccountingEntry as vi.Mock).mockResolvedValueOnce({
      id: '1',
      date: '2024-01-01',
      document_type: 'Invoice',
      description: 'Test Description',
      amount: 100,
      vat: 5,
      recorder_id: 'EMP001',
      created_at: new Date().toISOString(),
    });

    render(<AccountingEntryPage />, { wrapper: ChakraRouterWrapper });
    fireEvent.click(screen.getByTestId('submit-button'));

    await waitFor(() => {
      expect(apiClient.createAccountingEntry).toHaveBeenCalledWith(expect.objectContaining({
        date: '2024-01-01',
        document_type: 'Invoice',
        description: 'Test Description',
        amount: 100,
        vat: 5,
        recorder_id: 'EMP001',
        attach_proof_base64: expect.any(String),
      }));
      expect(screen.getByText('Entry recorded.')).toBeInTheDocument();
    });
  });

  test('handles failed form submission', async () => {
    const errorMessage = 'Network Error';
    (apiClient.createAccountingEntry as vi.Mock).mockRejectedValueOnce({ response: { data: { detail: errorMessage } } });

    render(<AccountingEntryPage />, { wrapper: ChakraRouterWrapper });
    fireEvent.click(screen.getByTestId('submit-button'));

    await waitFor(() => {
      expect(apiClient.createAccountingEntry).toHaveBeenCalled();
      expect(screen.getByText('Error recording entry.')).toBeInTheDocument();
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });
});
