import React, { useState } from 'react';
import { Box, Typography, Paper, Button, CircularProgress } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { useNavigate } from 'react-router-dom';

const AddMedicine = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleRunScript = () => {
        setLoading(true);
        setError(null);
        setResult(null);

        fetch('http://localhost:5050/run-script')
            .then(res => res.json())
            .then(data => {
                console.log('📡 Backend responded:', data);
                setResult(data.output);
            })
            .catch(err => {
                console.error('❌ Backend error:', err);
                setError('Something went wrong when calling the backend.');
            })
            .finally(() => {
                setLoading(false);
            });
    };

    return (
        <Box sx={{ p: 3 }}>
            <Button
                startIcon={<ArrowBackIcon />}
                onClick={() => navigate('/')}
                sx={{ mb: 3 }}
            >
                Back to Home
            </Button>

            <Paper elevation={2} sx={{ p: 3, mb: 2 }}>
                <Typography variant="h4" gutterBottom>
                    Add New Medicine
                </Typography>
                <Typography variant="body1" color="text.secondary">
                    This page will contain the form for adding new medications.
                </Typography>
            </Paper>

            <Button
                variant="contained"
                onClick={handleRunScript}
                disabled={loading}
                sx={{ mb: 2 }}
            >
                {loading ? <CircularProgress size={24} /> : 'Run OCR and Analyze'}
            </Button>

            {error && (
                <Typography variant="body2" color="error">
                    {error}
                </Typography>
            )}

            {result && (
                <Paper elevation={1} sx={{ p: 2, mt: 2 }}>
                    <Typography variant="subtitle1" gutterBottom>
                        Raw Backend Output:
                    </Typography>
                    <Typography
                        variant="body2"
                        component="pre"
                        sx={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}
                    >
                        {result}
                    </Typography>
                </Paper>
            )}
        </Box>
    );
};

export default AddMedicine;
