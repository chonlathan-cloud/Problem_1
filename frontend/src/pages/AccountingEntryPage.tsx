import React, { useState } from 'react';
import AccountingEntryForm from '../components/AccountingEntryForm';
import { createAccountingEntry } from '../services/api_client';
import { useToast, Box } from '@chakra-ui/react';

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

const AccountingEntryPage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();

  const handleSubmit = async (data: AccountingEntryFormInputs) => {
    setIsLoading(true);

    let attachProofBase64 = '';
    if (data.attach_proof && data.attach_proof.length > 0) {
      const file = data.attach_proof[0];
      const reader = new FileReader();

      reader.onload = async (e) => {
        if (e.target && typeof e.target.result === 'string') {
          attachProofBase64 = e.target.result.split(',')[1];
          const payload = {
            ...data,
            attach_proof_base64: attachProofBase64,
            date: data.date, // Ensure date is string format YYYY-MM-DD
          };
          delete payload.attach_proof;
          
          try {
            await createAccountingEntry(payload);
            toast({
              title: "Entry recorded.",
              description: "Accounting entry has been successfully recorded.",
              status: "success",
              duration: 5000,
              isClosable: true,
            });
          } catch (error: any) {
            toast({
              title: "Error recording entry.",
              description: error.response?.data?.detail || error.message,
              status: "error",
              duration: 5000,
              isClosable: true,
            });
          } finally {
            setIsLoading(false);
          }
        }
      };
      reader.readAsDataURL(file);
    } else {
      // Handle case where no attachment is provided if it's optional
      const payload = { 
        ...data, 
        attach_proof_base64: attachProofBase64, // Empty string if no attachment
        date: data.date, 
      };
      delete payload.attach_proof;

      try {
        await createAccountingEntry(payload);
        toast({
          title: "Entry recorded.",
          description: "Accounting entry has been successfully recorded.",
          status: "success",
          duration: 5000,
          isClosable: true,
        });
      } catch (error: any) {
        toast({
          title: "Error recording entry.",
          description: error.response?.data?.detail || error.message,
          status: "error",
          duration: 5000,
          isClosable: true,
        });
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <Box p={4}>
      <h1>Record New Accounting Entry</h1>
      <AccountingEntryForm onSubmit={handleSubmit} isLoading={isLoading} />
    </Box>
  );
};

export default AccountingEntryPage;

