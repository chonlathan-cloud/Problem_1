import React, { useState } from 'react';
import AccountingEntryForm from '../components/AccountingEntryForm';
import { createAccountingEntry } from '../services/api_client';
import { useToast, Box, Heading } from '@chakra-ui/react';

// Define the shape of data coming from the form
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

    // Helper to send data
    const sendData = async (payload: any) => {
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

    if (data.attach_proof && data.attach_proof.length > 0) {
      const file = data.attach_proof[0];
      const reader = new FileReader();

      reader.onload = async (e) => {
        if (e.target && typeof e.target.result === 'string') {
          const attachProofBase64 = e.target.result.split(',')[1];
          
          // แยก attach_proof ออกจาก object data เพื่อไม่ให้ส่งไป backend
          const { attach_proof, ...restOfData } = data;

          const payload = {
            ...restOfData,
            attach_proof_base64: attachProofBase64,
            date: data.date, 
          };
          
          await sendData(payload);
        }
      };
      reader.readAsDataURL(file);
    } else {
      // กรณีไม่มีไฟล์
      const { attach_proof, ...restOfData } = data;
      const payload = { 
        ...restOfData, 
        attach_proof_base64: '', 
        date: data.date, 
      };
      await sendData(payload);
    }
  };

  return (
    <Box p={4}>
      <Heading mb={6}>Record New Accounting Entry</Heading>
      <AccountingEntryForm onSubmit={handleSubmit} isLoading={isLoading} />
    </Box>
  );
};

export default AccountingEntryPage;