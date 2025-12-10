import React, { Component, ErrorInfo, ReactNode } from 'react';
import { Box, Heading, Text, VStack } from '@chakra-ui/react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(_: Error): State {
    // Update state so the next render will show the fallback UI.
    return { hasError: true };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
    // You could also log error messages to an error reporting service here
  }

  public render(): ReactNode {
    if (this.state.hasError) {
      return (
        <VStack p={8} spacing={4} align="center" justify="center" minH="100vh">
          <Box textAlign="center">
            <Heading as="h2" size="xl" color="red.500">
              Oops, there is an error!
            </Heading>
            <Text fontSize="lg" mt={4}>
              Something went wrong. Please try again later or contact support.
            </Text>
          </Box>
        </VStack>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
