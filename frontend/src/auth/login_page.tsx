import React, { useState } from 'react';
import { useAuth } from './auth_context';
import { useNavigate } from 'react-router-dom';
import { Box, Button, FormControl, FormLabel, Input, Heading, VStack, useToast } from '@chakra-ui/react';

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();
  const toast = useToast();

  const handleLogin = () => {
    // In a real application, you'd send these credentials to a backend authentication endpoint
    // and receive a JWT token.
    if (username === 'employee' && password === 'password') {
      const mockToken = 'mock_jwt_token'; // This should come from a successful API call
      login(mockToken);
      toast({
        title: "Login successful.",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
      navigate('/record-entry'); // Redirect to protected page
    } else {
      toast({
        title: "Login failed.",
        description: "Invalid username or password.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Box p={8} maxWidth="md" borderWidth={1} borderRadius={8} boxShadow="lg" margin="auto" mt={10}>
      <Heading mb={6} textAlign="center">Login</Heading>
      <VStack spacing={4}>
        <FormControl>
          <FormLabel>Username</FormLabel>
          <Input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </FormControl>
        <FormControl>
          <FormLabel>Password</FormLabel>
          <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </FormControl>
        <Button colorScheme="teal" onClick={handleLogin} width="full">
          Login
        </Button>
      </VStack>
    </Box>
  );
};

export default LoginPage;
