import React from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { useNavigate } from 'react-router-dom';

const AddMedicine = () => {
    const navigate = useNavigate();

    return (
        <Box sx={{ p: 3 }}>
            <Button
                startIcon={<ArrowBackIcon />}
                onClick={() => navigate('/')}
                sx={{ mb: 3 }}
            >
                Back to Home
            </Button>
            <Paper elevation={2} sx={{ p: 3 }}>
                <Typography variant="h4" gutterBottom>
                    Add New Medicine
                </Typography>
                <Typography variant="body1" color="text.secondary">
                    This page will contain the form for adding new medications.
                </Typography>
            </Paper>
        </Box>
    );
};

export default AddMedicine; 