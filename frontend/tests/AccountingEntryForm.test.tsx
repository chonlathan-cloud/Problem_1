import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ChakraProvider } from '@chakra-ui/react';
import AccountingEntryForm from '../src/components/AccountingEntryForm';
import { vi } from 'vitest';

const ChakraWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <ChakraProvider>{children}</ChakraProvider>
);

describe('AccountingEntryForm', () => {
  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  test('renders all form fields', () => {
    render(<AccountingEntryForm onSubmit={mockOnSubmit} isLoading={false} />, { wrapper: ChakraWrapper });

    expect(screen.getByLabelText(/Date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Document Type/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Amount/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/VAT/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Recorder ID/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Remarks/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Attach Proof \(PDF\/Image\)/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Record Entry/i })).toBeInTheDocument();
  });

  test('shows validation errors for required fields on submit', async () => {
    render(<AccountingEntryForm onSubmit={mockOnSubmit} isLoading={false} />, { wrapper: ChakraWrapper });

    fireEvent.click(screen.getByRole('button', { name: /Record Entry/i }));

    await waitFor(() => {
      expect(screen.getByText(/Date is required/i)).toBeInTheDocument();
      expect(screen.getByText(/Document Type is required/i)).toBeInTheDocument();
      expect(screen.getByText(/Description is required/i)).toBeInTheDocument();
      expect(screen.getByText(/Amount is required/i)).toBeInTheDocument();
      expect(screen.getByText(/VAT is required/i)).toBeInTheDocument();
      expect(screen.getByText(/Recorder ID is required/i)).toBeInTheDocument();
      expect(screen.getByText(/Proof attachment is required/i)).toBeInTheDocument();
    });
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test('submits form with valid data', async () => {
    render(<AccountingEntryForm onSubmit={mockOnSubmit} isLoading={false} />, { wrapper: ChakraWrapper });

    fireEvent.change(screen.getByLabelText(/Date/i), { target: { value: '2024-01-01' } });
    fireEvent.change(screen.getByLabelText(/Document Type/i), { target: { value: 'Invoice' } });
    fireEvent.change(screen.getByLabelText(/Description/i), { target: { value: 'Office Supplies' } });
    fireEvent.change(screen.getByLabelText(/Amount/i), { target: { value: '150.75' } });
    fireEvent.change(screen.getByLabelText(/VAT/i), { target: { value: '5.0' } });
    fireEvent.change(screen.getByLabelText(/Recorder ID/i), { target: { value: 'EMP001' } });
    fireEvent.change(screen.getByLabelText(/Remarks/i), { target: { value: 'Some remarks' } });

    // Create a mock file
    const file = new File(['dummy content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText(/Attach Proof \(PDF\/Image\)/i);
    fireEvent.change(input, { target: { files: [file] } });

    fireEvent.click(screen.getByRole('button', { name: /Record Entry/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(expect.objectContaining({
        date: '2024-01-01',
        document_type: 'Invoice',
        description: 'Office Supplies',
        amount: 150.75,
        vat: 5,
        recorder_id: 'EMP001',
        remarks: 'Some remarks',
        attach_proof: expect.any(FileList),
      }));
    });
  });

  test('shows error for invalid amount', async () => {
    render(<AccountingEntryForm onSubmit={mockOnSubmit} isLoading={false} />, { wrapper: ChakraWrapper });

    fireEvent.change(screen.getByLabelText(/Amount/i), { target: { value: '0' } });
    fireEvent.click(screen.getByRole('button', { name: /Record Entry/i }));

    await waitFor(() => {
      expect(screen.getByText(/Amount must be greater than 0/i)).toBeInTheDocument();
    });
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test('shows error for invalid VAT', async () => {
    render(<AccountingEntryForm onSubmit={mockOnSubmit} isLoading={false} />, { wrapper: ChakraWrapper });

    fireEvent.change(screen.getByLabelText(/VAT/i), { target: { value: '8' } });
    fireEvent.click(screen.getByRole('button', { name: /Record Entry/i }));

    await waitFor(() => {
      expect(screen.getByText(/VAT cannot be greater than 7/i)).toBeInTheDocument();
    });
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
});
