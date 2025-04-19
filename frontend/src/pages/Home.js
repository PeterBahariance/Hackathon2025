import React from 'react';
import { Box, Typography, Container } from '@mui/material';
import Layout from '../components/Layout';

const Home = () => {
    return (
        <Layout>
            <Container maxWidth="md">
                <Box sx={{ my: 4, textAlign: 'center' }}>
                    <Typography variant="h1" component="h1" gutterBottom>
                        Welcome to Medication Tracker
                    </Typography>
                    <Typography variant="h5" component="h2" gutterBottom>
                        Track your medications with ease
                    </Typography>
                </Box>
            </Container>
        </Layout>
    );
};

export default Home; 