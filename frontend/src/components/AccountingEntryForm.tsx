import React from 'react';
import { useForm } from 'react-hook-form';
import {
  FormControl,
  FormLabel,
  Input,
  Button,
  Stack,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  Textarea,
  FormErrorMessage,
} from '@chakra-ui/react';

interface AccountingEntryFormInputs {
  date: string;
  document_type: string;
  description: string;
  amount: number;
  vat: number;
  recorder_id: string;
  remarks?: string;
  attach_proof: FileList;
}

interface AccountingEntryFormProps {
  onSubmit: (data: AccountingEntryFormInputs) => void;
  isLoading: boolean;
}

const AccountingEntryForm: React.FC<AccountingEntryFormProps> = ({ onSubmit, isLoading }) => {
  const { register, handleSubmit, formState: { errors } } = useForm<AccountingEntryFormInputs>();

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={4}>
        <FormControl isInvalid={!!errors.date}>
          <FormLabel>Date</FormLabel>
          <Input type="date" {...register('date', { required: 'Date is required' })} />
          <FormErrorMessage>{errors.date && errors.date.message}</FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!errors.document_type}>
          <FormLabel>Document Type</FormLabel>
          <Input {...register('document_type', { required: 'Document Type is required' })} />
          <FormErrorMessage>{errors.document_type && errors.document_type.message}</FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!errors.description}>
          <FormLabel>Description</FormLabel>
          <Input {...register('description', { required: 'Description is required' })} />
          <FormErrorMessage>{errors.description && errors.description.message}</FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!errors.amount}>
          <FormLabel>Amount</FormLabel>
          <NumberInput min={0.01} precision={2} step={0.01}>
            <NumberInputField {...register('amount', { required: 'Amount is required', valueAsNumber: true, min: { value: 0.01, message: 'Amount must be greater than 0' } })} />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
          <FormErrorMessage>{errors.amount && errors.amount.message}</FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!errors.vat}>
          <FormLabel>VAT (%)</FormLabel>
          <NumberInput min={0} max={7} precision={2} step={0.1}>
            <NumberInputField {...register('vat', { required: 'VAT is required', valueAsNumber: true, min: { value: 0, message: 'VAT cannot be negative' }, max: { value: 7, message: 'VAT cannot be greater than 7' } })} />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
          <FormErrorMessage>{errors.vat && errors.vat.message}</FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!errors.recorder_id}>
          <FormLabel>Recorder ID</FormLabel>
          <Input {...register('recorder_id', { required: 'Recorder ID is required' })} />
          <FormErrorMessage>{errors.recorder_id && errors.recorder_id.message}</FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!errors.remarks}>
          <FormLabel>Remarks</FormLabel>
          <Textarea {...register('remarks')} />
          <FormErrorMessage>{errors.remarks && errors.remarks.message}</FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!errors.attach_proof}>
          <FormLabel>Attach Proof (PDF/Image)</FormLabel>
          <Input type="file" {...register('attach_proof', { required: 'Proof attachment is required' })} />
          <FormErrorMessage>{errors.attach_proof && errors.attach_proof.message}</FormErrorMessage>
        </FormControl>

        <Button mt={4} colorScheme="teal" isLoading={isLoading} type="submit">
          Record Entry
        </Button>
      </Stack>
    </form>
  );
};

export default AccountingEntryForm;
